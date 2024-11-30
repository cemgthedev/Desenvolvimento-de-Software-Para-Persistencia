import hashlib

# Função para calcular hash SHA-256
def calculate_sha256(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    sha256_hash = hashlib.sha256(file_data).hexdigest()
    print(f"SHA-256 do arquivo {file_path}: {sha256_hash}")
    return sha256_hash