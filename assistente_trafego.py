import ollama
import time

def detectar_gargalo_simulacao():
    # Simula a detecção de um gargalo
    # Em uma integração real, esses dados viriam do SUMO
    return {
        'origem': 'Zona Norte',
        'destino': 'Centro',
        'veiculos_parados': 25,
        'tempo_espera': 120
    }

def analisar_com_ia(dados):
    prompt = f"""
    Você é um especialista em tráfego da cidade de Sorocaba.
    Analise o seguinte gargalo:
    - Origem: {dados['origem']}
    - Destino: {dados['destino']}
    - Veículos parados: {dados['veiculos_parados']}
    - Tempo de espera médio: {dados['tempo_espera']} segundos

    Recomende uma ação específica para melhorar o fluxo.
    Seja direto e prático.
    """

    response = ollama.chat(model='gemma2:2b', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

if __name__ == '__main__':
    print("🤖 Assistente de Tráfego de Sorocaba com IA\n")
    print("Monitorando a simulação... (Pressione Ctrl+C para parar)\n")

    try:
        while True:
            # Detecta o gargalo
            dados_gargalo = detectar_gargalo_simulacao()

            # Mostra o gargalo
            print(f"🚨 GARGALO DETECTADO!")
            print(f"   {dados_gargalo['origem']} → {dados_gargalo['destino']}")
            print(f"   Veículos parados: {dados_gargalo['veiculos_parados']}")
            print(f"   Tempo de espera: {dados_gargalo['tempo_espera']}s")

            # Consulta a IA
            print("\n Consultando a IA...")
            recomendacao = analisar_com_ia(dados_gargalo)

            # Mostra a recomendação
            print(f"\n RECOMENDAÇÃO DA IA:\n{recomendacao}\n")
            print("-" * 50)

            # Aguarda 10 segundos
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n🛑 Assistente encerrado.")