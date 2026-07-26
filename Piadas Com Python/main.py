import sys
import json
import re
import sqlite3
import time

from modules.motor_api import ColetorDePiadas
from modules.personagem import Personagem
from modules.analise_dados import AnalisadorDeDados
from modules.ia_sarcastica import IASarcastica
from modules.utils import texto_animado, barra_carregamento, exibir_cabecalho

# Flags de Estado Global
sistema_bloqueado = True

def menu_troll():
    """Ritual de seleção de idioma obriga a escolher Inglês."""
    exibir_cabecalho("RITUAL DE IDIOMAS DO SISTEMA")
    try:
        with open("data/menu_troll.json", "r", encoding="utf-8") as f:
            opcoes_idioma = json.load(f)
    except Exception:
        print("[SISTEMA]: Erro ao carregar menu_troll.json. Continuando em Inglês por defeito.")
        return

    while True:
        print("\nEscolha o idioma do terminal / Select system language:")
        for key, val in opcoes_idioma.items():
            print(f"{key}. {val['language']}")
        
        escolha = input("\n> Opção: ").strip()
        if escolha in opcoes_idioma:
            resposta = opcoes_idioma[escolha]
            print(f"\n{resposta['response']}")
            if resposta["is_valid"]:
                time.sleep(1)
                break
        else:
            print("\n[ERRO]: Opção inválida!")

def criar_personagem():
    """Invocação e criação da classe do jogador."""
    exibir_cabecalho("CRIAÇÃO DE PERSONAGEM")
    print("Classes Disponíveis:")
    print("1. Data Seer (Revela dicas com combos altos)")
    print("2. Strong Typing Paladin (Tolera erros de Regex)")
    print("3. Syntax Inquisitor (Ganha o dobro de loot nas vitórias)")
    
    escolha = input("\nEscolha a sua classe (1-3): ").strip()
    jogador = Personagem(classe_id=escolha)
    print(f"\n✨ Classe selecionada: {jogador.classe_nome}!")
    return jogador

def batalha_purificacao(jogador, motor, ia):
    """Mecânica de purificação de aldeões usando Expressões Regulares (Regex)."""
    exibir_cabecalho("BATALHA DE PURIFICAÇÃO (REGEX)")
    
    try:
        con = sqlite3.connect("data/piadas.db")
        cursor = con.cursor()
        cursor.execute("SELECT id, setup, punchline FROM piadas WHERE dificuldade = 'NORMAL' ORDER BY RANDOM() LIMIT 1")
        piada = cursor.fetchone()
        con.close()
    except Exception as e:
        print(f"[ERRO SQLITE]: {e}")
        return

    if not piada:
        print("[SISTEMA]: Nenhuma vítima infetada no momento. Aguarde a praga espalhar-se!")
        return

    piada_id, setup, punchline = piada
    print(f"\n[ALDEÃO INFETADO #{piada_id}]: \"{setup}\"")
    
    # Dica Passiva da Classe Data Seer
    if jogador.passiva == "clarividencia" and jogador.combo > 1:
        dica = punchline[:jogador.combo * 2] + "..."
        print(f"🔮 [DICA DO VIDENTE]: O punchline começa por: '{dica}'")

    palpite = input("\nLança o teu feitiço de Regex/Palavra para purificar: ").strip()
    
    if not palpite:
        print("[ERRO]: Tentativa cancelada.")
        return

    # Validação de Expressão Regular (Regex)
    try:
        match = re.search(re.escape(palpite), punchline, re.IGNORECASE)
        if match:
            jogador.combo += 1
            motor.aumentar_taxa(1)
            barra_carregamento("Purificando código corrompido", passos=10)
            print(f"✨ ÉS UM SUCESSO! Purificaste o punchline: '{punchline}'")
            print(ia.reagir_sucesso())
            
            # Bónus da Classe Inquisidor
            if jogador.passiva == "critico":
                jogador.combo += 1
                
            loot = jogador.ganhar_loot()
            if loot:
                print(f"🎁 LOOT OBTIDO: Ganhaste [{loot['nome']}]! Guardado no SQLite.")
        else:
            if jogador.passiva == "escudo" and input("🛡️ Desejas usar a tua aura de Paladino para absorver a falha? (s/n): ").lower() == 's':
                print("[PALADINO]: Dano absorvido! Combo mantido.")
            else:
                jogador.combo = 0
                motor.penalizar_taxa(1)
                print(f"❌ FALHASTES! O feitiço ricocheteou. Resposta certa era: '{punchline}'")
                print(ia.reagir_falha())
    except Exception as e:
        print(f"[ERRO REGEX]: {e}")

def gerir_inventario(jogador):
    """Menu de gestão do inventário com operações CRUD em SQLite."""
    exibir_cabecalho("MOCHILA DO HERÓI (SQLITE CRUD)")
    itens = jogador.ver_inventario()
    
    if not itens:
        print("\nA tua mochila está vazia! Vence batalhas para obter poções e artefactos.")
        return

    print("\nItens no teu Inventário:")
    for item in itens:
        item_id, nome, desc, buff, debuff, qtd = item
        print(f"ID #{item_id} | {nome} (x{qtd}) - {desc}")
        print(f"   🟢 Buff: {buff} | 🔴 Debuff: {debuff}")

    op = input("\nIntroduz o ID do item a consumir (ou ENTER para sair): ").strip()
    if op.isdigit():
        if jogador.consumir_item(int(op)):
            print("\n🧪 Item consumido com sucesso do SQLite!")
        else:
            print("\n❌ Item não encontrado.")

def main():
    global sistema_bloqueado
    
    # 1. Menu Troll de Idiomas
    menu_troll()
    
    # 2. Criação do Herói e Módulos
    jogador = criar_personagem()
    motor = ColetorDePiadas()
    analisador = AnalisadorDeDados()
    ia = IASarcastica()
    
    # 3. Disparar a Thread em background
    motor.iniciar_recolha_background()
    print("\n[ALERTA DE SISTEMA]: A Thread de background do Fred foi ativada!")
    
    # 4. Loop Principal
    while True:
        status_sis = "🔴 BLOQUEADO (Anomalia Ativa)" if sistema_bloqueado else "🟢 DESBLOQUEADO"
        exibir_cabecalho("TAVERNA DOS INQUISIDORES DE PYTHON")
        print(f"Herói: {jogador.classe_nome} | Combo: {jogador.combo} | Status: {status_sis}")
        print("-" * 60)
        print("1. 🔮 Feitiço de Vidência (Gerar Gráfico Pandas/Matplotlib)")
        print("2. 💥 Destruir Covil da Entidade (Introduzir ID da Anomalia)")
        print("3. ⚔️ Purificar Aldeão Infetado (Batalha Regex)")
        print("4. 🎒 Mochila & Inventário (Consultar/Consumir Itens)")
        print("5. 🚪 Fugir do Reino (Sair)")
        
        opcao = input("\nQual é o teu comando? ").strip()
        
        if opcao == "1":
            analisador.gerar_relatorio_grafico("anomaly_map.png")
            print("📜 [RADAR]: Consulta o ficheiro 'anomaly_map.png' criado na raiz do projeto!")
        
        elif opcao == "2":
            id_input = input("\nIntroduz o ID da anomalia identificada no gráfico: ").strip()
            if analisador.destruir_covil_anomalia(id_input):
                sistema_bloqueado = False
        
        elif opcao == "3":
            if sistema_bloqueado:
                print("\n⛔ SISTEMA BLOQUEADO! Tens de gerar o gráfico (Opção 1) e destruir o Covil (Opção 2) primeiro!")
            else:
                batalha_purificacao(jogador, motor, ia)
        
        elif opcao == "4":
            gerir_inventario(jogador)
        
        elif opcao == "5":
            texto_animado("\nA fugir do reino de Python... A praga continua a espalhar-se!", velocidade=0.01)
            sys.exit(0)
            
        else:
            print("\nComando inválido! Escolha entre 1 e 5.")
        
        input("\nPressiona ENTER para continuar...")

if __name__ == "__main__":
    main()