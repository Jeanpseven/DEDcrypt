import base64
import os
import sys
import re
import subprocess

def remove_comments(script):
    return re.sub(r"#.*", "", script)

def decode_dedsec_string(encoded_string):
    decoded = base64.b64decode(encoded_string)
    return decoded

def get_script_filename():
    script_filename = sys.argv[0]
    if script_filename.endswith(".py"):
        script_filename = script_filename[:-3]  # Remove a extensão .py se estiver presente
    return script_filename

def process_file(input_path, output_filename):
    with open(input_path, "r") as file:
        script_content = file.read()

    script_without_comments = remove_comments(script_content)
    dedsec_encoded = script_without_comments.split('="')[-1][:-3]

    dedsec_decoded = decode_dedsec_string(dedsec_encoded)
    dedsec_decoded = dedsec_decoded.replace(b"exec", b"print")

    with open(output_filename, "wb") as file:
        file.write(dedsec_decoded)

    print("Arquivo descriptografado salvo em:", output_filename)

def main():
    if len(sys.argv) == 3:
        input_path = sys.argv[1]
        output_filename = sys.argv[2]

        if not os.path.exists(input_path):
            script_filename = get_script_filename()
            input_path = os.path.join(os.path.dirname(script_filename), input_path)
            if not os.path.exists(input_path):
                print("Caminho inválido. Certifique-se de fornecer um arquivo válido.")
                sys.exit(1)

        if os.path.isfile(input_path):
            process_file(input_path, output_filename)

            # Executa o script criptografado sem comentários e com "exec" substituído por "print"
            subprocess.run(f"python {output_filename}", shell=True)

        else:
            print("Caminho inválido. Certifique-se de fornecer um arquivo válido.")

    else:
        print("Uso: python script.py <caminho_do_arquivo_criptografado> <nome_do_arquivo_de_saida>")
        input_path = input("Digite o caminho para o arquivo criptografado: ")
        output_filename = input("Digite o nome do arquivo de saída: ")
        process_file(input_path, output_filename)

        # Executa o script criptografado sem comentários e com "exec" substituído por "print"
        subprocess.run(f"python {output_filename}", shell=True)

if __name__ == "__main__":
    main()
