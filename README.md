# 🔎 Advanced Network Scanner

`advance_network_scan` is a **multi-tool automation framework** for penetration testers, red teamers, and network administrators.  
It combines popular open-source scanning and enumeration tools into a **single unified interface**, provides **real-time output**, and automatically generates a **comprehensive HTML report**.

---

## ✨ Features

- 🖥 **Multi-tool integration**
  - Nmap (basic, aggressive, NSE scripts)
  - Masscan (top ports, full port scan)
  - SNMP-check & SNMPwalk for SNMP enumeration
  - ARP-scan for local network discovery
- ⚡ **Real-time output streaming** while scans run
- 🔀 **Multithreaded execution** (run multiple scans at once)
- 📊 **Automatic HTML report generation** with:
  - Command executed
  - Success/failure status
  - Full scan output
- 📁 **Clean and organized report storage** with timestamps
- 🚨 Handles missing tools gracefully (shows "Not Installed")
- 🔒 Root privilege warning for scans that require it

---

## 🛠 Requirements

- Python **3.7+**
- Linux (tested on **Kali Linux**, **Parrot OS**, **Ubuntu**)
- Tools:
  - `nmap`
  - `masscan`
  - `arp-scan`
  - `snmp-check`
  - `snmpwalk`

### Install dependencies (Debian/Kali-based):

```bash
sudo apt update
sudo apt install -y nmap masscan arp-scan snmp snmp-mibs-downloader

Installation

Clone the repository:

git clone https://github.com/yourusername/advance_network_scan.git
cd advance_network_scan


Make the script executable:

chmod +x advance_network_scan.py


Run:

./advance_network_scan.py

🚀 Usage

Start the tool:

python3 advance_network_scan.py

Example Workflow
Enter IP or Network Range (e.g., 192.168.1.0/24): 192.168.1.0/24
Select scans to run (comma separated, 0 for all): 1,2,3


Watch results in real-time

At the end, an HTML report is generated automatically:

[+] Report saved as: scan_report_20250909_153045.html

🧪 Available Scans
#	Tool	Description	Example Command
1	ARP-scan	Layer 2 network discovery	arp-scan 192.168.1.0/24
2	Nmap (Basic)	Service/version detection	nmap -sV 192.168.1.10
3	Nmap (Aggressive)	OS detection, versioning, scripts, traceroute	nmap -A -T4 192.168.1.10
4	Masscan (Top Ports)	High-speed scan of top 1000 ports	masscan 192.168.1.0/24 --top-ports 1000 --rate 5000
5	Masscan (Full Range)	Full 1–65535 port scan	masscan 192.168.1.10 --ports 1-65535 --rate 10000
6	Nmap NSE	Vulnerability scan using built-in NSE scripts	nmap --script vuln 192.168.1.10
7	SNMP-check	Basic SNMP enumeration	snmp-check 192.168.1.10
8	SNMPwalk	Deep SNMP enumeration (MIBs)	snmpwalk -v2c -c public 192.168.1.10
📊 Reporting

Reports are saved in HTML format

Includes:

Command used

Status (success / failure)

Full scan output

File naming convention:

scan_report_YYYYMMDD_HHMMSS.html

Example Report Snippet
<h2>Nmap (Basic)</h2>
<span class="status success">Success</span>
<p>Command: nmap -sV 192.168.1.10</p>
<pre>
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5 (protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.51 ((Debian))
</pre>

⚠️ Legal Disclaimer

This tool is intended for educational purposes and authorized penetration testing only.
Unauthorized scanning of systems you do not own or lack explicit permission to test is illegal.

👨‍💻 Author

Veer Kumar
Cybersecurity Enthusiast • Red Teaming & OSINT • Open-Source Advocate
