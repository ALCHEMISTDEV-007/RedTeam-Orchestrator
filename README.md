# 🛡️ AI-Powered Red Team Orchestrator

An automated Vulnerability Assessment and Reconnaissance tool that bridges the gap between traditional network scanning and LLM-powered security analysis. 

This tool utilizes `nmap` for target reconnaissance and feeds the raw network data into Google's Gemini AI to generate a color-coded, strategic risk assessment directly in the terminal.

## ✨ Features
* **Automated Reconnaissance:** Executes TCP Connect scans (`-sT` and `-sV`) to map open ports and service versions without requiring raw socket/root privileges in virtual environments.
* **AI Security Analyst:** Leverages the `google-genai` SDK to analyze discovered services against known misconfigurations and CVEs.
* **Beautiful CLI:** Uses the `rich` Python library to generate clean, readable vulnerability tables and impact analysis right in the terminal.

## 🚀 Future Scope
* **Hardware Integration:** Porting the orchestrator onto a **Raspberry Pi** to function as a physical, plug-and-play network "drop-box" for localized pentesting.
* **Ecosystem Integration:** Expanding the vulnerability detection capabilities to serve as a proactive reconnaissance module for broader defense initiatives like the **Silent Shield** project.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ALCHEMISTDEV-007/RedTeam-Orchestrator.git
   cd RedTeam-Orchestrator
   
2. **Set up the Virtual Environment & Dependencies:**
Bash

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. **Configure API Keys:**
Create a .env file in the root directory and add your Google Gemini API key:
Code snippet

    GEMINI_API_KEY="your_api_key_here"

##💻 Usage

Run the script as a standard user (no sudo required due to the -sT bypass):
Bash

python3 orchestrator.py -t <TARGET_IP_OR_DOMAIN>

Example testing on localhost:
Bash

python3 orchestrator.py -t 127.0.0.1

##⚠️ Disclaimer

This tool is built for educational purposes, ethical hacking, and authorized security auditing only. Do not scan networks or infrastructure you do not own or have explicit permission to test.
