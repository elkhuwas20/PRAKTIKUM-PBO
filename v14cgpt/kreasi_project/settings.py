"""Konfigurasi Django untuk KREASI.

Nilai sensitif dan konfigurasi yang berbeda antar lingkungan dibaca dari environment.
Mode default aman untuk deployment; untuk pengembangan lokal, set DJANGO_DEBUG=1.
"""
import os
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    """Parse boolean environment secara konsisten dan menolak nilai ambigu."""
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ImproperlyConfigured(f"Nilai {name} harus berupa boolean (0/1 atau true/false).")


DEBUG = env_bool("DJANGO_DEBUG", default=False)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    if DEBUG:
        # Kunci lokal hanya untuk menjalankan proyek di komputer pengembang.
        SECRET_KEY = "local-development-only-change-before-deployment"
    else:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY wajib diatur pada lingkungan produksi."
        )

_allowed_hosts_value = os.environ.get("DJANGO_ALLOWED_HOSTS", "").strip()
if not DEBUG and not _allowed_hosts_value:
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS wajib diatur ke hostname aplikasi pada lingkungan produksi."
    )
ALLOWED_HOSTS = [
    host.strip()
    for host in (_allowed_hosts_value or "127.0.0.1,localhost,testserver").split(",")
    if host.strip()
]
if not DEBUG and (not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS):
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS harus berisi hostname eksplisit ketika DEBUG dinonaktifkan."
    )

# Aktifkan hanya bila hosting memakai reverse proxy tepercaya yang mengatur ulang
# X-Forwarded-Proto. Ini membantu Django mengenali HTTPS untuk pemeriksaan CSRF.
if env_bool("DJANGO_TRUST_X_FORWARDED_PROTO", default=False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portal.apps.PortalConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise menyajikan aset static hasil collectstatic melalui WSGI,
    # tanpa mengubah serving berkas upload yang tetap melewati endpoint berizin.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "kreasi_project.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "kreasi_project.wsgi.application"
ASGI_APPLICATION = "kreasi_project.asgi.application"


def database_from_url(database_url):
    """Bangun konfigurasi DB dari URL umum penyedia hosting tanpa parser tambahan."""
    parsed = urlparse(database_url)
    scheme = parsed.scheme.lower()
    if scheme in {"postgres", "postgresql"}:
        query = parse_qs(parsed.query)
        options = {}
        if query.get("sslmode"):
            options["sslmode"] = query["sslmode"][0]
        config = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": unquote(parsed.path.lstrip("/")),
            "USER": unquote(parsed.username or ""),
            "PASSWORD": unquote(parsed.password or ""),
            "HOST": parsed.hostname or "",
            "PORT": str(parsed.port or ""),
            "CONN_MAX_AGE": 60,
            "CONN_HEALTH_CHECKS": True,
        }
        if options:
            config["OPTIONS"] = options
        if not config["NAME"]:
            raise ImproperlyConfigured("DATABASE_URL PostgreSQL harus menyertakan nama database.")
        return {"default": config}
    if scheme == "sqlite":
        # Konvensi URL: sqlite:///db.sqlite3 relatif ke BASE_DIR, sedangkan
        # sqlite:////var/lib/kreasi.db memakai path absolut /var/lib/kreasi.db.
        raw_path = unquote(parsed.path or "")
        if database_url.lower().startswith("sqlite:////"):
            database_name = "/" + raw_path.lstrip("/")
        else:
            relative_path = raw_path.lstrip("/")
            database_name = str((BASE_DIR / relative_path).resolve()) if relative_path else str(BASE_DIR / "db.sqlite3")
        return {"default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": database_name,
            # SQLite ignores select_for_update(); IMMEDIATE serializes writers before
            # they read the snapshot, reducing lost updates from concurrent sessions.
            "OPTIONS": {"timeout": 20, "transaction_mode": "IMMEDIATE"},
        }}
    raise ImproperlyConfigured("Skema DATABASE_URL yang didukung: sqlite://, postgres://, atau postgresql://.")


_database_url = os.environ.get("DATABASE_URL", "").strip()
if _database_url:
    DATABASES = database_from_url(_database_url)
else:
    _db_engine = os.environ.get("DB_ENGINE", "django.db.backends.sqlite3").strip()
    _db_name = os.environ.get("DB_NAME") or os.environ.get("DJANGO_DB_PATH") or str(BASE_DIR / "db.sqlite3")
    if _db_engine.endswith("sqlite3") and _db_name != ":memory:":
        db_path = Path(_db_name).expanduser()
        _db_name = str(db_path.resolve() if db_path.is_absolute() else (BASE_DIR / db_path).resolve())
    _default_db = {"ENGINE": _db_engine, "NAME": _db_name}
    if _db_engine.endswith("sqlite3"):
        _default_db["OPTIONS"] = {"timeout": 20, "transaction_mode": "IMMEDIATE"}
    if _db_engine.endswith("postgresql"):
        _default_db.update({
            "USER": os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", ""),
            "PORT": os.environ.get("DB_PORT", ""),
            "CONN_MAX_AGE": 60,
            "CONN_HEALTH_CHECKS": True,
        })
        if os.environ.get("DB_SSLMODE"):
            _default_db["OPTIONS"] = {"sslmode": os.environ["DB_SSLMODE"]}
    DATABASES = {"default": _default_db}

# Akun sistem menggunakan model autentikasi Django yang diperluas untuk KREASI.
AUTH_USER_MODEL = "portal.PortalUser"
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Makassar"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0
# Jangan publikasikan berkas upload sebagai static; akses tetap melalui document_detail.
MEDIA_URL = "/media/"
_media_root = Path(os.environ.get("DJANGO_MEDIA_ROOT", str(BASE_DIR / "media"))).expanduser()
MEDIA_ROOT = _media_root.resolve() if _media_root.is_absolute() else (BASE_DIR / _media_root).resolve()
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024
FILE_UPLOAD_PERMISSIONS = 0o640
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o750

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
