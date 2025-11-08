from pathlib import Path
from ecc_core import (
    generate_keypair, save_private_key_pem, save_public_key_pem,
    load_private_key_pem, load_public_key_pem,
    encrypt_message, decrypt_message
)
from helper import read_text, write_text, timer
import json, sys

DATA_DIR = Path("data")
DEFAULT_IN = DATA_DIR / "input.txt"
DEFAULT_OUT = DATA_DIR / "output.txt"
PRIV_PEM = DATA_DIR / "privkey.pem"
PUB_PEM  = DATA_DIR / "pubkey.pem"

def print_header():
    print("="*40)
    print("===  PROGRAM ENKRIPSI ECC (ECIES)  ===")
    print("="*40)

def input_path(prompt: str, default: Path) -> Path:
    p = input(f"{prompt} (tekan Enter untuk {default}): ").strip()
    if not p:
        return default
    return Path(p)

def aksi_buat_kunci():
    priv, pub = generate_keypair()
    save_private_key_pem(priv, PRIV_PEM)
    save_public_key_pem(pub, PUB_PEM)
    print("\n🔐 Kunci berhasil dibuat:")
    print(f"   - Kunci Privat : {PRIV_PEM}")
    print(f"   - Kunci Publik : {PUB_PEM}")

def aksi_enkripsi():
    print("\n--- Proses Enkripsi ---")
    in_path = input_path("Masukkan path file input", DEFAULT_IN)
    out_path = input_path("Masukkan path file output", DEFAULT_OUT)

    if not in_path.exists():
        print(f"[!] File input tidak ditemukan: {in_path}")
        return

    # pastikan kunci publik ada
    if not PUB_PEM.exists():
        print("[!] Kunci publik tidak ditemukan. Membuat kunci baru secara otomatis...")
        aksi_buat_kunci()

    pub = load_public_key_pem(PUB_PEM)
    plaintext = read_text(str(in_path))
    if plaintext == "":
        print(f"[!] File {in_path} kosong.")
        return

    print("🔒 Melakukan Enkripsi...")
    with timer() as t:
        enc = encrypt_message(plaintext.encode("utf-8"), pub)
    write_text(str(out_path), json.dumps(enc, indent=2))
    print("✅ Enkripsi selesai dalam {:.4f} detik.".format(t.elapsed))
    print(f"PS: Hasil enkripsi tersimpan di {out_path}")

def aksi_dekripsi():
    print("\n--- Proses Dekripsi ---")
    in_path = input_path("Masukkan path file input (hasil enkripsi JSON)", DEFAULT_OUT)
    if not in_path.exists():
        print(f"[!] File {in_path} tidak ditemukan.")
        return

    if not PRIV_PEM.exists():
        print("[!] Kunci privat tidak ditemukan. Silakan buat kunci dahulu (menu 1).")
        return

    priv = load_private_key_pem(PRIV_PEM)
    konten = read_text(str(in_path))
    if not konten:
        print(f"[!] File {in_path} kosong.")
        return

    try:
        paket = json.loads(konten)
    except Exception:
        print("[!] Format file bukan JSON enkripsi yang valid.")
        return

    print("🔓 Melakukan Dekripsi...")
    with timer() as t:
        try:
            plaintext = decrypt_message(paket, priv).decode("utf-8")
        except Exception as e:
            print(f"[X] Dekripsi gagal: {e}")
            return

    print("✅ Dekripsi selesai dalam {:.4f} detik.".format(t.elapsed))
    print("\n----- HASIL PLAINTEXT -----")
    print(plaintext)
    print("---------------------------")
    # simpan hasil dekripsi
    dec_path = DATA_DIR / "decrypted.txt"
    write_text(str(dec_path), plaintext)
    print(f"PS: Plaintext juga disimpan di {dec_path}")

def main():
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    while True:
        print_header()
        print("1. Enkripsi File")
        print("2. Dekripsi File")
        print("3. Buat Sepasang Kunci (jika belum ada)")
        print("0. Keluar")
        print("-"*40)
        pilih = input("Pilih (0-3): ").strip()
        if pilih == "1":
            aksi_enkripsi()
        elif pilih == "2":
            aksi_dekripsi()
        elif pilih == "3":
            aksi_buat_kunci()
        elif pilih == "0":
            print("Terima kasih. Program selesai.")
            sys.exit(0)
        else:
            print("[INFO] Pilihan tidak dikenali. Silakan coba lagi.")
        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
