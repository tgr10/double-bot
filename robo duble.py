import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class SeleniumScraper:
    def __init__(self, url, quantia):
        self.browser_lib = webdriver.Chrome()
        self.url = url
        self.quantia = quantia

    def set_value_entry(self):
        value_field = WebDriverWait(self.browser_lib, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"input[type='number"))
        )
        value_field.clear()
        value_field.send_keys(str(self.quantia))  # Certifique-se de converter para string antes de enviar o valor

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
        time.sleep(2)
        login_box = self.browser_lib.find_element(By.XPATH, "//input[@name='username']")
        login_box.send_keys(login)
        senha_box = self.browser_lib.find_element(By.XPATH, "(//input[@name='password'])[1]")
        senha_box.send_keys(senha)
        time.sleep(1)
        self.browser_lib.find_element(By.XPATH, "(//button[normalize-space()='Entrar'])[1]").click()
        while isCaptcha:
            a = input("Resolva o captcha e digite 1 quando estiver pronto: ")
            if a == "1":
                isCaptcha = False
        time.sleep(3)

    def goto_double_page(self):
        self.browser_lib.get(self.url)  # Use a URL passada como argumento
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
        quantia_input = WebDriverWait(self.browser_lib, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='number']"))
        )
        quantia_input.clear()
        quantia_input.send_keys(str(self.quantia))  # Certifique-se de converter para string antes de enviar o valor

    def main(self):
        self.login_to_blaze("thiagotgrosa@yahoo.com", "258852@tG")
        self.goto_double_page()
        self.set_value_entry()
        self.make_bet()

        # Fechar o navegador
        self.browser_lib.quit()


if __name__ == "__main__":
    url = "https://blaze.com/pt/games/double"  # Insira a URL desejada
    quantia = 10  # Insira o valor de quantia desejado
    obj = SeleniumScraper(url, quantia=quantia)
    obj.main()
