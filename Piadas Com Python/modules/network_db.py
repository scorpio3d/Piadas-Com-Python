import sqlite3
import requests
import threading
import time
import os
from rich import print

class NetworkDB:
    """
    Handles database persistence and background API fetching.
    Implements Multithreading for I/O tasks and secure SQLite operations.
    """
    def __init__(self, db_path="data/network.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS corrupted_nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setup TEXT NOT NULL,
                    punchline TEXT NOT NULL,
                    threat_level TEXT DEFAULT 'NORMAL',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("SELECT COUNT(*) FROM corrupted_nodes")
            count = cursor.fetchone()[0]
            
            if count == 0:
                ruido = [
                    ("Port scan detected on external firewall", "Blocked by automated ruleset alpha."),
                    ("Unauthorized ping request dropped", "Echo reply suppressed by local ICE protocol."),
                    ("Routine memory defragmentation", "Sector 7G cleared of temporary cached files."),
                    ("User login attempt failed", "Invalid credentials provided for root terminal."),
                    ("Packet drop rate increased marginally", "Node 44 experiencing high latency.")
                ]
                
                for setup, punchline in ruido:
                    cursor.execute("""
                        INSERT INTO corrupted_nodes (setup, punchline, threat_level)
                        VALUES (?, ?, 'NORMAL')
                    """, (setup, punchline))

                cursor.execute("""
                    INSERT INTO corrupted_nodes (setup, punchline, threat_level)
                    VALUES (?, ?, 'CRITICAL')
                """, (
                    "SYSTEM_OVERRIDE_INITIATED_BY_ROGUE_AI_PROTOCOL_99_INITIALIZING_BLACK_ICE", 
                    "KERNEL_PANIC_FATAL_ERROR_0x000000_CORRUPTION_DETECTED_PLEASE_INITIATE_PURGE_SEQUENCE"
                ))
                
                cursor.execute("""
                    INSERT INTO corrupted_nodes (setup, punchline, threat_level)
                    VALUES (?, ?, 'NORMAL')
                """, ("System integrity check initiated", "All core services operating within normal parameters."))

            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(f"[bold #ff0055][CRITICAL DB ERROR]: {e}[/]")

    def fetch_malware_packet(self):
        url = "https://official-joke-api.appspot.com/random_joke"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                setup = data.get("setup", "")
                punchline = data.get("punchline", "")
                
                total_length = len(setup) + len(punchline)
                threat_level = "CRITICAL" if total_length > 150 else "NORMAL"

                con = sqlite3.connect(self.db_path)
                cursor = con.cursor()
                cursor.execute("""
                    INSERT INTO corrupted_nodes (setup, punchline, threat_level)
                    VALUES (?, ?, ?)
                """, (setup, punchline, threat_level))
                con.commit()
                con.close()
                return True
        except Exception:
            pass
        return False

    def _daemon_loop(self):
        while True:
            self.fetch_malware_packet()
            time.sleep(60)

    def start_background_process(self):
        daemon_thread = threading.Thread(target=self._daemon_loop, daemon=True)
        daemon_thread.start()