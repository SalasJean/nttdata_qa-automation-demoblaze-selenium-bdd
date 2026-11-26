"""Step definitions del feature de Registro (Sign up) en Demoblaze."""

from typing import Any

from pytest_bdd import parsers, scenarios, then, when

from pages.home_page import HomePage
from pages.signup_page import SignupPage
from tests.step_defs.common_steps import *  # noqa: F401, F403
from tests.step_defs.common_steps import generar_credenciales_unicas

scenarios("signup.feature")


@when("el usuario abre el modal de Sign up")
def abrir_modal_signup(home_page: HomePage) -> None:
    """Abre el modal de registro desde el navbar."""
    home_page.abrir_modal_signup()


@when(
    "registra un usuario nuevo con credenciales validas generadas desde la configuracion"
)
def registrar_usuario_configurado(
    signup_page: SignupPage, context: dict[str, Any]
) -> None:
    """Registra un usuario nuevo generado a partir de settings.py."""
    username, password = generar_credenciales_unicas(context)
    signup_page.registrar_usuario(username, password)


@when(
    parsers.re(
        r'ingresa en Sign up el usuario "(?P<username>[^"]*)" y contrasena "(?P<password>[^"]*)"'
    )
)
def ingresar_credenciales_signup(
    signup_page: SignupPage, username: str, password: str
) -> None:
    """Ingresa usuario y contrasena en el modal de Sign up."""
    signup_page.ingresar_credenciales(username, password)


@when("confirma el registro en Sign up")
def confirmar_registro_signup(signup_page: SignupPage) -> None:
    """Presiona el boton Sign up del modal."""
    signup_page.confirmar_registro()


@then("el registro finaliza correctamente sin errores")
def verificar_fin_registro(home_page: HomePage) -> None:
    """Verifica que el usuario permanece en el catalogo principal tras registrarse."""
    assert home_page.es_visible(home_page.NAV_LOGIN_LINK), (
        "El enlace de Login deberia estar visible tras completar el registro."
    )
