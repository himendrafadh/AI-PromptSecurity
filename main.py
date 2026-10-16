from fastapi import FastAPI
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

# Inisialisasi Aplikasi FastAPI
app = FastAPI(title="Privacy Protection API", version="1.0")

print("Menginisialisasi NLP Engine Presidio...")
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# =====================================================================
# 1. CUSTOM RECOGNIZER: NIK INDONESIA (16 Digit)
# =====================================================================
nik_pattern = Pattern(
    name="nik_pattern", 
    regex=r"\b\d{16}\b", # Mencari 16 digit angka berurutan
    score=0.85
)
nik_recognizer = PatternRecognizer(
    supported_entity="ID_NIK",
    patterns=[nik_pattern],
    context=["nik", "ktp", "nomor induk", "identitas"] # Konteks untuk meningkatkan akurasi
)
analyzer.registry.add_recognizer(nik_recognizer)


# =====================================================================
# 2. CUSTOM RECOGNIZER: NOMOR HP INDONESIA (+62 / 08)
# =====================================================================
phone_pattern = Pattern(
    name="phone_id_pattern",
    regex=r"\b(?:\+62|62|0)8[1-9][0-9]{6,10}\b", # Mendukung awalan +62, 62, atau 08
    score=0.85
)
phone_recognizer = PatternRecognizer(
    supported_entity="ID_PHONE",
    patterns=[phone_pattern],
    context=["hp", "telepon", "nomor", "hubungi", "wa"]
)
analyzer.registry.add_recognizer(phone_recognizer)


# =====================================================================
# DATA MODELS (Untuk Request & Response API)
# =====================================================================
class PromptRequest(BaseModel):
    text: str

class PromptResponse(BaseModel):
    original_text: str
    masked_text: str


# =====================================================================
# API ENDPOINT
# =====================================================================
@app.post("/sanitize", response_model=PromptResponse)
def sanitize_prompt(request: PromptRequest):
    # Tentukan entitas apa saja yang ingin dideteksi
    # Termasuk entitas bawaan Presidio (PERSON, EMAIL_ADDRESS) dan Custom kita
    entities_to_find = ["PERSON", "EMAIL_ADDRESS", "ID_NIK", "ID_PHONE"]
    
    # 1. Tahap Analisis: Cari posisi PII di dalam teks
    analysis_results = analyzer.analyze(
        text=request.text, 
        entities=entities_to_find, 
        language='en' # Menggunakan base bahasa Inggris karena kita butuh deteksi PERSON bawaannya
    )
    
    # 2. Tahap Masking: Samarkan entitas yang ditemukan
    anonymized_result = anonymizer.anonymize(
        text=request.text,
        analyzer_results=analysis_results
    )
    
    return PromptResponse(
        original_text=request.text,
        masked_text=anonymized_result.text
    )

print("Sistem NLP siap! Menunggu request...")