# 🛡️ AI Privacy Shield — AI Prompt Security

> **Real-Time PII Masking & Privacy Guard for AI Prompts (ChatGPT & Google Gemini)**

**AI Privacy Shield** adalah solusi keamanan privasi data berbasis **Chrome Extension (Manifest V3)** dan **FastAPI Backend (Python)**. Sistem ini memanfaatkan **Microsoft Presidio** yang dikustomisasi khusus untuk mendeteksi dan menyamarkan data pribadi sensitif (*Personally Identifiable Information* / PII) Indonesia—seperti **NIK (Nomor Induk Kependudukan)**, **Nomor Handphone (+62 / 08xx)**, **Nama Orang**, dan **Email**—sebelum prompt dikirimkan ke model AI publik.

---

## 🚀 Fitur Utama

- 🔍 **Real-Time Prompt Interception**: Menangkap teks prompt pada antarmuka web AI (ChatGPT, Google Gemini) sebelum terkirim ke server penyedia LLM.
- ⚡ **High-Performance Sanitization API**: Didukung oleh FastAPI dan Uvicorn untuk pemrosesan teks asinkron berkecepatan tinggi.
- 🇮🇩 **Custom Indonesian PII Recognizers**:
  - **ID_NIK**: Regex 16-digit berbasis pola kependudukan dengan *context-aware detection* ("nik", "ktp", "nomor induk", dll).
  - **ID_PHONE**: Deteksi variasi nomor telepon Indonesia (`+62`, `62`, atau `08`).
  - **Standard Entities**: Mendukung entitas global Presidio bawaan (`PERSON`, `EMAIL_ADDRESS`, dsb).
- 📊 **Evaluation & Benchmark Ready**: Disertai skrip pembuat dataset sintetis (*Faker*) dan pengunduh data uji IndoNER (*IndoNLU Benchmark*) untuk evaluasi metrik *Precision*, *Recall*, dan *F1-Score*.

---

## 📁 Struktur Direktori

```text
AI Prompt Security/
│
├── main.py                     # Entry point FastAPI & Logika Microsoft Presidio
├── requirements.txt            # Daftar pustaka & dependensi Python
├── .gitignore                  # Berkas pengabaian git
├── README.md                   # Dokumentasi proyek
│
├── extension/                  # Chrome Extension (Manifest V3)
│   ├── manifest.json           # Konfigurasi perizinan & content scripts
│   └── content.js              # Script injeksi untuk intercept prompt chat
│
├── skrip_dataset.py            # Generator dataset dummy (Faker id_ID)
├── dataset_sintetis.csv        # Hasil generate 120 sampel kalimat uji
└── dataset_indonlu.py          # Script pengambil data IndoNER dari IndoNLU GitHub
```

---

## 🛠️ Prasyarat Sistem

- **Python**: Versi 3.10 atau lebih baru
- **Google Chrome**: Versi 110 atau lebih baru (Mendukung Manifest V3)
- **Git**

---

## ⚙️ Panduan Instalasi & Pengaturan

### 1. Kloning Repositori & Buat Virtual Environment

```bash
# Masuk ke folder proyek
cd "AI Prompt Security"

# Buat virtual environment
python -m venv .venv

# Aktivasi virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Atau Windows Command Prompt (CMD)
.venv\Scripts\activate.bat
```

### 2. Instal Dependensi Python

```bash
pip install -r requirements.txt
```

### 3. Unduh Model Bahasa spaCy

Microsoft Presidio memerlukan model spaCy untuk mendeteksi entitas dasar (seperti `PERSON`):

```bash
python -m spacy download en_core_web_lg
```
*(Catatan: Anda juga bisa menggunakan model yang lebih ringan seperti `en_core_web_sm` jika menghemat memori).*

---

## 🖥️ Menjalankan Backend API

Jalankan server API FastAPI secara lokal menggunakan Uvicorn:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- API Base URL: `http://127.0.0.1:8000`
- Dokumentasi Interaktif (Swagger UI): `http://127.0.0.1:8000/docs`
- Redoc UI: `http://127.0.0.1:8000/redoc`

### Contoh Pengujian Endpoint API

**Endpoint**: `POST /sanitize`

**Request Body**:
```json
{
  "text": "Tolong buatkan surat untuk Budi Santoso dengan NIK 3201234567890001 dan hubungi via wa 081234567890."
}
```

**Response**:
```json
{
  "original_text": "Tolong buatkan surat untuk Budi Santoso dengan NIK 3201234567890001 dan hubungi via wa 081234567890.",
  "masked_text": "Tolong buatkan surat untuk <PERSON> dengan NIK <ID_NIK> dan hubungi via wa <ID_PHONE>."
}
```

---

## 🧩 Memasang Ekstensi di Google Chrome

1. Buka browser **Google Chrome**.
2. Masuk ke halaman pengelolaan ekstensi: `chrome://extensions`
3. Aktifkan **Developer mode** (Mode pengembang) di sudut kanan atas.
4. Klik tombol **Load unpacked** di sudut kiri atas.
5. Arahkan dan pilih folder `extension/` dari repositori ini.
6. Buka tab baru ke **[ChatGPT](https://chatgpt.com)** atau **[Google Gemini](https://gemini.google.com)**.
7. Tekan `F12` > buka tab **Console**, pastikan muncul pesan:
   ```text
   🔒 AI Privacy Shield aktif! Sedang memantau kolom chat...
   ```

---

## 📈 Dataset & Pengujian Model

Proyek ini dilengkapi alat evaluasi untuk memvalidasi performa deteksi entitas:

1. **Pembuatan Dataset Sintetis (Faker ID)**:
   ```bash
   python skrip_dataset.py
   ```
   Menghasilkan `dataset_sintetis.csv` yang berisi 100 kalimat bertag PII (NIK & No HP) dan 20 kalimat netral (*False Positive test*).

2. **Pengujian dengan Data Riil IndoNER (IndoNLU)**:
   ```bash
   python dataset_indonlu.py
   ```
   Mengunduh dan mengekstrak data uji CoNLL dari repositori resmi IndoBenchmark untuk validasi entitas nama dan organisasi berbahasa Indonesia.

---

## 🧰 Tech Stack

- **Backend**: FastAPI, Uvicorn, Pydantic
- **NLP / Privacy Engine**: Microsoft Presidio Analyzer & Anonymizer, spaCy
- **Frontend / Client**: Chrome Extension Manifest V3 (Vanilla JavaScript)
- **Data & Testing**: Faker (Bahasa Indonesia), IndoNLU Dataset, Pandas

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan akademik dan penelitian pada mata kuliah **Data & Network Security**.
