# 🎓 KREASI - Website Version

## 📋 Deskripsi

Website KREASI adalah versi **pure HTML, CSS, dan JavaScript** (tanpa framework) yang fully functional dengan localStorage sebagai database. Website ini memiliki semua fitur sistem manajemen kolaborasi dan rekam jejak mahasiswa informatika.

---

## ✨ Fitur Lengkap

### 🎯 Fitur Utama:
- ✅ **Authentication System** (Login/Logout/Register)
- ✅ **Role-Based Access** (Mahasiswa & Dosen)
- ✅ **Dashboard** dengan statistik lengkap
- ✅ **Prestasi Management** (Ajukan, Upload, Validasi)
- ✅ **Proyek Kolaborasi** (Buat, Daftar, Rekrut)
- ✅ **Talent Pool** (Database mahasiswa dengan filter)
- ✅ **Profil Management** (Edit, Tambah keahlian)
- ✅ **Notifikasi System** (Real-time toast)
- ✅ **Sistem Poin** (Gamifikasi dengan target TAK/SAT)
- ✅ **LocalStorage** (Data persisten di browser)
- ✅ **Responsive Design** (Mobile-friendly)
- ✅ **Modern UI** (Gradient, Animation, Shadow)

---

## 📂 Struktur Folder

```
PROJEK/
├── index.html              # Landing page
├── css/
│   └── style.css          # Main stylesheet (lengkap!)
├── js/
│   └── app.js             # Main JavaScript (lengkap!)
├── pages/
│   ├── login.html         # Halaman login
│   ├── register.html      # Halaman register
│   ├── dashboard.html     # Dashboard user
│   ├── prestasi.html      # Manajemen prestasi
│   ├── proyek.html        # Bursa proyek
│   ├── profil.html        # Profil user
│   └── talent-pool.html   # Database talenta
├── assets/                # Untuk gambar/icon (opsional)
└── README.md              # File ini
```

---

## 🚀 Cara Menjalankan

### **Metode 1: Langsung Buka di Browser**
1. Buka folder `PROJEK`
2. Double-click file `index.html`
3. Website akan terbuka di browser

### **Metode 2: Menggunakan Live Server (Recommended)**
1. Install VS Code extension "Live Server"
2. Right-click pada `index.html`
3. Pilih "Open with Live Server"
4. Website akan buka di `http://localhost:5500`

---

## 👥 Demo Account

Untuk testing, gunakan demo data:

### **Mahasiswa:**
- Email: `budi@student.ac.id`
- Password: `123456`
- NIM: 2509106001

### **Dosen:**
- Email: `ahmad@lecturer.ac.id`
- Password: `123456`
- NIP: 198501012010121001

**Cara membuat demo data:**
1. Klik tombol "Demo Data" di landing page
2. Atau registrasi manual

---

## 🎨 Fitur UI/UX

### **Design System:**
- **Colors:** Primary (#4a90e2), Success (#27ae60), Warning (#f39c12), Danger (#e74c3c)
- **Gradients:** 4 gradient themes untuk cards
- **Typography:** Segoe UI font family
- **Shadows:** 3 levels (sm, md, lg)
- **Animations:** Fade in, slide in, modal animations
- **Responsive:** Mobile-first design

### **Components:**
- Navbar dengan user menu
- Hero section
- Stats counters
- Feature cards
- Form controls
- Buttons (6 variants)
- Alerts (4 types)
- Modals
- Progress bars
- Tables
- Toast notifications

---

## 💻 Alur Penggunaan

### **MAHASISWA:**

1. **Register** 
   - Klik "Register" di navbar
   - Pilih "Mahasiswa"
   - Isi NIM, Prodi, Angkatan
   - Submit

2. **Login**
   - Masukkan email & password
   - Redirect ke Dashboard

3. **Dashboard**
   - Lihat poin, prestasi, proyek
   - Progress bar TAK/SAT dan Beasiswa
   - Quick actions

4. **Tambah Prestasi**
   - Klik "Tambah Prestasi"
   - Isi form (judul, kategori, deskripsi, tanggal)
   - Submit → Status: Pending

5. **Daftar Proyek**
   - Browse bursa proyek
   - Klik "Daftar"
   - Tulis pesan lamaran
   - Submit → Tunggu approval

6. **Lihat Profil**
   - Edit bio
   - Tambah keahlian
   - Lihat prestasi & proyek

---

### **DOSEN:**

1. **Register**
   - Pilih "Dosen"
   - Isi NIP, Jurusan, Jabatan
   - Submit

2. **Login**
   - Masukkan email & password

3. **Dashboard**
   - Lihat prestasi pending
   - Lihat proyek yang dibuat
   - Total validasi

4. **Validasi Prestasi**
   - Klik "Validasi Prestasi"
   - Lihat daftar pending
   - Approve/Reject dengan catatan
   - Mahasiswa dapat +50 poin jika approved

5. **Buat Proyek**
   - Klik "Buat Proyek"
   - Isi detail proyek
   - Submit

6. **Rekrut Anggota**
   - Buka detail proyek
   - Lihat pendaftar
   - Terima/tolak
   - Mahasiswa dapat +30 poin jika diterima

7. **Talent Pool**
   - Cari mahasiswa by keahlian
   - Filter by prodi
   - Filter by poin
   - Lihat profil lengkap

---

## 🎯 Sistem Poin (Gamifikasi)

| Aktivitas | Poin |
|-----------|------|
| Prestasi Divalidasi | +50 |
| Diterima di Proyek | +30 |

| Target | Min Poin |
|--------|----------|
| TAK/SAT | 200 |
| Beasiswa | 500 |

---

## 💾 Data Management (localStorage)

### **Data yang Disimpan:**

```javascript
// users
[{
  id: "id_xxx",
  nama: "...",
  email: "...",
  password: "...",
  role: "mahasiswa/dosen",
  nim/nip: "...",
  prodi/jurusan: "...",
  keahlian: [],
  createdAt: "..."
}]

// prestasi
[{
  id: "id_xxx",
  userId: "...",
  judul: "...",
  kategori: "...",
  deskripsi: "...",
  tanggal: "...",
  status: "pending/approved/rejected",
  validatorId: "...",
  catatan: "...",
  createdAt: "..."
}]

// proyek
[{
  id: "id_xxx",
  pembuatId: "...",
  namaProyek: "...",
  deskripsi: "...",
  tipe: "...",
  maxAnggota: 0,
  anggota: [{userId, status}],
  status: "open/full/closed",
  createdAt: "..."
}]

// notifikasi
[{
  id: "id_xxx",
  userId: "...",
  tipe: "...",
  judul: "...",
  pesan: "...",
  isRead: false,
  createdAt: "..."
}]
```

### **Reset Data:**
```javascript
// Di Console Browser
localStorage.clear();
sessionStorage.clear();
```

---

## 🔧 Customization

### **Ubah Warna:**
Buka `css/style.css` dan edit di bagian `:root`
```css
:root {
    --primary-color: #4a90e2;  /* Ubah sesuai selera */
    --secondary-color: #50c878;
    /* ... */
}
```

### **Tambah Fitur Baru:**
1. Edit `js/app.js` untuk logic
2. Tambah HTML page di folder `pages/`
3. Styling di `css/style.css`

---

## 📱 Responsive Breakpoints

- **Desktop:** > 768px
- **Tablet:** 768px
- **Mobile:** < 768px

---

## 🐛 Troubleshooting

### **Data Tidak Tersimpan:**
- Pastikan browser mendukung localStorage
- Check Console untuk error
- Clear cache dan reload

### **Login Gagal:**
- Pastikan sudah register dulu
- Check email & password
- Gunakan demo account untuk testing

### **Halaman Tidak Load:**
- Check path file benar (`../css/style.css`)
- Buka dengan Live Server, bukan file://

---

## ✅ Checklist Fitur

- [x] Landing Page
- [x] Login/Register
- [x] Dashboard (Mahasiswa & Dosen)
- [x] Prestasi Management
- [x] Proyek Management
- [x] Profil User
- [x] Talent Pool
- [x] Sistem Poin
- [x] Notifikasi (Toast)
- [x] LocalStorage Database
- [x] Responsive Design
- [x] Animations
- [x] Form Validation

---

## 🎉 Kesimpulan

Website KREASI sudah **fully functional** dengan:
- ✅ Pure HTML, CSS, JavaScript (No Framework!)
- ✅ Data persistent dengan localStorage
- ✅ Modern UI dengan animations
- ✅ Responsive design
- ✅ Role-based system
- ✅ Gamifikasi lengkap
- ✅ ~3000+ lines of code

**Status:** ✅ **Production Ready!**

---

**Developed with ❤️ for KREASI Project**

*Happy Coding!* 🚀
