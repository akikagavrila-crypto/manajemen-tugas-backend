
# Sistem Manajemen Tugas Mahasiswa

REST API untuk mengelola data mahasiswa, mata kuliah, tugas, dan label tugas. Project ini menggunakan FastAPI dan PostgreSQL melalui Supabase.

## Teknologi

- Python
- FastAPI
- PostgreSQL
- Supabase
- Psycopg
- Pydantic
- Uvicorn

## Fitur

- CRUD data mahasiswa
- CRUD data mata kuliah
- CRUD data tugas
- CRUD data label
- Menghubungkan tugas dengan label
- Melihat daftar dan detail data
- Mengecek koneksi database
- Dokumentasi API melalui Swagger UI

## Struktur Database

Project ini memiliki 5 tabel:

1. `mahasiswa`
2. `mata_kuliah`
3. `tugas`
4. `label`
5. `tugas_label`

### Relasi Antar Tabel

- `tugas.id_mahasiswa` → `mahasiswa.id_mahasiswa`
- `tugas.id_matkul` → `mata_kuliah.id_matkul`
- `tugas_label.id_tugas` → `tugas.id_tugas`
- `tugas_label.id_label` → `label.id_label`

Diagram ERD tersedia di [`docs/erd.png`](docs/erd.png).

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/akikagavrila-crypto/manajemen-tugas-backend.git
cd manajemen-tugas-backend
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

Aktifkan di Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Database

Buat file `.env` di direktori utama project:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

Ganti nilai tersebut dengan connection string PostgreSQL dari Supabase.

**Penting:** Jangan mengunggah file `.env` ke GitHub karena berisi kredensial database.

### 5. Jalankan Server

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

## Dokumentasi API

Setelah server berjalan, buka:

- Swagger UI: http://127.0.0.1:8001/docs
- Root endpoint: http://127.0.0.1:8001/
- Cek database: http://127.0.0.1:8001/cek-database

Alamat tersebut berlaku saat backend dijalankan secara lokal.

## Daftar Endpoint

### Mahasiswa

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/mahasiswa` | Melihat semua mahasiswa |
| GET | `/mahasiswa/{id}` | Melihat detail mahasiswa |
| POST | `/mahasiswa` | Menambahkan mahasiswa |
| PUT | `/mahasiswa/{id}` | Mengubah data mahasiswa |
| PATCH | `/mahasiswa/{id}` | Mengubah sebagian data mahasiswa |
| DELETE | `/mahasiswa/{id}` | Menghapus mahasiswa |

### Mata Kuliah

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/mata-kuliah` | Melihat semua mata kuliah |
| GET | `/mata-kuliah/{id}` | Melihat detail mata kuliah |
| POST | `/mata-kuliah` | Menambahkan mata kuliah |
| PUT | `/mata-kuliah/{id}` | Mengubah data mata kuliah |
| PATCH | `/mata-kuliah/{id}` | Mengubah sebagian data mata kuliah |
| DELETE | `/mata-kuliah/{id}` | Menghapus mata kuliah |

### Tugas

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/tugas` | Melihat semua tugas |
| GET | `/tugas/{id}` | Melihat detail tugas |
| POST | `/tugas` | Menambahkan tugas |
| PUT | `/tugas/{id}` | Mengubah data tugas |
| PATCH | `/tugas/{id}` | Mengubah sebagian data tugas |
| DELETE | `/tugas/{id}` | Menghapus tugas |

### Label

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/label` | Melihat semua label |
| GET | `/label/{id}` | Melihat detail label |
| POST | `/label` | Menambahkan label |
| PUT | `/label/{id}` | Mengubah data label |
| PATCH | `/label/{id}` | Mengubah sebagian data label |
| DELETE | `/label/{id}` | Menghapus label |

### Relasi Tugas dan Label

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/tugas-label` | Melihat relasi tugas dan label |
| POST | `/tugas-label` | Menambahkan relasi tugas dan label |
| DELETE | `/tugas-label/{id}` | Menghapus relasi tugas dan label |

Lihat [`docs/endpoints.md`](docs/endpoints.md) dan Swagger UI untuk detail request dan response.

## Struktur Project

```text
manajemen-tugas-backend/
├── main.py
├── requirements.txt
├── README.md
├── .env
├── docs/
│   ├── endpoints.md
│   └── erd.png
└── screenshots/
```

## Pengujian API

Pengujian dilakukan melalui Swagger UI menggunakan fitur **Try it out** dan **Execute**.

Operasi yang diuji meliputi:

- GET: melihat data
- POST: menambahkan data
- PUT: mengubah data
- DELETE: menghapus data

## Repository

GitHub: https://github.com/akikagavrila-crypto/manajemen-tugas-backend

## Pengembang

Project Sistem Manajemen Tugas Mahasiswa.
