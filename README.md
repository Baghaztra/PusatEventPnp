# Pusat Event PNP

## 📌 Deskripsi

**Pusat Event PNP** adalah sebuah platform berbasis web untuk pengelolaan dan publikasi event-event kampus di lingkungan **Politeknik Negeri Padang (PNP)**. Proyek ini merupakan tugas proyek semester 5 dan dikembangkan secara mandiri.

Aplikasi ini dibangun dengan arsitektur **frontend-backend terpisah**, menggunakan **Vue.js** untuk frontend, **Flask** untuk backend, serta **MySQL** sebagai database.

---

## 📦 Teknologi yang Digunakan

* **Vue 3** (Frontend)
* **Vite** (Bundler frontend)
* **Flask** (Backend)
* **Python 3.10**
* **MySQL** (Database)

---

## 📁 Struktur Repository

```
Pusat-Event-PNP/
├── backend/      # Proyek backend Flask
└── frontend/     # Proyek frontend Vue 3
```

---

## 📜 Fitur Utama

* 📃 Manajemen event (CRUD event)
* 🔍 Pencarian event berdasarkan kategori dan tanggal
* 📊 Dashboard admin untuk monitoring event
* 📑 Publikasi event ke halaman utama frontend

---

## 🛠️ Cara Menjalankan Proyek

### 📌 Backend (Flask)

1. Masuk ke folder backend:

   ```bash
   cd backend
   ```
2. Buat virtual environment dan aktifkan:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependency:

   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server backend:

   ```bash
   flask run
   ```

### 📌 Frontend (Vue 3)

1. Masuk ke folder frontend:

   ```bash
   cd frontend
   ```
2. Install dependency:

   ```bash
   npm install
   ```
3. Jalankan server frontend:

   ```bash
   npm run dev
   ```

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan akademik semester 5 di Politeknik Negeri Padang.

> **Baghaztra Van Ril** (Developer)
