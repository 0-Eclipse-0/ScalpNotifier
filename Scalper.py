from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

class Scalper:
    def __init__(self, url, itemClass):
        # Initialize headless browser
        chromeArgs = webdriver.ChromeOptions()
        chromeArgs.add_argument('headless')

        self.itemClass = itemClass
        self.target = url
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeArgs)

        try:
            self.driver.get(url)
        except Exception as e:
            print(e)


    # Modify and parse source for useful information
    def getSource(self):
        # Scroll to get all items
        for i in range(1, 10):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Remove price deductions


            sleep(4)

        # Javascript to remove price deductions
        self.driver.execute_script(
            """
            const deductions = document.getElementsByClassName("xmqliwb");

            for (let i = deductions.length - 1; i >= 0; i--) {
                deductions[i].parentNode.removeChild(deductions[i]);
            }
            """
        );

    # Get information from each item
    def getItems(self):
        items = []

        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        for div in soup.findAll('div', attrs={'class':'x3ct3a4'}):
            innerText = div.getText(separator=':').split(':')
            innerText.append("https://facebook.com" + div.a['href'])
            innerText.append(div.find('img').attrs['src'])
            items.append(innerText)

        return items

    # Close browser
    def end(self):
        self.driver.quit()
