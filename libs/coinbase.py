import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from . import utils


def scraping():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("user-agent=Chrome/80.0.3987.132")
    options.add_experimental_option("detach", False)

    navegador = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
    # navegador = webdriver.Chrome(options=options)
    navegador.get('https://www.coinbase.com/pt/explore')

    sleep(3)

    txt = ''
    # Analisa o conteúdo HTML da página usando BeautifulSoup
    soup = BeautifulSoup(navegador.page_source, 'html.parser')

    breakpoint_div1 = soup.find('div', {'data-testid': 'market-health'})
    breakpoint_div2 = breakpoint_div1.find(attrs={'role': 'region'})

    """
    Obter o Percentual
    """
    # Regex
    pattern_percentage = re.compile(r'styles__PercentageText-.+')
    element_percentage = breakpoint_div2.find('span', class_=pattern_percentage)
    text_percentage = element_percentage.get_text(strip=True)

    """
    Obter o Icone
    """
    # Encontrar todos os elementos span que tenham o atributo data-icon-name com valor "diagonalDownArrow" ou "diagonalUpArrow"
    icons = breakpoint_div2.find('span', attrs={'data-icon-name': ['diagonalDownArrow', 'diagonalUpArrow']})
    text_icon_name = icons.get('data-icon-name')

    value_percentage = ''

    if text_icon_name == 'diagonalDownArrow':
        value_percentage = '-'

    if text_percentage:
        format_text_percentage = text_percentage.replace(",", ".").replace("%", "")
        value_percentage += format_text_percentage

    print(f"CoinBase: Nas últimas 24 horas, o mercado está com o valor: {value_percentage}")

