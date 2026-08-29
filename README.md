# 🚦 Análise de Tráfego com IA — Gêmeo Digital - Mobilidade Inteligente

> **Projeto desenvolvido para a Softex**  
> Integração de simulação de tráfego (SUMO) com Inteligência Artificial (Gemma 2) para detecção e recomendação de melhorias em gargalos viários na cidade de Sorocaba/SP.

---

## 📌 Sobre o Projeto

Este projeto simula o tráfego da cidade de **Sorocaba/SP** utilizando o **SUMO** (Simulation of Urban MObility) e aplica **Inteligência Artificial** (Gemma 2) para identificar gargalos e sugerir ações práticas para melhorar a fluidez do trânsito.

O sistema demonstra a **base de um Gêmeo Digital da Mobilidade**, onde dados de tráfego são analisados em tempo real para gerar recomendações automáticas para a gestão pública.

---

## 🎯 Objetivos

- ✅ Simular o tráfego da cidade de Sorocaba com base em dados reais de rotas e fluxos veiculares
- ✅ Detectar gargalos em tempo real durante a simulação
- ✅ Utilizar IA (Gemma 2) para analisar os gargalos e gerar recomendações práticas
- ✅ Integrar SUMO, Python e IA em um único fluxo de trabalho
- ✅ Demonstrar o potencial de um Gêmeo Digital para mobilidade urbana

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| [SUMO](https://sumo.dlr.de/) | Simulador de tráfego urbano — cria a malha viária, rotas e fluxos de veículos |
| [TraCI](https://sumo.dlr.de/docs/TraCI.html) | Interface Python para controle e leitura de dados do SUMO em tempo real |
| [Asyncio](https://docs.python.org/3/library/asyncio.html) | Biblioteca para comunicação assíncrona entre sistemas |
| [MAVSDK](https://mavsdk.mavlink.io/) | SDK para controle de drones (planejado para integração futura com drone 5G) |
| [Ollama](https://ollama.com/) | Plataforma para execução de modelos de IA localmente |
| [Gemma 2 (2B)](https://ai.google.dev/gemma) | Modelo de linguagem da Google — análise e recomendação de ações |
| Python 3.11 | Linguagem principal para integração entre SUMO e IA |
| Git/GitHub | Versionamento e entrega do código |

---

## 🗺️ O Mapa de Sorocaba

O mapa de Sorocaba utilizado neste projeto foi construído a partir de dados viários reais da cidade. Ele contém:

| Elemento | Descrição |
|----------|-----------|
| **Ruas e Avenidas** | Malha viária completa da cidade |
| **Cruzamentos** | Interseções com semáforos e prioridades |
| **Semáforos** | Ciclos programados para controle de fluxo |
| **Zonas de Origem-Destino** | Áreas mapeadas para análise de fluxo |
| **Corredores Críticos** | Principais rotas de deslocamento (ex: Zona Norte → Centro) |

---

## 📂 Estrutura do Projeto
Projeto-da-Softex/

│
├── 📁 Dados de Simulação (SUMO)

│ ├── cidade.net.xml # Mapa viário de Sorocaba (ruas, cruzamentos, semáforos)

│ ├── cidade.rou.xml # Rotas de veículos (origem, destino, horários) 

│ ├── cidade.rou.alt.xml # Rotas alternativas para variações de fluxo 

│ ├── trips.trips.xml # Viagens individuais (origem-destino) 

│ └── osm.sumocfg # Arquivo de configuração do SUMO

│
├── 📁 Código Fonte

│ ├── main.py # Código base do projeto (SUMO + integração inicial)

│ ├── assistente_trafego.py # Integração com IA — detecta gargalos e chama o Gemma 2

│ └── detector_gargalos.py # Módulo para detecção de gargalos em tempo real

│
└── 📄 README.md # Este arquivo


---

## 🚀 Como Executar o Projeto

### Pré-requisitos

| Requisito | Versão | Status |
|-----------|--------|--------|
| Windows 10/11 ou Linux | — | ✅ |
| Python | 3.11 ou superior | ✅ |
| SUMO | 1.27.1 ou superior | ✅ |
| Ollama | Última versão | ✅ |
| Modelo Gemma 2 | 2B (leve, ~1.6 GB) | ✅ |

### Passo a passo

#### 1. Clone o repositório

git clone https://github.com/Polyalves2/Projeto-da-Softex.git
cd Projeto-da-Softex
2. Instale o Ollama e o modelo Gemma 2

## Baixe o Ollama em https://ollama.com  use o comando no Linux
ollama pull gemma2:2b
3. Instale as dependências Python

pip install ollama traci
4. Execute a simulação do SUMO

sumo-gui -c osm.sumocfg
A janela do SUMO vai abrir com o mapa de Sorocaba

Clique no botão Play (▶️) para iniciar a simulação

Deixe a simulação rodando em segundo plano

5. Em outro terminal, execute o assistente com IA

python assistente_trafego.py
O terminal vai mostrar a detecção de gargalos em tempo real

**A IA (Gemma 2) vai gerar recomendações automáticas**

*Como Funciona a Integração SUMO + IA*
Arquitetura do Sistema
O fluxo de trabalho é dividido em etapas que conectam todas as tecnologias:

    A[SUMO<br>Simulação de Sorocaba] --> B[TraCI<br>Leitura de dados em tempo real]
    B --> C[Python<br>Detecção de gargalos]
    C --> D[Asyncio<br>Comunicação assíncrona]
    D --> E[Gemma 2<br>Análise e recomendação]
    E --> F[Terminal<br>Exibição da recomendação]
    
    G[MAVSDK<br>Drone 5G - Futuro] -.-> A
    
**Explicação detalhada:**

Etapa	Tecnologia	O que acontece
1. Simulação	SUMO	O SUMO roda o mapa de Sorocaba com veículos em movimento
2. Monitoramento	TraCI	O script Python lê dados em tempo real: posição, velocidade, filas
3. Comunicação	Asyncio	Gerencia a troca de dados entre SUMO, Python e IA de forma eficiente
4. Detecção	Python	Quando há mais de 10 veículos parados, um gargalo é detectado
5. IA acionada	Ollama + Gemma 2	O modelo recebe os dados do gargalo (local, veículos parados, tempo)
6. Recomendação	Gemma 2	A IA gera uma sugestão prática para melhorar o fluxo
7. Futuro	MAVSDK	Conexão com drone 5G para coleta de dados aéreos
   
   **O que a IA Analisa**
   
Dado	Como é obtido	Para que serve
Origem do gargalo	Localização dos veículos parados	Identificar onde o problema começa
Destino do gargalo	Rota dos veículos	Identificar para onde o fluxo está indo
Número de veículos parados	Contagem de veículos com velocidade < 0.1 m/s	Medir a severidade do gargalo
Tempo de espera	Tempo médio de parada	Calcular o impacto no tráfego
Recomendações Geradas

A IA é capaz de sugerir:

✅ Aumento do tempo de verde em semáforos específicos

✅ Criação de lanes dedicadas para determinadas rotas

✅ Sinalização de trânsito para melhor organização do fluxo

✅ Redução do tempo de espera estimado

✅ Monitoramento contínuo para ajustes dinâmicos

📈 Impacto esperado

Indicador	Resultado Esperado
Redução de atrasos semafóricos	15-20%
Economia anual (combustível + horas extras)	R$ 240 mil
Redução de reclamações	30% no primeiro ano
Redução de emissão de CO₂	Significativa

📚 Referências Técnicas

SUMO Documentation — Simulação de tráfego

TraCI Documentation — Interface Python para SUMO

Asyncio Documentation — Comunicação assíncrona

MAVSDK Documentation — SDK para controle de drones

Ollama Documentation — Execução de modelos de IA

Gemma 2 — Modelo de IA da Google

***Este projeto foi desenvolvido para fins educacionais como parte do programa da Softex.***



