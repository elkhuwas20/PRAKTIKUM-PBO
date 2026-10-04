from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from .models import *
from .forms import *


# ============= AUTHENTICATION =============
def register_mahasiswa(request):
    """Registrasi mahasiswa baru"""
    if request.method == 'POST':
        form = MahasiswaRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrasi berhasil! Selamat datang di KREASI.')
            return redirect('dashboard')
    else:
        form = MahasiswaRegistrationForm()
    return render(request, 'core/register_mahasiswa.html', {'form': form})


def register_dosen(request):
    """Registrasi dosen baru"""
    if request.method == 'POST':
        form = DosenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrasi berhasil! Selamat datang di KREASI.')
            return redirect('dashboard')
    else:
        form = DosenRegistrationForm()
    return render(request, 'core/register_dosen.html', {'form': form})


def login_view(request):
    """Login user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau password salah.')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('home')


# ============= HOME & DASHBOARD =============
def home(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    stats = {
        'total_mahasiswa': ProfilMahasiswa.objects.count(),
        'total_dosen': ProfilDosen.objects.count(),
        'total_proyek': Proyek.objects.count(),
        'total_prestasi': Prestasi.objects.filter(status='approved').count(),
    }
    return render(request, 'core/home.html', {'stats': stats})


@login_required
def dashboard(request):
    """Dashboard user"""
    context = {}
    
    if request.user.role == 'mahasiswa':
        try:
            profil = request.user.profil_mahasiswa
            context = {
                'profil': profil,
                'prestasi_pending': profil.prestasi.filter(status='pending').count(),
                'prestasi_approved': profil.prestasi.filter(status='approved').count(),
                'proyek_diikuti': profil.proyek_diikuti.filter(status='accepted').count(),
                'notifikasi_unread': request.user.notifikasi.filter(is_read=False).count(),
            }
        except ProfilMahasiswa.DoesNotExist:
            pass
    
    elif request.user.role == 'dosen':
        try:
            profil = request.user.profil_dosen
            context = {
                'profil': profil,
                'prestasi_pending': Prestasi.objects.filter(status='pending').count(),
                'proyek_dibuat': request.user.proyek_dibuat.count(),
                'validasi_done': profil.validasi_prestasi.count(),
            }
        except ProfilDosen.DoesNotExist:
            pass
    
    return render(request, 'core/dashboard.html', context)


# ============= PROFIL =============
@login_required
def profil_view(request):
    """View profil user"""
    if request.user.role == 'mahasiswa':
        profil = get_object_or_404(ProfilMahasiswa, user=request.user)
        keahlian_list = profil.keahlian.all()
        prestasi_list = profil.prestasi.all()
        proyek_list = profil.proyek_diikuti.filter(status='accepted')
        
        return render(request, 'core/profil_mahasiswa.html', {
            'profil': profil,
            'keahlian_list': keahlian_list,
            'prestasi_list': prestasi_list,
            'proyek_list': proyek_list,
        })
    
    elif request.user.role == 'dosen':
        profil = get_object_or_404(ProfilDosen, user=request.user)
        proyek_list = request.user.proyek_dibuat.all()
        validasi_list = profil.validasi_prestasi.all()[:10]
        
        return render(request, 'core/profil_dosen.html', {
            'profil': profil,
            'proyek_list': proyek_list,
            'validasi_list': validasi_list,
        })


@login_required
def edit_profil(request):
    """Edit profil mahasiswa"""
    if request.user.role != 'mahasiswa':
        messages.error(request, 'Akses ditolak.')
        return redirect('dashboard')
    
    profil = get_object_or_404(ProfilMahasiswa, user=request.user)
    
    if request.method == 'POST':
        form = ProfilMahasiswaForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('profil')
    else:
        form = ProfilMahasiswaForm(instance=profil)
    
    return render(request, 'core/edit_profil.html', {'form': form})


# ============= KEAHLIAN =============
@login_required
def tambah_keahlian(request):
    """Tambah keahlian mahasiswa"""
    if request.user.role != 'mahasiswa':
        messages.error(request, 'Akses ditolak.')
        return redirect('dashboard')
    
    profil = get_object_or_404(ProfilMahasiswa, user=request.user)
    
    if request.method == 'POST':
        form = KeahlianForm(request.POST)
        if form.is_valid():
            keahlian = form.save(commit=False)
            keahlian.mahasiswa = profil
            keahlian.save()
            messages.success(request, f'Keahlian "{keahlian.nama_keahlian}" berhasil ditambahkan!')
            return redirect('profil')
    else:
        form = KeahlianForm()
    
    return render(request, 'core/tambah_keahlian.html', {'form': form})


@login_required
def hapus_keahlian(request, pk):
    """Hapus keahlian"""
    keahlian = get_object_or_404(Keahlian, pk=pk, mahasiswa__user=request.user)
    keahlian.delete()
    messages.success(request, 'Keahlian berhasil dihapus!')
    return redirect('profil')


# ============= PRESTASI =============
@login_required
def prestasi_list(request):
    """Daftar prestasi"""
    if request.user.role == 'mahasiswa':
        profil = get_object_or_404(ProfilMahasiswa, user=request.user)
        prestasi_list = profil.prestasi.all()
    else:
        prestasi_list = Prestasi.objects.all()
    
    return render(request, 'core/prestasi_list.html', {'prestasi_list': prestasi_list})


@login_required
def tambah_prestasi(request):
    """Tambah prestasi baru"""
    if request.user.role != 'mahasiswa':
        messages.error(request, 'Akses ditolak.')
        return redirect('dashboard')
    
    profil = get_object_or_404(ProfilMahasiswa, user=request.user)
    
    if request.method == 'POST':
        form = PrestasiForm(request.POST, request.FILES)
        if form.is_valid():
            prestasi = form.save(commit=False)
            prestasi.mahasiswa = profil
            prestasi.save()
            messages.success(request, 'Prestasi berhasil diajukan! Menunggu validasi dosen.')
            return redirect('prestasi_list')
    else:
        form = PrestasiForm()
    
    return render(request, 'core/tambah_prestasi.html', {'form': form})


@login_required
def prestasi_detail(request, pk):
    """Detail prestasi"""
    prestasi = get_object_or_404(Prestasi, pk=pk)
    return render(request, 'core/prestasi_detail.html', {'prestasi': prestasi})


@login_required
def validasi_prestasi(request, pk):
    """Validasi prestasi (dosen only)"""
    if request.user.role != 'dosen':
        messages.error(request, 'Akses ditolak.')
        return redirect('dashboard')
    
    prestasi = get_object_or_404(Prestasi, pk=pk)
    profil_dosen = get_object_or_404(ProfilDosen, user=request.user)
    
    if request.method == 'POST':
        form = ValidasiPrestasiForm(request.POST, instance=prestasi)
        if form.is_valid():
            prestasi = form.save(commit=False)
            prestasi.validator = profil_dosen
            prestasi.tanggal_validasi = timezone.now()
            prestasi.save()
            
            # Tambah poin jika approved
            if prestasi.status == 'approved':
                prestasi.mahasiswa.tambah_poin(50)
                pesan_notif = f'Prestasi "{prestasi.judul}" Anda telah disetujui! +50 poin'
            else:
                pesan_notif = f'Prestasi "{prestasi.judul}" Anda ditolak.'
            
            # Buat notifikasi
            Notifikasi.objects.create(
                user=prestasi.mahasiswa.user,
                tipe='validasi',
                judul='Update Status Prestasi',
                pesan=pesan_notif,
                link=f'/prestasi/{prestasi.pk}/'
            )
            
            messages.success(request, 'Validasi berhasil!')
            return redirect('prestasi_list')
    else:
        form = ValidasiPrestasiForm(instance=prestasi)
    
    return render(request, 'core/validasi_prestasi.html', {'form': form, 'prestasi': prestasi})


# ============= PROYEK =============
@login_required
def proyek_list(request):
    """Bursa proyek"""
    proyek_list = Proyek.objects.all()
    
    # Filter
    tipe = request.GET.get('tipe')
    if tipe:
        proyek_list = proyek_list.filter(tipe_proyek=tipe)
    
    status = request.GET.get('status')
    if status:
        proyek_list = proyek_list.filter(status=status)
    
    return render(request, 'core/proyek_list.html', {'proyek_list': proyek_list})


@login_required
def proyek_detail(request, pk):
    """Detail proyek"""
    proyek = get_object_or_404(Proyek, pk=pk)
    anggota_list = proyek.anggota.filter(status='accepted')
    pendaftar_list = proyek.anggota.filter(status='pending')
    
    # Cek apakah user sudah mendaftar
    sudah_mendaftar = False
    if request.user.role == 'mahasiswa':
        try:
            profil = request.user.profil_mahasiswa
            sudah_mendaftar = proyek.anggota.filter(mahasiswa=profil).exists()
        except ProfilMahasiswa.DoesNotExist:
            pass
    
    context = {
        'proyek': proyek,
        'anggota_list': anggota_list,
        'pendaftar_list': pendaftar_list,
        'sudah_mendaftar': sudah_mendaftar,
    }
    return render(request, 'core/proyek_detail.html', context)


@login_required
def buat_proyek(request):
    """Buat proyek baru"""
    if request.method == 'POST':
        form = ProyekForm(request.POST)
        if form.is_valid():
            proyek = form.save(commit=False)
            proyek.pembuat = request.user
            proyek.save()
            messages.success(request, f'Proyek "{proyek.nama_proyek}" berhasil dibuat!')
            return redirect('proyek_detail', pk=proyek.pk)
    else:
        form = ProyekForm()
    
    return render(request, 'core/buat_proyek.html', {'form': form})


@login_required
def daftar_proyek(request, pk):
    """Mahasiswa mendaftar ke proyek"""
    if request.user.role != 'mahasiswa':
        messages.error(request, 'Hanya mahasiswa yang bisa mendaftar proyek.')
        return redirect('proyek_detail', pk=pk)
    
    proyek = get_object_or_404(Proyek, pk=pk)
    profil = get_object_or_404(ProfilMahasiswa, user=request.user)
    
    # Cek apakah sudah mendaftar
    if proyek.anggota.filter(mahasiswa=profil).exists():
        messages.warning(request, 'Anda sudah mendaftar di proyek ini.')
        return redirect('proyek_detail', pk=pk)
    
    # Cek apakah proyek penuh
    if proyek.is_full:
        messages.error(request, 'Proyek sudah penuh!')
        return redirect('proyek_detail', pk=pk)
    
    if request.method == 'POST':
        form = LamaranProyekForm(request.POST)
        if form.is_valid():
            anggota = form.save(commit=False)
            anggota.proyek = proyek
            anggota.mahasiswa = profil
            anggota.save()
            
            # Notifikasi pembuat proyek
            Notifikasi.objects.create(
                user=proyek.pembuat,
                tipe='proyek',
                judul='Pendaftar Baru',
                pesan=f'{profil.user.get_full_name()} mendaftar ke proyek "{proyek.nama_proyek}"',
                link=f'/proyek/{proyek.pk}/'
            )
            
            messages.success(request, 'Lamaran berhasil dikirim!')
            return redirect('proyek_detail', pk=pk)
    else:
        form = LamaranProyekForm()
    
    return render(request, 'core/daftar_proyek.html', {'form': form, 'proyek': proyek})


@login_required
def terima_anggota(request, pk):
    """Pembuat proyek menerima anggota"""
    anggota = get_object_or_404(AnggotaProyek, pk=pk)
    
    # Cek apakah user adalah pembuat proyek
    if request.user != anggota.proyek.pembuat:
        messages.error(request, 'Akses ditolak.')
        return redirect('dashboard')
    
    # Cek apakah proyek masih ada slot
    if anggota.proyek.is_full:
        messages.error(request, 'Proyek sudah penuh!')
        return redirect('proyek_detail', pk=anggota.proyek.pk)
    
    anggota.status = 'accepted'
    anggota.tanggal_bergabung = timezone.now()
    anggota.save()
    
    # Tambah poin mahasiswa
    anggota.mahasiswa.tambah_poin(30)
    
    # Update status proyek jika penuh
    if anggota.proyek.is_full:
        anggota.proyek.status = 'full'
        anggota.proyek.save()
    
    # Notifikasi mahasiswa
    Notifikasi.objects.create(
        user=anggota.mahasiswa.user,
        tipe='proyek',
        judul='Lamaran Diterima',
        pesan=f'Selamat! Anda diterima di proyek "{anggota.proyek.nama_proyek}"',
        link=f'/proyek/{anggota.proyek.pk}/'
    )
    
    messages.success(request, f'{anggota.mahasiswa.user.get_full_name()} berhasil diterima!')
    return redirect('proyek_detail', pk=anggota.proyek.pk)


@login_required
def tolak_anggota(request, pk):
    """Pembuat proyek menolak anggota"""
    anggota = get_object_or_404(AnggotaProyek, pk=pk)
    
    if request.user != anggota.proyek.pembuat:
        messages.error(request, 'Akses ditolak.')
        return redirect('dashboard')
    
    anggota.status = 'rejected'
    anggota.save()
    
    # Notifikasi mahasiswa
    Notifikasi.objects.create(
        user=anggota.mahasiswa.user,
        tipe='proyek',
        judul='Lamaran Ditolak',
        pesan=f'Lamaran Anda di proyek "{anggota.proyek.nama_proyek}" ditolak.',
        link=f'/proyek/'
    )
    
    messages.success(request, 'Lamaran berhasil ditolak.')
    return redirect('proyek_detail', pk=anggota.proyek.pk)


# ============= TALENT POOL =============
@login_required
def talent_pool(request):
    """Database talenta mahasiswa"""
    mahasiswa_list = ProfilMahasiswa.objects.all()
    
    # Search & Filter
    form = CariMahasiswaForm(request.GET)
    if form.is_valid():
        keahlian = form.cleaned_data.get('keahlian')
        if keahlian:
            mahasiswa_list = mahasiswa_list.filter(keahlian__nama_keahlian__icontains=keahlian).distinct()
        
        prodi = form.cleaned_data.get('prodi')
        if prodi:
            mahasiswa_list = mahasiswa_list.filter(prodi__icontains=prodi)
        
        min_poin = form.cleaned_data.get('min_poin')
        if min_poin:
            mahasiswa_list = mahasiswa_list.filter(poin__gte=min_poin)
    
    return render(request, 'core/talent_pool.html', {
        'mahasiswa_list': mahasiswa_list,
        'form': form,
    })


# ============= NOTIFIKASI =============
@login_required
def notifikasi_list(request):
    """Daftar notifikasi user"""
    notifikasi_list = request.user.notifikasi.all()
    
    # Mark all as read
    request.user.notifikasi.filter(is_read=False).update(is_read=True)
    
    return render(request, 'core/notifikasi_list.html', {'notifikasi_list': notifikasi_list})


# ============= STATISTICS =============
@login_required
def statistics(request):
    """Statistik sistem (untuk dosen & admin)"""
    stats = {
        'total_users': User.objects.count(),
        'total_mahasiswa': ProfilMahasiswa.objects.count(),
        'total_dosen': ProfilDosen.objects.count(),
        'total_proyek': Proyek.objects.count(),
        'total_prestasi': Prestasi.objects.count(),
        'prestasi_approved': Prestasi.objects.filter(status='approved').count(),
        'prestasi_pending': Prestasi.objects.filter(status='pending').count(),
        'proyek_open': Proyek.objects.filter(status='open').count(),
    }
    
    # Top mahasiswa by poin
    top_mahasiswa = ProfilMahasiswa.objects.order_by('-poin')[:10]
    
    return render(request, 'core/statistics.html', {
        'stats': stats,
        'top_mahasiswa': top_mahasiswa,
    })
