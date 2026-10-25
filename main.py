
import os
from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL belum diatur di file .env")
    return psycopg.connect(
        database_url,
        sslmode="require",
        row_factory=dict_row,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_connection() as conn:
        conn.execute("SELECT 1")
    yield


app = FastAPI(
    title="Sistem Manajemen Tugas Mahasiswa",
    description="REST API untuk mengelola tugas mahasiswa",
    version="1.0.0",
    lifespan=lifespan,
)


# =========================
# MODEL DATA
# =========================

class MahasiswaInput(BaseModel):
    nim: str = Field(min_length=1, max_length=30)
    nama: str = Field(min_length=1, max_length=100)
    email: EmailStr


class MahasiswaUpdate(BaseModel):
    nim: Optional[str] = Field(default=None, max_length=30)
    nama: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = None


class MataKuliahInput(BaseModel):
    kode_matkul: str = Field(min_length=1, max_length=30)
    nama_matkul: str = Field(min_length=1, max_length=100)


class MataKuliahUpdate(BaseModel):
    kode_matkul: Optional[str] = Field(default=None, max_length=30)
    nama_matkul: Optional[str] = Field(default=None, max_length=100)


class TugasInput(BaseModel):
    judul: str = Field(min_length=1, max_length=200)
    catatan: Optional[str] = None
    deadline: Optional[date] = None
    prioritas: str = Field(default="sedang", pattern="^(rendah|sedang|tinggi)$")
    status: str = Field(
        default="belum selesai",
        pattern="^(belum selesai|dikerjakan|selesai)$",
    )
    id_mahasiswa: int
    id_matkul: int


class TugasUpdate(BaseModel):
    judul: Optional[str] = Field(default=None, max_length=200)
    catatan: Optional[str] = None
    deadline: Optional[date] = None
    prioritas: Optional[str] = Field(
        default=None, pattern="^(rendah|sedang|tinggi)$"
    )
    status: Optional[str] = Field(
        default=None, pattern="^(belum selesai|dikerjakan|selesai)$"
    )
    id_mahasiswa: Optional[int] = None
    id_matkul: Optional[int] = None


class LabelInput(BaseModel):
    nama_label: str = Field(min_length=1, max_length=60)


class LabelUpdate(BaseModel):
    nama_label: Optional[str] = Field(default=None, max_length=60)


class TugasLabelInput(BaseModel):
    id_tugas: int
    id_label: int


# =========================
# FUNGSI BANTU DATABASE
# =========================

def rows(query, params=()):
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def row(query, params=()):
    result = rows(query, params)
    return result[0] if result else None


def create_record(table, fields):
    allowed = {
        "mahasiswa": "id_mahasiswa",
        "mata_kuliah": "id_matkul",
        "tugas": "id_tugas",
        "label": "id_label",
        "tugas_label": "id_tugas_label",
    }

    if table not in allowed:
        raise HTTPException(status_code=400, detail="Tabel tidak diizinkan.")

    keys = list(fields)
    columns = ", ".join(keys)
    placeholders = ", ".join("%s" for _ in keys)
    id_col = allowed[table]

    sql = (
        f"INSERT INTO {table} ({columns}) "
        f"VALUES ({placeholders}) RETURNING {id_col}"
    )

    try:
        with get_connection() as conn:
            result = conn.execute(
                sql, [fields[key] for key in keys]
            ).fetchone()
            return result[id_col]
    except psycopg.IntegrityError as e:
        raise HTTPException(
            status_code=409,
            detail=f"Data bertentangan dengan aturan database: {e}",
        ) from e


def update_record(table, id_col, item_id, payload, allowed_fields):
    fields = {
        key: value
        for key, value in payload.items()
        if key in allowed_fields and value is not None
    }

    if not fields:
        raise HTTPException(
            status_code=400,
            detail="Tidak ada data yang dikirim untuk diperbarui.",
        )

    assignments = ", ".join(f"{key} = %s" for key in fields)

    try:
        with get_connection() as conn:
            result = conn.execute(
                f"UPDATE {table} SET {assignments} WHERE {id_col} = %s",
                [*fields.values(), item_id],
            )
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Data tidak ditemukan."
                )
    except psycopg.IntegrityError as e:
        raise HTTPException(
            status_code=409,
            detail=f"Data bertentangan dengan aturan database: {e}",
        ) from e

    return row(
        f"SELECT * FROM {table} WHERE {id_col} = %s",
        (item_id,),
    )


def delete_record(table, id_col, item_id):
    try:
        with get_connection() as conn:
            result = conn.execute(
                f"DELETE FROM {table} WHERE {id_col} = %s",
                (item_id,),
            )
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Data tidak ditemukan."
                )
    except psycopg.IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return {"pesan": "Data berhasil dihapus."}


def require_record(query, params):
    result = row(query, params)
    if result is None:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan.")
    return result


# =========================
# BERANDA DAN CEK DATABASE
# =========================

@app.get("/")
def beranda():
    return {
        "pesan": "API Manajemen Tugas Mahasiswa berhasil dijalankan!"
    }


@app.get("/cek-database")
def cek_database():
    with get_connection() as conn:
        conn.execute("SELECT 1")
    return {"pesan": "Koneksi ke Supabase berhasil."}


# =========================
# CRUD MAHASISWA
# =========================

@app.get("/mahasiswa")
def daftar_mahasiswa():
    return {
        "pesan": "Daftar mahasiswa berhasil diambil.",
        "data": rows("SELECT * FROM mahasiswa ORDER BY id_mahasiswa"),
    }


@app.get("/mahasiswa/{id_mahasiswa}")
def detail_mahasiswa(id_mahasiswa: int):
    return require_record(
        "SELECT * FROM mahasiswa WHERE id_mahasiswa = %s",
        (id_mahasiswa,),
    )


@app.post("/mahasiswa", status_code=status.HTTP_201_CREATED)
def tambah_mahasiswa(item: MahasiswaInput):
    new_id = create_record("mahasiswa", item.model_dump(mode="json"))
    return require_record(
        "SELECT * FROM mahasiswa WHERE id_mahasiswa = %s", (new_id,)
    )


@app.put("/mahasiswa/{id_mahasiswa}")
def ubah_mahasiswa(id_mahasiswa: int, item: MahasiswaInput):
    return update_record(
        "mahasiswa",
        "id_mahasiswa",
        id_mahasiswa,
        item.model_dump(mode="json"),
        {"nim", "nama", "email"},
    )


@app.patch("/mahasiswa/{id_mahasiswa}")
def patch_mahasiswa(id_mahasiswa: int, item: MahasiswaUpdate):
    return update_record(
        "mahasiswa",
        "id_mahasiswa",
        id_mahasiswa,
        item.model_dump(exclude_unset=True, mode="json"),
        {"nim", "nama", "email"},
    )


@app.delete("/mahasiswa/{id_mahasiswa}")
def hapus_mahasiswa(id_mahasiswa: int):
    return delete_record("mahasiswa", "id_mahasiswa", id_mahasiswa)


# =========================
# CRUD MATA KULIAH
# =========================

@app.get("/mata-kuliah")
def daftar_matkul():
    return {
        "pesan": "Daftar mata kuliah berhasil diambil.",
        "data": rows("SELECT * FROM mata_kuliah ORDER BY id_matkul"),
    }


@app.get("/mata-kuliah/{id_matkul}")
def detail_matkul(id_matkul: int):
    return require_record(
        "SELECT * FROM mata_kuliah WHERE id_matkul = %s", (id_matkul,)
    )


@app.post("/mata-kuliah", status_code=status.HTTP_201_CREATED)
def tambah_matkul(item: MataKuliahInput):
    new_id = create_record("mata_kuliah", item.model_dump())
    return require_record(
        "SELECT * FROM mata_kuliah WHERE id_matkul = %s", (new_id,)
    )


@app.put("/mata-kuliah/{id_matkul}")
def ubah_matkul(id_matkul: int, item: MataKuliahInput):
    return update_record(
        "mata_kuliah",
        "id_matkul",
        id_matkul,
        item.model_dump(),
        {"kode_matkul", "nama_matkul"},
    )


@app.patch("/mata-kuliah/{id_matkul}")
def patch_matkul(id_matkul: int, item: MataKuliahUpdate):
    return update_record(
        "mata_kuliah",
        "id_matkul",
        id_matkul,
        item.model_dump(exclude_unset=True),
        {"kode_matkul", "nama_matkul"},
    )


@app.delete("/mata-kuliah/{id_matkul}")
def hapus_matkul(id_matkul: int):
    return delete_record("mata_kuliah", "id_matkul", id_matkul)


# =========================
# CRUD TUGAS
# =========================

TUGAS_QUERY = """
SELECT t.*,
       m.nama AS nama_mahasiswa,
       mk.nama_matkul AS nama_matkul
FROM tugas t
JOIN mahasiswa m ON t.id_mahasiswa = m.id_mahasiswa
JOIN mata_kuliah mk ON t.id_matkul = mk.id_matkul
"""


@app.get("/tugas")
def daftar_tugas():
    return {
        "pesan": "Daftar tugas berhasil diambil.",
        "data": rows(TUGAS_QUERY + " ORDER BY t.id_tugas"),
    }


@app.get("/tugas/{id_tugas}")
def detail_tugas(id_tugas: int):
    return require_record(
        TUGAS_QUERY + " WHERE t.id_tugas = %s",
        (id_tugas,),
    )


@app.post("/tugas", status_code=status.HTTP_201_CREATED)
def tambah_tugas(item: TugasInput):
    new_id = create_record("tugas", item.model_dump())
    return detail_tugas(new_id)


@app.put("/tugas/{id_tugas}")
def ubah_tugas(id_tugas: int, item: TugasInput):
    update_record(
        "tugas",
        "id_tugas",
        id_tugas,
        item.model_dump(),
        {
            "judul", "catatan", "deadline", "prioritas",
            "status", "id_mahasiswa", "id_matkul",
        },
    )
    return detail_tugas(id_tugas)


@app.patch("/tugas/{id_tugas}")
def patch_tugas(id_tugas: int, item: TugasUpdate):
    update_record(
        "tugas",
        "id_tugas",
        id_tugas,
        item.model_dump(exclude_unset=True),
        {
            "judul", "catatan", "deadline", "prioritas",
            "status", "id_mahasiswa", "id_matkul",
        },
    )
    return detail_tugas(id_tugas)


@app.delete("/tugas/{id_tugas}")
def hapus_tugas(id_tugas: int):
    return delete_record("tugas", "id_tugas", id_tugas)


# =========================
# CRUD LABEL
# =========================

@app.get("/label")
def daftar_label():
    return {
        "pesan": "Daftar label berhasil diambil.",
        "data": rows("SELECT * FROM label ORDER BY id_label"),
    }


@app.get("/label/{id_label}")
def detail_label(id_label: int):
    return require_record(
        "SELECT * FROM label WHERE id_label = %s", (id_label,)
    )


@app.post("/label", status_code=status.HTTP_201_CREATED)
def tambah_label(item: LabelInput):
    new_id = create_record("label", item.model_dump())
    return require_record(
        "SELECT * FROM label WHERE id_label = %s", (new_id,)
    )


@app.put("/label/{id_label}")
def ubah_label(id_label: int, item: LabelInput):
    return update_record(
        "label",
        "id_label",
        id_label,
        item.model_dump(),
        {"nama_label"},
    )


@app.patch("/label/{id_label}")
def patch_label(id_label: int, item: LabelUpdate):
    return update_record(
        "label",
        "id_label",
        id_label,
        item.model_dump(exclude_unset=True),
        {"nama_label"},
    )


@app.delete("/label/{id_label}")
def hapus_label(id_label: int):
    return delete_record("label", "id_label", id_label)


# =========================
# RELASI TUGAS DAN LABEL
# =========================

@app.get("/tugas-label")
def daftar_tugas_label():
    return {
        "pesan": "Daftar relasi tugas dan label berhasil diambil.",
        "data": rows("""
            SELECT tl.id_tugas_label, tl.id_tugas, tl.id_label,
                   t.judul, l.nama_label
            FROM tugas_label tl
            JOIN tugas t ON tl.id_tugas = t.id_tugas
            JOIN label l ON tl.id_label = l.id_label
            ORDER BY tl.id_tugas_label
        """),
    }


@app.post("/tugas-label", status_code=status.HTTP_201_CREATED)
def tambah_tugas_label(item: TugasLabelInput):
    new_id = create_record("tugas_label", item.model_dump())
    return require_record(
        "SELECT * FROM tugas_label WHERE id_tugas_label = %s",
        (new_id,),
    )


@app.delete("/tugas-label/{id_tugas_label}")
def hapus_tugas_label(id_tugas_label: int):
    return delete_record(
        "tugas_label", "id_tugas_label", id_tugas_label
    )
