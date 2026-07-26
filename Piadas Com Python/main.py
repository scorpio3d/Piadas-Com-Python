import sys
import json
import re
import sqlite3
import time
import random
from rich.console import Console

from modules.motor_api import ColetorDePiadas
from modules.personagem import Personagem
from modules.analise_dados import AnalisadorDeDados
from modules.ia_sarcastica import IASarcastica
from modules.utils import texto_animado, barra_carregamento, exibir_cabecalho

console = Console()
sistema_bloqueado = True

def menu_troll():
    """Protocolo de seleção de idioma do sistema."""
    exibir_cabecalho("PROTOCOLO DE LINGUAGEM DO SISTEMA", cor="bold yellow")
    try:
        with open("data/menu_troll.json", "r", encoding="utf-8") as f:
            opcoes_idioma = json.load(f)
    except Exception:
        console.print("[bold red][SISTEMA]: Erro ao carregar pacotes de linguagem. Continuando em Inglês.[/bold red]")
        return

    while True:
        console.print("\nSelecione o idioma da interface / Select interface language:")
        for key, val in opcoes_idioma.items():
            console.print(f"[cyan]{key}.[/cyan] {val['language']}")
        
        escolha = input("\n> Input: ").strip()
        if escolha in opcoes_idioma:
            resposta = opcoes_idioma[escolha]
            console.print(f"\n[yellow]{resposta['response']}[/yellow]")
            if resposta["is_valid"]:
                time.sleep(1)
                break
        else:
            console.print("\n[bold red][ERRO]: Syntax_Error. Opção não reconhecida![/bold red]")

def criar_personagem():
    """Registo do Operador no Sistema."""
    exibir_cabecalho("REGISTO DE OPERADOR", cor="bold cyan")
    console.print("Perfis de Operador Disponíveis:")
    console.print("1. [bold magenta]Netrunner[/bold magenta] (Infiltração de dados e bypass de firewalls)")
    console.print("2. [bold blue]Cyber-Enforcer[/bold blue] (Blindagem ICE contra erros críticos)")
    console.print("3. [bold red]Code-Breaker[/bold red] (Extração maximizada de pacotes de dados)")
    
    escolha = input("\nDefina o seu perfil (1-3): ").strip()
    jogador = Personagem(classe_id=escolha)
    console.print(f"\n✨ Perfil carregado: [bold green]{jogador.classe_nome}[/bold green]!")
    return jogador

def batalha_purificacao(jogador, motor, ia):
    """Mecânica de Múltipla Escolha com Honeypots (Armadilhas Black ICE - 15%)."""
    exibir_cabecalho("OVERRIDE DE SISTEMA", cor="bold red")

    eh_trap = random.random() < 0.15

    try:
        con = sqlite3.connect("data/piadas.db")
        cursor = con.cursor()

        cursor.execute("SELECT id, setup, punchline FROM piadas WHERE dificuldade = 'NORMAL' ORDER BY RANDOM() LIMIT 1")
        piada_certa = cursor.fetchone()

        if not piada_certa:
            console.print("\n[yellow][REDE]: Nenhum nó de dados infetado no momento. Aguarde o scan![/yellow]")
            con.close()
            return

        piada_id, setup, punchline_correta = piada_certa

        if eh_trap:
            cursor.execute("SELECT punchline FROM piadas WHERE id != ? ORDER BY RANDOM() LIMIT 4", (piada_id,))
            opcoes = [row[0] for row in cursor.fetchall()]
            con.close()

            opcoes_genericas = [
                "Error 404: Packet lost in transmission.",
                "SyntaxError: Invalid payload structure.",
                "NullPointer: Memory address restricted.",
                "Segmentation Fault: Triggered by Rogue AI."
            ]
            while len(opcoes) < 4:
                opcoes.append(opcoes_genericas.pop())

            random.shuffle(opcoes)
        else:
            cursor.execute("SELECT punchline FROM piadas WHERE id != ? ORDER BY RANDOM() LIMIT 3", (piada_id,))
            distratores = [row[0] for row in cursor.fetchall()]
            con.close()

            opcoes_genericas = [
                "Error 404: Packet not found.",
                "SyntaxError: invalid query syntax.",
                "NullPointerException on data stream."
            ]
            while len(distratores) < 3:
                distratores.append(opcoes_genericas.pop())

            opcoes = [punchline_correta] + distratores
            random.shuffle(opcoes)

    except Exception as e:
        console.print(f"[bold red][ERRO BASE DE DADOS]: {e}[/bold red]")
        return

    if eh_trap:
        console.print(f"\n👁️ [bold purple][HONEYPOT DETETADO - NÓ #{piada_id}]:[/bold purple] \"{setup}\"")
    else:
        console.print(f"\n[bold green][NÓ CORROMPIDO #{piada_id}]:[/bold green] \"{setup}\"")

    console.print("\nQual é a chave de desencriptação correta para limpar o Malware?")
    for idx, opcao in enumerate(opcoes, 1):
        console.print(f"  [cyan]{idx}.[/cyan] {opcao}")
    
    console.print("  [bold yellow]5. ⚠️ CANCELAR SESSÃO! (É uma armadilha Black ICE!)[/bold yellow]")

    if jogador.passiva == "clarividencia" and jogador.combo > 0:
        if eh_trap:
            console.print("\n🔮 [bold magenta][SCAN DO NETRUNNER]: Os pacotes de dados estão mascarados... Isto é uma Armadilha![/bold magenta]")
        else:
            dica = punchline_correta[:4]
            console.print(f"\n🔮 [bold magenta][SCAN DO NETRUNNER]: A chave começa com os bytes: '{dica}...'[/bold magenta]")

    escolha = input("\nInjetar comando (1-5): ").strip()

    if escolha not in ["1", "2", "3", "4", "5"]:
        console.print("\n[bold red]❌ Syntax Error! Injeção falhou.[/bold red]")
        return

    if escolha == "5":
        if eh_trap:
            jogador.combo += 2
            motor.aumentar_taxa(2)
            barra_carregamento("A contornar Black ICE", passos=12)
            console.print("\n✨ [bold green]CRÍTICO! Bypass efetuado com sucesso à armadilha da Rogue AI.[/bold green]")
            console.print(f"[bold red]{ia.reagir_sucesso()}[/bold red]")

            loot = jogador.ganhar_loot()
            if loot:
                console.print(f"🎁 [bold gold1]DADOS EXTRAÍDOS: Obtiveste [{loot['nome']}]! Guardado no SQLite.[/bold gold1]")
        else:
            jogador.combo = 0
            motor.penalizar_taxa(1)
            console.print("\n❌ [bold red]PARANOIA DE SISTEMA! O Nó era legítimo e cortaste a ligação à toa.[/bold red]")
            console.print(f"[bold red]{ia.reagir_falha()}[/bold red]")

    else:
        if eh_trap:
            jogador.combo = 0
            motor.penalizar_taxa(1)
            console.print("\n❌ [bold red]SISTEMA COMPROMETIDO! Caíste num Honeypot e ativaste o Black ICE da Rogue AI![/bold red]")
            console.print(f"[bold red]{ia.reagir_falha()}[/bold red]")
        else:
            opcao_escolhida = opcoes[int(escolha) - 1]
            pattern = re.escape(punchline_correta)

            if re.search(pattern, opcao_escolhida, re.IGNORECASE):
                jogador.combo += 1
                motor.aumentar_taxa(1)
                barra_carregamento("A compilar chave de desencriptação", passos=10)
                console.print("\n✨ [bold green]OVERRIDE SUCESSO! Nó de dados purgado do Malware![/bold green]")
                console.print(f"[bold green]{ia.reagir_sucesso()}[/bold green]")

                if jogador.passiva == "critico":
                    jogador.combo += 1

                loot = jogador.ganhar_loot()
                if loot:
                    console.print(f"🎁 [bold yellow]DADOS EXTRAÍDOS: Obtiveste [{loot['nome']}]! Guardado no SQLite.[/bold yellow]")
            else:
                if jogador.passiva == "escudo" and input("\n🛡️ Ativar Blindagem ICE para absorver o feedback negativo? (s/n): ").lower() == 's':
                    console.print("\n[bold blue][CYBER-ENFORCER]: Sobrecarga bloqueada! Ligação mantida.[/bold blue]")
                else:
                    jogador.combo = 0
                    motor.penalizar_taxa(1)
                    console.print(f"\n❌ [bold red]FALHA DE INJEÇÃO! A chave correta era: '{punchline_correta}'[/bold red]")
                    console.print(f"[bold red]{ia.reagir_falha()}[/bold red]")

def gerir_inventario(jogador):
    """Menu de gestão do inventário/drive local."""
    exibir_cabecalho("DRIVE LOCAL DO OPERADOR (SQLITE CRUD)", cor="bold green")
    itens = jogador.ver_inventario()
    
    if not itens:
        console.print("\n[yellow]A tua drive local está vazia. Infiltra-te em nós para extrair scripts.[/yellow]")
        return

    console.print("\nScripts e Fragmentos Guardados:")
    for item in itens:
        item_id, nome, desc, buff, debuff, qtd = item
        console.print(f"[bold cyan]ID #{item_id}[/bold cyan] | [bold white]{nome}[/bold white] (x{qtd}) - {desc}")
        console.print(f"   🟢 Overclock: {buff} | 🔴 Memory Leak: {debuff}")

    op = input("\nIntroduz o ID do script a executar (ou ENTER para sair): ").strip()
    if op.isdigit():
        if jogador.consumir_item(int(op)):
            console.print("\n🧪 [bold green]Script executado e apagado da base de dados![/bold green]")
        else:
            console.print("\n❌ [bold red]Endereço de memória não encontrado.[/bold red]")

def main():
    global sistema_bloqueado
    
    menu_troll()
    jogador = criar_personagem()
    motor = ColetorDePiadas()
    analisador = AnalisadorDeDados()
    ia = IASarcastica()
    
    motor.iniciar_recolha_background()
    console.print("\n[bold magenta][ALERTA]: O Processo Fantasma da Rogue AI infiltrou-se no Background![/bold magenta]")
    
    while True:
        status_sis = "[bold red]🔴 FIREWALL ATIVA (Acesso Negado)[/bold red]" if sistema_bloqueado else "[bold green]🟢 ROOT ACCESS CONCEDIDO[/bold green]"
        
        exibir_cabecalho("TERMINAL CYBER-DECK UPLINK", cor="bold yellow")
        console.print(f"👨‍💻 [bold cyan]Operador:[/bold cyan] {jogador.classe_nome} | ⚡ [bold yellow]Sync-Combo:[/bold yellow] {jogador.combo} | 🛡️ [bold white]Segurança:[/bold white] {status_sis}")
        console.print("[dim]" + "-" * 60 + "[/dim]")
        
        console.print("1. 🔓 Scan de Rede (Gerar Radar Pandas de Anomalias)")
        console.print("2. 🔑 Bypass de Kernel (Inserir ID da Anomalia Crítica)")
        console.print("3. ⚔️ Debug de Nó Corrompido (Batalha Regex)")
        console.print("4. 💾 Drive Local & Scripts (Consultar Banco de Dados)")
        console.print("5. 🚪 Desconectar da Matrix (Sair)")
        
        opcao = input("\nInput do Operador: ").strip()
        
        if opcao == "1":
            analisador.gerar_relatorio_grafico("anomaly_map.png")
        
        elif opcao == "2":
            id_input = input("\nIntroduza o Root ID da anomalia crítica: ").strip()
            if analisador.destruir_covil_anomalia(id_input):
                sistema_bloqueado = False
        
        elif opcao == "3":
            if sistema_bloqueado:
                console.print("\n⛔ [bold red]ACESSO NEGADO! O ICE da Rogue AI está ativo. Corra o Scan (1) e faça Bypass ao Kernel (2) primeiro![/bold red]")
            else:
                batalha_purificacao(jogador, motor, ia)
        
        elif opcao == "4":
            gerir_inventario(jogador)
        
        elif opcao == "5":
            texto_animado("\nA apagar rastos de IP e a desconectar da Matrix... A rede continua corrompida!", velocidade=0.01, cor="bold red")
            sys.exit(0)
            
        else:
            console.print("\n[bold red]Syntax Error! Input inválido.[/bold red]")
        
        input("\nPressione ENTER para nova *query*...")

if __name__ == "__main__":
    main()