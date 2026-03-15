# 🛡️ ALCHEMIST: AI Red-Team Orchestrator v2.0

![Version](https://img.shields.io/badge/version-2.0.0-red)
![License](https://img.shields.io/badge/license-MIT-blue)

**ALCHEMIST** is a precision reconnaissance framework that transforms raw network data into actionable security intelligence. Built for the modern Red Teamer, it combines low-level network probing with the Gemini 3.1 neural engine.

---

## ⚡ New in V2.0

* **Ghost Mode (Stealth):** Integrated "Low & Slow" connection throttling (`-T2`) to evade basic Intrusion Detection Systems (IDS).
* **The Archivist:** Automated Markdown reporting. Every scan is now immortalized in the `/reports` directory with unique tracking IDs.
* **Modernized Core:** Fully migrated to the `google-genai` SDK for near-zero latency analysis.
* **Enhanced UI:** Custom ASCII branding and `rich` terminal formatting for high-readability reports.

---

## 🛠️ Modules

### 👻 Ghost Module (`--stealth`)

Bypasses standard firewall tripwires by enforcing a 1-second delay between probes and capping packet rates. Ideal for covert reconnaissance.

### 📚 Archivist Module

Automatically generates structured `.md` files containing:

* Raw Scan Metadata
* AI-Driven Risk Assessment
* Specific Exploit Paths
* Prioritized Remediation Steps

---

## 🚀 Installation & Usage

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/ALCHEMISTDEV-007/RedTeam-Orchestrator.git
cd RedTeam-Orchestrator
pip install -r requirements.txt
```

### 2️⃣ Standard Execution

```bash
alchemist -t <target_ip>
```

### 3️⃣ Stealth Execution

```bash
alchemist -t <target_ip> --stealth
```

---

## ⚠️ Disclaimer

This tool is built **strictly for ethical hacking, penetration testing, and authorized security auditing**.
Unauthorized use against systems you do not own or have permission to test is illegal.

---

## 👨‍💻 Author

**The Alchemist**
Architect of intelligent red-team systems.
