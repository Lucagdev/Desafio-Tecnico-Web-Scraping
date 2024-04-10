# Web Scraping no Reclame Aqui com Python

 Este projeto é um exemplo de como podemos automatizar a coleta de informações de sites utilizando Python. Especificamente, focamos no site "Reclame Aqui", uma plataforma conhecida por reunir reclamações de consumidores sobre diversas empresas. O objetivo é extrair dados estatísticos de empresas do setor de moda, como notas e percentuais relacionados ao atendimento ao cliente.

## O que é Web Scraping?

 Web Scraping é a técnica de extrair informações de sites de forma automatizada. Imagine que você queira coletar informações específicas de um site, como preços de produtos, avaliações de serviços, ou, como neste projeto, estatísticas sobre empresas listadas no Reclame Aqui. Em vez de copiar e colar manualmente essas informações, o Web Scraping permite que você colete esses dados automaticamente, economizando tempo e esforço.

## Pré-requisitos

 Antes de começar, você precisará ter instalado em seu computador:

 - **Python 3:** A linguagem de programação usada para desenvolver o script.
 - **Selenium:** Uma ferramenta que permite interagir com páginas da web de forma automatizada.
 - **BeautifulSoup4:** Uma biblioteca para extrair dados de arquivos HTML e XML.
 - **Pandas:** Uma biblioteca de análise de dados que usaremos para organizar as informações coletadas em uma tabela e salvá-las em um arquivo Excel.
 - **WebDriver (ChromeDriver):** Uma ferramenta que permite ao Selenium controlar o navegador Chrome.

## Instalação

Para usar este script, siga os passos abaixo:

1. **Instalar o Python 3**

   Visite [https://www.python.org/downloads/](https://www.python.org/downloads/) para baixar e instalar o Python. Durante a instalação, certifique-se de marcar a opção para adicionar o Python ao PATH do seu sistema operacional.

2. **Instalar as bibliotecas necessárias**

   Abra o terminal ou prompt de comando e execute o seguinte comando para instalar Selenium, BeautifulSoup4 e Pandas:

 - pip install selenium beautifulsoup4 pandas


3. **Baixar o WebDriver**

 - Para o Chrome, visite [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads) para baixar a versão mais recente do ChromeDriver. Descompacte o arquivo baixado e anote o caminho onde você o salvou.

4. **Clonar o Repositório**

 Se você tem git instalado, você pode clonar o repositório do projeto usando o comando abaixo:

 - git clone https://github.com/Lucagdev/Desafio-Tecnico-Web-Scraping.git

 Caso contrário, você pode simplesmente baixar os arquivos do projeto como um arquivo ZIP e extrair para uma pasta em seu computador.

## Executando o Script

 - Navegue até a pasta do projeto no terminal ou prompt de comando.
 - Execute o script com o comando `python scraping.py`.
 - O script abrirá automaticamente o navegador, acessará o site Reclame Aqui, e começará a coletar os dados solicitados.

## Resultados

 Após a execução, você encontrará um arquivo Excel na pasta do projeto com as informações coletadas. Este arquivo contém os dados das empresas consultadas, incluindo a nota geral, percentuais de reclamações respondidas, índice de solução, e mais.

---

 Esperamos que este projeto ofereça uma introdução prática e útil ao poder do Web Scraping com Python!
