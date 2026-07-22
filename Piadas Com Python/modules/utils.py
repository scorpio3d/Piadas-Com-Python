import sys
import time

def barra_carregamento(mensagem="A processar", segundos=3):
    """
    Gera uma barra de loading animada no terminal.
    Usa sys.stdout e '\r' para reescrever a linha dinâmica.
    """
    tamanho_barra = 40
    print() # Linha em branco para dar espaço
    
    for i in range(tamanho_barra + 1):
        # Calcula a percentagem
        percentagem = int(100 * (i / tamanho_barra))
        
        # Cria a barra visual (ex: ████████----------)
        preenchido = '█' * i
        vazio = '-' * (tamanho_barra - i)
        
        # \r volta ao início da linha sem saltar para a linha de baixo
        sys.stdout.write(f'\r[IA SARCÁSTICA] {mensagem}... [{preenchido}{vazio}] {percentagem}%')
        sys.stdout.flush() # Força a atualização do terminal
        
        # O tempo_sleep é dinâmico conforme o tempo total que queremos que demore
        time.sleep(segundos / tamanho_barra)
        
    print("\n") # Salta de linha quando termina