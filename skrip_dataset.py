import csv
import random
from faker import Faker

# Inisialisasi Faker dengan bahasa Indonesia
fake = Faker('id_ID')

def generate_nik():
    # NIK selalu 16 digit angka
    return str(fake.random_number(digits=16, fix_len=True))

def generate_phone():
    # Variasi prefix nomor HP Indonesia
    prefixes = ['0812', '0852', '0813', '0857', '+62812', '+62852']
    return random.choice(prefixes) + str(fake.random_number(digits=8, fix_len=True))

templates = [
    "Tolong periksa data atas nama {name} dengan NIK {nik}.",
    "Nomor HP saya {phone}, tolong hubungi segera.",
    "Apakah NIK {nik} ini sudah terdaftar di sistem?",
    "Berikut kontak daruratnya: {name} ({phone}).",
    "Saya {name}, bisakah ubah nomor telepon menjadi {phone}?",
    "tolong buatkan surat peringatan untuk {name} nik {nik}"
]

data = []

# Generate 100 baris data yang mengandung PII
for _ in range(100):
    name = fake.name()
    nik = generate_nik()
    phone = generate_phone()
    
    choice = random.choice(['nik', 'phone', 'both'])
    if choice == 'nik':
        text = random.choice([t for t in templates if '{nik}' in t and '{phone}' not in t]).format(name=name, nik=nik)
        data.append([text, True, "NIK", nik])
    elif choice == 'phone':
        text = random.choice([t for t in templates if '{phone}' in t and '{nik}' not in t]).format(name=name, phone=phone)
        data.append([text, True, "PHONE", phone])
    else:
        text = f"Data pendaftar: {name} dengan NIK {nik} dan HP {phone}"
        data.append([text, True, "MULTIPLE", f"{nik}|{phone}"])

# Generate 20 baris kalimat aman tanpa PII (Uji False Positive)
safe_templates = [
    "Bagaimana cara mereset password di portal?",
    "Tolong jelaskan apa itu mekanisme reverse proxy.",
    "Kapan jadwal perbaikan server bulan ini?",
    "Jelaskan perbedaan antara TCP dan UDP."
]
for _ in range(20):
    data.append([random.choice(safe_templates), False, "NONE", "NONE"])

# Ekspor hasil ke file CSV
with open('dataset_sintetis.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['text', 'contains_pii', 'entity_type', 'entity_value'])
    writer.writerows(data)

print("Berhasil membuat dataset_sintetis.csv dengan 120 baris data pengujian!")