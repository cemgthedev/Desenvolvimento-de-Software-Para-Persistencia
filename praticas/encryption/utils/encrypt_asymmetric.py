from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.hashes import SHA256

# Função para criptografar com chave pública
def encrypt_asymmetric(file_path, public_key):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        encrypted_data = public_key.encrypt(
            file_data,
            OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
        )
    encrypted_file = f"{file_path}.enc"
    with open(encrypted_file, 'wb') as f:
        f.write(encrypted_data)
    print(f"Arquivo criptografado: {encrypted_file}")
    return encrypted_file