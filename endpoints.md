
# Dokumentasi Endpoint API
## Sistem Manajemen Tugas Mahasiswa

REST API ini dibuat menggunakan FastAPI, Python, dan PostgreSQL melalui Supabase.

**Base URL:** `http://127.0.0.1:8001`

## 1. Endpoint Utama

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/` | Menampilkan pesan API |
| GET | `/cek-database` | Memeriksa koneksi database |

## 2. Mahasiswa

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/mahasiswa` | Menampilkan semua mahasiswa |
| GET | `/mahasiswa/{id_mahasiswa}` | Menampilkan detail mahasiswa |
| POST | `/mahasiswa` | Menambahkan mahasiswa |
| PUT | `/mahasiswa/{id_mahasiswa}` | Mengganti data mahasiswa |
| PATCH | `/mahasiswa/{id_mahasiswa}` | Memperbarui sebagian data mahasiswa |
| DELETE | `/mahasiswa/{id_mahasiswa}` | Menghapus mahasiswa |

## 3. Mata Kuliah

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/mata-kuliah` | Menampilkan semua mata kuliah |
| GET | `/mata-kuliah/{id_matkul}` | Menampilkan detail mata kuliah |
| POST | `/mata-kuliah` | Menambahkan mata kuliah |
| PUT | `/mata-kuliah/{id_matkul}` | Mengganti data mata kuliah |
| PATCH | `/mata-kuliah/{id_matkul}` | Memperbarui sebagian data mata kuliah |
| DELETE | `/mata-kuliah/{id_matkul}` | Menghapus mata kuliah |

## 4. Tugas

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/tugas` | Menampilkan semua tugas |
| GET | `/tugas/{id_tugas}` | Menampilkan detail tugas |
| POST | `/tugas` | Menambahkan tugas |
| PUT | `/tugas/{id_tugas}` | Mengganti data tugas |
| PATCH | `/tugas/{id_tugas}` | Memperbarui sebagian data tugas |
| DELETE | `/tugas/{id_tugas}` | Menghapus tugas |

## 5. Label

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/label` | Menampilkan semua label |
| GET | `/label/{id_label}` | Menampilkan detail label |
| POST | `/label` | Menambahkan label |
| PUT | `/label/{id_label}` | Mengganti data label |
| PATCH | `/label/{id_label}` | Memperbarui sebagian data label |
| DELETE | `/label/{id_label}` | Menghapus label |

## 6. Relasi Tugas dan Label

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/tugas-label` | Menampilkan relasi tugas dan label |
| POST | `/tugas-label` | Menambahkan relasi tugas dan label |
| DELETE | `/tugas-label/{id_tugas_label}` | Menghapus relasi tugas dan label |

## 7. Format Data Tugas

Contoh JSON untuk menambahkan tugas melalui `POST /tugas`:

```json
{
  "judul": "Membuat ERD",
  "catatan": "Tugas basis data",
  "deadline": "2026-11-01",
  "prioritas": "tinggi",
  "status": "belum selesai",
  "id_mahasiswa": 1,
  "id_matkul": 1
}
```

Pastikan `id_mahasiswa` dan `id_matkul` sesuai dengan ID yang tersedia di database.

Nilai prioritas yang diperbolehkan:
- `rendah`
- `sedang`
- `tinggi`

Nilai status yang diperbolehkan:
- `belum selesai`
- `dikerjakan`
- `selesai`

## 8. Kode Status HTTP

| Kode | Keterangan |
|---|---|
| 200 | Permintaan berhasil |
| 201 | Data berhasil dibuat |
| 400 | Permintaan tidak valid |
| 404 | Data tidak ditemukan |
| 409 | Terjadi konflik data |
| 422 | Data input tidak valid |

## 9. Dokumentasi Swagger

Jalankan backend, kemudian buka:

`http://127.0.0.1:8001/docs`

Pengujian API dilakukan melalui Swagger UI dengan metode GET, POST, PUT, PATCH, dan DELETE.
