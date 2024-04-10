from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import re

# Classe para configurar o WebDriver, instala o ChromeDriver e inicializa o navegador com algumas configurações
class ConfiguracaoWebDriver:
    def __init__(self):
        self.servico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(service=self.servico)
        self._configurar_navegador()

    def _configurar_navegador(self):
        self.navegador.maximize_window()

    def obter_navegador(self):
       # Retorna a instância do navegador
        return self.navegador

class ScrapingReclameAqui:

    def __init__(self, navegador):
        self.navegador = navegador

    # Navega para a seção da página onde iremos interagir para coletar os dados
    def navegar_e_extrair(self, xpath_categoria, xpath_empresa):
        
        # Encontra a div de categorias/ranking
        div_categorias = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="homeRankings"]/div/astro-island/div')))

        # Desce a página até que o elemento esteja centralizado na tela
        self.navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", div_categorias)

        # Encontra o botão para selecionar a categoria E-commerce - Moda
        categoria_moda = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="homeRankings"]/div/astro-island/div/nav/div[2]/button[4]')))

        # Seleciona a categoria
        categoria_moda.click()

        # Navega até a categoria e seleciona a empresa
        WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_categoria))).click()
        WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_empresa))).click()

        # Aguarda o carregamento da página e extrai os dados
        return self._extrair_dados_empresa()
    
    #Função auxiliar para extrair as métricas específicas de cada elemento que desejamos 
    def _extrair_metricas(self, detalhes):
        metricas = {}
        for div in detalhes:
            texto = div.text.strip()
            if "Esta empresa recebeu" in texto:
                metricas['Total de Reclamações Recebidas'] = texto.split()[3]
            elif "Respondeu" in texto:
                metricas['Reclamações Respondidas'] = texto.split()[1]
            elif "aguardando resposta" in texto:
                metricas['Reclamações Aguardando Resposta'] = texto.split()[1]
            elif "avaliadas, e a nota média" in texto:
                # Extrai a nota como um inteiro e depois a transformamos em decimal para ficar no formato "0.00"
                nota_inteira = texto.split()[-1].replace(".", "")
                metricas['Nota do Consumidor'] = f"{nota_inteira[0]}.{nota_inteira[1:]}" if nota_inteira else "N/D"
            elif "voltariam a fazer negócio" in texto:
                metricas['Voltariam a Fazer Negócio (%)'] = texto.split()[3].rstrip('%')
            elif "A empresa resolveu" in texto:
                metricas['Índice de Solução (%)'] = texto.split()[3]
            elif "O tempo médio de resposta é" in texto:
                metricas['Tempo Médio de Resposta'] = " ".join(texto.split()[6:8]).replace(".", "")  

        return metricas

    # Extrai e retorna os dados da empresa da página atual
    def _extrair_dados_empresa(self):

        # Espera até que o elemento esteja visível antes de interagir com ele
        try:
            WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            print("Página carregada com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar a página: {e}")

        soup = BeautifulSoup(self.navegador.page_source, 'html.parser')

        #  Encontra todos os divs que contêm informações sobre a empresa
        detalhes = soup.find_all('div', class_='go4263471347')

        # Extrai a pontuação da empresa
        pontuacao = soup.find('b', class_='go3621686408').get_text(strip=True)

        # Cria um dicionário para armazenar as métricas
        metricas = self._extrair_metricas(detalhes)

        # Extrai o nome da empresa
        xpath_nome_empresa = '//*[@id="hero"]/div[2]/div/div[2]/div[1]/h1'
        nome_empresa = WebDriverWait(self.navegador, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_nome_empresa))).text

        #Define a estrutura dos dados
        dados_empresa = {
            "Empresa": nome_empresa,
            "Pontuação": pontuacao,
            "Total de Reclamações Recebidas": metricas.get('Total de Reclamações Recebidas', 'N/D'),
            "Reclamações Respondidas": metricas.get('Reclamações Respondidas', 'N/D'),
            "Reclamações Aguardando Resposta": metricas.get('Reclamações Aguardando Resposta', 'N/D'),
            "Nota do Consumidor": metricas.get('Nota do Consumidor', 'N/D'),
            "Voltariam a Fazer Negócio (%)": metricas.get('Voltariam a Fazer Negócio (%)', 'N/D'),
            "Índice de Solução (%)": metricas.get('Índice de Solução (%)', 'N/D'),
            "Tempo Médio de Resposta": metricas.get('Tempo Médio de Resposta', 'N/D')
        }

        # Retorna à página anterior
        self.navegador.back()

        # Aguarda um momento para carregar a pa´gina
        sleep(2)

        return dados_empresa

    #Método principal para executar o scraping e coletar os dados
    def executar(self):
        # Cria o espaço para os dados a serem coletados
        dados_coletados = []

        # Loop para iterar nos 3 primeiros elementos com tag <a e extrair dados das MELHORES Empresas
        for i in range(1, 4):
            xpath_categoria = '//*[@id="homeRankings"]/div/astro-island/div/div[3]/div/div[1]'
            xpath_empresa = f'(//*[@id="homeRankings"]/div/astro-island/div/div[3]/div/div[1]//a)[{i}]'
            dados_empresa = self.navegar_e_extrair(xpath_categoria, xpath_empresa)
            dados_coletados.append(dados_empresa)

        # Loop para iterar nos 3 primeiros elementos com tag <a e extrair dados das PIORES Empresas
        for i in range(1, 4):
            xpath_categoria = '//*[@id="homeRankings"]/div/astro-island/div/div[3]/div/div[2]'
            xpath_empresa = f'(//*[@id="homeRankings"]/div/astro-island/div/div[3]/div/div[2]//a)[{i}]'
            dados_empresa = self.navegar_e_extrair(xpath_categoria, xpath_empresa)
            dados_coletados.append(dados_empresa)

        # Cria um DataFrame no Pandas
        df = pd.DataFrame(dados_coletados)

        # Salva o DataFrame em um arquivo Excel
        df.to_excel("Dados Coletados Reclame Aqui.xlsx", index=False)

        # Exibe o DataFrame no terminal
        print(df)

# Execução principal
if __name__ == "__main__":
    # Configura o WebDriver
    configuracao_web_driver = ConfiguracaoWebDriver()
    navegador = configuracao_web_driver.obter_navegador()

    # Navega até a página inicial
    navegador.get('https://www.reclameaqui.com.br')

    # Cria a instância do scraping e executa
    scraping = ScrapingReclameAqui(navegador)
    scraping.executar()

    # Fecha o navegador
    navegador.quit()
