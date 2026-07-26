import sys
import time
import rich
import os
from rich.console import Console
from rich.panel import Panel

from modules.operator import Operator
from modules.network_db import NetworkDB
from modules.data_scanner import DataScanner
from modules.regex_combat import RegexCombat
os.system("")

# 1. FORÇAR O TERMINAL A USAR CORES NÉON (TRUECOLOR)
rich.reconfigure(color_system="truecolor", force_terminal=True)
console = Console()
system_locked = True

def print_header(title, color="bold #00f0ff"):
    """Generates a Cyberpunk-style header with Neon Colors."""
    panel = Panel(f"⚡ {title} ⚡", expand=False, border_style=color, padding=(0, 2))
    console.print(panel)

def main():
    global system_locked
    
    console.clear()
    print_header("NEON INQUISITOR: UPLINK TERMINAL", "bold #ff0055")
    console.print("[dim]Establishing secure connection to the mainframe...[/dim]\n")
    time.sleep(1)
    
    db_engine = NetworkDB()
    db_engine.start_background_process()
    
    player = Operator(profile_id="1")
    scanner = DataScanner()
    combat = RegexCombat()
    
    console.print("\n[bold #00ff00][*] Background Daemon Active. Monitoring Rogue AI Packets...[/]\n")
    time.sleep(1)
    
    while True:
        status_color = "[bold #ff0055]🔴 BLACK ICE ACTIVE (Access Denied)[/]" if system_locked else "[bold #00ff00]🟢 ROOT ACCESS GRANTED[/]"
        
        print_header("MAIN SYSTEM MENU", "bold #00f0ff")
        console.print(f"👨‍💻 [bold #00f0ff]Operator:[/bold #00f0ff] {player.get_name()} | ⚡ [bold #fdf500]Sync-Combo:[/bold #fdf500] {player.get_combo()}")
        console.print(f"🛡️  [bold white]Security Status:[/bold white] {status_color}")
        console.print("[dim #555555]" + "-" * 60 + "[/]")
        
        console.print("1. 🔓 [bold white]Network Scan[/] [dim #00f0ff](Pandas Anomaly Radar)[/]")
        console.print("2. 🔑 [bold white]Kernel Bypass[/] [dim #00f0ff](Input Critical Threat ID)[/]")
        console.print("3. ⚔️  [bold white]Debug Corrupted Node[/] [dim #00f0ff](Regex Override Sequence)[/]")
        console.print("4. 💾 [bold white]Local Drive[/] [dim #00f0ff](SQLite Inventory)[/]")
        console.print("5. 🚪 [bold white]Disconnect[/] [dim #ff0055](Erase Traces & Exit)[/]")
        
        choice = input("\n> Operator Input: ").strip()
        
        match choice:
            case "1":
                scanner.generate_radar_scan("radar_scan.png")
                
            case "2":
                target = input("\n> Enter Critical Threat Root ID: ").strip()
                if scanner.bypass_kernel(target):
                    system_locked = False
                
            case "3":
                if system_locked:
                    console.print("\n⛔ [bold #ff0055]ACCESS DENIED: Black ICE Firewall is active. Execute Scan (1) and Bypass (2) first.[/]")
                else:
                    combat.initiate_override(player)
                    
            case "4":
                drive = player.read_local_drive()
                print_header("LOCAL DRIVE CONTENTS", "bold #00ff00")
                if not drive:
                    console.print("[bold #fdf500]Drive is empty. Purge corrupted nodes to extract data.[/]")
                else:
                    for i, item in enumerate(drive, 1):
                        console.print(f"  [bold #00f0ff]{i}.[/] {item}")
                
            case "5":
                console.print("\n[bold #ff0055]Erasing IP traces and disconnecting from the Matrix...[/]")
                sys.exit(0)
                
            case _:
                console.print("\n[bold #ff0055]Syntax Error: Invalid command.[/]")
                
        input("\nPress ENTER to continue...")
        console.clear()

if __name__ == "__main__":
    main()