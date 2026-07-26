import sqlite3
import requests
import threading
import time
from datetime import datetime

class ColetorDePiadas:
    """
    Motor encarregue de ligar à API, gerir a base de dados SQLite 
    e manter a Thread de infeção a correr em background.
    """
    def __init__(self, db_path="data/piadas.db"):
        self.db_path = db_path
        self.taxa_recolha = 1  # Quantidade de requisições por ciclo
        self.intervalo_segundos = 30  # Intervalo entre recolhas
        self._inicializar_bd()
        self._injetar_anomalia_inicial()

    def _inicializar_bd(self):
        """Cria a tabela 'piadas' caso ainda não exista no SQLite."""
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS piadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setup TEXT NOT NULL,
                    punchline TEXT NOT NULL,
                    dificuldade TEXT DEFAULT 'NORMAL',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(f"[ERRO CRÍTICO SQLITE]: Falha ao criar tabela de piadas: {e}")

    def _injetar_anomalia_inicial(self):
        """
        Injeta a anomalia do 'Covil da Entidade' com 500+ caracteres.
        Isto cria o pico gigante no gráfico do Pandas/Matplotlib!
        """
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            
            # Verifica se a anomalia já foi injetada anteriormente
            cursor.execute("SELECT COUNT(*) FROM piadas WHERE setup LIKE 'SYSTEM_CORRUPTION%'")
            if cursor.fetchone()[0] == 0:
                setup_corrompido = "SYSTEM_CORRUPTION_LAIR_FOUND: " + "X" * 300
                punchline_corrompida = "FATAL_ENTITY_CORE_OVERLOAD: " + "01" * 150
                
                cursor.execute("""
                    INSERT INTO piadas (setup, punchline, dificuldade)
                    VALUES (?, ?, 'BOSS')
                """, (setup_corrompido, punchline_corrompida))
                
                con.commit()
            con.close()
        except sqlite3.Error as e:
            print(f"[ERRO SQLITE]: Falha ao injetar anomalia inicial: {e}")

    def buscar_piada_api(self):
        """
        Conecta-se à API pública de piadas e guarda o resultado no SQLite.
        Classifica piadas curtas como 'NORMAL' e piadas longas (>50 chars) como 'BOSS'.
        """
        url = "https://official-joke-api.appspot.com/random_joke"
        try:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                dados = resposta.json()
                setup = dados.get("setup", "")
                punchline = dados.get("punchline", "")

                # Classificação automática baseada na complexidade
                dificuldade = "BOSS" if len(punchline) > 50 else "NORMAL"

                con = sqlite3.connect(self.db_path)
                cursor = con.cursor()
                cursor.execute("""
                    INSERT INTO piadas (setup, punchline, dificuldade)
                    VALUES (?, ?, ?)
                """, (setup, punchline, dificuldade))
                con.commit()
                con.close()
                return True
        except requests.RequestException:
            # Se a API falhar ou não houver internet, a thread ignora sem rebentar o programa
            pass
        except sqlite3.Error as e:
            print(f"[ERRO SQLITE]: Erro ao gravar piada da API: {e}")
        return False

    def _loop_recolha(self):
        """Ciclo infinito executado exclusivamente pela Thread em background."""
        while True:
            for _ in range(self.taxa_recolha):
                self.buscar_piada_api()
            time.sleep(self.intervalo_segundos)

    def iniciar_recolha_background(self):
        """Dispara a Thread em background (daemon=True garante que morre com a app)."""
        thread = threading.Thread(target=self._loop_recolha, daemon=True)
        thread.start()

    def aumentar_taxa(self, quantidade=1):
        """Aumenta a velocidade de recolha da API (Bónus de acerto)."""
        self.taxa_recolha += quantidade

    def penalizar_taxa(self, quantidade=1):
        """Reduz a velocidade de recolha da API (Penalização de erro)."""
        self.taxa_recolha = max(1, self.taxa_recolha - quantidade)