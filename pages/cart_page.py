"""Page Object del carrito de compras y modal Place Order en Demoblaze."""

import allure
from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class CartPage(BasePage):
    """Gestiona la tabla del carrito, el formulario de orden y su confirmacion."""

    CART_PRODUCT_TITLES: Locator = (
        By.CSS_SELECTOR,
        "#tbodyid tr.success td:nth-child(2)",
    )
    PLACE_ORDER_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "button[data-target='#orderModal']",
    )
    ORDER_MODAL: Locator = (By.ID, "orderModal")
    NAME_INPUT: Locator = (By.ID, "name")
    COUNTRY_INPUT: Locator = (By.ID, "country")
    CITY_INPUT: Locator = (By.ID, "city")
    CARD_INPUT: Locator = (By.ID, "card")
    MONTH_INPUT: Locator = (By.ID, "month")
    YEAR_INPUT: Locator = (By.ID, "year")
    PURCHASE_BUTTON: Locator = (By.CSS_SELECTOR, "#orderModal button.btn-primary")

    CONFIRMATION_MODAL: Locator = (By.CSS_SELECTOR, "div.sweet-alert.visible")
    CONFIRMATION_TITLE: Locator = (By.CSS_SELECTOR, "div.sweet-alert h2")
    CONFIRMATION_DETAILS: Locator = (By.CSS_SELECTOR, "div.sweet-alert p.lead")
    CONFIRMATION_OK_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "div.sweet-alert button.confirm",
    )

    @allure.step("Obtener listado de productos en el carrito")
    def obtener_productos_en_carrito(self) -> list[str]:
        """Espera los items del carrito y retorna los titulos visibles."""
        self.es_visible(self.CART_PRODUCT_TITLES)
        return self.obtener_textos(self.CART_PRODUCT_TITLES)

    @allure.step("Abrir modal de orden de compra (Place Order)")
    def abrir_modal_orden(self) -> None:
        """Hace clic en Place Order y espera la apertura del modal."""
        self.hacer_clic(self.PLACE_ORDER_BUTTON)
        self.es_visible(self.ORDER_MODAL)

    @allure.step("Completar formulario de compra para {nombre}")
    def completar_formulario_orden(
        self,
        nombre: str,
        pais: str,
        ciudad: str,
        tarjeta: str,
        mes: str,
        anio: str,
    ) -> None:
        """Llena los campos del modal Place Order."""
        self.es_visible(self.ORDER_MODAL)
        self.escribir(self.NAME_INPUT, nombre)
        self.escribir(self.COUNTRY_INPUT, pais)
        self.escribir(self.CITY_INPUT, ciudad)
        self.escribir(self.CARD_INPUT, tarjeta)
        self.escribir(self.MONTH_INPUT, mes)
        self.escribir(self.YEAR_INPUT, anio)

    @allure.step("Confirmar compra con boton Purchase")
    def confirmar_compra(self) -> None:
        """Hace clic en Purchase para enviar la orden."""
        self.hacer_clic(self.PURCHASE_BUTTON)

    @allure.step("Obtener titulo de confirmacion de compra")
    def obtener_titulo_confirmacion(self) -> str:
        """Retorna el encabezado del modal SweetAlert de confirmacion."""
        self.es_visible(self.CONFIRMATION_MODAL)
        return self.obtener_texto(self.CONFIRMATION_TITLE)

    @allure.step("Obtener detalle de confirmacion de compra")
    def obtener_detalle_confirmacion(self) -> str:
        """Retorna el cuerpo del modal SweetAlert con los datos de la orden."""
        self.es_visible(self.CONFIRMATION_MODAL)
        return self.obtener_texto(self.CONFIRMATION_DETAILS)

    @allure.step("Aceptar modal de confirmacion con OK")
    def aceptar_confirmacion(self) -> None:
        """Hace clic en OK y espera el cierre del modal de confirmacion."""
        self.hacer_clic(self.CONFIRMATION_OK_BUTTON)
        self.esperar_invisibilidad(self.CONFIRMATION_MODAL)
