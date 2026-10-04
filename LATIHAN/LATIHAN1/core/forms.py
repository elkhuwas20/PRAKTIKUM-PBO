from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProfilMahasiswa, ProfilDosen, Prestasi, Proyek, AnggotaProyek, Keahlian


class MahasiswaRegistrationForm(UserCreationForm):
    """Form registrasi mahasiswa"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    nim = forms.CharField(max_length=20, required=True)
    prodi = forms.CharField(max_length=100, required=True)
    angkatan = forms.IntegerField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = 'mahasiswa'
        
        if commit:
            user.save()
            ProfilMahasiswa.objects.create(
                user=user,
                nim=self.cleaned_data['nim'],
                prodi=self.cleaned_data['prodi'],
                angkatan=self.cleaned_data['angkatan']
            )
        return user


class DosenRegistrationForm(UserCreationForm):
    """Form registrasi dosen"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    nip = forms.CharField(max_length=20, required=True)
    jurusan = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = 'dosen'
        user.is_staff = True  # Dosen memiliki akses admin
        
        if commit:
            user.save()
            ProfilDosen.objects.create(
                user=user,
                nip=self.cleaned_data['nip'],
                jurusan=self.cleaned_data['jurusan']
            )
        return user


class ProfilMahasiswaForm(forms.ModelForm):
    """Form update profil mahasiswa"""
    class Meta:
        model = ProfilMahasiswa
        fields = ['prodi', 'angkatan', 'ipk', 'bio', 'linkedin', 'github', 'portfolio_url']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'prodi': forms.TextInput(attrs={'class': 'form-control'}),
            'angkatan': forms.NumberInput(attrs={'class': 'form-control'}),
            'ipk': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class KeahlianForm(forms.ModelForm):
    """Form tambah keahlian"""
    class Meta:
        model = Keahlian
        fields = ['nama_keahlian', 'level']
        widgets = {
            'nama_keahlian': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }


class PrestasiForm(forms.ModelForm):
    """Form pengajuan prestasi"""
    class Meta:
        model = Prestasi
        fields = ['judul', 'kategori', 'deskripsi', 'tanggal', 'penyelenggara', 'bukti_file']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'tanggal': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'penyelenggara': forms.TextInput(attrs={'class': 'form-control'}),
            'bukti_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ValidasiPrestasiForm(forms.ModelForm):
    """Form validasi prestasi oleh dosen"""
    class Meta:
        model = Prestasi
        fields = ['status', 'catatan_validator']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'catatan_validator': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ProyekForm(forms.ModelForm):
    """Form pembuatan proyek"""
    class Meta:
        model = Proyek
        fields = ['nama_proyek', 'tipe_proyek', 'deskripsi', 'max_anggota', 
                  'tanggal_mulai', 'tanggal_selesai', 'persyaratan']
        widgets = {
            'nama_proyek': forms.TextInput(attrs={'class': 'form-control'}),
            'tipe_proyek': forms.Select(attrs={'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'max_anggota': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'tanggal_mulai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tanggal_selesai': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'persyaratan': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class LamaranProyekForm(forms.ModelForm):
    """Form melamar ke proyek"""
    class Meta:
        model = AnggotaProyek
        fields = ['pesan_lamaran']
        widgets = {
            'pesan_lamaran': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Ceritakan mengapa Anda cocok untuk proyek ini...'
            }),
        }


class CariMahasiswaForm(forms.Form):
    """Form pencarian mahasiswa di talent pool"""
    keahlian = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari berdasarkan keahlian...'
        })
    )
    prodi = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari berdasarkan program studi...'
        })
    )
    min_poin = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimal poin'
        })
    )
