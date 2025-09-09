#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import sys
from threading import Thread

# ==============================
# Configuration
# ==============================
AUTHOR_NAME = "Veer Kumar"  # Change this to your name
TOOL_DESCRIPTIONS = {
    1: ("ARP-scan", "Layer 2 network discovery", "sudo arp-scan {target}"),
    2: ("Nmap (Basic)", "Service/version detection", "nmap -sV {target}"),
    3: ("Nmap (Aggressive)", "Aggressive scan with OS detection, versioning, scripts, traceroute", "nmap -A -T4 {target}"),
    4: ("Masscan (Top Ports)", "High-speed scan of top 1000 ports", "sudo masscan {target} --top-ports 1000 --rate 5000"),
    5: ("Masscan (Full Range)", "Full range scan on all 65535 ports", "sudo masscan {target} --ports 1-65535 --rate 10000"),
    6: ("Nmap NSE", "Vulnerability scanning using NSE scripts", "nmap --script vuln {target}"),
    7: ("SNMP-check (Basic)", "SNMP enumeration", "snmp-check {target}"),
    8: ("SNMPwalk (Advanced)", "Deep SNMP enumeration", "snmpwalk -v2c -c public {target}")
}

# ==============================
# Colors for terminal output
# ==============================
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ==============================
# UI Functions
# ==============================
def show_banner():
    banner = f"""
{Colors.HEADER}##########################################################
#               {Colors.OKGREEN}ADVANCED NETWORK SCANNER{Colors.HEADER}                 #
#                  Author: {Colors.OKBLUE}{AUTHOR_NAME}{Colors.HEADER}                    #
#                                                        #
#  A professional network scanning tool for pentesters.  #
##########################################################{Colors.ENDC}
"""
    print(banner)


def show_scan_options():
    print(f"\n{Colors.HEADER}Available Scanning Tools:{Colors.ENDC}")
    for num, (name, desc, _) in TOOL_DESCRIPTIONS.items():
        print(f"  {Colors.BOLD}{num}.{Colors.ENDC} {name} - {desc}")
    print(f"\n{Colors.BOLD}0.{Colors.ENDC} Run ALL scans")

# ==============================
# Helper Functions
# ==============================
def is_tool_installed(tool):
    try:
        subprocess.check_output(f"which {tool}", shell=True, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def run_command_live(command, tool_name, report_data):
    print(f"\n{Colors.OKBLUE}[+] Running {tool_name}...{Colors.ENDC}")
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        output = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                print(f"{Colors.OKGREEN}{line.strip()}{Colors.ENDC}", flush=True)
                output.append(line)

        exit_code = process.poll()
        report_data[tool_name] = {
            "command": command,
            "output": "".join(output),
            "status": "Success" if exit_code == 0 else f"Failed (Code: {exit_code})"
        }

    except Exception as e:
        report_data[tool_name] = {
            "command": command,
            "output": f"Error: {str(e)}",
            "status": "Error"
        }

# ==============================
# Report Generator
# ==============================
def generate_html_report(report_data, filename):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Advanced Network Scanner Report</title>
<style>
body {{
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 20px;
  background-color: #f5f5f5;
  color: #333;
}}
.container {{
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  border-radius: 5px;
}}
.header {{
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  padding: 20px;
  border-radius: 5px 5px 0 0;
  margin-bottom: 20px;
}}
.scan-section {{
  margin-bottom: 25px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}}
.scan-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.status {{
  padding: 3px 10px;
  border-radius: 3px;
  font-weight: bold;
}}
.success {{
  background-color: #dff0d8;
  color: #3c763d;
}}
.failed {{
  background-color: #f2dede;
  color: #a94442;
}}
pre {{
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: Consolas, Monaco, 'Andale Mono', monospace;
}}
.command {{
  font-family: monospace;
  color: #31708f;
  background-color: #d9edf7;
  padding: 2px 5px;
  border-radius: 3px;
}}
.footer {{
  margin-top: 30px;
  text-align: center;
  color: #777;
  font-size: 12px;
}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Advanced Network Scanner Report</h1>
    <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p>Author: {AUTHOR_NAME}</p>
  </div>
"""

    for tool, data in report_data.items():
        status_class = "success" if data["status"].startswith("Success") else "failed"
        html += f"""
    <div class="scan-section">
        <div class="scan-header">
            <h2>{tool}</h2>
            <span class="status {status_class}">{data['status']}</span>
        </div>
        <p>Command: <span class="command">{data['command']}</span></p>
        <pre>{data['output']}</pre>
    </div>"""

    html += """
    <div class="footer">
        <p>Report generated by Advanced Network Scanner</p>
    </div>
</div>
</body>
</html>"""

    with open(filename, 'w') as f:
        f.write(html)
    print(f"\n{Colors.OKGREEN}[+] Report saved as: {filename}{Colors.ENDC}")

# ==============================
# Main Scan Logic
# ==============================
def run_selected_scans(target, selected_scans):
    report_data = {}
    threads = []

    if 0 in selected_scans:
        selected_scans = list(TOOL_DESCRIPTIONS.keys())

    for scan_num in selected_scans:
        tool_name, _, command_template = TOOL_DESCRIPTIONS[scan_num]
        command = command_template.format(target=target)

        if is_tool_installed(command.split()[0]):
            thread = Thread(target=run_command_live, args=(command, tool_name, report_data))
            thread.start()
            threads.append(thread)
        else:
            report_data[tool_name] = {
                "command": command,
                "output": f"Error: {tool_name.split()[0]} is not installed",
                "status": "Not Installed"
            }

    for thread in threads:
        thread.join()

    filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    generate_html_report(report_data, filename)


def main():
    show_banner()

    # Get target
    while True:
        target = input(f"\n{Colors.BOLD}Enter IP or Network Range (e.g., 192.168.1.0/24): {Colors.ENDC}").strip()
        if target:
            break
        print(f"{Colors.FAIL}[-] Invalid input. Please try again.{Colors.ENDC}")

    # Get scan selection
    show_scan_options()
    while True:
        try:
            choices = input(f"\n{Colors.BOLD}Select scans to run (comma separated, 0 for all): {Colors.ENDC}").strip()
            selected_scans = [int(choice) for choice in choices.split(",") if choice.strip().isdigit()]

            valid_choices = [0] + list(TOOL_DESCRIPTIONS.keys())
            if all(choice in valid_choices for choice in selected_scans):
                break
            print(f"{Colors.FAIL}[-] Invalid selection. Please choose from the available options.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}[-] Invalid input. Please enter numbers separated by commas.{Colors.ENDC}")

    print(f"\n{Colors.HEADER}[+] Starting scans on {target}...{Colors.ENDC}")
    run_selected_scans(target, selected_scans)


if __name__ == "__main__":
    # Check if running as root (required for some scans)
    if os.geteuid() != 0:
        print(f"{Colors.WARNING}[!] Warning: Some scans may require root privileges.{Colors.ENDC}")

    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[-] Scan interrupted by user.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}[-] Unexpected error: {str(e)}{Colors.ENDC}")
        sys.exit(1)
