
# 📊 TKA Scrapper — Pengambil Data Hasil TKA Kemendikdasmen

> **Scraper otomatis berbasis Python + Playwright** untuk mengekstrak data hasil **Tes Kemampuan Akademik (TKA)** dari portal resmi [Kemendikdasmen](https://tka.kemendikdasmen.go.id/hasiltka/) dan menyimpannya ke file Excel (`.xlsx`).

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-1.49.1-green?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-orange?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🎯 Fitur Utama

- ✅ **Scraping otomatis** dari portal resmi TKA Kemendikdasmen
- ✅ **Pilih jenjang** — SMA, SMK, Paket C, SLB, atau semua sekaligus
- ✅ **Pilih provinsi** — satu, beberapa, atau semua 39 provinsi se-Indonesia
- ✅ **Output Excel (.xlsx)** siap analisis dengan kolom rata-rata otomatis

---

## 📋 Prasyarat

- **Python 3.9+**
- **pip** (Python package manager)
- Koneksi internet untuk mengakses portal TKA

---

## 🚀 Cara Instalasi & Penggunaan

### 1. Clone repositori ini

```bash
git clone https://github.com/ghazy-rajendra/TKA-Scrapper.git
cd TKA-Scrapper
```

### 2. Install dependensi Python

```bash
pip install -r requirements.txt
```

### 3. Install browser Playwright (Chromium)

```bash
playwright install chromium
```

### 4. Jalankan scraper

```bash
python scrape_tka.py
```

---

## 📁 Struktur Output

File hasil scraping disimpan otomatis di direktori yang sama dengan format nama:

```
hasil_tka_<provinsi>_<jenjang>.xlsx
```

### Kolom pada file Excel

| Kolom | Keterangan |
|-------|-----------|
| `KODE PROV` | Kode provinsi |
| `PROVINSI` | Nama provinsi |
| `<Mata Pelajaran>` | Nilai rata-rata per mapel |
| `Rata-rata Keseluruhan TKA` | Rata-rata semua mapel |

---

## 📦 Dependensi

| Paket | Versi | 
|-------|-------|
| `playwright` | 
| `pandas` | 2.2.3 | 
| `openpyxl` | (auto) |

---

## 📄 Lisensi

Proyek ini menggunakan lisensi **MIT** — bebas digunakan untuk keperluan pribadi maupun akademis.

---

## ⚠️ Disclaimer

Tool ini dibuat untuk keperluan **riset dan analisis data pendidikan** secara independen. Data yang diambil bersumber dari portal publik resmi **Kemendikdasmen RI** hasil TKA Tahun 2025. Penggunaan data hasil scraping sepenuhnya menjadi tanggung jawab pengguna.

---
