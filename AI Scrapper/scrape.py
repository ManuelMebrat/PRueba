from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
import time
from bs4 import BeautifulSoup

# Función para elegir el WebDriver según el navegador
def get_webdriver(browser_name, driver_path=""):

    if browser_name.lower() == "edge":
        service = EdgeService(driver_path)
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=service, options=options)

    elif browser_name.lower() == "safari":
        # SafariDriver no requiere un servicio o ruta, está integrado en macOS
        driver = webdriver.Safari()

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    return driver

# Función para raspar un sitio web
def scrape_website(websiteurl, browser_name="edge", driver_path=""):
    print(f"Launching {browser_name} browser...")

    # Obtener el WebDriver correspondiente
    driver = get_webdriver(browser_name, driver_path)

    try:
        driver.get(websiteurl)  # Cargar la página
        print('Page loaded')

        time.sleep(10)  # Esperar a que cargue completamente
        html = driver.page_source  # Obtener el código fuente de la página

        return html  # Devolver el contenido HTML
    finally:
        driver.quit()  # Cerrar el navegador después de terminar

# Funciones para procesar el contenido HTML
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')  
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = '\n'.join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
