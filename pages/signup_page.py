"""Page Object del modal de registro (Sign up) en Demoblaze."""

import allure
from selenium.webdriver.common.by import By

from core.base_page import BasePage, Locator


class SignupPage(BasePage):
    """Encapsula los localizadores y acciones del modal Sign up."""

    MODAL: Locator = (By.ID, "signInModal")
    USERNAME_INPUT: Locator = (By.ID, "sign-username")
    PASSWORD_INPUT: Locator = (By.ID, "sign-password")
    SIGNUP_BUTTON: Locator = (By.CSS_SELECTOR, "#signInModal button.btn-primary")

    @allure.step("Ingresar credenciales en Sign up para usuario: {username}")
    def ingresar_credenciales(self, username: str, password: str) -> None:
        """Completa los campos de usuario y contrasena en el modal de registro."""
        self.es_visible(self.MODAL)
        self.escribir(self.USERNAME_INPUT, username)
        self.escribir(self.PASSWORD_INPUT, password)

    @allure.step("Confirmar registro en el modal Sign up")
    def confirmar_registro(self) -> None:
        """Hace clic en el boton Sign up del modal."""
        self.hacer_clic(self.SIGNUP_BUTTON)

    @allure.step("Registrar usuario completo: {username}")
    def registrar_usuario(self, username: str, password: str) -> None:
        """Ingresa credenciales y envia el formulario de registro."""
        self.ingresar_credenciales(username, password)
        self.confirmar_registro()

    @allure.step("Esperar cierre del modal Sign up")
    def esperar_cierre_modal(self) -> None:
        """Espera que el modal Sign up deje de ser visible tras aceptar la alerta."""
        self.esperar_invisibilidad(self.MODAL)
