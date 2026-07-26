import sys
import time
import os
import json
import rich
from rich.console import Console
from rich.panel import Panel

from modules.operator import Operator
from modules.network_db import NetworkDB
from modules.data_scanner import DataScanner
from modules.regex_combat import RegexCombat

os.system("")
rich.reconfigure(color_system="truecolor", force_terminal=True)
console = Console()
system_locked = True

def print_header(title, color="bold #00f0ff"):
    panel = Panel(f"/// {title} ///", expand=False, border_style=color, padding=(0, 2))
    console.print(panel)

def select_class():
    console.clear()
    print_header("OPERATOR REGISTRATION", "bold #00f0ff")
    console.print("\n[bold white]Select your combat profile:[/]")
    console.print("  [bold #00ff00]1.[/] Netrunner [dim](Passive: Neural Scan - Identifies Honeypots)[/]")
    console.print("  [bold #00ff00]2.[/] Cyber-Enforcer [dim](Passive: ICE Armor - Blocks first failure)[/]")
    console.print("  [bold #00ff00]3.[/] Code-Breaker [dim](Passive: Deep Extraction - Double data extraction)[/]")
    
    while True:
        choice = input("\n> Initialize Profile (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        console.print("[bold #ff0055][ERROR] Invalid syntax. Select 1, 2, or 3.[/]")

def main():
    global system_locked
    
    profile_id = select_class()
    player = Operator(profile_id=profile_id)
    
    console.clear()
    print_header("NEON INQUISITOR: UPLINK TERMINAL", "bold #ff0055")
    console.print("[dim]Establishing secure connection to the mainframe...[/dim]\n")
    time.sleep(1)
    
    db_engine = NetworkDB()
    db_engine.start_background_process()
    
    scanner = DataScanner()
    combat = RegexCombat()
    
    console.print("\n[bold #00ff00][*] Background Daemon Active. Monitoring Rogue AI Packets...[/]\n")
    time.sleep(1)
    
    while True:
        status_color = "[bold #ff0055][BLACK ICE ACTIVE] (Access Denied)[/]" if system_locked else "[bold #00ff00][ROOT ACCESS GRANTED][/]"
        
        print_header("MAIN SYSTEM MENU", "bold #00f0ff")
        console.print(f"[bold #00f0ff]Operator:[/] {player.get_name()} | [bold #fdf500]Sync-Combo:[/] {player.get_combo()}")
        console.print(f"[bold white]Security Status:[/] {status_color}")
        console.print("[dim #555555]" + "-" * 60 + "[/]")
        
        # Menu carregado dinamicamente a partir do JSON externo
        try:
            with open("data/menu_config.json", "r", encoding="utf-8") as f:
                menu_options = json.load(f)
                for key, opt in menu_options.items():
                    console.print(f"{key}. [bold white]{opt['title']}[/] [dim #00f0ff]({opt['desc']})[/]")
        except (FileNotFoundError, json.JSONDecodeError):
            console.print("1. [bold white]Network Scan[/]")
            console.print("2. [bold white]Kernel Bypass[/]")
            console.print("3. [bold white]Debug Corrupted Node[/]")
            console.print("4. [bold white]Local Drive[/]")
            console.print("5. [bold white]Disconnect[/]")
        
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
                    console.print("\n[bold #ff0055][ACCESS DENIED] Black ICE Firewall is active. Execute Scan (1) and Bypass (2) first.[/]")
                else:
                    survived = combat.initiate_override(player)
                    if not survived:
                        system_locked = True
                        console.print("\n[bold #ff0055][CRITICAL PENALTY] You have been kicked out of the kernel. System Locked.[/]")
                    
            case "4":
                drive = player.read_local_drive()
                print_header("LOCAL DRIVE CONTENTS", "bold #00ff00")
                if not drive:
                    console.print("[bold #fdf500]Drive is empty. Purge corrupted nodes to extract data.[/]")
                else:
                    for i, item in enumerate(drive, 1):
                        console.print(f"  [bold #00f0ff]{i}.[/] {item}")
                
            case "5":
                console.print("\n[bold #ff0055][SYS-DISCONNECT] Erasing IP traces and closing connection...[/]")
                sys.exit(0)
                
            case _:
                console.print("\n[bold #ff0055][ERROR] Invalid command syntax.[/]")
                
        input("\nPress ENTER to continue...")
        console.clear()

if __name__ == "__main__":
    main()