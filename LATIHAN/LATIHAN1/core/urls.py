from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/mahasiswa/', views.register_mahasiswa, name='register_mahasiswa'),
    path('register/dosen/', views.register_dosen, name='register_dosen'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard & Profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil_view, name='profil'),
    path('profil/edit/', views.edit_profil, name='edit_profil'),
    
    # Keahlian
    path('keahlian/tambah/', views.tambah_keahlian, name='tambah_keahlian'),
    path('keahlian/<int:pk>/hapus/', views.hapus_keahlian, name='hapus_keahlian'),
    
    # Prestasi
    path('prestasi/', views.prestasi_list, name='prestasi_list'),
    path('prestasi/tambah/', views.tambah_prestasi, name='tambah_prestasi'),
    path('prestasi/<int:pk>/', views.prestasi_detail, name='prestasi_detail'),
    path('prestasi/<int:pk>/validasi/', views.validasi_prestasi, name='validasi_prestasi'),
    
    # Proyek
    path('proyek/', views.proyek_list, name='proyek_list'),
    path('proyek/<int:pk>/', views.proyek_detail, name='proyek_detail'),
    path('proyek/buat/', views.buat_proyek, name='buat_proyek'),
    path('proyek/<int:pk>/daftar/', views.daftar_proyek, name='daftar_proyek'),
    path('anggota/<int:pk>/terima/', views.terima_anggota, name='terima_anggota'),
    path('anggota/<int:pk>/tolak/', views.tolak_anggota, name='tolak_anggota'),
    
    # Talent Pool
    path('talent-pool/', views.talent_pool, name='talent_pool'),
    
    # Notifikasi
    path('notifikasi/', views.notifikasi_list, name='notifikasi_list'),
    
    # Statistics
    path('statistics/', views.statistics, name='statistics'),
]
