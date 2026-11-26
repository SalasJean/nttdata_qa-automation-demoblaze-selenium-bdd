"""Steps reutilizables por los distintos features de Demoblaze."""

from typing import Any
import uuid

import allure
from pytest_bdd import given, parsers, then, when

from config.settings import TEST_PASSWORD, TEST_USERNAME
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage


def generar_credenciales_unicas(context: dict[str, Any]) -> tuple[str, str]:
    """Genera un usuario unico basado en configuracion y lo guarda en contexto."""
    sufijo = uuid.uuid4().hex[:6]
    username = f"{TEST_USERNAME}_{sufijo}"
    password = TEST_PASSWORD
    context["registered_username"] = username
    context["registered_password"] = password
    return username, password


@given("el usuario abre la aplicacion Demoblaze")
def abrir_aplicacion(home_page: HomePage) -> None:
    """Abre la pagina principal de Demoblaze."""
    home_page.abrir_home()


@given(
    "existe un usuario nuevo registrado con credenciales validas desde la configuracion"
)
def registrar_usuario_precondicion(
    home_page: HomePage, signup_page: SignupPage, context: dict[str, Any]
) -> None:
    """Registra un usuario nuevo como precondicion y valida el alta exitosa."""
    username, password = generar_credenciales_unicas(context)
    home_page.abrir_modal_signup()
    signup_page.registrar_usuario(username, password)
    alerta = signup_page.aceptar_alerta()
    assert (
        alerta == "Sign up successful."
    ), f"Se esperaba 'Sign up successful.' y se obtuvo '{alerta}'"
    signup_page.esperar_cierre_modal()


@given("el usuario inicia sesion con las mismas credenciales registradas")
def iniciar_sesion_precondicion(
    home_page: HomePage, login_page: LoginPage, context: dict[str, Any]
) -> None:
    """Abre Login e inicia sesion usando las credenciales recien registradas."""
    username = context["registered_username"]
    password = context["registered_password"]
    home_page.abrir_modal_login()
    login_page.iniciar_sesion(username, password)
    login_page.esperar_cierre_modal()
    saludo = home_page.obtener_saludo_usuario(username)
    assert f"Welcome {username}" in saludo, (
        f"Saludo esperado 'Welcome {username}', obtenido '{saludo}'"
    )


@given("al navegar a la pagina principal la URL debe corresponder a index.html")
@then("al navegar a la pagina principal la URL debe corresponder a index.html")
def navegar_y_verificar_home(home_page: HomePage) -> None:
    """Navega al enlace Home y verifica que la URL contenga index.html."""
    home_page.ir_a_pagina_principal()
    url_actual = home_page.obtener_url_actual()
    assert url_actual.endswith("/index.html") or "index.html" in url_actual, (
        f"Se esperaba URL con 'index.html', pero fue '{url_actual}'"
    )


@then(parsers.parse('debe mostrarse la alerta con el mensaje "{mensaje_esperado}"'))
def verificar_mensaje_alerta(
    home_page: HomePage, context: dict[str, Any], mensaje_esperado: str
) -> None:
    """Lee el texto de la alerta activa sin cerrarla y valida su mensaje."""
    mensaje_actual = home_page.obtener_texto_alerta(aceptar=False)
    context["last_alert_text"] = mensaje_actual
    allure.attach(
        mensaje_actual,
        name="Mensaje de Alerta JS",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert mensaje_actual == mensaje_esperado, (
        f"Alerta esperada '{mensaje_esperado}', pero se obtuvo '{mensaje_actual}'"
    )


@when("acepta la alerta actual")
def aceptar_alerta_actual(
    home_page: HomePage, signup_page: SignupPage, context: dict[str, Any]
) -> None:
    """Acepta la alerta del navegador y espera el cierre del modal si aplica."""
    mensaje = home_page.aceptar_alerta()
    if mensaje == "Sign up successful." or (
        context.get("last_alert_text") == "Sign up successful."
    ):
        signup_page.esperar_cierre_modal()
