"""Page Object del modal de inicio de sesion (Login) en Demoblaze."""

import allure
from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class LoginPage(BasePage):
    """Encapsula los localizadores y acciones del modal de Login."""

    MODAL: Locator = (By.ID, "logInModal")
    USERNAME_INPUT: Locator = (By.ID, "loginusername")
    PASSWORD_INPUT: Locator = (By.ID, "loginpassword")
    LOGIN_BUTTON: Locator = (By.CSS_SELECTOR, "#logInModal button.btn-primary")

    @allure.step("Ingresar credenciales en Login para usuario: {username}")
    def ingresar_credenciales(self, username: str, password: str) -> None:
        """Completa los campos de usuario y contrasena en el modal de Login."""
        self.es_visible(self.MODAL)
        self.escribir(self.USERNAME_INPUT, username)
        self.escribir(self.PASSWORD_INPUT, password)

    @allure.step("Confirmar inicio de sesion en el modal Login")
    def confirmar_login(self) -> None:
        """Hace clic en el boton Log in del modal."""
        self.hacer_clic(self.LOGIN_BUTTON)

    @allure.step("Iniciar sesion con usuario: {username}")
    def iniciar_sesion(self, username: str, password: str) -> None:
        """Ingresa credenciales y envia el formulario de inicio de sesion."""
        self.ingresar_credenciales(username, password)
        self.confirmar_login()

    @allure.step("Esperar cierre del modal Login")
    def esperar_cierre_modal(self) -> None:
        """Espera a que el modal de Login desaparezca tras autenticarse."""
        self.esperar_invisibilidad(self.MODAL)
