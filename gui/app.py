# gui/app.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
from pathlib import Path
from ecc_core import (
    generate_keypair, save_private_key_pem, save_public_key_pem,
    load_private_key_pem, load_public_key_pem,
    encrypt_message, decrypt_message
)
import json

DATA = Path("../data")
PRIV = DATA / "privkey.pem"
PUB  = DATA / "pubkey.pem"

def gen_keys():
    priv, pub = generate_keypair()
    save_private_key_pem(priv, PRIV)
    save_public_key_pem(pub, PUB)
    messagebox.showinfo("ECC", "Key pair dibuat.")

def do_encrypt():
    if not PUB.exists():
        messagebox.showwarning("ECC", "Buat kunci dulu.")
        return
    pub = load_public_key_pem(PUB)
    pt = txt.get("1.0", tk.END).encode("utf-8")
    enc = encrypt_message(pt, pub)
    out.delete("1.0", tk.END)
    out.insert(tk.END, json.dumps(enc, indent=2))

def do_decrypt():
    if not PRIV.exists():
        messagebox.showwarning("ECC", "Kunci privat tidak ada.")
        return
    priv = load_private_key_pem(PRIV)
    try:
        enc = json.loads(out.get("1.0", tk.END))
    except Exception:
        messagebox.showerror("ECC", "JSON tidak valid.")
        return
    try:
        pt = decrypt_message(enc, priv).decode("utf-8")
        txt.delete("1.0", tk.END)
        txt.insert(tk.END, pt)
    except Exception as e:
        messagebox.showerror("ECC", f"Dekripsi gagal: {e}")

root = tk.Tk()
root.title("ECC - ECIES Demo")
frm = tk.Frame(root); frm.pack(padx=10, pady=10)

tk.Button(frm, text="Generate Keys", command=gen_keys).grid(row=0, column=0, padx=5)
tk.Button(frm, text="Encrypt →", command=do_encrypt).grid(row=0, column=1, padx=5)
tk.Button(frm, text="← Decrypt", command=do_decrypt).grid(row=0, column=2, padx=5)

tk.Label(frm, text="Plaintext").grid(row=1, column=0, columnspan=2, sticky="w")
txt = scrolledtext.ScrolledText(frm, width=50, height=12)
txt.grid(row=2, column=0, columnspan=2, pady=5)

tk.Label(frm, text="Ciphertext (JSON)").grid(row=1, column=2, sticky="w")
out = scrolledtext.ScrolledText(frm, width=50, height=12)
out.grid(row=2, column=2, pady=5)

root.mainloop()
