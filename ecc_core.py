# ecc_core.py
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os, base64

CURVE = ec.SECP256R1()  # P-256

# ---------- Util Kunci ----------
def generate_keypair():
    """Menghasilkan pasangan kunci ECC (private, public)."""
    private_key = ec.generate_private_key(CURVE, default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key_pem(private_key, path, password: bytes | None = None):
    enc = serialization.BestAvailableEncryption(password) if password else serialization.NoEncryption()
    pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        enc
    )
    with open(path, "wb") as f:
        f.write(pem)

def save_public_key_pem(public_key, path):
    pem = public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(path, "wb") as f:
        f.write(pem)

def load_private_key_pem(path, password: bytes | None = None):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=password, backend=default_backend())

def load_public_key_pem(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())

# ---------- ECIES (ECDH + HKDF + AES-GCM) ----------
def _derive_aes_key(shared_secret: bytes, salt: bytes | None = None, info: bytes = b"ecc-ecies-v1"):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        info=info,
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)

def encrypt_message(plaintext: bytes, peer_public_key) -> dict:
    """
    ECIES:
      - Ephemeral key (ke)
      - ECDH: ss = ke ⊙ pub_peer
      - HKDF(ss) -> k_AES
      - AES-GCM(k_AES, nonce, plaintext) -> ciphertext (bertag)
      - Return: eph_pub (PEM, b64), salt, nonce, ciphertext (b64)
    """
    # 1) ECDH ephemeral
    eph_private = ec.generate_private_key(CURVE, default_backend())
    eph_public = eph_private.public_key()
    shared_secret = eph_private.exchange(ec.ECDH(), peer_public_key)

    # 2) Derive AES key
    salt = os.urandom(16)
    aes_key = _derive_aes_key(shared_secret, salt=salt)

    # 3) AES-GCM
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # 4) Serialize eph public key
    eph_pub_pem = eph_public.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        "eph_pub_pem_b64": base64.b64encode(eph_pub_pem).decode(),
        "salt_b64":        base64.b64encode(salt).decode(),
        "nonce_b64":       base64.b64encode(nonce).decode(),
        "ciphertext_b64":  base64.b64encode(ciphertext).decode()
    }

def decrypt_message(enc_bundle: dict, my_private_key) -> bytes:
    """Dekripsi ECIES (kebalikan encrypt_message)."""
    eph_pub_pem = base64.b64decode(enc_bundle["eph_pub_pem_b64"])
    salt        = base64.b64decode(enc_bundle["salt_b64"])
    nonce       = base64.b64decode(enc_bundle["nonce_b64"])
    ciphertext  = base64.b64decode(enc_bundle["ciphertext_b64"])

    eph_public = serialization.load_pem_public_key(eph_pub_pem, backend=default_backend())
    shared_secret = my_private_key.exchange(ec.ECDH(), eph_public)
    aes_key = _derive_aes_key(shared_secret, salt=salt)
    aesgcm = AESGCM(aes_key)
    return aesgcm.decrypt(nonce, ciphertext, None)
