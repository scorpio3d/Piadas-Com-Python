import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from rich import print

class DataScanner:
    """
    Data Analysis module utilizing Pandas and Matplotlib.
    Reads SQLite data, transforms it, and outputs a Cyberpunk anomaly radar.
    """
    
    def __init__(self, db_path="data/network.db"):
        self.db_path = db_path

    def generate_radar_scan(self, output_path="radar_scan.png"):
        if not os.path.exists(self.db_path):
            print("[bold #ff0055][SYSTEM FAULT] No network data found. Waiting for background thread...[/]")
            return False

        try:
            con = sqlite3.connect(self.db_path)
            
            query = """
                SELECT * FROM (
                    SELECT id, (LENGTH(setup) + LENGTH(punchline)) AS payload_size, threat_level
                    FROM corrupted_nodes
                    WHERE threat_level = 'CRITICAL'
                    ORDER BY RANDOM()
                    LIMIT 1
                )
                UNION ALL
                SELECT * FROM (
                    SELECT id, (LENGTH(setup) + LENGTH(punchline)) AS payload_size, threat_level
                    FROM corrupted_nodes
                    WHERE threat_level = 'NORMAL'
                    ORDER BY RANDOM()
                    LIMIT 6
                )
            """
            df = pd.read_sql_query(query, con)
            con.close()

            if df.empty:
                print("[bold #fdf500][*] Network is currently clean. Awaiting Rogue AI packets...[/]")
                return False

            df = df.sample(frac=1).reset_index(drop=True)
            df['node_label'] = "Node #" + df['id'].astype(str)
            
            plt.figure(figsize=(8, 4))
            colors = ['#ff0055' if threat == 'CRITICAL' else '#00f0ff' for threat in df['threat_level']]
            
            plt.bar(df['node_label'], df['payload_size'], color=colors, edgecolor='black')
            plt.title("NETWORK ANOMALY RADAR", fontsize=12, fontweight='bold', color='#00f0ff')
            plt.xlabel("Corrupted Nodes")
            plt.ylabel("Payload Size (Bytes)")
            
            plt.gca().set_facecolor('#121212')
            plt.gcf().patch.set_facecolor('#121212')
            plt.gca().tick_params(colors='white')
            plt.gca().spines['bottom'].set_color('white')
            plt.gca().spines['left'].set_color('white')
            plt.tight_layout()
            
            plt.savefig(output_path, dpi=120, facecolor=plt.gcf().get_facecolor())
            plt.close()

            print("\n[bold #00f0ff]📡 NETWORK SCAN COMPLETE...[/]")
            print(f"[dim]Visual telemetry saved locally as '{output_path}' for audit[/]\n")
            
            for _, row in df.iterrows():
                if row['payload_size'] > 150:
                    print(f"  [bold #ff0055]🚨 CRITICAL ROOTKIT DETECTED -> Node ID #{row['id']} ({row['payload_size']} bytes)[/]")
                else:
                    print(f"  [dim]✔️ Minor Malware -> Node ID #{row['id']} ({row['payload_size']} bytes)[/]")

            return True

        except Exception as e:
            print(f"[bold #ff0055][CRITICAL ERROR] Scanner malfunction: {e}[/]")
            return False

    def bypass_kernel(self, target_id):
        if not str(target_id).isdigit():
            print("\n[bold #ff0055]❌ Syntax Error! ID input must be numeric.[/]")
            return False

        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            
            cursor.execute("SELECT threat_level FROM corrupted_nodes WHERE id = ?", (target_id,))
            res = cursor.fetchone()

            if res and res[0] == "CRITICAL":
                cursor.execute("DELETE FROM corrupted_nodes WHERE id = ?", (target_id,))
                con.commit()
                con.close()
                print(f"\n💥 [bold #00ff00]OVERRIDE SUCCESS: Rootkit ID #{target_id} purged from SQLite![/]")
                print("🟢 [bold #00ff00]BLACK ICE OFFLINE! Access to Node Debugging (Option 3) granted.[/]")
                return True
            else:
                con.close()
                print(f"\n❌ [bold #ff0055]BYPASS FAILED: Node #{target_id} is not the Critical Rootkit. Run the scan again.[/]")
                return False

        except sqlite3.Error as e:
            print(f"[bold #ff0055][SQLITE ERROR]: {e}[/]")
            return False