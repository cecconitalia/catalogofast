import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fetch_caniev_results_manager():
    url = "https://www.snai.it/virtuali/ultimi-risultati/caniev"
    
    # Configuração das opções do Chrome
    chrome_options = Options()
    # Para depuração, comente a linha abaixo para visualizar o navegador
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--lang=it")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )
    
    # Cria o objeto Service com o caminho do ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        
        # Aguarda que a tabela com os resultados esteja presente (até 30 segundos)
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        
        # Tempo extra para que o conteúdo dinâmico seja renderizado
        time.sleep(5)
        
        # Extrai todas as linhas (<tr>) da tabela
        rows = table.find_elements(By.TAG_NAME, "tr")
        results = []
        
        for row in rows:
            # Extrai os textos das células (<td> ou <th>) da linha
            cells = row.find_elements(By.XPATH, ".//td|.//th")
            cell_texts = [cell.text.strip() for cell in cells if cell.text.strip()]
            if cell_texts:
                results.append(cell_texts)
            if len(results) >= 20:  # Limita aos 20 primeiros resultados
                break
        
        return results
        
    except Exception as e:
        print("Erro ao buscar os resultados:", e)
        return []
    
    finally:
        driver.quit()

if __name__ == "__main__":
    results = fetch_caniev_results_manager()
    if results:
        print("Últimas 20 partidas:")
        for idx, row in enumerate(results, start=1):
            print(f"{idx}: {' | '.join(row)}")
    else:
        print("Nenhum resultado encontrado ou ocorreu um erro.")
