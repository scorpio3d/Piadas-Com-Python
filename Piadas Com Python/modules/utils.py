import sys
import time

def texto_animado(texto, velocidade=0.02):
    """Prints text letter by letter for a RPG retro terminal feel."""
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(velocidade)
    print()

def barra_carregamento(descricao="Casting spell", passos=15, tempo=0.03):
    """Simulates a magic/loading progress bar."""
    print(f"\n{descricao}:")
    for i in range(passos + 1):
        percentual = (i / passos) * 100
        barra = "█" * i + "-" * (passos - i)
        sys.stdout.write(f"\r[{barra}] {percentual:.0f}%")
        sys.stdout.flush()
        time.sleep(tempo)
    print("\n")

def exibir_cabecalho(titulo):
    """Displays formatted ASCII headers."""
    print("=" * 60)
    print(f" 🔥 {titulo.upper()} 🔥".center(60))
    print("=" * 60)