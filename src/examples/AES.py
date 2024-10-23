import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os

# Hilfsfunktion zum Erstellen eines Schlüssels aus einem Passwort
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 Bytes = 256 bit für AES-256
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Verschlüsseln der JSON-Datei
def encrypt_json(data: dict, password: str, output_file: str):
    # JSON zu String serialisieren
    json_data = json.dumps(data).encode()

    # Zufällige Salt und Nonce (IV) erzeugen
    salt = os.urandom(16)
    iv = os.urandom(12)

    # Schlüssel aus Passwort ableiten
    key = derive_key(password, salt)

    # AES-GCM Cipher erstellen
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Verschlüsseln der Daten
    ciphertext = encryptor.update(json_data) + encryptor.finalize()

    # Datei schreiben: Salt, IV und Ciphertext speichern
    with open(output_file, 'wb') as f:
        f.write(salt + iv + encryptor.tag + ciphertext)

# Entschlüsseln der Datei und Rückgabe als dict
def decrypt_json(password: str, input_file: str) -> dict:
    # Datei lesen
    with open(input_file, 'rb') as f:
        file_data = f.read()

    # Salt, IV und Ciphertext extrahieren
    salt = file_data[:16]
    iv = file_data[16:28]
    tag = file_data[28:44]
    ciphertext = file_data[44:]

    # Schlüssel aus Passwort ableiten
    key = derive_key(password, salt)

    # AES-GCM Cipher erstellen
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Daten entschlüsseln
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Entschlüsselten JSON-String zu einem dict umwandeln
    return json.loads(decrypted_data.decode())

# Beispiel-Daten
data = {
    'name': 'Alice',
    'age': 30,
    'city': 'Wonderland'
}

# Beispiel-Passwort
password = 'strongpassword'

# Datei verschlüsseln und speichern
encrypt_json(data, password, 'encrypted_data.bin')

# Datei entschlüsseln und in ein dict umwandeln
decrypted_data = decrypt_json(password, 'encrypted_data.bin')
print(decrypted_data)
