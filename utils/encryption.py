import base64
import hashlib
import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
print(secret_key)

if (secret_key is None) :
    raise ValueError("No esta definida la clave en el archivo .env")

secret_key = base64.urlsafe_b64encode(hashlib.sha256(secret_key.encode()).digest())
fernet = Fernet(secret_key)

def encrypt(data):
    if isinstance(data, str):
        data = data.encode()
    encrypted_data = fernet.encrypt(data)
    encrypted_data_str = encrypted_data.decode('utf-8')
    encrypted_data_str = encrypted_data.decode()
    return encrypted_data_str


def decrypt(encrypted_data):
    if(not isinstance(encrypted_data, bytes)):
        encrypted_data = encrypted_data.encode()
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode()

# print(decrypt('gAAAAABoDS-TGCI1tVPaSvCcNvBtP8BKCEGbpBEWapD54jGw2nCMY_LczIKn2QLUXVJ_0XnUgDctoIrNmOr0fy9cJGOl7Uj1-pTLDmn9OnwXTtstJiyqJYKBw1ftZamM1jv6dyBqGn_o'))