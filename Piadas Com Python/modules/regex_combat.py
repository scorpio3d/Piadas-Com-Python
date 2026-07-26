import sqlite3
import random
import re
from rich import print

class RegexCombat:
    """
    Handles the core gameplay loop: Debugging Corrupted Nodes.
    Uses the 're' module for pattern matching and validation.
    """
    def __init__(self, db_path="data/network.db"):
        self.db_path = db_path
        
    def initiate_override(self, operator):
        is_trap = random.random() < 0.15 
        
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            
            cursor.execute("SELECT id, setup, punchline FROM corrupted_nodes WHERE threat_level = 'NORMAL' ORDER BY RANDOM() LIMIT 1")
            node = cursor.fetchone()
            
            if not node:
                print("\n[bold #fdf500][NETWORK WARNING] No corrupted nodes detected. Waiting for background thread...[/]")
                con.close()
                return
                
            node_id, setup, correct_key = node
            
            cursor.execute("SELECT punchline FROM corrupted_nodes WHERE id != ? ORDER BY RANDOM() LIMIT 3", (node_id,))
            distractors = [row[0] for row in cursor.fetchall()]
            con.close()
            
        except sqlite3.Error as e:
            print(f"[bold #ff0055][CRITICAL DB ERROR]: {e}[/]")
            return
            
        generic_errors = [
            "Error 404: Packet lost in transmission.",
            "SyntaxError: Invalid payload structure.",
            "NullPointer: Memory address restricted."
        ]
        while len(distractors) < 3:
            distractors.append(generic_errors.pop())
            
        options = [correct_key] + distractors
        random.shuffle(options)
        
        if is_trap:
            options = distractors + ["Segmentation Fault: Triggered by Rogue AI."]
            random.shuffle(options)
            
        print(f"\n👁️  [bold purple][CORRUPTED NODE #{node_id}]:[/] \"{setup}\"")
        print("\nSelect the correct decryption key (Regex Pattern) to purge the Malware:")
        
        for idx, opt in enumerate(options, 1):
            print(f"  [bold #00f0ff]{idx}.[/] {opt}")
        print("  [bold #fdf500]5. ⚠️ CANCEL SESSION! (Suspected Black ICE Honeypot)[/]")
        
        if operator.get_passive() == "clarividencia" and operator.get_combo() > 0:
            if is_trap:
                print("\n🔮 [bold #ff0055][NETRUNNER SCAN]: Warning! Masked code signature... This is a Honeypot![/]")
            else:
                dica = correct_key[:4]
                print(f"\n🔮 [bold #00f0ff][NETRUNNER SCAN]: The Regex key starts with: '^{dica}...'[/]")
                
        choice = input("\n> Inject command (1-5): ").strip()
        
        if choice not in ["1", "2", "3", "4", "5"]:
            print("\n[bold #ff0055]❌ Syntax Error! Injection failed.[/]")
            return
            
        if choice == "5":
            if is_trap:
                operator.add_combo(2)
                print("\n✨ [bold #00ff00]CRITICAL SUCCESS! Black ICE trap bypassed successfully.[/]")
                operator.extract_data("Trojan Data Fragment")
                print("💾 [dim]Extracted 'Trojan Data Fragment' to Local Drive.[/dim]")
            else:
                operator.reset_combo()
                print("\n❌ [bold #ff0055]SYSTEM PARANOIA! The node was legitimate. You dropped the connection for nothing.[/]")
        else:
            if is_trap:
                operator.reset_combo()
                print("\n❌ [bold #ff0055]SYSTEM COMPROMISED! You fell for a Honeypot and triggered the Black ICE![/]")
            else:
                chosen_option = options[int(choice) - 1]
                pattern = re.escape(correct_key)
                if re.search(pattern, chosen_option, re.IGNORECASE):
                    operator.add_combo(1)
                    print("\n✨ [bold #00ff00]OVERRIDE SUCCESS! Node purged of Malware![/]")
                    
                    if operator.get_passive() == "critico":
                        operator.add_combo(1)
                        print("💾 [dim]Code-Breaker Passive: Double data extraction![/dim]")
                else:
                    if operator.get_passive() == "escudo":
                        print("\n[bold #00f0ff]🛡️ [CYBER-ENFORCER]: ICE Armor absorbed the negative feedback! Connection maintained.[/]")
                    else:
                        operator.reset_combo()
                        print(f"\n❌ [bold #ff0055]INJECTION FAILURE! The correct key was: '{correct_key}'[/]")