# WiFiSplit

<div align="center">

<pre style="font-size:14px; font-weight:bold; color:#00ffcc; background:#0d1117; padding:20px; border-radius:10px;">
██╗    ██╗██╗███████╗██╗    ███████╗██████╗ ██╗     ██╗████████╗
██║    ██║██║██╔════╝██║    ██╔════╝██╔══██╗██║     ██║╚══██╔══╝
██║ █╗ ██║██║█████╗  ██║    ███████╗██████╔╝██║     ██║   ██║   
██║███╗██║██║██╔══╝  ██║    ╚════██║██╔═══╝ ██║     ██║   ██║   
╚███╔███╔╝██║██║     ██║    ███████║██║     ███████╗██║   ██║   
 ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝    ╚══════╝╚═╝     ╚══════╝╚═╝   ╚═╝   
</pre>

<h3>🔓 WiFiSplit – Parallel Wi-Fi Cracking Tool</h3>

by <b>MozzieGM</b>  
<a href="https://github.com/MozzieGM">github.com/MozzieGM</a>  

</div>

---

## ⚠️ Legal Disclaimer

<div style="background:#1a1a1a; padding:12px; border-radius:8px; color:#ff5555;">
⚠️ <b>WiFiSplit</b> is a tool made <u>exclusively for educational purposes and authorized penetration testing</u>.<br>
Using this software on networks without explicit authorization is <b>illegal</b> and punishable by law.<br>
The author (MozzieGM) is not responsible for any misuse or damage caused by this tool.
</div>

---

## 📖 About

WiFiSplit is a Python tool to analyze Wi-Fi `.pcap` capture files, extract WPA/WPA2 handshakes, split wordlists, and run **Aircrack-ng** in parallel with real-time monitoring.

- ⚡ **Focus:** Performance, clarity, and cross-platform (Windows/Linux).  
- 🌍 **Languages:** Portuguese 🇧🇷 and English 🇺🇸.  
- 📑 **Reports:** Generates clean cracking reports automatically.  

---

## ✨ Features

- 📡 **PCAP Analysis:** Detects WPA/WPA2 handshakes from capture files.  
- 📂 **Wordlist Management:** Custom or auto-split wordlists.  
- 🔥 **Parallel Cracking:** Run Aircrack-ng in multiple processes.  
- ⏱️ **Real-Time Monitoring:** Dynamic updates in the terminal.  
- 🎨 **ASCII Branding:** WiFiSplit logo on startup.  

---

## 📂 Project Structure

```bash
WiFiSplit/
│── main.py               # Main script
│── wordlist_generator.py # Demo wordlist generator
│
├── PCAP/                 # Place your .pcap capture files here
├── WordList/             # Place or generate wordlists here
├── Resultados/           # Cracking results are saved here
│
└── README.md             # This file
```

## 🚀 Installation & Usage

```bash
# Clone the repo
git clone https://github.com/MozzieGM/WiFiSplit.git
cd WiFiSplit

# Install dependencies
pip install -r requirements.txt

# Run WiFiSplit
python main.py
```
### Generate demo wordlist:

```bash
python wordlist_generator.py
```

## 📑 Example Report

```text
📡 WiFiSplit Report
====================

✅ Password found: 1234vida

BSSID: 00:5f:67:5b:b8:31
ESSID: DemoNetwork
EAPOL Packets: 50

📂 Wordlist:
File: wordlist_demo.txt
Total passwords: 50,000
Parallel processes: 4

⚙️ Execution:
Start: 2025-09-07 14:16:36
End:   2025-09-07 14:16:37
⏱️ Total time: 0 min 1 sec

💻 System:
OS: Windows 10
CPU cores: 16
```

## 📜 License

This project is under the MIT License.<br>
Feel free to use, modify, and share with proper attribution.

<div align="center">

👨‍💻 Developed with ❤️ by MozzieGM
🔗 <a href="https://github.com/MozzieGM">github.com/MozzieGM</a>

</div> 