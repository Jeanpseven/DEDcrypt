import base64
import os
import sys
import re
import subprocess

def remove_comments(script):
    return re.sub(r"# .*", "", script)

def decode_dedsec_string(encoded_string):
    decoded = base64.b64decode(encoded_string)
    return decoded

def get_script_filename():
    script_filename = sys.argv[0]
    if script_filename.endswith(".py"):
        script_filename = script_filename[:-3]  # Remove a extensão .py se estiver presente
    return script_filename

def find_crypt_file():
    script_filename = get_script_filename()
    for file in os.listdir():
        if file.endswith(".py") and file != script_filename:
            return file
    return None

def process_file(input_path, output_filename):
    with open(input_path, "r", encoding="utf-8") as file:
        script_content = file.read()

    script_without_comments = remove_comments(script_content)
    dedsec_encoded = script_without_comments.split('="')[-1][:-3]

    dedsec_decoded = decode_dedsec_string(dedsec_encoded)
    dedsec_decoded = dedsec_decoded.replace(b"exec", b"print")

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(dedsec_decoded.decode("utf-8"))

    print("Arquivo descriptografado salvo em:", output_filename)

def main():
    input_path = input("Digite o caminho para o arquivo criptografado (ou deixe em branco para procurar no diretório atual): ")
    output_filename = input("Digite o nome do arquivo de saída: ")

    if not input_path:
        input_path = find_crypt_file()

    if not input_path:
        print("Nenhum arquivo criptografado encontrado no diretório atual.")
        sys.exit(1)

    if not os.path.exists(input_path):
        print("Caminho inválido. Certifique-se de fornecer um arquivo válido.")
        sys.exit(1)

    if os.path.isfile(input_path):
        process_file(input_path, output_filename)

    else:
        print("Caminho inválido. Certifique-se de fornecer um arquivo válido.")

if __name__ == "__main__":
    main()
