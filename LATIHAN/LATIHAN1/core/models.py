from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# ============= CUSTOM USER MODEL =============
class User(AbstractUser):
    """Extended User model dengan role"""
    ROLE_CHOICES = [
        ('mahasiswa', 'Mahasiswa'),
        ('dosen', 'Dosen'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='mahasiswa')
    phone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ============= PROFIL MAHASISWA =============
class ProfilMahasiswa(models.Model):
    """Profil lengkap mahasiswa dengan portofolio"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_mahasiswa')
    nim = models.CharField(max_length=20, unique=True)
    prodi = models.CharField(max_length=100)
    angkatan = models.IntegerField()
    ipk = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    poin = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'profil_mahasiswa'
        verbose_name = 'Profil Mahasiswa'
        verbose_name_plural = 'Profil Mahasiswa'
    
    def __str__(self):
        return f"{self.nim} - {self.user.get_full_name()}"
    
    def tambah_poin(self, jumlah):
        """Menambah poin mahasiswa"""
        if jumlah > 0:
            self.poin += jumlah
            self.save()


# ============= PROFIL DOSEN =============
class ProfilDosen(models.Model):
    """Profil lengkap dosen"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_dosen')
    nip = models.CharField(max_length=20, unique=True)
    jurusan = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100, blank=True)
    bidang_keahlian = models.TextField(blank=True)
    
    class Meta:
        db_table = 'profil_dosen'
        verbose_name = 'Profil Dosen'
        verbose_name_plural = 'Profil Dosen'
    
    def __str__(self):
        return f"{self.nip} - {self.user.get_full_name()}"


# ============= KEAHLIAN =============
class Keahlian(models.Model):
    """Keahlian/Skill mahasiswa"""
    mahasiswa = models.ForeignKey(ProfilMahasiswa, on_delete=models.CASCADE, related_name='keahlian')
    nama_keahlian = models.CharField(max_length=100)
    level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    
    class Meta:
        db_table = 'keahlian'
        verbose_name = 'Keahlian'
        verbose_name_plural = 'Keahlian'
        unique_together = ['mahasiswa', 'nama_keahlian']
    
    def __str__(self):
        return f"{self.nama_keahlian} ({self.level})"


# ============= PRESTASI =============
class Prestasi(models.Model):
    """Prestasi mahasiswa yang perlu divalidasi"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu Validasi'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]
    
    KATEGORI_CHOICES = [
        ('lomba', 'Lomba/Kompetisi'),
        ('penelitian', 'Penelitian'),
        ('pengabdian', 'Pengabdian Masyarakat'),
        ('organisasi', 'Organisasi'),
        ('sertifikasi', 'Sertifikasi'),
        ('lainnya', 'Lainnya'),
    ]
    
    mahasiswa = models.ForeignKey(ProfilMahasiswa, on_delete=models.CASCADE, related_name='prestasi')
    judul = models.CharField(max_length=255)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    deskripsi = models.TextField()
    tanggal = models.DateField()
    penyelenggara = models.CharField(max_length=200, blank=True)
    bukti_file = models.FileField(upload_to='prestasi_bukti/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    validator = models.ForeignKey(ProfilDosen, on_delete=models.SET_NULL, null=True, blank=True, related_name='validasi_prestasi')
    catatan_validator = models.TextField(blank=True)
    tanggal_validasi = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prestasi'
        verbose_name = 'Prestasi'
        verbose_name_plural = 'Prestasi'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.judul} - {self.mahasiswa.nim}"


# ============= PROYEK =============
class Proyek(models.Model):
    """Proyek kolaborasi"""
    STATUS_CHOICES = [
        ('open', 'Terbuka'),
        ('full', 'Penuh'),
        ('closed', 'Ditutup'),
        ('completed', 'Selesai'),
    ]
    
    TIPE_CHOICES = [
        ('lomba', 'Lomba/Kompetisi'),
        ('penelitian', 'Penelitian'),
        ('pengabdian', 'Pengabdian Masyarakat'),
        ('asisten', 'Asisten Laboratorium'),
        ('startup', 'Startup/Bisnis'),
        ('lainnya', 'Lainnya'),
    ]
    
    nama_proyek = models.CharField(max_length=255)
    deskripsi = models.TextField()
    tipe_proyek = models.CharField(max_length=20, choices=TIPE_CHOICES)
    pembuat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proyek_dibuat')
    max_anggota = models.IntegerField(validators=[MinValueValidator(1)])
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    persyaratan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proyek'
        verbose_name = 'Proyek'
        verbose_name_plural = 'Proyek'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nama_proyek
    
    @property
    def jumlah_anggota(self):
        return self.anggota.filter(status='accepted').count()
    
    @property
    def is_full(self):
        return self.jumlah_anggota >= self.max_anggota


# ============= ANGGOTA PROYEK =============
class AnggotaProyek(models.Model):
    """Anggota yang tergabung dalam proyek"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu'),
        ('accepted', 'Diterima'),
        ('rejected', 'Ditolak'),
        ('invited', 'Diundang'),
    ]
    
    ROLE_CHOICES = [
        ('leader', 'Ketua'),
        ('member', 'Anggota'),
    ]
    
    proyek = models.ForeignKey(Proyek, on_delete=models.CASCADE, related_name='anggota')
    mahasiswa = models.ForeignKey(ProfilMahasiswa, on_delete=models.CASCADE, related_name='proyek_diikuti')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pesan_lamaran = models.TextField(blank=True)
    tanggal_bergabung = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'anggota_proyek'
        verbose_name = 'Anggota Proyek'
        verbose_name_plural = 'Anggota Proyek'
        unique_together = ['proyek', 'mahasiswa']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.mahasiswa.nim} - {self.proyek.nama_proyek}"


# ============= NOTIFIKASI =============
class Notifikasi(models.Model):
    """Notifikasi untuk user"""
    TIPE_CHOICES = [
        ('validasi', 'Validasi Prestasi'),
        ('proyek', 'Proyek'),
        ('undangan', 'Undangan'),
        ('sistem', 'Sistem'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifikasi')
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)
    judul = models.CharField(max_length=255)
    pesan = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifikasi'
        verbose_name = 'Notifikasi'
        verbose_name_plural = 'Notifikasi'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.judul} - {self.user.username}"


# ============= AKTIVITAS LOG =============
class AktivitasLog(models.Model):
    """Log aktivitas user untuk analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aktivitas_log')
    aktivitas = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'aktivitas_log'
        verbose_name = 'Aktivitas Log'
        verbose_name_plural = 'Aktivitas Log'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.aktivitas}"
