"""Factory para crear y configurar instancias de Selenium WebDriver."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import (
    BROWSER,
    DETACH,
    HEADLESS,
    IMPLICIT_WAIT,
    PAGE_LOAD_TIMEOUT,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def _build_chrome_options() -> ChromeOptions:
    """Construye las opciones de Chrome reduciendo senales de automatizacion."""
    options = ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    if DETACH:
        options.add_experimental_option("detach", True)

    return options


def crear_driver() -> WebDriver:
    """Crea, configura y devuelve una instancia de WebDriver."""
    if BROWSER != "chrome":
        raise ValueError(f"Navegador no soportado: '{BROWSER}'. Use 'chrome'.")

    options = _build_chrome_options()
    driver = webdriver.Chrome(options=options)

    # Oculta navigator.webdriver para reducir deteccion de automatizacion
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": (
                "Object.defineProperty(navigator, 'webdriver', "
                "{get: () => undefined})"
            )
        },
    )

    driver.maximize_window()
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    if IMPLICIT_WAIT > 0:
        driver.implicitly_wait(IMPLICIT_WAIT)

    logger.info(
        "WebDriver iniciado | browser=%s | headless=%s | detach=%s | page_load=%ss",
        BROWSER,
        HEADLESS,
        DETACH,
        PAGE_LOAD_TIMEOUT,
    )
    return driver
