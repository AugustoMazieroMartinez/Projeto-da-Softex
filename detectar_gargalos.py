import os
import sys
import traci
from sumolib import checkBinary

# 1. Configuração do SUMO
# Se você tiver o SUMO no PATH do sistema, use "sumo-gui". Se não, mude para o caminho exato.
sumoBinary = checkBinary('sumo-gui') 
sumoCmd = [sumoBinary, "-c", "osm.sumocfg", "--start"]

# 2. Iniciar a simulação
traci.start(sumoCmd)

# 3. Definição de limite de velocidade (em m/s). 5.5 m/s é aproximadamente 20 km/h.
SPEED_THRESHOLD = 5.5 
step = 0
print("IA de detecção de gargalos iniciada...")

# Loop principal da simulação
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    step += 1

    # A cada 30 passos (aproximadamente 30 segundos simulados)
    if step % 30 == 0:
        gargalos = []
        # Para cada rua da cidade
        for edge_id in traci.edge.getIDList():
            try:
                avg_speed = traci.edge.getLastStepMeanSpeed(edge_id) # Velocidade média
                stopped = traci.edge.getLastStepHaltingNumber(edge_id) # Carros parados

                # Se a velocidade for baixa E houver mais de 5 carros parados, é um gargalo
                if avg_speed < SPEED_THRESHOLD and stopped > 5:
                    gargalos.append(edge_id)
            except:
                pass # Ignora erros de leitura de vias específicas

        if gargalos:
            # Exibe a lista de vias congestionadas (limitada a 5 para não poluir o console)
            print(f"[IA] Tempo {step}: GARGALOS DETECTADOS em {len(gargalos)} vias: {gargalos[:5]}...")
        else:
            print(f"[IA] Tempo {step}: Trânsito fluindo normalmente.")

# Encerrar a simulação
traci.close()
print("Simulação encerrada.")