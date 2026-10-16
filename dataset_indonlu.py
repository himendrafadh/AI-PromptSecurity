import urllib.request

# Tembak langsung ke raw file data testing di repositori GitHub resmi IndoNLU
url = "https://raw.githubusercontent.com/indobenchmark/indonlu/master/dataset/nerp_indonlu/test_preprocess.txt"
print("Mengunduh raw data IndoNER langsung dari GitHub...")

response = urllib.request.urlopen(url)
lines = response.read().decode('utf-8').splitlines()

sentences = []
current_sentence = {'tokens': [], 'tags': []}

# Parsing format CoNLL (Kata \t Label) menjadi struktur array
for line in lines:
    if line.strip() == "":
        if current_sentence['tokens']:
            sentences.append(current_sentence)
            current_sentence = {'tokens': [], 'tags': []}
    else:
        parts = line.split('\t')
        if len(parts) >= 2:
            current_sentence['tokens'].append(parts[0])
            current_sentence['tags'].append(parts[1])

print("\n--- Struktur Data Berhasil Dimuat ---")
print(f"Total kalimat pengujian yang ditarik: {len(sentences)} kalimat")
print("\nContoh Kalimat ke-5 dan Label Entitasnya:")
print("-" * 40)

# Tampilkan sampel data
sample = sentences[4]
for token, tag in zip(sample['tokens'], sample['tags']):
    print(f"{token.ljust(15)} : {tag}")