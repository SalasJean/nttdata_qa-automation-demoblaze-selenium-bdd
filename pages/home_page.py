"""Page Object de la pagina principal, barra de navegacion y catalogo de Demoblaze."""

import allure
from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from core.base_page import BasePage, Locator


class HomePage(BasePage):
    """Gestiona navegacion principal, autenticacion en navbar y catalogo."""

    NAV_HOME_LINK: Locator = (By.CSS_SELECTOR, "a.nav-link[href='index.html']")
    NAV_SIGNUP_LINK: Locator = (By.ID, "signin2")
    NAV_LOGIN_LINK: Locator = (By.ID, "login2")
    NAV_CART_LINK: Locator = (By.ID, "cartur")
    NAV_USER_GREETING: Locator = (By.ID, "nameofuser")
    CATALOG_CONTAINER: Locator = (By.ID, "tbodyid")
    PRODUCT_CARDS_LINKS: Locator = (By.CSS_SELECTOR, "#tbodyid .card-title a")

    @staticmethod
    def _categoria_locator(categoria: str) -> Locator:
        """Construye el localizador dinamico de una categoria por su nombre."""
        return (
            By.XPATH,
            f"//a[@id='itemc' and normalize-space()='{categoria}']",
        )

    @staticmethod
    def _producto_locator(producto: str) -> Locator:
        """Construye el localizador dinamico de un producto por su titulo."""
        return (
            By.XPATH,
            f"//div[@id='tbodyid']//h4[contains(@class,'card-title')]//a[normalize-space()='{producto}']",
        )

    @allure.step("Abrir la aplicacion Demoblaze")
    def abrir_home(self) -> None:
        """Abre la URL base configurada y espera que el catalogo sea visible."""
        self.abrir_url(BASE_URL)
        self.es_visible(self.CATALOG_CONTAINER)

    @allure.step("Navegar a la pagina principal (index.html)")
    def ir_a_pagina_principal(self) -> None:
        """Hace clic en Home en el navbar y espera que la URL contenga index.html."""
        self.hacer_clic(self.NAV_HOME_LINK)
        self.esperar_carga_completa()
        self.esperar_url_contenga("index.html")

    @allure.step("Abrir modal de Sign up")
    def abrir_modal_signup(self) -> None:
        """Abre el modal de registro desde el navbar."""
        self.hacer_clic(self.NAV_SIGNUP_LINK)

    @allure.step("Abrir modal de Login")
    def abrir_modal_login(self) -> None:
        """Abre el modal de inicio de sesion desde el navbar."""
        self.hacer_clic(self.NAV_LOGIN_LINK)

    @allure.step("Ir al carrito de compras")
    def ir_al_carrito(self) -> None:
        """Navega al carrito desde el navbar."""
        self.hacer_clic(self.NAV_CART_LINK)
        self.esperar_url_contenga("cart.html")

    @allure.step("Obtener saludo del usuario autenticado en el navbar")
    def obtener_saludo_usuario(self, username: str | None = None) -> str:
        """Espera el saludo en el navbar y devuelve su texto."""
        if username:
            self.esperar_texto_en_elemento(
                self.NAV_USER_GREETING, f"Welcome {username}"
            )
        return self.obtener_texto(self.NAV_USER_GREETING)

    @allure.step("Seleccionar categoria: {categoria}")
    def seleccionar_categoria(self, categoria: str) -> None:
        """Selecciona una categoria del menu lateral y espera los productos."""
        self.hacer_clic(self._categoria_locator(categoria))
        self.es_visible(self.PRODUCT_CARDS_LINKS)

    @allure.step("Seleccionar producto: {producto}")
    def seleccionar_producto(self, producto: str) -> None:
        """Hace clic en la tarjeta del producto indicado."""
        self.hacer_clic(self._producto_locator(producto))
        self.esperar_carga_completa()
