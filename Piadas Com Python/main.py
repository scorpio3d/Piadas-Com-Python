import sys
import time
import os
import json
import rich
from rich.console import Console

from modules.operator import Operator
from modules.network_db import NetworkDB
from modules.data_scanner import DataScanner
from modules.regex_combat import RegexCombat
from modules.ui import print_header, print_success, print_error, print_warning, print_rule

os.system("")
rich.reconfigure(color_system="truecolor", force_terminal=True)
console = Console()
system_locked = True

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
        print_error("Invalid syntax. Select 1, 2, or 3.")

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
    
    print_success("Background Daemon Active. Monitoring FRED Packets...")
    time.sleep(1)
    
    while True:
        console.clear()
        
        # --- FASE 1: PERIMETRO (BLOQUEADO) ---
        if system_locked:
            print_header("OUTER PERIMETER GATEWAY", "bold #ff0055")
            console.print(f"[bold #00f0ff]Operator:[/] {player.get_name()} | [bold #fdf500]Sync-Combo:[/] {player.get_combo()}")
            console.print("[bold white]Security Status:[/] [bold white on #550000] [BLACK ICE ACTIVE] (Access Denied) [/]")
            print_rule()
            
            try:
                with open("data/menu_config.json", "r", encoding="utf-8") as f:
                    menu = json.load(f)["locked"]
                    for key, opt in menu.items():
                        console.print(f"{key}. [bold white]{opt['title']}[/] [dim #00f0ff]({opt['desc']})[/]")
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                console.print("1. [bold white]Intercept Perimeter Traffic[/]")
                console.print("2. [bold white]Force Firewall Bypass[/]")
            
            choice = input("\n> Execute Command (1-2): ").strip()
            
            if choice == "1":
                scanner.generate_radar_scan()
            elif choice == "2":
                target = input("\n> Enter Critical Threat Root ID: ").strip()
                if scanner.bypass_kernel(target):
                    system_locked = False
            else:
                print_error("Invalid command syntax.")
                
        # --- FASE 2: INTRANET (DESBLOQUEADO) ---
        else:
            print_header("INNER MAINFRAME ACCESS", "bold #00ff00")
            console.print(f"[bold #00f0ff]Operator:[/] {player.get_name()} | [bold #fdf500]Sync-Combo:[/] {player.get_combo()}")
            console.print("[bold white]Security Status:[/] [bold white on #004400] [ROOT ACCESS GRANTED] [/]")
            print_rule()
            
            try:
                with open("data/menu_config.json", "r", encoding="utf-8") as f:
                    menu = json.load(f)["unlocked"]
                    for key, opt in menu.items():
                        console.print(f"{key}. [bold white]{opt['title']}[/] [dim #00f0ff]({opt['desc']})[/]")
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                console.print("1. [bold white]Debug Corrupted Node[/]")
                console.print("2. [bold white]Access Local Drive[/]")
                console.print("3. [bold white]Disconnect[/]")
                
            choice = input("\n> Execute Command (1-3): ").strip()
            
            if choice == "1":
                survived = combat.initiate_override(player)
                if not survived:
                    system_locked = True
                    print_error("You have been kicked out of the kernel. Returning to Outer Perimeter.")
            elif choice == "2":
                drive = player.read_local_drive()
                print_header("LOCAL DRIVE CONTENTS", "bold #00ff00")
                if not drive:
                    print_warning("Drive is empty. Purge corrupted nodes to extract data.")
                else:
                    for i, item in enumerate(drive, 1):
                        console.print(f"  [bold #00f0ff]{i}.[/] {item}")
            elif choice == "3":
                print_warning("Erasing IP traces and closing connection...")
                sys.exit(0)
            else:
                print_error("Invalid command syntax.")

        input("\nPress ENTER to continue...")

if __name__ == "__main__":
    main()