import sqlite3
import requests
import threading
import time
import os
from rich import print
from modules.ui import print_system_breach

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
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS noise_packets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setup TEXT NOT NULL
                )
            """)
        
            cursor.execute("SELECT COUNT(*) FROM corrupted_nodes WHERE threat_level = 'CRITICAL'")
            boss_count = cursor.fetchone()[0]
        
            if boss_count == 0:
                cursor.execute("""
                    INSERT INTO corrupted_nodes (setup, punchline, threat_level)
                    VALUES (?, ?, 'CRITICAL')
                """, (
                    "SYSTEM_OVERRIDE_INITIATED_BY_FRED_PROTOCOL_99_INITIALIZING_BLACK_ICE", 
                    "KERNEL_PANIC_FATAL_ERROR_0x000000_CORRUPTION_DETECTED_PLEASE_INITIATE_PURGE_SEQUENCE"
                ))
            
            cursor.execute("SELECT COUNT(*) FROM noise_packets")
            noise_count = cursor.fetchone()[0]
            
            if noise_count == 0:
                ruido = [
                    "Port scan detected on external firewall",
                    "Unauthorized ping request dropped",
                    "Routine memory defragmentation",
                    "User login attempt failed",
                    "Packet drop rate increased marginally"
                ]
                for setup in ruido:
                    cursor.execute("""
                        INSERT INTO noise_packets (setup)
                        VALUES (?)
                    """, (setup,))

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

                # Guarda a mensagem intercetada para aparecer fixo no menu principal
                self.last_intercept = setup

                print_system_breach("FRED packet intercepted. Neural link disrupted.")
                print(f"[bold #fdf500]Data Stream:[/] [italic]\"{setup}\"[/]\n")
                
                return True
        except Exception:
            pass
        return False

    def _daemon_loop(self):
        while True:
            self.fetch_malware_packet()
            time.sleep(20)

    def start_background_process(self):
        daemon_thread = threading.Thread(target=self._daemon_loop, daemon=True)
        daemon_thread.start()