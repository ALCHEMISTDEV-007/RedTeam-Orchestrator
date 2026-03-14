import argparse
import os
import sys
import subprocess

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv
import google.generativeai as genai

console = Console()

def setup_environment():
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/] GEMINI_API_KEY not found in .env file.")
        console.print("Please copy .env.example to .env and add your valid Gemini API Key.")
        sys.exit(1)
        
    genai.configure(api_key=api_key)

def scan_target(target_ip: str) -> str:
    """Uses subprocess to execute nmap and returns raw stdout."""
    # Build the nmap command
    # Using -sT (TCP Connect) instead of -sS (SYN) to avoid needing root/raw socket privileges
    command = ["nmap", "-sT", "-sV", "-p", "80,8080,443", target_ip]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Scanning {target_ip} with nmap ({' '.join(command[1:])})...", total=None)
        
        try:
            # Run the command and capture output
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            raw_output = result.stdout
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Nmap Execution Error (Exit Code {e.returncode}):[/]\n{e.stderr}")
            sys.exit(1)
        except Exception as e:
            console.print(f"[bold red]Unexpected Error running Nmap:[/] {e}")
            sys.exit(1)
            
    # Print the raw stdout for debugging as requested
    console.print("\n[bold yellow]--- Raw Nmap Output Debug ---[/]")
    console.print(raw_output)
    console.print("[bold yellow]-------------------------------[/]\n")

    return raw_output

def analyze_results(scan_text: str) -> list:
    """Sends raw Nmap text to Gemini and returns structured analysis."""
    if not scan_text or "0 IP addresses (0 hosts up) scanned" in scan_text:
        return []

    system_instruction = (
        "Act as a Senior Security Analyst. Analyze this raw Nmap scan output. "
        "Identify the top 3 potential CVEs or security misconfigurations associated with these detected versions. "
        "Provide a professional risk assessment, explaining the potential impact, and give specific patching/remediation steps for each. "
        "Return the output strictly as a valid JSON array of objects, without any markdown code blocks wrapping it. "
        "Each object must have the following keys: "
        "'title' (string), 'risk_score' (string, e.g., 'High', 'Medium', 'Low'), "
        "'description' (string), and 'remediation' (string)."
    )
    
    try:
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=system_instruction
        )
        
        prompt = f"Target Raw Nmap Data:\n{scan_text}"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Asking AI for Security Analysis...", total=None)
            response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        
        import json
        # Strip potential markdown formatting from AI output
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        return json.loads(response_text)
    except Exception as e:
        console.print(f"[bold red]AI Analysis Error:[/] {e}")
        return []

def display_results(target_ip: str, analysis: list):
    """Formats and prints the analysis findings in a rich table."""
    console.print(Panel(f"[bold cyan]Vulnerability Assessment Report for {target_ip}[/]", expand=False))

    if analysis:
        console.print("\n[bold magenta]AI Security Risk Assessment:[/]")
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column("Title", style="cyan", width=30)
        table.add_column("Risk", justify="center", width=10)
        table.add_column("Impact Analysis", style="white")
        table.add_column("Remediation", style="green")

        for finding in analysis:
            risk = finding.get('risk_score', 'Unknown')
            risk_color = "red" if any(x in risk.lower() for x in ["high", "critical"]) else ("yellow" if "medium" in risk.lower() else "green")
            
            table.add_row(
                finding.get('title', 'N/A'),
                f"[bold {risk_color}]{risk}[/]",
                finding.get('description', 'N/A'),
                finding.get('remediation', 'N/A')
            )
        
        console.print(table)
    else:
        console.print("\n[bold yellow]No AI analysis available or failed to parse results.[/]")

def main():
    parser = argparse.ArgumentParser(description="Automated Vulnerability Assessment and Security Auditing Tool")
    parser.add_argument("-t", "--target", required=True, help="Target IP address or hostname to scan")
    args = parser.parse_args()

    setup_environment()
    target_ip = args.target

    console.print(f"\n[bold blue]Starting assessment on target:[/] [white]{target_ip}[/]")
    
    # Run Nmap Scan via subprocess
    scan_text = scan_target(target_ip)
    
    # Perform AI Analysis on raw Nmap output
    analysis_results = analyze_results(scan_text)
    
    # Render Output using Rich
    display_results(target_ip, analysis_results)
    
    console.print("\n[bold green]Assessment Complete.[/]\n")

if __name__ == "__main__":
    main()
