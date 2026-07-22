import threading
import time
import requests
import sqlite3
import os

class ColetorDePiadas:
    def __init__(self, db_path="data/piadas.db"):
        self.db_path = db_path
        self.url_api = "https://official-joke-api.appspot.com/random_joke"
        self._inicializar_base_dados()

    def _inicializar_base_dados(self):
        """
        Cria a base de dados SQLite e a tabela, caso não existam.
        Demonstra integração com bases de dados e criação de tabelas.
        """
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS piadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setup TEXT NOT NULL,
                    punchline TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(f"[SYSTEM FAILURE] Erro na base de dados: {e}")

    def _buscar_piada(self):
        """
        Função que será executada pela thread. 
        Busca a piada na API e guarda na base de dados a cada minuto.
        """
        while True:
            try:
                resposta = requests.get(self.url_api, timeout=10)
                if resposta.status_code == 200:
                    dados = resposta.json()
                    
                    # Guardar na base de dados (Evitando SQL Injection com parâmetros)
                    con = sqlite3.connect(self.db_path)
                    cursor = con.cursor()
                    cursor.execute(
                        "INSERT INTO piadas (setup, punchline) VALUES (?, ?)", 
                        (dados['setup'], dados['punchline'])
                    )
                    con.commit()
                    con.close()
                    
            except requests.exceptions.RequestException:
                pass # Em background, ignoramos falhas de rede para não quebrar a consola
            except sqlite3.Error:
                pass 
                
            # A regra de ouro do professor: esperar 1 minuto (60 segundos)
            time.sleep(60)

    def iniciar_recolha_background(self):
        """
        Inicia a thread (Multithreading para I/O-bound tasks).
        Configurada como daemon para morrer quando o programa principal fechar.
        """
        thread_api = threading.Thread(target=self._buscar_piada)
        thread_api.daemon = True
        thread_api.start()
        return thread_api