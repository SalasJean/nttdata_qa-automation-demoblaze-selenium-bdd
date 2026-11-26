"""Step definitions del feature de Inicio de Sesion (Login) en Demoblaze."""

from typing import Any

from pytest_bdd import parsers, scenarios, then, when

from pages.home_page import HomePage
from pages.login_page import LoginPage
from tests.step_defs.common_steps import *  # noqa: F401, F403

scenarios("login.feature")


@when("el usuario abre el modal de Login")
def abrir_modal_login(home_page: HomePage) -> None:
    """Abre el modal de Login desde el navbar."""
    home_page.abrir_modal_login()


@when("inicia sesion con las mismas credenciales registradas")
def iniciar_sesion_con_registrado(
    login_page: LoginPage, context: dict[str, Any]
) -> None:
    """Ingresa las credenciales registradas en el paso previo y confirma Login."""
    username = context["registered_username"]
    password = context["registered_password"]
    login_page.iniciar_sesion(username, password)
    login_page.esperar_cierre_modal()


@then("el navbar debe mostrar el saludo de bienvenida con el usuario registrado")
def verificar_saludo_navbar(home_page: HomePage, context: dict[str, Any]) -> None:
    """Verifica que el navbar muestre 'Welcome <username>'."""
    username = context["registered_username"]
    saludo = home_page.obtener_saludo_usuario(username)
    assert saludo == f"Welcome {username}", (
        f"Se esperaba 'Welcome {username}' en navbar, pero se obtuvo '{saludo}'"
    )


@when(
    parsers.re(
        r'ingresa en Login el usuario "(?P<username>[^"]*)" y contrasena "(?P<password>[^"]*)"'
    )
)
def ingresar_credenciales_login(
    login_page: LoginPage, username: str, password: str
) -> None:
    """Ingresa usuario y contrasena en el modal de Login."""
    login_page.ingresar_credenciales(username, password)


@when("confirma el inicio de sesion en Login")
def confirmar_login(login_page: LoginPage) -> None:
    """Presiona el boton Log in del modal."""
    login_page.confirmar_login()
