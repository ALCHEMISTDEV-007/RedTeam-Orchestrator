import os
from datetime import datetime
import sys
import argparse
import subprocess
import pyfiglet
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Initialize UI
console = Console()
load_dotenv()

def print_banner():
    # ASCII Art for the Alchemist identity
    banner = pyfiglet.figlet_format("ALCHEMIST", font="slant")
    console.print(f"[bold red]{banner}[/bold red]")
    console.print("[bold cyan]⫸  PRECISION RED-TEAM ORCHESTRATOR v2.0[/bold cyan]")
    console.print("[bold white]⫸  DEV: THE ALCHEMIST (B.P.I.W. PROJECTION)[/bold white]")
    console.print("—" * 60 + "\n")

def get_ai_analysis(scan_data):
    """Modernized Gemini Analysis using the google-genai SDK"""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    sys_instruct = (
        "You are a Senior Red Team Lead. Analyze the following Nmap output. "
        "Identify critical vulnerabilities, potential exploit paths, and remediation steps. "
        "Format your response as a structured list of risks."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=sys_instruct),
            contents=f"Nmap Scan Results:\n{scan_data}"
        )
        return response.text
    except Exception as e:
        return f"[!] AI Analysis Failed: {str(e)}"

def scan_target(target_ip: str, stealth: bool = False) -> str:
    """Uses subprocess to execute nmap with optional evasion tactics."""
    # Base command
    command = ["nmap", "-sT", "-sV", "-p", "80,8080,443"]
    
    if stealth:
        console.print("[bold purple]⫸  GHOST MODE ENGAGED: Evading IDS via 'Low & Slow' connection throttling...[/bold purple]")
        # -T2: Polite timing (slows down scan)
        # --max-rate 10: Never send more than 10 packets per second
        # --scan-delay 1s: Wait exactly 1 second between every single probe
        command.extend(["-T2", "--max-rate", "10", "--scan-delay", "1s"])
    
    command.append(target_ip)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Scanning {target_ip}...", total=None)
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Nmap Execution Error (Exit Code {e.returncode}):\n{e.stderr}[/bold red]")
            sys.exit(1)

def save_report(target_ip: str, report_content: str):
    """Saves the AI assessment to a Markdown file for persistence."""
    # 1. Create a 'reports' directory if it doesn't already exist
    os.makedirs("reports", exist_ok=True)
    
    # 2. Generate a clean timestamp (e.g., 20260315_123000)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/alchemist_{target_ip}_{timestamp}.md"
    
    # 3. Write the formatted Markdown file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"# 🛡️ Alchemist Recon Report: {target_ip}\n")
        file.write(f"**Scan Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write("---\n\n")
        file.write(report_content)
        
    # 4. Notify the user
    console.print(f"[bold green]⫸  ARCHIVE SUCCESS: Report saved locally to {filename}[/bold green]\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alchemist Red Team Orchestrator")
    parser.add_argument("-t", "--target", required=True, help="Target IP or Domain")
    parser.add_argument("-s", "--stealth", action="store_true", help="Enable Ghost Mode (Low & Slow Evasion)")
    args = parser.parse_args()

    print_banner()
    
    scan_data = scan_target(args.target, args.stealth)
    
    
    if scan_data:
        console.print("[cyan][*] Passing scan data to AI for analysis...[/cyan]")
        ai_report = get_ai_analysis(scan_data)
        
        # Print it to the screen
        console.print("\n")
        console.print(Panel(ai_report, title="Alchemist AI Analysis Report"))
        
        # Save it to the hard drive
        save_report(args.target, ai_report)