import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

class AnalisadorDeDados:
    """
    Handles data analysis and visualization using Pandas and Matplotlib.
    Generates the Dark Energy Radar to locate system anomalies (Entity Lair).
    """
    def __init__(self, db_path="data/piadas.db"):
        self.db_path = db_path

    def gerar_relatorio_grafico(self, output_path="anomaly_map.png"):
        """
        Reads jokes from SQLite into a Pandas DataFrame, calculates corruption levels,
        and generates a Matplotlib bar chart highlighting the entity anomaly in red.
        """
        try:
            con = sqlite3.connect(self.db_path)
            query = "SELECT id, setup, punchline FROM piadas"
            df = pd.read_sql_query(query, con)
            con.close()

            if df.empty:
                print("[WARNING]: Database is empty. No graph generated.")
                return False

            # Calculate total character length as "Corruption Level"
            df['tamanho'] = df['setup'].str.len() + df['punchline'].str.len()

            # Set bar colors: Red for the anomaly (> 400 chars), Blue for normal jokes
            cores = ['#d9534f' if length > 400 else '#0275d8' for length in df['tamanho']]

            # Create plot
            plt.figure(figsize=(10, 6))
            bars = plt.bar(df['id'], df['tamanho'], color=cores, edgecolor='black', alpha=0.85)

            plt.title("⚡ DARK ENERGY RADAR - ENTITY CORRUPTION MAP ⚡", fontsize=13, fontweight='bold', pad=15)
            plt.xlabel("Soul ID (SQLite Row ID)", fontsize=11)
            plt.ylabel("Corruption Level (Character Length)", fontsize=11)
            plt.grid(axis='y', linestyle='--', alpha=0.5)

            # Save the chart as an image
            plt.tight_layout()
            plt.savefig(output_path, dpi=120)
            plt.close()

            print(f"\n[RADAR]: Scan complete! Map generated and saved as '{output_path}'.")
            return True

        except Exception as e:
            print(f"[ERROR]: Failed to generate visual report: {e}")
            return False

    def obter_id_anomalia(self):
        """
        Identifies the SQLite ID of the entity anomaly (character length > 400).
        """
        try:
            con = sqlite3.connect(self.db_path)
            query = "SELECT id, setup, punchline FROM piadas"
            df = pd.read_sql_query(query, con)
            con.close()

            if df.empty:
                return None

            df['tamanho'] = df['setup'].str.len() + df['punchline'].str.len()
            anomalia = df[df['tamanho'] > 400]

            if not anomalia.empty:
                return int(anomalia.iloc[0]['id'])
            return None

        except Exception as e:
            print(f"[ERROR]: Failed to locate anomaly ID: {e}")
            return None

    def destruir_covil_anomalia(self, id_palpite):
        """
        Validates player input. If correct, purges the anomaly record from SQLite
        and unlocks the main spellcasting terminal.
        """
        id_real = self.obter_id_anomalia()

        if id_real is None:
            print("[RADAR]: No active anomaly detected. System is already UNLOCKED!")
            return True

        try:
            if int(id_palpite) == id_real:
                con = sqlite3.connect(self.db_path)
                cursor = con.cursor()
                cursor.execute("DELETE FROM piadas WHERE id = ?", (id_real,))
                con.commit()
                con.close()
                print(f"\n✨ [SUCCESS]: Entity Lair at ID #{id_real} destroyed! System UNLOCKED!")
                return True
            else:
                print(f"\n❌ [FAIL]: Incorrect ID! The Entity shield deflected your spell.")
                return False
        except ValueError:
            print("\n❌ [ERROR]: Invalid input! Enter a numeric ID.")
            return False
        except sqlite3.Error as e:
            print(f"[SQLITE ERROR]: Failed to purge anomaly: {e}")
            return False