from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def startGUI():
        # Build app window
        chromeArgs = webdriver.ChromeOptions()
        chromeArgs.add_argument('--app=http://localhost')
        chromeArgs.add_experimental_option("detach", True)
        chromeArgs.add_experimental_option("excludeSwitches", ['enable-automation']);
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='114.0.5735.90').install()), options=chromeArgs)
        driver.set_window_size(635,453)