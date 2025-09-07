import subprocess
import re
import os
import math
import time
import sys
from scapy.all import rdpcap, EAPOL, Dot11
import platform
from datetime import datetime

# Detect system and set Aircrack-ng path
if platform.system() == "Windows":
    AIRCRACK = r"C:\aircrack-ng-1.7-win\bin\aircrack-ng.exe"
else:
    AIRCRACK = "aircrack-ng"  # Use from PATH on Linux/Mac

# Base directory (where main.py is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project folders
PCAP_DIR = os.path.join(BASE_DIR, "PCAP")
WORDLIST_DIR = os.path.join(BASE_DIR, "WordList")
RESULTS_DIR = os.path.join(BASE_DIR, "Results")

# Create folders if they don't exist
os.makedirs(PCAP_DIR, exist_ok=True)
os.makedirs(WORDLIST_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Translations
LANGS = {
    "pt": {
        "choose_lang": "👉 Escolha o idioma (pt/en): ",
        "pcap_files": "📂 Arquivos PCAP disponíveis:",
        "no_pcap": "❌ Nenhum arquivo PCAP encontrado.",
        "choose_pcap": "\n👉 Escolha o número do PCAP: ",
        "analyzing": "\n🔎 Analisando pacotes...",
        "no_handshake": "❌ Nenhum handshake encontrado no arquivo.",
        "targets": "\n   #  BSSID              ESSID                     EAPOL Packets\n",
        "choose_target": "\n👉 Escolha o número do alvo: ",
        "wordlists": "\n📂 Wordlists disponíveis:",
        "no_wordlist": "❌ Nenhuma wordlist encontrada.",
        "choose_wordlist": "\n👉 Escolha a wordlist: ",
        "recommend": "\n⚡ Recomendo usar no máximo 4 partes (processos).\n   Depende do seu computador, fique de olho no uso da sua CPU!\n",
        "choose_parts": "👉 Quantas partes (processos) deseja usar? ",
        "invalid_option": "❌ Opção inválida, tente novamente.",
        "invalid_input": "❌ Entrada inválida, digite apenas números.",
        "starting": "\n▶️ Iniciando processo",
        "monitoring": "\n📊 Monitorando progresso...\n",
        "report": "📡 Relatório WiFiSplit",
        "password_found": "✅ Senha encontrada:",
        "time_total": "⏱️ Tempo total:",
        "saved": "💾 Resultado salvo em:",
        "not_found": "❌ Nenhuma senha encontrada.",
        "file": "Arquivo:",
        "total_passwords": "Total de senhas:",
        "parallel": "Processos paralelos:",
        "execution": "⚙️ Execução:",
        "system": "💻 Sistema:"
    },
    "en": {
        "choose_lang": "👉 Choose language (pt/en): ",
        "pcap_files": "📂 Available PCAP files:",
        "no_pcap": "❌ No PCAP files found.",
        "choose_pcap": "\n👉 Choose the PCAP number: ",
        "analyzing": "\n🔎 Analyzing packets...",
        "no_handshake": "❌ No handshake found in file.",
        "targets": "\n   #  BSSID              ESSID                     EAPOL Packets\n",
        "choose_target": "\n👉 Choose target number: ",
        "wordlists": "\n📂 Available wordlists:",
        "no_wordlist": "❌ No wordlists found.",
        "choose_wordlist": "\n👉 Choose the wordlist: ",
        "recommend": "\n⚡ I recommend using a maximum of 4 parts (processes).\n   Depends on your computer, keep an eye on your CPU usage!\n",
        "choose_parts": "👉 How many parts (processes) do you want to use? ",
        "invalid_option": "❌ Invalid option, try again.",
        "invalid_input": "❌ Invalid input, enter only numbers.",
        "starting": "\n▶️ Starting process",
        "monitoring": "\n📊 Monitoring progress...\n",
        "report": "📡 WiFiSplit Report",
        "password_found": "✅ Password found:",
        "time_total": "⏱️ Total time:",
        "saved": "💾 Result saved at:",
        "not_found": "❌ No password found.",
        "file": "File:",
        "total_passwords": "Total passwords:",
        "parallel": "Parallel processes:",
        "execution": "⚙️ Execution:",
        "system": "💻 System:"
    }
}


# Language selection
# === Language selection ===
# === Language selection ===
while True:
    print("👉 Choose language / Escolha o idioma")
    print("1 - Português")
    print("2 - English")
    
    choice = input("Option: ").strip()
    
    if choice == "1":
        lang = "pt"
        break
    elif choice == "2":
        lang = "en"
        break
    else:
        print("❌ Invalid option, please choose 1 or 2.\n")

T = LANGS[lang]

# === Legal disclaimer ===
if lang == "pt":
    disclaimer = """
⚠️ AVISO LEGAL
Este programa, WiFiSplit, foi desenvolvido apenas para fins educacionais e de pesquisa.
Use somente em redes e dispositivos para os quais você tem autorização expressa.
O uso indevido pode violar leis locais e resultar em sanções civis e criminais.
"""
else:
    disclaimer = """
⚠️ LEGAL DISCLAIMER
This program, WiFiSplit, was developed for educational and research purposes only.
Use only on networks and devices for which you have explicit authorization.
Misuse may violate local laws and result in civil and criminal penalties.
"""

print(disclaimer)
input("👉 Press ENTER to continue... ")

# === Clear screen ===
if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")

# === Project banner ===
banner = r"""
██╗    ██╗██╗███████╗██╗    ███████╗██████╗ ██╗     ██╗████████╗
██║    ██║██║██╔════╝██║    ██╔════╝██╔══██╗██║     ██║╚══██╔══╝
██║ █╗ ██║██║█████╗  ██║    ███████╗██████╔╝██║     ██║   ██║   
██║███╗██║██║██╔══╝  ██║    ╚════██║██╔═══╝ ██║     ██║   ██║   
╚███╔███╔╝██║██║     ██║    ███████║██║     ███████╗██║   ██║   
 ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝    ╚══════╝╚═╝     ╚══════╝╚═╝   ╚═╝   
                                                                
                  by MozzieGM | github.com/MozzieGM
"""
print(banner)

def clean_output(line):
    return re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', line).replace("\r", "").strip()

def list_files(folder, extension):
    return [f for f in os.listdir(folder) if f.lower().endswith(extension)]

def analyze_pcap(pcap_file):
    packets = rdpcap(pcap_file)
    eapol = [p for p in packets if p.haslayer(EAPOL)]
    results = []
    if eapol:
        for p in packets:
            if p.haslayer(Dot11) and p.type == 0 and p.subtype == 8:
                bssid = p.addr2
                essid = p.info.decode(errors="ignore")
                results.append((bssid, essid, len(eapol)))
        seen, unique = set(), []
        for r in results:
            if r[0] not in seen:
                unique.append(r)
                seen.add(r[0])
        return unique
    return []

def split_wordlist(wordlist, parts):
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    size = math.ceil(len(lines) / parts)
    split_files = []
    for i in range(parts):
        start = i * size
        end = start + size
        split_name = os.path.join(WORDLIST_DIR, f"part_{i+1}.txt")
        with open(split_name, "w", encoding="utf-8") as f:
            f.writelines(lines[start:end])
        split_files.append(split_name)
    return split_files

def save_result(pcap_file, bssid, essid, eapol_count, wordlist, password,
                start_exec, end_exec, minutes, seconds, processes):
    total_passwords = sum(1 for _ in open(wordlist, "r", encoding="utf-8", errors="ignore"))

    output_name = os.path.basename(pcap_file).replace(".pcap", "_result.txt")
    output_path = os.path.join(RESULTS_DIR, output_name)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(T["report"] + "\n")
        f.write("====================\n\n")

        f.write(f"{T['password_found']} {password}\n\n")
        f.write(f"BSSID: {bssid}\n")
        f.write(f"ESSID: {essid}\n")
        f.write(f"EAPOL Packets: {eapol_count}\n\n")

        f.write(T["wordlists"] + "\n")
        f.write(f"{T['file']} {os.path.basename(wordlist)}\n")
        f.write(f"{T['total_passwords']} {total_passwords:,}\n")
        f.write(f"{T['parallel']} {processes}\n\n")

        f.write(T["execution"] + "\n")
        f.write(f"Start: {start_exec}\n")
        f.write(f"End:   {end_exec}\n")
        f.write(f"{T['time_total']} {minutes} min {seconds} sec\n\n")

        f.write(T["system"] + "\n")
        f.write(f"OS: {platform.system()} {platform.release()}\n")
        f.write(f"CPU cores: {os.cpu_count()}\n")

    return output_path

def run_parallel(pcap_file, bssid, essid, wordlists, start_time, eapol_count):
    processes = []
    password = None
    status = {i: {"line": "", "pass": ""} for i in range(1, len(wordlists) + 1)}
    start_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for idx, wl in enumerate(wordlists, 1):
        cmd = [AIRCRACK, "-w", wl, "-b", bssid, "-e", essid, pcap_file]
        print(f"{T['starting']} {idx}: {' '.join(cmd)}")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        processes.append((idx, p))

    print(T["monitoring"])

    while processes and password is None:
        for idx, p in list(processes):
            line = p.stdout.readline()
            if not line:
                if p.poll() is not None:
                    processes.remove((idx, p))
                continue

            line = clean_output(line)

            if "keys tested" in line and "Time left" in line:
                status[idx]["line"] = line
            elif "Current passphrase" in line:
                status[idx]["pass"] = line

            sys.stdout.write("\033[H\033[J")  
            for i in range(1, len(wordlists) + 1):
                print(f"[Part {i}] {status[i]['line']}")
                print(f"[Part {i}] {status[i]['pass']}\n")
            sys.stdout.flush()

            match = re.search(r"KEY FOUND! \[ (.+?) \]", line)
            if match:
                password = match.group(1)
                end_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                end_time = time.time()
                minutes, seconds = divmod(int(end_time - start_time), 60)

                # Terminate all processes
                for _, pr in processes:
                    try:
                        pr.terminate()
                        pr.wait(timeout=2)
                    except Exception:
                        pass
                processes.clear()

                output_path = save_result(
                    pcap_file, bssid, essid, eapol_count, wordlists[idx-1],
                    password, start_exec, end_exec, minutes, seconds, len(wordlists)
                )

                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")

                print(T["report"])
                print("====================\n")
                print(f"{T['password_found']} {password}")
                print(f"{T['time_total']} {minutes} min {seconds} sec")
                print(f"{T['saved']} {output_path}")
                return password

    return None

def choose_option(qtd, message):
    try:
        choice = int(input(message))
        if 1 <= choice <= qtd:
            return choice - 1
        else:
            print(T["invalid_option"])
            return None
    except ValueError:
        print(T["invalid_input"])
        return None

# ==== Main flow ====
if __name__ == "__main__":
    print(T["pcap_files"])
    pcaps = list_files(PCAP_DIR, ".pcap")
    if not pcaps:
        print(T["no_pcap"])
        sys.exit(1)

    pcap_idx = None
    while pcap_idx is None:
        for i, f in enumerate(pcaps, 1):
            print(f"  {i}. {f}")
        pcap_idx = choose_option(len(pcaps), T["choose_pcap"])

    pcap_file = os.path.join(PCAP_DIR, pcaps[pcap_idx])

    print(T["analyzing"])
    targets = analyze_pcap(pcap_file)
    if not targets:
        print(T["no_handshake"])
        exit()

    print(T["targets"])
    for i, (bssid, essid, eapol_count) in enumerate(targets, 1):
        print(f"   {i}  {bssid:<18} {essid:<25} {eapol_count}")

    target_idx = None
    while target_idx is None:
        target_idx = choose_option(len(targets), T["choose_target"])

    bssid, essid, eapol_count = targets[target_idx]

    print(T["wordlists"])
    wordlists = list_files(WORDLIST_DIR, ".txt")
    if not wordlists:
        print(T["no_wordlist"])
        sys.exit(1)

    word_idx = None
    while word_idx is None:
        for i, f in enumerate(wordlists, 1):
            print(f"  {i}. {f}")
        word_idx = choose_option(len(wordlists), T["choose_wordlist"])

    wordlist = os.path.join(WORDLIST_DIR, wordlists[word_idx])

    print(T["recommend"])

    parts = None
    while parts is None:
        try:
            parts = int(input(T["choose_parts"]))
            if parts < 1:
                print(T["invalid_option"])
                parts = None
        except ValueError:
            print(T["invalid_input"])
            parts = None

    start_time = time.time()

    if parts == 1:
        divided_wordlists = [wordlist]
    else:
        divided_wordlists = split_wordlist(wordlist, parts)

    try:
        password = run_parallel(pcap_file, bssid, essid, divided_wordlists, start_time, eapol_count)
        if not password:
            end_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_time = time.time()
            minutes, seconds = divmod(int(end_time - start_time), 60)

            output_path = save_result(
                pcap_file, bssid, essid, eapol_count, wordlist,
                T["not_found"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                end_exec, minutes, seconds, len(divided_wordlists)
            )

            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")

            print(T["report"])
            print("====================\n")
            print(T["not_found"])
            print(f"{T['time_total']} {minutes} min {seconds} sec")
            print(f"{T['saved']} {output_path}")

    finally:
        if parts > 1:
            for wl in divided_wordlists:
                try:
                    os.remove(wl)
                except Exception:
                    pass
