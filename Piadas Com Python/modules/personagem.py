import sqlite3
import json
import random

class Personagem:
    """
    Manages player character stats, classes, passive skills, 
    and inventory CRUD operations with SQLite.
    Game content is loaded dynamically from JSON files.
    """
    def __init__(self, classe_id="1", db_path="data/piadas.db"):
        self.db_path = db_path
        self.classes = self._carregar_json("data/classes.json")
        self.itens_disponiveis = self._carregar_json("data/itens.json")
        
        info_classe = self.classes.get(classe_id, self.classes.get("1", {}))
        self.classe_nome = info_classe.get("nome", "Unknown Class")
        self.passiva = info_classe.get("passiva", "none")
        self.combo = 0
        
        self._inicializar_tabela_inventario()

    def _carregar_json(self, caminho):
        """Helper method to load external configuration JSONs safely."""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[DATA ERROR]: Failed to load {caminho}: {e}")
            return {} if caminho.endswith("classes.json") else []

    def _inicializar_tabela_inventario(self):
        """Ensures the 'inventario' table exists in SQLite (Persistence)."""
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_item TEXT NOT NULL,
                    efeito TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    buff TEXT NOT NULL,
                    debuff TEXT NOT NULL,
                    quantidade INTEGER DEFAULT 1
                )
            """)
            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(f"[SQLITE ERROR]: Failed to create inventory table: {e}")

    def ganhar_loot(self):
        """Grants random item from loaded JSON data and updates SQLite (INSERT/UPDATE)."""
        if not self.itens_disponiveis:
            return None

        item = random.choice(self.itens_disponiveis)
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            
            cursor.execute("SELECT id, quantidade FROM inventario WHERE efeito = ?", (item["efeito"],))
            existente = cursor.fetchone()

            if existente:
                novo_qtd = existente[1] + 1
                cursor.execute("UPDATE inventario SET quantidade = ? WHERE id = ?", (novo_qtd, existente[0]))
            else:
                cursor.execute("""
                    INSERT INTO inventario (nome_item, efeito, descricao, buff, debuff, quantidade)
                    VALUES (?, ?, ?, ?, ?, 1)
                """, (item["nome"], item["efeito"], item["desc"], item["buff"], item["debuff"]))

            con.commit()
            con.close()
            return item
        except sqlite3.Error as e:
            print(f"[SQLITE ERROR]: Failed to save loot: {e}")
            return None

    def ver_inventario(self):
        """Reads stored inventory from SQLite (SELECT)."""
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute("SELECT id, nome_item, descricao, buff, debuff, quantidade FROM inventario")
            itens = cursor.fetchall()
            con.close()
            return itens
        except sqlite3.Error as e:
            print(f"[SQLITE ERROR]: Failed to read inventory: {e}")
            return []

    def consumir_item(self, item_id):
        """Consumes or reduces item count in SQLite (DELETE/UPDATE)."""
        try:
            con = sqlite3.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute("SELECT quantidade FROM inventario WHERE id = ?", (item_id,))
            resultado = cursor.fetchone()

            if resultado:
                qtd_atual = resultado[0]
                if qtd_atual > 1:
                    cursor.execute("UPDATE inventario SET quantidade = ? WHERE id = ?", (qtd_atual - 1, item_id))
                else:
                    cursor.execute("DELETE FROM inventario WHERE id = ?", (item_id,))
                con.commit()
                con.close()
                return True
            con.close()
            return False
        except sqlite3.Error as e:
            print(f"[SQLITE ERROR]: Failed to consume item: {e}")
            return False