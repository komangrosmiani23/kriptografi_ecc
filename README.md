# kriptografi_ecc
Implementasi **Elliptic Curve Cryptography (ECC)** menggunakan bahasa pemrograman **Python** untuk melakukan proses **enkripsi dan dekripsi data teks**.  
Proyek ini dibuat sebagai bagian dari tugas besar mata kuliah *Kriptografi*.

## Deskripsi Proyek
Aplikasi ini mengimplementasikan algoritma **Elliptic Curve Integrated Encryption Scheme (ECIES)**, yaitu kombinasi dari:
- **ECC (Elliptic Curve Cryptography)** untuk pertukaran kunci (key exchange), dan  
- **AES-GCM** untuk proses enkripsi dan dekripsi pesan.

Pendekatan ini memungkinkan proses kriptografi yang aman, cepat, dan efisien pada data teks berukuran kecil hingga menengah.

## Struktur Folder
ecc_project/
├─ main.py → Program utama (menu enkripsi/dekripsi)
├─ ecc_core.py → Modul utama ECC (pembuatan kunci, enkripsi, dekripsi)
├─ helper.py → Fungsi bantu (I/O file, pengukuran waktu, utilitas)
├─ gui/app.py → Antarmuka pengguna berbasis Tkinter (opsional)
├─ data/
│ ├─ input.txt → File teks masukan (plaintext)
│ ├─ output.txt → Hasil enkripsi (ciphertext JSON)
│ ├─ decrypted.txt → Hasil dekripsi (plaintext kembali)
│ ├─ privkey.pem → Kunci privat ECC
│ └─ pubkey.pem → Kunci publik ECC
└─ .gitignore → Daftar file yang diabaikan Git


## Cara Menjalankan Program

### 1️ Persiapan Lingkungan
Pastikan Python sudah terpasang.  
Versi yang disarankan: **Python 3.10+**

Instal dependensi:
```bash
pip install cryptography

### 2 Jalankan Program
Masuk ke folder proyek lalu jalankan:
python main.py

### 3 Menu Program
=== PROGRAM ENKRIPSI ECC (ECIES) ===
1. Enkripsi File
2. Dekripsi File
3. Buat Sepasang Kunci
0. Keluar

Keterangan:
Menu 1 → Enkripsi teks dari data/input.txt
Menu 2 → Dekripsi file data/output.txt
Menu 3 → Membuat pasangan kunci privat & publik otomatis

### Contoh Kasus Uji

Plaintext : HELLO ECC TEST
Kunci Publik (Q):
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmll0d4ZOBQf/6zXtGxuT3hEx17BD
vm430pjrGEBI5MQ4uixc4rH2oEVxFdMdbDYrYvPoEDLRd2/rge3Vmmf58A==
-----END PUBLIC KEY-----
Hasil Enkripsi (Ciphertext):
{
  "eph_pub_pem_b64": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0K...",
  "salt_b64": "LQ4G/mhYP96mfKYKebMNew==",
  "nonce_b64": "xL7Y5Pb006yLIaRu",
  "ciphertext_b64": "P+wEi4cfrV2drFyJHZG77Z7w6WHloyxkdrwuhzc"
}
Hasil Dekripsi : HELLO ECC TEST

## Hasil Pengujian
| Jenis Uji              | Tujuan                                  | Hasil                            |
| ---------------------- | --------------------------------------- | -------------------------------- |
| Pengujian Fungsional   | Verifikasi proses enkripsi & dekripsi   | ✅ Berhasil                       |
| Uji Sensitivitas Kunci | Cek perubahan kecil pada kunci          | ✅ Ciphertext berubah total       |
| Uji Efek Avalanche     | Perubahan 1 huruf → hasil berubah besar | ✅ Aman                           |
| Uji Nilai Acak         | Enkripsi ulang teks sama                | ✅ Ciphertext berbeda setiap kali |
| Uji Kegagalan Dekripsi | Kunci salah → dekripsi gagal            | ✅ Tidak terbaca                  |



## Kontributor
Komang Rosmiani & Angelin Nadya Sulu
Mahasiswa Program Studi Teknik Informatika
Universitas Dipa Makassar

## Lisensi
Proyek ini dibuat untuk keperluan akademik.
Bebas digunakan untuk pembelajaran dan penelitian dengan tetap menyertakan atribusi kepada penulis.
