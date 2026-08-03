from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()

def print_header(title, border_color="bold #00f0ff"):
    """Desenha um painel geometrico estruturado para titulos de seccao."""
    panel = Panel(f"/// {title} ///", expand=False, border_style=border_color, padding=(0, 2))
    console.print(panel)

def print_success(message):
    """Apresenta uma mensagem de sucesso com fundo verde escuro de alto contraste."""
    console.print(f"\n[bold white on #004400] [ OK ] {message} [/]")

def print_error(message):
    """Apresenta um erro critico com fundo vermelho escuro de alto contraste."""
    console.print(f"\n[bold white on #550000] [ FATAL ] {message} [/]")

def print_warning(message):
    """Apresenta um aviso de sistema com fundo amarelo/dourado."""
    console.print(f"\n[bold black on #fdf500] [ WARNING ] {message} [/]")

# --- NOVAS FUNÇÕES DE ESTÉTICA CIBERNÉTICA ---

def print_system_breach(message):
    """Alerta maximo com ASCII e texto a piscar (blink) para ataques do FRED."""
    console.print(f"\n[blink bold #ff0055]>> ! <<[/] [bold white on #ff0055] BREACH DETECTED [/] [blink bold #ff0055]>> ! <<[/]")
    console.print(f"[bold #ff0055]{message}[/]")

def print_glitch_text(message):
    """Simula texto corrompido, cortado ou ficheiros danificados."""
    console.print(f"\n[bold dim white][strike]SYS_CORRUPTION[/strike][/] [italic #00f0ff]{message}[/]")

def print_scan_log(message):
    """Log de terminal puramente tecnico e processual."""
    console.print(f"\n[bold #00f0ff]|> NET_LOG_ENTRY:[/] [dim white]{message}[/]")

def print_rule(title=""):
    """Cria uma linha divisoria tipografica elegante com suporte a titulo opcional."""
    if title:
        console.print(Rule(f"[bold #00f0ff]{title}[/]", style="dim #00f0ff"))
    else:
        console.print(Rule(style="dim #00f0ff"))