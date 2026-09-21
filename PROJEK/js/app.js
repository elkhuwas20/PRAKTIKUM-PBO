// ========== KREASI - Main JavaScript File ==========

// ===== DATA MANAGEMENT (localStorage) =====
class DataManager {
    constructor() {
        this.initializeData();
    }

    initializeData() {
        if (!localStorage.getItem('users')) {
            localStorage.setItem('users', JSON.stringify([]));
        }
        if (!localStorage.getItem('prestasi')) {
            localStorage.setItem('prestasi', JSON.stringify([]));
        }
        if (!localStorage.getItem('proyek')) {
            localStorage.setItem('proyek', JSON.stringify([]));
        }
        if (!localStorage.getItem('notifikasi')) {
            localStorage.setItem('notifikasi', JSON.stringify([]));
        }
    }

    // Users
    getUsers() {
        return JSON.parse(localStorage.getItem('users')) || [];
    }

    saveUser(user) {
        const users = this.getUsers();
        users.push(user);
        localStorage.setItem('users', JSON.stringify(users));
    }

    updateUser(userId, updates) {
        const users = this.getUsers();
        const index = users.findIndex(u => u.id === userId);
        if (index !== -1) {
            users[index] = { ...users[index], ...updates };
            localStorage.setItem('users', JSON.stringify(users));
        }
    }

    getUserByEmail(email) {
        return this.getUsers().find(u => u.email === email);
    }

    getCurrentUser() {
        const userId = sessionStorage.getItem('currentUserId');
        if (!userId) return null;
        return this.getUsers().find(u => u.id === userId);
    }

    login(email, password) {
        const user = this.getUserByEmail(email);
        if (user && user.password === password) {
            sessionStorage.setItem('currentUserId', user.id);
            return user;
        }
        return null;
    }

    logout() {
        sessionStorage.removeItem('currentUserId');
    }

    isLoggedIn() {
        return sessionStorage.getItem('currentUserId') !== null;
    }

    // Prestasi
    getPrestasi() {
        return JSON.parse(localStorage.getItem('prestasi')) || [];
    }

    savePrestasi(prestasi) {
        const allPrestasi = this.getPrestasi();
        allPrestasi.push(prestasi);
        localStorage.setItem('prestasi', JSON.stringify(allPrestasi));
    }

    updatePrestasi(prestasiId, updates) {
        const allPrestasi = this.getPrestasi();
        const index = allPrestasi.findIndex(p => p.id === prestasiId);
        if (index !== -1) {
            allPrestasi[index] = { ...allPrestasi[index], ...updates };
            localStorage.setItem('prestasi', JSON.stringify(allPrestasi));
        }
    }

    getPrestasiByUser(userId) {
        return this.getPrestasi().filter(p => p.userId === userId);
    }

    // Proyek
    getProyek() {
        return JSON.parse(localStorage.getItem('proyek')) || [];
    }

    saveProyek(proyek) {
        const allProyek = this.getProyek();
        allProyek.push(proyek);
        localStorage.setItem('proyek', JSON.stringify(allProyek));
    }

    updateProyek(proyekId, updates) {
        const allProyek = this.getProyek();
        const index = allProyek.findIndex(p => p.id === proyekId);
        if (index !== -1) {
            allProyek[index] = { ...allProyek[index], ...updates };
            localStorage.setItem('proyek', JSON.stringify(allProyek));
        }
    }

    // Notifikasi
    getNotifikasi(userId) {
        const allNotifikasi = JSON.parse(localStorage.getItem('notifikasi')) || [];
        return allNotifikasi.filter(n => n.userId === userId);
    }

    saveNotifikasi(notifikasi) {
        const allNotifikasi = JSON.parse(localStorage.getItem('notifikasi')) || [];
        allNotifikasi.push(notifikasi);
        localStorage.setItem('notifikasi', JSON.stringify(allNotifikasi));
    }
}

// Initialize DataManager
const dataManager = new DataManager();

// ===== UI UTILITIES =====
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <strong>${type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ'}</strong>
        <span>${message}</span>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

function generateId() {
    return 'id_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function calculatePoin(user) {
    let poin = 0;
    
    // Poin dari prestasi yang disetujui
    const prestasi = dataManager.getPrestasiByUser(user.id);
    poin += prestasi.filter(p => p.status === 'approved').length * 50;
    
    // Poin dari proyek
    const proyek = dataManager.getProyek();
    proyek.forEach(p => {
        if (p.anggota && p.anggota.some(a => a.userId === user.id && a.status === 'accepted')) {
            poin += 30;
        }
    });
    
    return poin;
}

// ===== NAVIGATION =====
function updateNavbar() {
    const user = dataManager.getCurrentUser();
    const navUser = document.querySelector('.nav-user');
    const navMenu = document.querySelector('.navbar-menu');
    
    if (user) {
        navUser.innerHTML = `
            <span>Hai, ${user.nama}</span>
            <div class="nav-avatar">${user.nama.charAt(0)}</div>
            <button class="btn btn-sm btn-outline" onclick="logout()">Logout</button>
        `;
        
        // Update menu based on role
        if (user.role === 'mahasiswa') {
            navMenu.innerHTML = `
                <li><a href="index.html"><i>🏠</i> Home</a></li>
                <li><a href="pages/dashboard.html"><i>📊</i> Dashboard</a></li>
                <li><a href="pages/prestasi.html"><i>🏆</i> Prestasi</a></li>
                <li><a href="pages/proyek.html"><i>💼</i> Proyek</a></li>
                <li><a href="pages/profil.html"><i>👤</i> Profil</a></li>
            `;
        } else if (user.role === 'dosen') {
            navMenu.innerHTML = `
                <li><a href="index.html"><i>🏠</i> Home</a></li>
                <li><a href="pages/dashboard.html"><i>📊</i> Dashboard</a></li>
                <li><a href="pages/prestasi.html"><i>🏆</i> Validasi</a></li>
                <li><a href="pages/proyek.html"><i>💼</i> Proyek</a></li>
                <li><a href="pages/talent-pool.html"><i>👥</i> Talent Pool</a></li>
            `;
        }
    } else {
        navUser.innerHTML = `
            <a href="pages/login.html" class="btn btn-outline">Login</a>
            <a href="pages/register.html" class="btn btn-outline">Register</a>
        `;
    }
}

function logout() {
    dataManager.logout();
    showToast('Berhasil logout!', 'success');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// ===== FORM VALIDATION =====
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function validateNIM(nim) {
    return /^\d{10}$/.test(nim);
}

function validateNIP(nip) {
    return /^\d{18}$/.test(nip);
}

// ===== STATS CALCULATION =====
function getSystemStats() {
    const users = dataManager.getUsers();
    const prestasi = dataManager.getPrestasi();
    const proyek = dataManager.getProyek();
    
    return {
        totalMahasiswa: users.filter(u => u.role === 'mahasiswa').length,
        totalDosen: users.filter(u => u.role === 'dosen').length,
        totalProyek: proyek.length,
        totalPrestasi: prestasi.filter(p => p.status === 'approved').length
    };
}

// ===== INITIALIZE ON PAGE LOAD =====
document.addEventListener('DOMContentLoaded', function() {
    // Update navbar
    updateNavbar();
    
    // Close modals on click outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
            }
        });
    });
    
    // Form validation real-time
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value) {
                this.style.borderColor = 'var(--danger-color)';
            } else {
                this.style.borderColor = '#ddd';
            }
        });
    });
});

// ===== DEMO DATA (Optional - for testing) =====
function createDemoData() {
    // Create demo users if none exist
    if (dataManager.getUsers().length === 0) {
        // Demo Mahasiswa
        dataManager.saveUser({
            id: generateId(),
            nama: 'Budi Santoso',
            email: 'budi@student.ac.id',
            password: '123456',
            role: 'mahasiswa',
            nim: '2509106001',
            prodi: 'Informatika',
            angkatan: 2025,
            keahlian: ['Python', 'Machine Learning', 'Data Analysis'],
            bio: 'Mahasiswa Informatika yang tertarik di bidang AI',
            createdAt: new Date().toISOString()
        });
        
        // Demo Dosen
        dataManager.saveUser({
            id: generateId(),
            nama: 'Dr. Ahmad Fauzi',
            email: 'ahmad@lecturer.ac.id',
            password: '123456',
            role: 'dosen',
            nip: '198501012010121001',
            jurusan: 'Informatika',
            jabatan: 'Lektor Kepala',
            createdAt: new Date().toISOString()
        });
        
        showToast('Demo data berhasil dibuat! Email: budi@student.ac.id, Password: 123456', 'info');
    }
}

// Export functions for use in other files
window.dataManager = dataManager;
window.showToast = showToast;
window.showModal = showModal;
window.hideModal = hideModal;
window.generateId = generateId;
window.formatDate = formatDate;
window.calculatePoin = calculatePoin;
window.updateNavbar = updateNavbar;
window.logout = logout;
window.getSystemStats = getSystemStats;
window.createDemoData = createDemoData;
