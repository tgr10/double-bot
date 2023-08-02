import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests

QUANTIA = "2"
URL = "https://blaze.com/pt/games/double"

# Resto do código permanece igual...


class SeleniumScraper:

    def __init__(self, url, quantia):
        self.browser_lib = webdriver.Chrome()
        self.url = url
        self.quantia_value = quantia

    def digitar_lentamente(self, elemento, texto, intervalo=0.2):
        for letra in texto:
            elemento.send_keys(letra)
            time.sleep(intervalo)

    def inserir_quantia(self):
        time.sleep(10)
        label_xpath = "/html[1]/body[1]/div[1]/main[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/input[1]"
        quantia_input = self.browser_lib.find_element(By.XPATH, label_xpath)
        quantia_input.click()  # Clique no elemento para interagir com ele
        quantia_input.clear()
        self.digitar_lentamente(quantia_input, self.quantia_value)

    def login_to_blaze(self, login="", senha=""):
        isCaptcha = True
        self.browser_lib.get("https://blaze.com/pt/games/double")
        wait = WebDriverWait(self.browser_lib, 5)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='unauthed-buttons']//div[1]")
            )
        )
        self.browser_lib.find_element(By.XPATH, "//div[@class='unauthed-buttons']//div[1]").click()
        time.sleep(1)
        login_box = self.browser_lib.find_element(By.XPATH, "//input[@name='username']")
        self.digitar_lentamente(login_box, login)
        senha_box = self.browser_lib.find_element(By.XPATH, "(//input[@name='password'])[1]")
        self.digitar_lentamente(senha_box, senha)
        time.sleep(1)
        self.browser_lib.find_element(By.XPATH, "(//button[normalize-space()='Entrar'])[1]").click()
        while isCaptcha:
            a = input("Resolva o captcha e digite 1 quando estiver pronto: ")
            if a == "1":
                isCaptcha = False
            time.sleep(3)

    def click_botao_comecar_jogo(self):
        try:
             botao_comecar_jogo = self.browser_lib.find_element(By.XPATH, "/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[1]")
             botao_comecar_jogo.click()
        except NoSuchElementException:
             print("Botão 'Começar o jogo' não encontrado.")


    def goto_double_page(self):
        self.browser_lib.get(self.url)
        time.sleep(2)

    @staticmethod
    def get_current_time_hours():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    @staticmethod
    def today_date():
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        print(today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))
        return today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d")

    @staticmethod
    def estrategia(result_array):
        color_count = 0
        last = None
        for color in result_array:
            if last is None:
                last = color
            if color == last:
                color_count += 1
            else:
                return color_count
        return color_count

    def get_last_result_double(self):
        today, yesterday = self.today_date()
        cur_time = self.get_current_time_hours()
        results = []
        try:
            r = requests.get(
                f"https://blaze.com/api/roulette_games/history?startDate={yesterday}T{cur_time}.000Z&endDate={today}T{cur_time}.000Z&page=1"
            )
            data = json.loads(r.text)

            for i, v in enumerate(data["records"]):
                val = v["color"]
                if i < 5:
                    results.append(val)
            if self.estrategia(results) < 0:
                return True
            return False
        except ValueError as e:
            print(e)

    def make_bet(self):
        quantia_input = WebDriverWait(self.browser_lib, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='number']"))
        )
        quantia_input.clear()
        quantia_input.send_keys(str(self.quantia_value))

    def main(self):
        self.browser_lib.maximize_window()
        self.login_to_blaze("", "")
        self.goto_double_page()
        self.inserir_quantia()
        self.make_bet()

        # Aguardar alguns segundos antes de clicar em "Começar o jogo"
        time.sleep(15)

        # Clicar em "Começar o jogo"
        self.click_botao_comecar_jogo()

        # Aguardar alguns segundos antes de fechar o navegador
        time.sleep(5 * 60)

        # Fechar o navegador
        self.browser_lib.quit()


if __name__ == "__main__":
    obj = SeleniumScraper(
        url=URL,
        quantia=QUANTIA
    )
    obj.main()
