import sqlite3
import random
import re
import json
import os
from rich import print

class RegexCombat:
    """
    Handles the core gameplay loop: Debugging Corrupted Nodes.
    The difficulty and honeypot chance scale dynamically based on the Operator's Combo.
    Features 3 Tiers of Malware Signatures loaded dynamically from external JSON.
    Raw terminal aesthetic applied.
    """
    def __init__(self, db_path="data/network.db", sig_path="data/signatures.json"):
        self.db_path = db_path
        self.sig_path = sig_path
        
        self.tier1_signatures = []
        self.tier2_signatures = []
        self.tier3_signatures = []
        
        self._load_signatures()
        
    def _load_signatures(self):
        """Loads malware signatures from an external JSON file."""
        if not os.path.exists(self.sig_path):
            print(f"[bold #ff0055][SYS-ERR] Signature registry '{self.sig_path}' missing. Loading kernel fallbacks.[/]")
            self._apply_fallback_signatures()
            return

        try:
            with open(self.sig_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tier1_signatures = data.get("tier1", [])
                self.tier2_signatures = data.get("tier2", [])
                self.tier3_signatures = data.get("tier3", [])
        except json.JSONDecodeError:
            print("[bold #ff0055][SYS-ERR] Signature registry corrupted (JSON parse error). Loading kernel fallbacks.[/]")
            self._apply_fallback_signatures()

    def _apply_fallback_signatures(self):
        """Failsafe mechanism in case the JSON data is destroyed."""
        self.tier1_signatures = [
            {"sig": "192.168.0.99", "regex": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "desc": "Rogue IP Address"}
        ]
        self.tier2_signatures = [
            {"sig": "PAYLOAD_XYZ", "regex": r"PAYLOAD_[A-Z]{3}", "desc": "Encrypted Dropper"}
        ]
        self.tier3_signatures = [
            {"sig": "EXEC:/bin/bash", "regex": r"EXEC:\/bin\/[a-z]{2,4}", "desc": "Root Shell Execution"}
        ]

    def initiate_override(self, operator):
        combo = operator.get_combo()
        
        # [SISTEMA DE HEAT / AGGRO]
        if combo < 3:
            awareness = "[bold #00ff00][LOW] Ghost in the system[/]"
            honeypot_chance = 0.10
            pool = self.tier1_signatures
            
        elif combo < 6:
            awareness = "[bold #fdf500][ELEVATED] Traces detected[/]"
            honeypot_chance = 0.25
            pool = (self.tier2_signatures * 3) + self.tier1_signatures
            
        else:
            awareness = "[bold #ff0055][CRITICAL] Active Hunt![/]"
            honeypot_chance = 0.45
            pool = (self.tier3_signatures * 5) + (self.tier2_signatures * 2) + self.tier1_signatures

        is_trap = random.random() < honeypot_chance 
        
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute("SELECT id, setup FROM corrupted_nodes WHERE threat_level = 'NORMAL' ORDER BY RANDOM() LIMIT 1")
            node = cursor.fetchone()
            con.close()
            
            if not node:
                print("\n[bold #fdf500][SYS-WARN] No corrupted nodes detected. Waiting for background daemon...[/]")
                return True
                
            node_id, setup = node
            
        except sqlite3.Error as e:
            print(f"[bold #ff0055][DB-FATAL] Error accessing network base: {e}[/]")
            return False
            
        target_malware = random.choice(pool)
        infected_text = f"{setup} ... [DATA_CORRUPTED] -> {target_malware['sig']} <- [EOF]"
        
        all_signatures = self.tier1_signatures + self.tier2_signatures + self.tier3_signatures
        all_regexes = [m["regex"] for m in all_signatures if m["regex"] != target_malware["regex"]]
        all_regexes.extend([r"[A-Z]{3}-\d{2}", r"\w+@\w+\.com", r"<\/?[\w\s]*>", r"^\/[a-z]+\/bin$"])
        
        options = [target_malware["regex"]]
        options.extend(random.sample(all_regexes, 3))
        random.shuffle(options)
        
        if is_trap:
            options = random.sample(all_regexes, 4)
            
        print(f"\n[bold purple][SYS-TRACE] ANALYSING NODE #{node_id}:[/] Intercepting data stream...")
        print(f"[bold white][NET-STAT] Rogue AI Awareness:[/] {awareness}")
        print(f"[dim][PACKET-DUMP] \"{infected_text}\"[/]")
        print("\n[bold #00f0ff][AWAITING-INPUT] Identify the signature and select the correct Regex Pattern to purge it:[/]")
        
        for idx, opt in enumerate(options, 1):
            print(f"  [bold #00ff00][ {idx} ][/] {opt}")
        print("  [bold #fdf500][ 5 ] [CANCEL SESSION] (Suspected Black ICE Honeypot)[/]")
        
        if operator.get_passive() == "clarividencia" and combo > 0:
            if is_trap:
                print("\n[bold #ff0055][PASSIVE-PROC: NEURAL SCAN] WARNING: No valid patterns detected. Honeypot signature confirmed.[/]")
            else:
                print(f"\n[bold #00f0ff][PASSIVE-PROC: NEURAL SCAN] Target signature type categorized as: {target_malware['desc']}[/]")
                
        choice = input("\n> Execute Pattern (1-5): ").strip()
        
        if choice not in ["1", "2", "3", "4", "5"]:
            print("\n[bold #ff0055][ERR-01] Syntax Error. Injection failed.[/]")
            return False 
            
        if choice == "5":
            if is_trap:
                operator.add_combo(2)
                print("\n[bold #00ff00][OVERRIDE-SUCCESS] Black ICE trap bypassed successfully.[/]")
                operator.extract_data("Trojan Data Fragment")
                print("[dim][DRIVE-WRITE] Extracted 'Trojan Data Fragment' to Local Storage.[/]")
                return True
            else:
                operator.reset_combo()
                print("\n[bold #ff0055][ERR-02] SYSTEM PARANOIA: The node was legitimate. Connection dropped prematurely.[/]")
                return True 
        else:
            if is_trap:
                operator.reset_combo()
                print("\n[bold #ff0055][ERR-FATAL] SYSTEM COMPROMISED: Code injected into Honeypot. Black ICE triggered.[/]")
                return False 
            else:
                chosen_regex = options[int(choice) - 1]
                if re.search(chosen_regex, infected_text):
                    operator.add_combo(1)
                    print(f"\n[bold #00ff00][OVERRIDE-SUCCESS] Target '{target_malware['sig']}' purged successfully.[/]")
                    
                    if operator.get_passive() == "critico":
                        operator.add_combo(1)
                        print("[dim][PASSIVE-PROC: DEEP EXTRACTION] Double data yield achieved.[/]")
                    return True
                else:
                    if operator.get_passive() == "escudo":
                        print("\n[bold #00f0ff][PASSIVE-PROC: ICE ARMOR] Negative feedback absorbed. Connection maintained.[/]")
                        return True
                    else:
                        operator.reset_combo()
                        print(f"\n[bold #ff0055][ERR-03] INJECTION FAILURE: The pattern '{chosen_regex}' failed to capture the payload.[/]")
                        return False