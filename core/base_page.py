"""Clase base de todos los Page Objects.

Encapsula interacciones reutilizables con esperas explicitas (WebDriverWait).
No contiene assertions: las verificaciones pertenecen a los step definitions.
"""

from typing import Tuple

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import EXPLICIT_WAIT
from utils.logger import get_logger

Locator = Tuple[str, str]
_IGNORED_EXCEPTIONS = (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)


class BasePage:
    """Clase base para Page Objects con esperas explicitas."""

    def __init__(self, driver: WebDriver, timeout: int | None = None) -> None:
        self.driver = driver
        self.timeout = timeout if timeout is not None else EXPLICIT_WAIT
        self.wait = WebDriverWait(
            driver, self.timeout, ignored_exceptions=_IGNORED_EXCEPTIONS
        )
        self.logger = get_logger(self.__class__.__name__)

    def _get_wait(self, timeout: int | None = None) -> WebDriverWait:
        """Retorna el WebDriverWait por defecto o uno con timeout personalizado."""
        if timeout is None or timeout == self.timeout:
            return self.wait
        return WebDriverWait(
            self.driver, timeout, ignored_exceptions=_IGNORED_EXCEPTIONS
        )

    def _esperar_visible(
        self, locator: Locator, timeout: int | None = None
    ) -> WebElement:
        """Espera a que un elemento sea visible en el DOM y lo retorna."""
        return self._get_wait(timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def _esperar_clickeable(
        self, locator: Locator, timeout: int | None = None
    ) -> WebElement:
        """Espera a que un elemento sea clickeable y lo retorna."""
        return self._get_wait(timeout).until(EC.element_to_be_clickable(locator))

    def abrir_url(self, url: str) -> None:
        """Navega hacia la URL indicada y espera la carga completa de la pagina."""
        self.logger.info("Abriendo URL: %s", url)
        self.driver.get(url)
        self.esperar_carga_completa()

    def escribir(self, locator: Locator, texto: str, limpiar: bool = True) -> None:
        """Espera visibilidad del campo, limpia si aplica y escribe el texto."""
        elemento = self._esperar_visible(locator)
        if limpiar:
            elemento.clear()
        if texto:
            elemento.send_keys(texto)

    def hacer_clic(self, locator: Locator) -> None:
        """Espera que el elemento sea clickeable y ejecuta clic de forma segura."""

        def _click(driver: WebDriver) -> bool:
            elemento = EC.element_to_be_clickable(locator)(driver)
            if not elemento:
                return False
            elemento.click()
            return True

        self.wait.until(_click)

    def es_visible(self, locator: Locator, timeout: int | None = None) -> bool:
        """Retorna True si el elemento se vuelve visible dentro del timeout."""
        try:
            self._esperar_visible(locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def esperar_invisibilidad(
        self, locator: Locator, timeout: int | None = None
    ) -> bool:
        """Espera a que un elemento deje de ser visible (por ejemplo, un modal)."""
        try:
            return bool(
                self._get_wait(timeout).until(
                    EC.invisibility_of_element_located(locator)
                )
            )
        except TimeoutException:
            return False

    def esperar_texto_en_elemento(
        self, locator: Locator, texto: str, timeout: int | None = None
    ) -> bool:
        """Espera a que el texto indicado aparezca dentro del elemento."""
        try:
            return bool(
                self._get_wait(timeout).until(
                    EC.text_to_be_present_in_element(locator, texto)
                )
            )
        except TimeoutException:
            return False

    def obtener_texto(self, locator: Locator) -> str:
        """Espera visibilidad del elemento y retorna su texto limpio."""
        return self._esperar_visible(locator).text.strip()

    def obtener_textos(self, locator: Locator) -> list[str]:
        """Retorna la lista de textos de todos los elementos que coinciden."""
        elementos = self.driver.find_elements(*locator)
        return [el.text.strip() for el in elementos if el.text.strip()]

    def obtener_url_actual(self) -> str:
        """Retorna la URL actual del navegador."""
        return self.driver.current_url

    def obtener_titulo(self) -> str:
        """Retorna el titulo actual de la pagina."""
        return self.driver.title

    def esperar_carga_completa(self) -> None:
        """Espera hasta que document.readyState sea 'complete'."""
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def esperar_url_contenga(self, fragmento: str) -> bool:
        """Espera a que la URL actual contenga el fragmento indicado."""
        return bool(self.wait.until(EC.url_contains(fragmento)))

    def obtener_texto_alerta(
        self, aceptar: bool = False, timeout: int | None = None
    ) -> str:
        """Espera una alerta JS del navegador, lee su texto y opcionalmente la acepta."""
        alerta = self._get_wait(timeout).until(EC.alert_is_present())
        texto = (alerta.text or "").strip()
        if aceptar:
            alerta.accept()
        return texto

    def aceptar_alerta(self, timeout: int | None = None) -> str:
        """Espera la alerta JS actual, la acepta y retorna su texto."""
        return self.obtener_texto_alerta(aceptar=True, timeout=timeout)
