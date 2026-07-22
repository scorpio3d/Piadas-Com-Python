import json
import random
import os

class AdversarioAI:
    def __init__(self):
        self.patience = 100
        # Os caminhos agora apontam para a pasta 'data/'
        self.reacoes_positivas = self._carregar_ficheiro("data/reacoes_positivas.json")
        self.reacoes_negativas = self._carregar_ficheiro("data/reacoes_negativas.json")

    def _carregar_ficheiro(self, nome_ficheiro):
        # Verifica se o ficheiro existe antes de o manipular[cite: 1]
        if not os.path.exists(nome_ficheiro):
            return [f"[SYSTEM FAILURE]: The file {nome_ficheiro} is missing."]
            
        try:
            # Uso de gestão de contexto (with) para o ficheiro[cite: 1]
            with open(nome_ficheiro, "r", encoding="utf-8") as ficheiro:
                dados = json.load(ficheiro)
                return dados
        except Exception as e:
            return [f"Error reading script files: {e}"]

    def reagir_erro(self):
        self.patience += 10
        insulto = random.choice(self.reacoes_negativas)
        print(f"\n[SYSTEM]: {insulto}")

    def reagir_sucesso(self):
        self.patience -= 50
        frustracao = random.choice(self.reacoes_positivas)
        print(f"\n[SYSTEM]: {frustracao}")