import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

console = Console()

class AnalisadorDeDados:
    """Módulo responsável pela Análise de Dados (Pandas) e Relatórios Gráficos (Matplotlib + Rich)."""
    
    def __init__(self, db_path="data/piadas.db"):
        self.db_path = db_path

    def gerar_relatorio_grafico(self, output_path="anomaly_map.png"):
        """Gera o gráfico em PNG (Matplotlib) E imprime uma tabela visual no Terminal (Rich)."""
        try:
            con = sqlite3.connect(self.db_path)
            
            # Query Pandas: Seleciona as 10 maiores entradas
            query = """
                SELECT id, (LENGTH(setup) + LENGTH(punchline)) AS tamanho
                FROM piadas
                ORDER BY tamanho DESC
                LIMIT 10
            """
            df = pd.read_sql_query(query, con)
            con.close()

            if df.empty:
                console.print("[yellow][RADAR]: A base de dados ainda não tem dados suficientes.[/yellow]")
                return False

            # --- 1. GERAR FICHEIRO PNG COM MATPLOTLIB (Para a Nota Académica) ---
            df['id_label'] = "ID " + df['id'].astype(str)
            plt.figure(figsize=(10, 5))
            max_val = df['tamanho'].max()
            colors = ['#ff4d4d' if val == max_val else '#4da6ff' for val in df['tamanho']]

            bars = plt.bar(df['id_label'], df['tamanho'], color=colors, edgecolor='black')
            plt.title("RADAR DE ANOMALIAS (Matplotlib Export)", fontsize=12, fontweight='bold')
            plt.xlabel("ID do Registo")
            plt.ylabel("Tamanho (Chars)")
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tight_layout()
            plt.savefig(output_path, dpi=120)
            plt.close()

            # --- 2. DESENHAR TABELA COM BARRAS VISUAIS NO TERMINAL (Para UX) ---
            tabela = Table(title="📡 RADAR DE ANOMALIAS DO TERMINAL (TOP 10 REGISTOS)", border_style="cyan")
            tabela.add_column("ID", justify="center", style="bold yellow")
            tabela.add_column("Tamanho", justify="right", style="bold white")
            tabela.add_column("Visualizador de Código", style="magenta")
            tabela.add_column("Status", justify="center")

            # Fator de escala para a barra não quebrar o terminal
            fator_escala = 30 / max_val if max_val > 0 else 1

            for _, row in df.iterrows():
                id_val = f"#{row['id']}"
                tamanho = row['tamanho']
                num_blocos = int(tamanho * fator_escala)
                
                # Se for a anomalia (o maior valor)
                if tamanho == max_val and tamanho > 200:
                    barra_visual = "█" * max(num_blocos, 1)
                    status = "[bold red]🚨 ANOMALIA CRÍTICA[/bold red]"
                    estilo_barra = f"[bold red]{barra_visual}[/bold red]"
                else:
                    barra_visual = "■" * max(num_blocos, 1)
                    status = "[green]Normal[/green]"
                    estilo_barra = f"[cyan]{barra_visual}[/cyan]"

                tabela.add_row(id_val, f"{tamanho} chars", estilo_barra, status)

            console.print("\n")
            console.print(tabela)
            console.print(f"[dim]📁 [Ficheiro 'anomaly_map.png' gerado silenciosamente na raiz para avaliação][/dim]\n")
            return True

        except Exception as e:
            console.print(f"[bold red][ERRO ANALISE DADOS]: {e}[/bold red]")
            return False

    def destruir_covil_anomalia(self, id_anomalia):
        """Purga a anomalia identificada pelo jogador na base de dados SQLite."""
        if not str(id_anomalia).isdigit():
            console.print("\n❌ [bold red]ID inválido! Introduza apenas números.[/bold red]")
            return False

        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            
            cursor.execute("SELECT setup FROM piadas WHERE id = ?", (id_anomalia,))
            res = cursor.fetchone()

            if res and "SYSTEM_CORRUPTION" in res[0]:
                cursor.execute("DELETE FROM piadas WHERE id = ?", (id_anomalia,))
                con.commit()
                con.close()
                console.print(f"\n💥 [bold green][SUCESSO]: Covil da Entidade (ID #{id_anomalia}) purgado do SQLite![/bold green]")
                console.print("🟢 [bold green]SISTEMA DESBLOQUEADO! O acesso às Batalhas foi liberado.[/bold green]")
                return True
            else:
                con.close()
                console.print(f"\n❌ [bold red][FALHA]: O ID #{id_anomalia} não é o Covil do Boss! Analisa o radar novamente.[/bold red]")
                return False

        except sqlite3.Error as e:
            console.print(f"[bold red][ERRO SQLITE]: {e}[/bold red]")
            return False