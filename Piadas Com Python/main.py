import sys
import time
import re
import sqlite3
import os
import json

# Importação dos nossos módulos personalizados
from modules.ia_sarcastica import AdversarioAI
from modules.motor_api import ColetorDePiadas

def barra_carregamento(mensagem="A processar", segundos=3):
    """
    Gera uma barra de loading animada no terminal.
    Usa sys.stdout e '\r' para reescrever a linha dinâmica.
    """
    tamanho_barra = 40
    print() 
    
    for i in range(tamanho_barra + 1):
        percentagem = int(100 * (i / tamanho_barra))
        preenchido = '█' * i
        vazio = '-' * (tamanho_barra - i)
        
        sys.stdout.write(f'\r[SYSTEM] {mensagem}... [{preenchido}{vazio}] {percentagem}%')
        sys.stdout.flush() 
        
        # Pausa dinâmica[cite: 1]
        time.sleep(segundos / tamanho_barra)
        
    print("\n")

def troll_language_selector():
    """
    Carrega o menu de idiomas a partir do JSON e obriga o utilizador a escolher Inglês.
    """
    ficheiro_menu = "data/menu_troll.json"
    
    # Verifica se o ficheiro existe antes de abrir[cite: 1]
    if not os.path.exists(ficheiro_menu):
        print(f"[SYSTEM FAILURE]: The file {ficheiro_menu} is missing.")
        return "en" 
        
    try:
        # Gestão de contexto para fecho seguro do ficheiro[cite: 1]
        with open(ficheiro_menu, "r", encoding="utf-8") as f:
            menu_data = json.load(f)
    except Exception as e:
        print(f"[SYSTEM FAILURE]: Could not load menu data. {e}")
        return "en"

    while True:
        print("\n" + "="*40)
        print("🌍 GLOBAL SETUP - SELECT YOUR LANGUAGE")
        print("="*40)
        
        for key, data in menu_data.items():
            print(f"{key}. {data['language']}")
            
        choice = input("\nEnter the number of your choice: ").strip()
        
        if choice in menu_data:
            selected_option = menu_data[choice]
            print(f"\n[SYSTEM]: {selected_option['response']}")
            time.sleep(1.5)
            
            if selected_option['is_valid']:
                return "en"
        else:
            print("\n[SYSTEM]: Invalid input. Are you just mashing the keyboard?")
            time.sleep(1.5)

def exportar_para_txt(db_path="data/piadas.db"):
    """
    Exporta o conteúdo da base de dados para um ficheiro de texto.
    """
    try:
        # Estabelecer ligação e criar cursor[cite: 1]
        con = sqlite3.connect(db_path)
        cursor = con.cursor()
        cursor.execute("SELECT setup, punchline, timestamp FROM piadas")
        piadas = cursor.fetchall()
        con.close()

        if not piadas:
            return False, "A base de dados ainda está vazia. A thread precisa de tempo!"

        # Escrita em ficheiro de texto[cite: 1]
        with open("data/exportacao_piadas.txt", "w", encoding="utf-8") as f:
            f.write("--- RELATÓRIO DE PIADAS (GERADO AUTOMATICAMENTE) ---\n\n")
            for setup, punchline, timestamp in piadas:
                f.write(f"[{timestamp}]\nQ: {setup}\nA: {punchline}\n")
                f.write("-" * 40 + "\n")
        
        return True, "Piadas exportadas com sucesso para 'data/exportacao_piadas.txt'."
    except Exception as e:
        return False, f"Erro ao exportar: {e}"

def menu_principal():
    """
    Loop central do programa que integra a Thread, a BD, a IA e o Regex.
    """
    # 1. O Menu Troll de arranque
    idioma = troll_language_selector()
    
    print("\n" + "="*50)
    print("🤖 SYSTEM BOOT SEQUENCE INITIATED")
    print("="*50)
    
    barra_carregamento("A estabelecer ligação com a API do Fred", 3)
    barra_carregamento("A carregar dicionário de insultos", 2)

    # 2. Inicializar Módulos
    ia = AdversarioAI()
    coletor = ColetorDePiadas()
    
    print("[SYSTEM]: A iniciar a thread de recolha em background (1 piada/minuto)...")
    # A thread arranca aqui, respeitando a regra principal do projeto[cite: 1]
    coletor.iniciar_recolha_background()
    time.sleep(2)

    # 3. Terminal Interativo (Loop)
    while True:
        print("\n" + "-"*40)
        print(" TERMINAL DE CONTROLO DE PIADAS ")
        print("-"*40)
        print("1. Consultar quantidade de piadas na Base de Dados")
        print("2. Procurar piadas por palavra-chave (Usa Regex!)")
        print("3. Exportar base de dados para TXT")
        print("4. Sair (Desistir)")
        
        escolha = input("\nEscolha a sua operação: ").strip()

        if escolha == "1":
            try:
                con = sqlite3.connect(coletor.db_path)
                cursor = con.cursor()
                cursor.execute("SELECT COUNT(*) FROM piadas")
                total = cursor.fetchone()[0]
                con.close()
                print(f"\n[INFO]: Temos atualmente {total} piadas guardadas no SQLite.")
                if total < 2:
                    print("[INFO]: Dê algum tempo à thread para trabalhar...")
            except sqlite3.Error as e:
                print(f"Erro ao ler a BD: {e}")

        elif escolha == "2":
            padrao = input("\nInsira o padrão Regex para procurar (ex: 'chicken|dog'): ").strip()
            try:
                # Validação de sintaxe da expressão regular
                re.compile(padrao) 
                
                con = sqlite3.connect(coletor.db_path)
                cursor = con.cursor()
                cursor.execute("SELECT setup, punchline FROM piadas")
                todas_piadas = cursor.fetchall()
                con.close()

                encontradas = 0
                print("\n--- RESULTADOS DA PESQUISA ---")
                for setup, punchline in todas_piadas:
                    texto_completo = f"{setup} {punchline}"
                    # Pesquisa flexível de padrões com ignore case[cite: 1]
                    if re.search(padrao, texto_completo, re.IGNORECASE):
                        print(f"-> {setup} | {punchline}")
                        encontradas += 1
                
                if encontradas == 0:
                    print("Nenhuma piada corresponde ao teu padrão brilhante.")
                    ia.reagir_erro()
                else:
                    ia.reagir_sucesso()

            except re.error:
                print("\n[ERRO]: Expressão Regular inválida!")
                ia.reagir_erro()

        elif escolha == "3":
            print("\n[SYSTEM]: A preparar ficheiro. Isto seria mais rápido se o teu disco não fosse uma batata.")
            barra_carregamento("A exportar dados do SQLite para TXT", 4)
            sucesso, mensagem = exportar_para_txt(coletor.db_path)
            
            print(f"\n[SISTEMA]: {mensagem}")
            if sucesso:
                ia.reagir_sucesso()
            else:
                ia.reagir_erro()

        elif escolha == "4":
            print("\n[SYSTEM]: A encerrar terminal. A thread de background será morta.")
            time.sleep(1)
            break

        else:
            print("\n[ERRO]: Opção inválida.")
            ia.reagir_erro()

if __name__ == "__main__":
    menu_principal()