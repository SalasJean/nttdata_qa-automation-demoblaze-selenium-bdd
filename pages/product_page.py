"""Page Object de la pagina de detalle de producto en Demoblaze."""

import allure
from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class ProductPage(BasePage):
    """Encapsula acciones de consulta y agregado al carrito desde el detalle."""

    PRODUCT_TITLE: Locator = (By.CSS_SELECTOR, "#tbodyid h2.name")
    ADD_TO_CART_BUTTON: Locator = (By.CSS_SELECTOR, "#tbodyid a.btn-success")

    @allure.step("Obtener titulo del producto en detalle")
    def obtener_nombre_producto(self) -> str:
        """Retorna el nombre visible del producto en su vista de detalle."""
        return self.obtener_texto(self.PRODUCT_TITLE)

    @allure.step("Agregar producto al carrito")
    def agregar_al_carrito(self) -> None:
        """Hace clic en el boton Add to cart."""
        self.es_visible(self.PRODUCT_TITLE)
        self.hacer_clic(self.ADD_TO_CART_BUTTON)
