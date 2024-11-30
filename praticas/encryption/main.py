from utils.keys import private_key, public_key
from utils.encrypt_asymmetric import encrypt_asymmetric
from utils.decrypt_asymmetric import decrypt_asymmetric
from utils.calculate_sha256 import calculate_sha256

# Criando arquivos encriptado e decriptado do arquivo original
file_path = "./data/archive.txt"
encrypted_file = encrypt_asymmetric(file_path, public_key)
decrypted_file = decrypt_asymmetric(encrypted_file, private_key)

# Menu para teste
# Caso - o arquivo foi alterado: Alteração do txt, seleção da opção 3 -> arquivo original e decriptado diferentes
# Caso - o arquivo não foi alterado: Seleção da opção 1, seleção da opção 2, seleção da opção 3 -> arquivo original e decriptado iguais

while True:
    opcao = input("Escolha uma opção:\n1 - Criptografar arquivo\n2 - Descriptografar arquivo\n3 - Calcular SHA-256 do arquivo original e do decriptado e verificar integridade\n4 - Sair\n")
    
    if opcao == '1':
        encrypt_asymmetric(file_path, public_key)
    elif opcao == '2':
        decrypt_asymmetric(encrypted_file, private_key)
    elif opcao == '3':
        sha256_file_origin = calculate_sha256(file_path)
        sha256_file_decrypted = calculate_sha256(decrypted_file)
        
        if sha256_file_origin == sha256_file_decrypted:
            print("O arquivo original e o decriptado com SHA-256 estão iguais")
        else:
            print("O arquivo original e o decriptado com SHA-256 estão diferentes")
    elif opcao == '4':
        break