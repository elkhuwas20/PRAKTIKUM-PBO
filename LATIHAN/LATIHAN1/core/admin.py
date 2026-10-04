from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


# ============= CUSTOM USER ADMIN =============
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'photo')}),
    )


# ============= PROFIL MAHASISWA ADMIN =============
class KeahlianInline(admin.TabularInline):
    model = Keahlian
    extra = 1


class PrestasiInline(admin.TabularInline):
    model = Prestasi
    extra = 0
    readonly_fields = ['status', 'validator']


@admin.register(ProfilMahasiswa)
class ProfilMahasiswaAdmin(admin.ModelAdmin):
    list_display = ['nim', 'get_nama', 'prodi', 'angkatan', 'poin', 'ipk']
    list_filter = ['prodi', 'angkatan']
    search_fields = ['nim', 'user__first_name', 'user__last_name', 'prodi']
    inlines = [KeahlianInline, PrestasiInline]
    
    def get_nama(self, obj):
        return obj.user.get_full_name()
    get_nama.short_description = 'Nama'


# ============= PROFIL DOSEN ADMIN =============
@admin.register(ProfilDosen)
class ProfilDosenAdmin(admin.ModelAdmin):
    list_display = ['nip', 'get_nama', 'jurusan', 'jabatan']
    list_filter = ['jurusan']
    search_fields = ['nip', 'user__first_name', 'user__last_name', 'jurusan']
    
    def get_nama(self, obj):
        return obj.user.get_full_name()
    get_nama.short_description = 'Nama'


# ============= KEAHLIAN ADMIN =============
@admin.register(Keahlian)
class KeahlianAdmin(admin.ModelAdmin):
    list_display = ['nama_keahlian', 'level', 'mahasiswa']
    list_filter = ['level']
    search_fields = ['nama_keahlian', 'mahasiswa__nim']


# ============= PRESTASI ADMIN =============
@admin.register(Prestasi)
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ['judul', 'mahasiswa', 'kategori', 'status', 'tanggal', 'validator']
    list_filter = ['status', 'kategori', 'tanggal']
    search_fields = ['judul', 'mahasiswa__nim', 'mahasiswa__user__first_name']
    date_hierarchy = 'tanggal'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Prestasi', {
            'fields': ('mahasiswa', 'judul', 'kategori', 'deskripsi', 'tanggal', 'penyelenggara', 'bukti_file')
        }),
        ('Validasi', {
            'fields': ('status', 'validator', 'catatan_validator', 'tanggal_validasi')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ============= PROYEK ADMIN =============
class AnggotaProyekInline(admin.TabularInline):
    model = AnggotaProyek
    extra = 0
    readonly_fields = ['tanggal_bergabung']


@admin.register(Proyek)
class ProyekAdmin(admin.ModelAdmin):
    list_display = ['nama_proyek', 'tipe_proyek', 'pembuat', 'status', 'jumlah_anggota', 'max_anggota', 'tanggal_mulai']
    list_filter = ['tipe_proyek', 'status', 'tanggal_mulai']
    search_fields = ['nama_proyek', 'deskripsi', 'pembuat__username']
    date_hierarchy = 'tanggal_mulai'
    inlines = [AnggotaProyekInline]
    readonly_fields = ['created_at', 'updated_at']


# ============= ANGGOTA PROYEK ADMIN =============
@admin.register(AnggotaProyek)
class AnggotaProyekAdmin(admin.ModelAdmin):
    list_display = ['mahasiswa', 'proyek', 'role', 'status', 'created_at']
    list_filter = ['role', 'status']
    search_fields = ['mahasiswa__nim', 'proyek__nama_proyek']
    date_hierarchy = 'created_at'


# ============= NOTIFIKASI ADMIN =============
@admin.register(Notifikasi)
class NotifikasiAdmin(admin.ModelAdmin):
    list_display = ['judul', 'user', 'tipe', 'is_read', 'created_at']
    list_filter = ['tipe', 'is_read', 'created_at']
    search_fields = ['judul', 'pesan', 'user__username']
    date_hierarchy = 'created_at'


# ============= AKTIVITAS LOG ADMIN =============
@admin.register(AktivitasLog)
class AktivitasLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'aktivitas', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'aktivitas', 'deskripsi']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']


# Customize Admin Site
admin.site.site_header = "KREASI Admin"
admin.site.site_title = "KREASI Admin Portal"
admin.site.index_title = "Selamat Datang di KREASI Admin"
