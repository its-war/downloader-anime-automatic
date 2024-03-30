from selenium.webdriver.common.by import By
import time
import os


def search_anime(driver, text=False):
    if text:
        nome_anime = text
    else:
        nome_anime = input("Nome do anime: ")

    nome_anime.replace(" ", "+")

    driver.get(f'https://www.anitube.vip/busca.php?s={nome_anime}&submit=Buscar')

    time.sleep(1)

    resultados = driver.find_element(By.CLASS_NAME, "lista_de_animes")
    elementos_animes = resultados.find_elements(By.CLASS_NAME, 'ani_loop_item')

    animes = []

    for elemento in elementos_animes:
        elemento_nome = elemento.find_element(By.CLASS_NAME, 'ani_loop_item_infos_nome').text
        elemento_download = (elemento.find_element(By.CLASS_NAME, 'ani_loop_item_infos_down')
                             .get_attribute('href'))

        detalhes_anime = {
            'nome': elemento_nome,
            'download': elemento_download
        }

        animes.append(detalhes_anime)

    return animes


def get_episodios_list(driver, link_anime):
    driver.get(link_anime)
    conteudo_tabela = driver.find_element(By.TAG_NAME, 'tbody')
    linhas_tabela = conteudo_tabela.find_elements(By.TAG_NAME, 'tr')

    episodios = []

    for linha in linhas_tabela:
        tds = linha.find_elements(By.TAG_NAME, 'td')
        numero = tds[0].text.split(' ').pop()
        download_link_ep = tds[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
        ep = {
            'numero': int(numero) if numero.isdigit() else len(episodios) + 1,
            'link': download_link_ep
        }
        episodios.append(ep)

    return episodios


def download_video(driver, link_video):
    driver.get(link_video)
    time.sleep(2)
    form = driver.find_elements(By.TAG_NAME, 'form')[1]
    form.submit()
    time.sleep(2)

    download_btn = driver.find_element(By.CLASS_NAME, 'download')
    driver.get(download_btn.get_attribute('href'))
    # time.sleep(10)


def esperar_download_completo(driver, timeout=60):
    tempo_inicio = time.time()
    while any(filename.endswith('.crdownload') for filename in os.listdir(r'C:\Users\War\Downloads')):
        if time.time() - tempo_inicio > timeout:
            print('Aguardando download...')
        time.sleep(1)
    driver.quit()
