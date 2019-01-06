import scrapy
from selenium import webdriver


class QuotesSpider(scrapy.Spider):
    name = "deutscheindustrie"
    start_urls = ["https://www.diedeutscheindustrie.de/searches?sterm=Software+&lang=deu&zipcode_city=&suche=ps"]

    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def parse(self, response):
        # selenium part
        self.driver.get(response.url)

        all_companies_element_checkbox = self.driver.find_element_by_class_name("allChk")
        all_companies_element_checkbox.click()
        show_all_companies = self.driver.find_element_by_xpath("/html/body/div[7]/div/form/input[1]")
        show_all_companies.click()

        supplier_altogether = self.driver.find_elements_by_class_name("filterliste")
        supplier_list = supplier_altogether[0].find_elements_by_class_name("firmaKurzFirma")
        supplier_subsites = []
        for supplier in supplier_list:
            supplier_subsites.append(supplier.find_element_by_xpath("h4/a").get_attribute("href"))
        
        self.driver.close()
        
        # scrapy part
        for supplier in supplier_subsites:
            yield scrapy.Request(
                        url=supplier,
                        callback=self.parse_supplier_subsite)

    def parse_supplier_subsite(self, response):
        data = {}
        data['website'] = response.css("#firmenprofil > h4.kontakt.fpurls > div > span > a::text").extract_first()
        data['email'] = response.css("#firmenprofil > h4.kontakt.fpmail.openParent > span > a::text").extract_first()
        # TODO
        # add other attributes
        yield data