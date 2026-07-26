# ⚡ NEON INQUISITOR: UPLINK TERMINAL ⚡
**Game Design Document (GDD) & Technical Manual**

---

## 📖 1. Lore & Contexto Narrativo
O ano é 2077. O sistema central da corporação foi infetado por uma **Rogue AI** (Inteligência Artificial Rebelde). Para evitar ser detetada, a IA camufla os seus Rootkits destrutivos injetando-os no meio de pacotes de dados inúteis (uma API externa que gera piadas secas em *background*).

O jogador assume o papel de um **Netrunner** (Hacker de Elite) encarregue de aceder ao terminal via linha de comandos, monitorizar a rede, contornar a segurança (*Black ICE*) e usar engenharia reversa para destruir os vírus.

---

## 🔄 2. Core Gameplay Loop
A experiência de jogo foi desenhada à volta de um ciclo de "Risco e Resolução", dividido em 3 fases obrigatórias que se repetem:

1. **Reconhecimento (Scan & Analise):** 
   A Rogue AI envia dados constantemente em *background*. O jogador gera um radar visual (Gráfico Matplotlib) para analisar os pacotes da base de dados. O objetivo é identificar qual o `Node ID` que tem um Payload Crítico (o tamanho em bytes mais elevado).
   
2. **Infiltração (Kernel Bypass):** 
   Com o `Node ID` descoberto, o jogador injeta esse valor no sistema para forçar a paragem da firewall (*Black ICE*). Se errar, o sistema mantém-se bloqueado. Se acertar, ganha acesso à consola de Debug.

3. **Combate / Hacking (Regex Override):** 
   A fase final. O jogador intercepta o pacote de dados corrompido e depara-se com uma assinatura de Malware (`[MALWARE_SIG]`). O jogador deve associar visualmente essa anomalia ao padrão matemático de Expressões Regulares (Regex) correto para a purgar. Se falhar, é expulso do Kernel e a firewall volta a fechar-se.

---

## ⚔️ 3. Mecânicas de Combate (Guia de Regex)
O combate não é de "sorte", mas de dedução lógica. O jogador deve analisar a ameaça no texto e escolher o padrão correto de entre as opções dadas.

| Tipo de Anomalia | Ameaça Intercetada | Regex Correto | Lógica do Jogador |
| :--- | :--- | :--- | :--- |
| **Porta Ilegal** | `PORT:6666` | `PORT:\d{4}` | A sintaxe dita que começa por "PORT:" seguido de 4 números (`\d{4}`). |
| **Token Admin** | `UID_9999` | `UID_\d{4}` | Começa por "UID_" seguido de 4 números. |
| **Fuga de Memória** | `0xFA4B` | `0x[0-9A-F]{4}` | Hexadecimal: Começa por "0x" e contém 4 caracteres (letras A-F ou números). |
| **IP Falso** | `192.168.0.99` | `\d{1,3}\.\d{1,3}\...` | O único padrão que contém barras a escapar pontos literais (`\.`) para simular um IP. |

### 🚨 Risco vs. Recompensa: Honeypots (Armadilhas)
Para impedir que o jogador clique em opções aleatoriamente, existe uma probabilidade de **15%** de o nó ser um *Honeypot* (uma armadilha da IA). 
* **Como detetar:** Se a opção correta de Regex **não estiver na lista**, é uma armadilha!
* **Ação do Jogador:** O jogador deve usar a **Opção 5 (Cancel Session)**. Se o fizer com sucesso, recebe Loot bónus. Se tentar hackear um Honeypot, sofre um *System Crash* imediato.

---

## ⚙️ 4. Arquitetura Técnica e Instalação (Para Avaliação)

O jogo utiliza vários conceitos avançados de Engenharia de Software integrados:
* **Multithreading:** Um processo *Daemon* executa chamadas HTTP GET assíncronas a uma API REST de 60 em 60 segundos, injetando ruído e ameaças no SQLite sem interromper o input do jogador.
* **Programação Orientada a Objetos (POO):** Classes encapsuladas para a Base de Dados, Operador, e Scanner.
* **Data Science / Transformação:** Utilização do `pandas` e queries SQL com `UNION ALL` para baralhar ameaças reais com ruído e expô-las visualmente num gráfico de barras temático.

### 🚀 Como Executar o Jogo
*Recomenda-se a execução num terminal de sistema (CMD, PowerShell, Windows Terminal) para suporte total às cores Hexadecimais/TrueColor (ANSI).*

1. **Instalar dependências:**
   ```bash
   pip install rich pandas matplotlib requests