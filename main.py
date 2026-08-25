import asyncio
import traci
from mavsdk import System

SUMO_CMD = ["sumo-gui", "-c", "osm.sumocfg", "--start"]

drone_state = {
    "lat": 0.0,
    "lon": 0.0,
    "alt": 0.0,
    "is_connected": False,
    "home_alt_amsl": 0.0
}

async def atualizar_telemetria(drone):
    async for position in drone.telemetry.position():
        drone_state["lat"] = position.latitude_deg
        drone_state["lon"] = position.longitude_deg
        drone_state["alt"] = position.relative_altitude_m

def encontrar_ponto_mais_congestionado():
    """Analisa as vias do SUMO e retorna as coordenadas GPS do local mais crítico."""
    edges = traci.edge.getIDList()
    pior_via = None
    max_veiculos = -1

    for edge in edges:
        # Ignora vias internas de cruzamento
        if edge.startswith(":"):
            continue
        
        # Número de veículos ou nível de ocupação da via
        qtd_veiculos = traci.edge.getLastStepVehicleNumber(edge)
        if qtd_veiculos > max_veiculos and qtd_veiculos > 0:
            max_veiculos = qtd_veiculos
            pior_via = edge

    if pior_via:
        # Pega a posição cartesiana da via no SUMO
        # convert2D pega o início da via (pos = 0)
        x_sumo, y_sumo = traci.simulation.convert2D(pior_via, 0.0)
        
        # Converte para GPS (WGS84)
        target_lon, target_lat = traci.simulation.convertGeo(x_sumo, y_sumo, fromGeo=False)
        return target_lat, target_lon, pior_via, max_veiculos
    
    return None, None, None, 0

async def controlador_co_simulacao(drone):
    print("Iniciando SUMO...")
    traci.start(SUMO_CMD)
    print("-- SUMO pronto!")

    # Adiciona o ícone do Drone no SUMO
    try:
        traci.poi.add("drone_poi", 0.0, 0.0, (255, 0, 0, 255), "drone", 100, "", 3.0, 3.0, 0.0)
    except Exception:
        pass

    ultimo_despacho = 0

    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            tempo_atual = traci.simulation.getTime()

            # 1. Atualiza a posição visual do drone no SUMO baseado no Gazebo
            if drone_state["lat"] != 0.0 and drone_state["lon"] != 0.0:
                x_sumo, y_sumo = traci.simulation.convertGeo(drone_state["lon"], drone_state["lat"], fromGeo=True)
                try:
                    traci.poi.setPosition("drone_poi", x_sumo, y_sumo)
                except Exception:
                    pass

            # 2. A cada 30 segundos de simulação, verifica se há um novo congestionamento para o drone atender
            if tempo_atual - ultimo_despacho >= 30.0 and drone_state["home_alt_amsl"] > 0:
                lat_alvo, lon_alvo, via, num_carros = encontrar_ponto_mais_congestionado()
                
                if lat_alvo:
                    print(f"\n[ALERTA DE TRÁFEGO] Congestionamento na via '{via}' ({num_carros} veículos)!")
                    print(f"  -> Enviando drone no Gazebo para Lat: {lat_alvo:.5f}, Lon: {lon_alvo:.5f}")
                    
                    alt_voo_amsl = drone_state["home_alt_amsl"] + 30.0 # 30 metros de altura
                    await drone.action.goto_location(lat_alvo, lon_alvo, alt_voo_amsl, 0)
                    ultimo_despacho = tempo_atual

            await asyncio.sleep(0.05)
    finally:
        try:
            traci.close()
        except Exception:
            pass

async def missao_inicial_drone(drone):
    """Conecta, decola e estabiliza o drone no Gazebo."""
    print("Conectando ao PX4...")
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Drone conectado no Gazebo!")
            break

    print("-- Aguardando estimador EKF2 e GPS...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok and health.is_armable:
            print("-- Drone pronto para voar!")
            break
        await asyncio.sleep(1)

    async for home in drone.telemetry.home():
        drone_state["home_alt_amsl"] = home.absolute_altitude_m
        break

    print("-- Decolando para 20m no Gazebo...")
    await drone.action.set_takeoff_altitude(20.0)
    await drone.action.arm()
    await drone.action.takeoff()
    await asyncio.sleep(8)
    print("-- Drone pronto e aguardando missões de tráfego do SUMO!")

async def main():
    drone = System()
    asyncio.create_task(atualizar_telemetria(drone))
    
    # Prepara o drone no Gazebo primeiro
    await missao_inicial_drone(drone)
    
    # Inicia a coordenação em tempo real com o SUMO
    await controlador_co_simulacao(drone)

if __name__ == "__main__":
    asyncio.run(main())