# main.py
from pathlib import Path
from ecc_core import (
    generate_keypair, save_private_key_pem, save_public_key_pem,
    load_private_key_pem, load_public_key_pem,
    encrypt_message, decrypt_message
)
from helper import read_text, write_text, timer

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64, json, sys
from math import ceil

DATA_DIR   = Path("data")
DEFAULT_IN = DATA_DIR / "input.txt"
DEFAULT_OUT= DATA_DIR / "output.txt"
PRIV_PEM   = DATA_DIR / "privkey.pem"
PUB_PEM    = DATA_DIR / "pubkey.pem"

# ---------- util tampil demo laporan ----------
def bytes_to_two_ints(b: bytes):
    """Ubah bytes ciphertext jadi dua bilangan besar (visualisasi C2 untuk laporan)."""
    if not b:
        return 0, 0
    half = ceil(len(b)/2)
    a = int.from_bytes(b[:half],  byteorder="big")
    c = int.from_bytes(b[half:],  byteorder="big")
    return a, c

def print_header():
    print("="*45)
    print("===  PROGRAM ENKRIPSI ECC (ECIES) - IND  ===")
    print("="*45)

def input_path(prompt: str, default: Path) -> Path:
    p = input(f"{prompt} (Enter untuk {default}): ").strip()
    return default if not p else Path(p)

# ---------- aksi ----------
def aksi_buat_kunci():
    priv, pub = generate_keypair()
    save_private_key_pem(priv, PRIV_PEM)
    save_public_key_pem(pub, PUB_PEM)
    print("\n🔐 Sepasang kunci berhasil dibuat:")
    print(f"   - Kunci Privat : {PRIV_PEM}")
    print(f"   - Kunci Publik : {PUB_PEM}")

def aksi_enkripsi():
    print("\n--- Proses Enkripsi ---")
    in_path  = input_path("Masukkan path file input", DEFAULT_IN)
    out_path = input_path("Masukkan path file output", DEFAULT_OUT)

    if not in_path.exists():
        print(f"[!] File input tidak ditemukan: {in_path}")
        return

    if not PUB_PEM.exists():
        print("[!] Kunci publik tidak ditemukan. Membuat kunci baru...")
        aksi_buat_kunci()

    pub = load_public_key_pem(PUB_PEM)
    plaintext = read_text(str(in_path))
    if plaintext == "":
        print(f"[!] File {in_path} kosong.")
        return

    print("🔒 Melakukan Enkripsi...")
    with timer() as t:
        enc = encrypt_message(plaintext.encode("utf-8"), pub)

    # --- siapkan data “angka” untuk format laporan ---
    # koordinat Q (kunci publik)
    pub_nums = pub.public_numbers()
    pub_x, pub_y = pub_nums.x, pub_nums.y

    # kunci privat (opsional, hanya jika ada)
    priv_val = None
    if PRIV_PEM.exists():
        try:
            priv = load_private_key_pem(PRIV_PEM)
            priv_val = priv.private_numbers().private_value
        except Exception:
            pass

    # C1 = koordinat ephemeral public key
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    import base64
    from math import ceil

    def bytes_to_two_ints(b: bytes):
        if not b:
            return 0, 0
        half = (len(b) + 1) // 2  # ceil
        a = int.from_bytes(b[:half],  byteorder="big")
        c = int.from_bytes(b[half:],  byteorder="big")
        return a, c

    eph_pub_pem = base64.b64decode(enc["eph_pub_pem_b64"])
    eph_public  = serialization.load_pem_public_key(eph_pub_pem, backend=default_backend())
    eph_nums    = eph_public.public_numbers()
    c1x, c1y    = eph_nums.x, eph_nums.y

    # C2 = pecah ciphertext (bytes) menjadi dua bilangan besar
    ciphertext_bytes = base64.b64decode(enc["ciphertext_b64"])
    c2a, c2b = bytes_to_two_ints(ciphertext_bytes)

    # --- gabungkan ke satu JSON untuk disimpan ke output.txt ---
    enc_augmented = {
        # blok asli untuk dekripsi (biarkan apa adanya!)
        "eph_pub_pem_b64": enc["eph_pub_pem_b64"],
        "salt_b64":        enc["salt_b64"],
        "nonce_b64":       enc["nonce_b64"],
        "ciphertext_b64":  enc["ciphertext_b64"],

        # blok tambahan khusus “format laporan”
        "report_plaintext": plaintext,
        "report_public_key": {"x": pub_x, "y": pub_y},
        # kunci privat opsional; hapus baris ini kalau tidak ingin disimpan
        "report_private_key_d": priv_val if priv_val is not None else "(tidak disimpan)",
        "report_C1": {"x": c1x, "y": c1y},
        "report_C2": {"a": c2a, "b": c2b}
    }

    # simpan JSON augmented
    write_text(str(out_path), json.dumps(enc_augmented, indent=2))
    print("✅ Enkripsi selesai dalam {:.4f} detik.".format(t.elapsed))
    print(f"PS: Hasil enkripsi+laporan disimpan di {out_path}")

    # tambahan: file ringkas “contoh uji” untuk mudah copy ke makalah
    demo_path = DATA_DIR / "demo_output.txt"
    demo_lines = [
        f"Plaintext : {plaintext}",
        f"Kunci Publik (Q) : ({pub_x}, {pub_y})",
    ]
    if priv_val is not None:
        demo_lines.append(f"Kunci Privat (d) : {priv_val}")
    demo_lines += [
        "Ciphertext :",
        f"C1 = ({c1x}, {c1y})",
        f"C2 = ({c2a}, {c2b})",
        "Dekripsi : (jalankan menu 'Dekripsi File')"
    ]
    write_text(str(demo_path), "\n".join(demo_lines))
    print(f"PS: Format 'contoh uji' untuk laporan juga ada di {demo_path}")


def aksi_dekripsi():
    print("\n--- Proses Dekripsi ---")
    in_path = input_path("Masukkan path file input (hasil enkripsi JSON)", DEFAULT_OUT)
    if not in_path.exists():
        print(f"[!] File {in_path} tidak ditemukan.")
        return

    if not PRIV_PEM.exists():
        print("[!] Kunci privat tidak ditemukan. Jalankan menu 3 untuk membuat kunci.")
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
    dec_path = DATA_DIR / "decrypted.txt"
    write_text(str(dec_path), plaintext)
    print(f"PS: Plaintext juga disimpan di {dec_path}")

def main():
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    while True:
        print_header()
        print("1. Enkripsi File (data/input.txt -> data/output.txt)")
        print("2. Dekripsi File (data/output.txt -> tampilkan & data/decrypted.txt)")
        print("3. Buat Sepasang Kunci (jika belum ada)")
        print("0. Keluar")
        print("-"*45)
        pilih = input("Pilih (0-3): ").strip()
        if   pilih == "1": aksi_enkripsi()
        elif pilih == "2": aksi_dekripsi()
        elif pilih == "3": aksi_buat_kunci()
        elif pilih == "0":
            print("Terima kasih. Program selesai.")
            sys.exit(0)
        else:
            print("[INFO] Pilihan tidak dikenali. Silakan coba lagi.")
        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
