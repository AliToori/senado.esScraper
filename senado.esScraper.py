 #!/usr/bin/env python3
import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class ScraperX:
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    # options.add_argument('--headless')

    def __init__(self):
        self.driver = webdriver.Chrome(options=self.options)

    def get_senate_members(self, url):
        name_link_list = []
        # self.driver.get(url)
        # time.sleep(3)
        # letters = [letter.get_attribute('href') for letter in self.driver.find_element_by_class_name('listaOriginal').find_elements_by_tag_name('a')]
        # for letter in letters:
        #     name_links = {}
        #     self.driver.get(letter)
        #     time.sleep(3)
            # try:
            #     name_links["Name-Links"] = [name.get_attribute('href') for name in self.driver.find_element_by_class_name('lista-alterna').find_elements_by_tag_name('a')]
            #     df = pd.DataFrame.from_dict(name_links)
            #     # if file does not exist write header
            #     if not os.path.isfile('SpainSenate_NameLinks.csv'):
            #         df.to_csv('SpainSenate_NameLinks.csv', index=None)
            #     else:  # else if exists so append without writing the header
            #         df.to_csv('SpainSenate_NameLinks.csv', mode='a', header=False, index=None)
            #     name_link_list.append(name_links)
            # except NoSuchElementException as nexc:
            #     print("Exception in name links:", nexc.msg)
            #     continue
        df = pd.read_csv("SpainSenate_NameLinks.csv", index_col=None)
        for index, row in df.iterrows():
            member = {}
            print('Opening Link: ', index, row['Name-Link'])
            self.driver.get(url=row['Name-Link'])
            time.sleep(3)
            full_name = self.driver.find_element_by_class_name('text_cab_doble').text
            first_name = re.findall(r'(?<=, )(.*)', full_name)
            first_name = first_name[0]
            first_name = str(first_name).title()
            last_name = re.findall(r'(.*)(?=,)', full_name)
            last_name = last_name[0]
            last_name = str(last_name).title()
            email_text = self.driver.find_element_by_class_name('contacto_senador').find_element_by_tag_name('a').get_attribute('href')
            email = re.findall(r'(?<=mailto:)(.*)', email_text)
            if len(email) > 0:
                email = email[0]
            else:
                email = email_text
            party = self.driver.find_element_by_class_name('content_left_colum2').find_elements_by_tag_name('a')[1].text
            party = str(party).title()
            gender = self.driver.find_element_by_class_name('content_left_colum2').find_elements_by_tag_name('li')[1].text
            gender = re.findall(r'(.*)(?=:)', gender)
            if gender == 'Electa':
                gender = 'F'
            else:
                gender = 'M'
            member["First-name"] = [first_name]
            member["Last-name"] = [last_name]
            member["Email"] = [email]
            member["Party"] = [party]
            member["Gender"] = [gender]
            df = pd.DataFrame.from_dict(member)
            # if file does not exist write header
            if not os.path.isfile('SpainSenate.csv'):
                df.to_csv('SpainSenate.csv', index=None)
            else:  # else if exists so append without writing the header
                df.to_csv('SpainSenate.csv', mode='a', header=False, index=None)

    def get_congress_members(self, url):
        self.driver.get(url)
        # time.sleep(3)
        # letters = [letter.get_attribute('href') for letter in self.driver.find_element_by_id('abecedario').find_elements_by_tag_name('a')]
        # for letter in letters:
        #     name_links = {}
        #     self.driver.get(letter)
        #     time.sleep(3)
        #     try:
        #         name_links["Name-Link"] = [name.get_attribute('href') for name in self.driver.find_element_by_class_name('listado_1').find_elements_by_tag_name('a')]
        #         df = pd.DataFrame.from_dict(name_links)
        #         # if file does not exist write header
        #         if not os.path.isfile('SpainCongress_NameLinks.csv'):
        #             df.to_csv('SpainCongress_NameLinks.csv', index=None)
        #         else:  # else if exists so append without writing the header
        #             df.to_csv('SpainCongress_NameLinks.csv', mode='a', header=False, index=None)
        #     except NoSuchElementException as nexc:
        #         print(nexc.msg)
        #         continue
        df = pd.read_csv("SpainCongress_NameLinks.csv", index_col=None)
        for index, row in df.iterrows():
            member = {}
            print('Opening Link: ', index, row['Name-Link'])
            self.driver.get(url=row['Name-Link'])
            time.sleep(1)
            full_name = self.driver.find_element_by_class_name('nombre_dip').text
            first_name = re.findall(r'(?<=, )(.*)', full_name)
            first_name = first_name[0]
            first_name = str(first_name).title()
            last_name = re.findall(r'(.*)(?=,)', full_name)
            last_name = last_name[0]
            last_name = str(last_name).title()
            try:
                email = self.driver.find_element_by_class_name('webperso_dip').find_elements_by_class_name('webperso_dip_parte')[1].text
            except IndexError as indexExc:
                print(indexExc.args)
                email = 'None'
            party = self.driver.find_elements_by_class_name('dip_rojo')[1].text
            party = str(party).title()
            gender = self.driver.find_elements_by_class_name('dip_rojo')[0].text
            gender = gender[:8]
            if gender == 'Diputado':
                gender = 'M'
            else:
                gender = 'F'
            member["First-name"] = [first_name]
            member["Last-name"] = [last_name]
            member["Email"] = [email]
            member["Party"] = [party]
            member["Gender"] = [gender]
            df = pd.DataFrame.from_dict(member)
            # if file does not exist write header
            if not os.path.isfile('SpainCongress.csv'):
                df.to_csv('SpainCongress.csv', index=None)
            else:  # else if exists so append without writing the header
                df.to_csv('SpainCongress.csv', mode='a', header=False, index=None)

    def finish(self):
        self.driver.close()
        self.driver.quit()


def main():
    # ***************************************************************
    #    The program starts from here
    # ***************************************************************
    senate_web_url = 'http://www.senado.es/web/composicionorganizacion/senadores/composicionsenado/senadoresenactivo/index.html'
    congress_web_url = 'http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados'
    scraperx = ScraperX()
    # scraperx.get_senate_members(url=senate_web_url)
    scraperx.get_congress_members(url=congress_web_url)
    scraperx.finish()


if __name__ == '__main__':
    main()