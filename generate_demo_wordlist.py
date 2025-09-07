import os
import random
import string

# Base directory (onde o script está)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDLIST_DIR = os.path.join(BASE_DIR, "WordList")

# Cria a pasta WordList se não existir
os.makedirs(WORDLIST_DIR, exist_ok=True)

def gerar_wordlist(nome_arquivo="wordlist_demo.txt", total=50000, tamanho=8):
    # Caminho final do arquivo
    arquivo = os.path.join(WORDLIST_DIR, nome_arquivo)

    # posição aleatória onde a senha correta vai entrar
    posicao_correta = random.randint(0, total - 1)

    with open(arquivo, "w", encoding="utf-8") as f:
        for i in range(total):
            if i == posicao_correta:
                senha = "1234vida"
            else:
                # gera senha aleatória (letras e números)
                senha = "".join(random.choices(string.ascii_lowercase + string.digits, k=tamanho))
            f.write(senha + "\n")

    print(f"✅ Wordlist gerada com {total} senhas (inclui '1234vida') em: {arquivo}")

if __name__ == "__main__":
    gerar_wordlist("wordlist_demo.txt", total=50000, tamanho=8)
