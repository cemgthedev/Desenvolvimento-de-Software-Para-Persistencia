from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.hashes import SHA256

# Função para decriptar com chave privada
def decrypt_asymmetric(file_path, private_key):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
        decrypted_data = private_key.decrypt(
        encrypted_data,
        OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
    )
    decrypted_file = file_path.replace('.enc', '.dec')
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted_data)
    print(f"Arquivo decriptado: {decrypted_file}")
    return decrypted_file