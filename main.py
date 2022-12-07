from bs4 import  BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import json


def get_data_with_selenium(url):

    # создаем обьект опций
    options = webdriver.ChromeOptions()
    # fake_useragent for anonymous
    options.add_argument(f"user-agent={UserAgent().ie}")
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe",
                              options=options)
    driver.get(url=url)
    # time.sleep(2)

    return driver


def json_file(name, src):
    # saving dictionary in json file
    with open(f"{name}.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # open each page and save to file
    with open(f"{name}.json", encoding="utf-8") as file:
        json.load(file)

def main():
    companies = ["apple", "kobo", "barnesandnoble", "blurb", "smashwords", "draft2digital", "bookbaby", "publishdrive", "ingramspark", "grammarfactory"]
    info_companies = []
    for compani in companies:
        try:
            driver = get_data_with_selenium(fr"https://www.trustpilot.com/review/www.{compani}.com")
            mark = driver.find_element(By.CLASS_NAME, "styles_header__yrrqf")
            info = mark.text.split("\n")
            informtion = \
                        [
                            {"Mark": info[1]},
                            {"People": info[2].split(' ')[0]}
                        ]
            stars = driver.find_element(By.CLASS_NAME, "styles_container__z2XKR")
            for el in stars.find_elements(By.TAG_NAME, "label"):
                if el.text.split("\n")[0] in ["5-star", "3-star", "1-star"]:
                    informtion.append\
                            (
                        {
                            el.text.split("\n")[0]: el.text.split("\n")[1]
                        }
                            )
            print(informtion)
            info_companies.append\
                    (
                        {compani: informtion}
                    )
        except Exception as ex:
            print(ex)
    json_file("Info", info_companies)

if __name__ == "__main__":
    main()