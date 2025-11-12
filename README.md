# 🔐 Implementasi Kriptografi ECC (Elliptic Curve Cryptography)

Proyek ini merupakan implementasi algoritma **Elliptic Curve Cryptography (ECC)** menggunakan bahasa pemrograman **Python** untuk melakukan proses **enkripsi dan dekripsi data teks**.  
Aplikasi ini dikembangkan sebagai bagian dari *Tugas Besar Mata Kuliah Kriptografi* di **Universitas Dipa Makassar**.

---

## 🧩 Deskripsi Proyek

Program ini menerapkan skema **Elliptic Curve Integrated Encryption Scheme (ECIES)**, yaitu kombinasi antara:
- **ECC (Elliptic Curve Cryptography)** untuk pertukaran kunci (*key exchange*), dan  
- **AES-GCM** untuk proses enkripsi dan dekripsi pesan.  

Pendekatan ini menghasilkan sistem enkripsi yang **aman, efisien, dan ramah sumber daya**, cocok untuk data teks berukuran kecil hingga menengah.

---

## 📂 Struktur Folder

```
ecc_project/
├── main.py → Program utama (menu enkripsi & dekripsi)
├── ecc_core.py → Modul utama algoritma ECC dan AES-GCM
├── helper.py → Modul bantu (fungsi I/O dan pengukur waktu)
├── data/
│ ├── input.txt → File teks masukan (plaintext)
│ ├── output.txt → File hasil enkripsi (ciphertext + format laporan)
│ ├── decrypted.txt → File hasil dekripsi
│ ├── privkey.pem → Kunci privat ECC
│ ├── pubkey.pem → Kunci publik ECC
│ └── demo_output.txt→ Format hasil uji (C1, C2, Q, d)
├── gui/ → Antarmuka pengguna (opsional)
├── README.md → Dokumentasi proyek (file ini)
└── .gitignore → Pengecualian file pada GitHub

```

## ⚙️ Cara Menjalankan Program

### 1️⃣ Persiapan
Pastikan Python telah terinstal (versi 3.10 atau lebih baru).  
Lalu instal pustaka yang dibutuhkan:
```bash
pip install cryptography
```

### 2️⃣ Jalankan Program
Masuk ke direktori proyek dan jalankan:
```
python main.py
```

### 3️⃣ Menu Program
=== PROGRAM ENKRIPSI ECC (ECIES) ===
1. Enkripsi File
2. Dekripsi File
3. Buat Sepasang Kunci
0. Keluar
```
Keterangan:
Menu 1 → Enkripsi teks dari data/input.txt
Menu 2 → Dekripsi file data/output.txt
Menu 3 → Membuat pasangan kunci privat & publik otomatis
```

## 4️⃣ Hasil Enkripsi

File hasil tersimpan di:
```
data/output.txt → hasil enkripsi dalam format JSON

data/demo_output.txt → format numerik untuk laporan (Q, d, C1, C2)

data/decrypted.txt → hasil dekripsi (plaintext kembali)
```

### 🧪 Contoh Kasus Uji

#### Plaintext : 
```HELLO ECC TEST```

#### Kunci Publik (Q):
```
(2458324197430087053273510, 426513602870948149631739)
```
### Kunci Privat (d):
```932854932785432```

#### Hasil Enkripsi (Ciphertext):
```
C1 = (178231260982481, 249313640731540)
C2 = (914591023768320, 203948610832482)

```
#### Hasil Dekripsi : 
```HELLO ECC TEST```

## 👩‍💻 Kontributor
Komang Rosmiani & Angelin Nadya Sulu
Mahasiswa Program Studi Teknik Informatika
Universitas Dipa Makassar

## 📜 Lisensi
Proyek ini dibuat untuk pembelajaran dan penelitian akademik.
Bebas digunakan untuk pembelajaran dan penelitian dengan tetap menyertakan atribusi kepada penulis.

## 🔗 Referensi
```
T. Indriyani, P. D. Airlangga, dan F. Jaka, “Enkripsi Data Menggunakan Metode Elliptic Curve Cryptography,” Seminar Nasional Sains dan Teknologi Terapan XI, 2023.

Y. Adrian, C. Friscilla, N. Suardiman, A. Wijaya, dan Sudimanto, “Analisis Perbandingan Waktu Enkripsi dan Dekripsi pada Algoritma ECC dan RSA,” Media Informatika, 2022.
```
