import requests
from bs4 import BeautifulSoup

def obter_calendario_economico():
    url = "https://br.investing.com/economic-calendar"
    
    # O cabeçalho (User-Agent) é fundamental. Sem ele, o site bloqueia a requisição instantaneamente.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    print("Acessando o site do Investing.com...\n")

    try:
        response = requests.get(url, headers=headers)
        # Verifica se houve algum erro na requisição (como erro 403 ou 404)
        response.raise_for_status()

        # Analisa o HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Localiza a tabela do calendário econômico pelo seu ID
        tabela_calendario = soup.find("table", {"id": "economicCalendarData"})

        if tabela_calendario:
            # Encontra todas as linhas que representam eventos
            linhas = tabela_calendario.find_all("tr", class_="js-event-item")
            print(f"Sucesso! Encontrados {len(linhas)} eventos no calendário.\n")
            print("--- Últimos Eventos ---")

            # Itera sobre os primeiros 10 eventos encontrados
            for linha in linhas[:10]:
                # Extrai a hora, moeda e nome do evento, lidando com possíveis campos vazios
                td_hora = linha.find("td", class_="time")
                td_moeda = linha.find("td", class_="left flagCur")
                td_evento = linha.find("td", class_="left event")

                hora = td_hora.text.strip() if td_hora else "N/A"
                moeda = td_moeda.text.strip() if td_moeda else "N/A"
                evento = td_evento.text.strip() if td_evento else "N/A"

                print(f"[{hora}] {moeda} - {evento}")
        else:
            print("Tabela do calendário não encontrada.")
            print("O site pode ter alterado a estrutura HTML ou bloqueado a visualização da tabela para bots.")

    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP (possível bloqueio do Cloudflare): {errh}")
    except requests.exceptions.RequestException as e:
        print(f"Erro geral ao tentar conectar: {e}")

if __name__ == "__main__":
    obter_calendario_economico()
