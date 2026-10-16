from datasets import load_dataset

print("Memulai unduhan dataset IndoNER dari Hugging Face...")

# Tarik subset 'ner' secara spesifik
dataset_ner = load_dataset("indonlp/indonlu", "ner", trust_remote_code=True)

# Ekstrak sampel kalimat ke-5 dari bagian pengujian ('test')
sample_tokens = dataset_ner['test'][4]['tokens']
sample_tags = dataset_ner['test'][4]['ner_tags']

print("\n--- Struktur Data Berhasil Dimuat ---")
print("Contoh Kalimat dan Label (0 = Bukan Entitas, selain 0 = Entitas PII/Lainnya):")
print("-" * 40)

# Petakan setiap kata (token) dengan label numeriknya
for token, tag in zip(sample_tokens, sample_tags):
    print(f"{token.ljust(15)} : {tag}")