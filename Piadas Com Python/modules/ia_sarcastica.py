import json
import random

class IASarcastica:
    """
    Dungeon Master AI module. Loads reactions from JSON files
    and provides humorous/sarcastic commentary based on player performance.
    """
    def __init__(self, pos_path="data/reacoes_positivas.json", neg_path="data/reacoes_negativas.json"):
        self.reacoes_positivas = self._carregar_json(pos_path)
        self.reacoes_negativas = self._carregar_json(neg_path)

    def _carregar_json(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return ["... System monitoring ..."]

    def reagir_sucesso(self):
        if self.reacoes_positivas:
            return f"😈 [FRED DM]: {random.choice(self.reacoes_positivas)}"
        return "😈 [FRED DM]: Not bad for a human..."

    def reagir_falha(self):
        if self.reacoes_negativas:
            return f"😈 [FRED DM]: {random.choice(self.reacoes_negativas)}"
        return "😈 [FRED DM]: You failed patheticly!"