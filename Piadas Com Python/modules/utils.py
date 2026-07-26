import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

# Objeto global para renderização com estilo no terminal
console = Console()

def texto_animado(texto, velocidade=0.02, cor="white"):
    """Escreve texto no terminal com estilo e cor usando o Rich."""
    console.print(f"[{cor}]{texto}[/{cor}]")

def barra_carregamento(descricao="A conjurar feitiço", passos=15, tempo=0.03):
    """Barra de progresso visual fluida e moderna."""
    for _ in track(range(passos), description=f"[bold magenta]{descricao}...[/bold magenta]"):
        time.sleep(tempo)

def exibir_cabecalho(titulo, cor="bold red"):
    """Cria um painel visual destacado para os menus e batalhas."""
    painel = Panel(
        f"🔥 {titulo.upper()} 🔥", 
        expand=False, 
        border_style=cor,
        padding=(0, 2)
    )
    console.print(painel)