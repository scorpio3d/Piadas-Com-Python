import sqlite3
import pandas as pd
from rich.console import Console
from rich.table import Table
from modules.ui import print_header, print_success, print_error, print_warning

console = Console()

class DataScanner:
    """
    Handles network packet scanning and renders a terminal-native 
    anomaly radar directly in the CLI using Rich UI components.
    """
    def __init__(self, db_path="data/network.db"):
        self.db_path = db_path

    def generate_radar_scan(self):
        try:
            con = sqlite3.connect(self.db_path)
            
            # --- FAILSAFE DE EMERGENCIA ---
            con.execute("""
                CREATE TABLE IF NOT EXISTS noise_packets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setup TEXT NOT NULL
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS corrupted_nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setup TEXT NOT NULL,
                    punchline TEXT NOT NULL,
                    threat_level TEXT DEFAULT 'NORMAL',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            query = """
                SELECT id, setup, 'NORMAL' as type FROM corrupted_nodes
                UNION ALL
                SELECT id, setup, 'NOISE' as type FROM noise_packets
            """
            df = pd.read_sql(query, con)
            con.close()
            
            if df.empty:
                print_warning("Network radar empty. No packets intercepted yet.")
                return

            df['payload_size'] = df['setup'].apply(lambda x: len(str(x)) * 12)

            console.clear()
            print_header("FRED ANOMALY RADAR", "bold #00f0ff")
            console.print("[dim]Scanning network frequencies and FRED packet payloads...[/dim]\n")

            table = Table(show_header=True, header_style="bold #00ff00", border_style="dim #555555")
            table.add_column("Node ID", style="bold #00f0ff", justify="center")
            table.add_column("Type", justify="center")
            table.add_column("Payload Preview", style="dim white")
            table.add_column("Signal Density (Bytes)", justify="right")
            table.add_column("Threat Level Bar", style="bold #ff0055")

            max_size = df['payload_size'].max() if not df.empty else 1
            if max_size == 0:
                max_size = 1

            for _, row in df.iterrows():
                normalized_size = row['payload_size']
                bars_count = int((normalized_size / max_size) * 20)
                bars_count = max(1, bars_count)
                bar_graph = "#" * bars_count
                
                type_styled = "[bold #ff0055]NOISE[/]" if row['type'] == 'NOISE' else "[bold #00ff00]TARGET[/]"
                
                table.add_row(
                    str(row['id']),
                    type_styled,
                    str(row['setup'][:35]) + "...",
                    f"{row['payload_size']} B",
                    bar_graph
                )

            console.print(table)
            console.print("\n[bold #00ff00][*] Scan complete. Identify the critical payload Node ID for Kernel Bypass.[/]")

        except Exception as e:
            print_error(f"Radar scan failed: {e}")

    def bypass_kernel(self, target_id):
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            
            cursor.execute("SELECT id, setup FROM corrupted_nodes WHERE id = ?", (target_id,))
            node = cursor.fetchone()
            
            cursor.execute("SELECT id FROM noise_packets WHERE id = ?", (target_id,))
            noise = cursor.fetchone()
            con.close()
            
            if node:
                print_success(f"Node #{target_id} isolated. FRED Firewall bypassed successfully.")
                return True
            elif noise:
                print_error(f"Node #{target_id} is standard network noise. Security lock engaged.")
                return False
            else:
                print_error(f"Node ID #{target_id} not found in current sector.")
                return False
                
        except sqlite3.Error as e:
            print_error(f"Database query error: {e}")
            return False