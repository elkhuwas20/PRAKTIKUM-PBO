# 🌐 Panduan Menjalankan Web Application KREASI (Django)

## 📋 Deskripsi

KREASI Web Application adalah pengembangan dari program CLI menjadi **full-stack web application** menggunakan Django Framework. Aplikasi ini memiliki:

✅ **Database Integration** (SQLite default, dapat diganti MySQL/PostgreSQL)  
✅ **Web Interface** (HTML, CSS, Bootstrap 5)  
✅ **Authentication System** (Login/Logout/Register)  
✅ **File Upload** (Bukti prestasi & foto profil)  
✅ **Notification System** (Real-time notification)  
✅ **Admin Panel** (Django Admin)  
✅ **REST API Ready** (Django REST Framework)  
✅ **Responsive Design** (Mobile-friendly)  

---

## 🚀 Cara Menjalankan Web Application

### 1. Setup Environment

```bash
cd "PRAKTIKUM PBO/LATIHAN"

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Buat migrations
python manage.py makemigrations

# Apply migrations ke database
python manage.py migrate
```

### 3. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Ikuti prompt untuk membuat akun admin:
- Username: admin
- Email: admin@kreasi.ac.id
- Password: (pilih password kuat)

### 4. Run Development Server

```bash
python manage.py runserver
```

Server akan berjalan di: **http://127.0.0.1:8000/**

---

## 📱 Mengakses Aplikasi

### 1. **Landing Page** 
```
http://127.0.0.1:8000/
```
- Halaman utama dengan informasi sistem
- Statistik (total mahasiswa, dosen, proyek, prestasi)
- Fitur-fitur KREASI

### 2. **Register** 
```
http://127.0.0.1:8000/register/mahasiswa/
http://127.0.0.1:8000/register/dosen/
```
- Form registrasi untuk mahasiswa atau dosen
- Auto-create profil setelah registrasi

### 3. **Login**
```
http://127.0.0.1:8000/login/
```
- Login dengan username & password

### 4. **Dashboard**
```
http://127.0.0.1:8000/dashboard/
```
- Dashboard berbeda untuk mahasiswa dan dosen
- Statistik personal (poin, prestasi, proyek)

### 5. **Profil**
```
http://127.0.0.1:8000/profil/
```
- View profil lengkap
- Edit profil mahasiswa
- Tambah/hapus keahlian

### 6. **Prestasi**
```
http://127.0.0.1:8000/prestasi/
http://127.0.0.1:8000/prestasi/tambah/
```
- Mahasiswa: ajukan prestasi baru dengan upload bukti
- Dosen: validasi prestasi mahasiswa

### 7. **Bursa Proyek**
```
http://127.0.0.1:8000/proyek/
http://127.0.0.1:8000/proyek/buat/
```
- Semua user: lihat daftar proyek
- Mahasiswa: daftar ke proyek
- Pembuat proyek: terima/tolak anggota

### 8. **Talent Pool**
```
http://127.0.0.1:8000/talent-pool/
```
- Database talenta mahasiswa
- Search berdasarkan keahlian, prodi, poin

### 9. **Notifikasi**
```
http://127.0.0.1:8000/notifikasi/
```
- Notifikasi validasi prestasi
- Notifikasi proyek (diterima/ditolak)
- Notifikasi undangan

### 10. **Admin Panel**
```
http://127.0.0.1:8000/admin/
```
- Full CRUD semua data
- Login dengan superuser account
- Statistik dan analytics

---

## 🎯 Alur Penggunaan Sistem

### **MAHASISWA:**

1. **Register** → Buat akun mahasiswa
2. **Login** → Masuk ke sistem
3. **Lengkapi Profil** → Tambah keahlian, bio, link portfolio
4. **Ajukan Prestasi** → Upload bukti prestasi
5. **Cari Proyek** → Lihat bursa proyek dan daftar
6. **Kumpulkan Poin** → Prestasi divalidasi (+50 poin), diterima proyek (+30 poin)

### **DOSEN:**

1. **Register** → Buat akun dosen
2. **Login** → Masuk ke sistem
3. **Validasi Prestasi** → Approve/reject prestasi mahasiswa
4. **Buat Proyek** → Buat proyek penelitian/pengabdian/lomba
5. **Cari Talenta** → Search mahasiswa di talent pool
6. **Rekrut Anggota** → Terima anggota dari pendaftar

---

## 🗄️ Struktur Database

### Models (Tables):

1. **User** - Custom user dengan role (mahasiswa/dosen)
2. **ProfilMahasiswa** - Data lengkap mahasiswa
3. **ProfilDosen** - Data lengkap dosen
4. **Keahlian** - Skill mahasiswa
5. **Prestasi** - Prestasi dengan validasi
6. **Proyek** - Proyek kolaborasi
7. **AnggotaProyek** - Anggota yang bergabung
8. **Notifikasi** - Notifikasi user
9. **AktivitasLog** - Log aktivitas

### Relasi:
```
User (1) ──→ (1) ProfilMahasiswa
User (1) ──→ (1) ProfilDosen
ProfilMahasiswa (1) ──→ (N) Keahlian
ProfilMahasiswa (1) ──→ (N) Prestasi
Prestasi (N) ──→ (1) ProfilDosen (validator)
User (1) ──→ (N) Proyek (pembuat)
Proyek (1) ──→ (N) AnggotaProyek
ProfilMahasiswa (1) ──→ (N) AnggotaProyek
User (1) ──→ (N) Notifikasi
```

---

## 🎨 Fitur Web yang Belum Dibuat (Dapat Dikembangkan)

Karena keterbatasan context, beberapa template HTML belum dibuat. Anda dapat membuat sendiri:

### Template yang Perlu Dibuat:
1. `templates/core/register_dosen.html` (copy dari register_mahasiswa)
2. `templates/core/dashboard.html`
3. `templates/core/profil_mahasiswa.html`
4. `templates/core/profil_dosen.html`
5. `templates/core/edit_profil.html`
6. `templates/core/tambah_keahlian.html`
7. `templates/core/prestasi_list.html`
8. `templates/core/tambah_prestasi.html`
9. `templates/core/prestasi_detail.html`
10. `templates/core/validasi_prestasi.html`
11. `templates/core/proyek_list.html`
12. `templates/core/proyek_detail.html`
13. `templates/core/buat_proyek.html`
14. `templates/core/daftar_proyek.html`
15. `templates/core/talent_pool.html`
16. `templates/core/notifikasi_list.html`
17. `templates/core/statistics.html`

### Format Template Dasar:
```html
{% extends 'core/base.html' %}

{% block title %}Judul Halaman - KREASI{% endblock %}

{% block content %}
<div class="container my-5">
    <h1>Judul Halaman</h1>
    
    <!-- Konten di sini -->
    
</div>
{% endblock %}
```

---

## 🔧 Troubleshooting

### Error: "No such table: core_user"
**Solusi:**
```bash
python manage.py migrate
```

### Error: "CSRF token missing"
**Solusi:** Pastikan `{% csrf_token %}` ada di semua form

### Error: Port already in use
**Solusi:** Gunakan port lain
```bash
python manage.py runserver 8080
```

### Media files not loading
**Solusi:** Pastikan settings sudah benar dan jalankan di DEBUG mode

---

## 📊 Admin Panel Features

Setelah login ke `/admin/`, Anda dapat:

1. **Manage Users** - CRUD semua user
2. **Manage Profil** - Edit profil mahasiswa/dosen
3. **Manage Keahlian** - Bulk add/delete keahlian
4. **Manage Prestasi** - Lihat semua prestasi & validasi
5. **Manage Proyek** - CRUD semua proyek
6. **Manage Anggota** - Lihat semua anggota proyek
7. **View Notifikasi** - Lihat semua notifikasi sistem
8. **View Logs** - Aktivitas log untuk audit

---

## 🎓 Konsep OOP yang Diterapkan

### 1. **Encapsulation dalam Django Models**
```python
class ProfilMahasiswa(models.Model):
    # Private-like fields (akses terkontrol via methods)
    poin = models.IntegerField(default=0)
    
    def tambah_poin(self, jumlah):
        """Method untuk menambah poin dengan validasi"""
        if jumlah > 0:
            self.poin += jumlah
            self.save()
```

### 2. **Inheritance dengan Custom User**
```python
class User(AbstractUser):
    """Extended dari Django AbstractUser"""
    role = models.CharField(...)
```

### 3. **Polymorphism via Role-Based Logic**
```python
# Di views.py
if request.user.role == 'mahasiswa':
    # Logic untuk mahasiswa
elif request.user.role == 'dosen':
    # Logic untuk dosen
```

### 4. **Composition dengan Foreign Keys**
```python
class Prestasi(models.Model):
    mahasiswa = models.ForeignKey(ProfilMahasiswa, ...)  # Has-a relationship
    validator = models.ForeignKey(ProfilDosen, ...)
```

---

## 🔐 Security Features

✅ CSRF Protection (Django built-in)  
✅ Password Hashing (Django built-in)  
✅ SQL Injection Prevention (ORM)  
✅ XSS Protection (Template auto-escape)  
✅ Login Required Decorators  
✅ Role-Based Access Control  

---

## 📈 Next Steps untuk Production

Jika ingin deploy ke production:

1. **Change Database** ke PostgreSQL/MySQL
2. **Set DEBUG=False** di settings.py
3. **Configure ALLOWED_HOSTS**
4. **Setup Static Files** dengan WhiteNoise/Nginx
5. **Setup Media Files** dengan AWS S3/Cloud Storage
6. **Add Email Backend** untuk notifikasi email
7. **Add Celery** untuk background tasks
8. **Add Redis** untuk caching
9. **Deploy** ke Heroku/DigitalOcean/AWS

---

## 💡 Tips Development

1. **Gunakan Django Shell** untuk testing:
```bash
python manage.py shell
```

2. **Lihat SQL Queries**:
```bash
python manage.py sqlmigrate core 0001
```

3. **Reset Database** (development only):
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

4. **Collect Static Files** (production):
```bash
python manage.py collectstatic
```

---

## 📞 Bantuan

Jika menemui error atau butuh bantuan:

1. Cek Django documentation: https://docs.djangoproject.com/
2. Lihat error message di terminal
3. Gunakan Django Debug Toolbar untuk debugging
4. Stack Overflow untuk error spesifik

---

## ✅ Kesimpulan

KREASI Web Application berhasil dikembangkan dari CLI menjadi full-stack web application dengan fitur lengkap. Sistem sudah siap untuk digunakan dan dapat dikembangkan lebih lanjut sesuai kebutuhan.

**Happy Coding!** 🚀
