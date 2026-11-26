"""Fixtures compartidos y hooks de evidencias estilo Serenity (Allure + PNG local)."""

from datetime import datetime
import hashlib
from pathlib import Path
import re
import time
from typing import Any, Generator

import allure
import pytest
from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoAlertPresentException,
    UnexpectedAlertPresentException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import (
    PROJECT_ROOT,
    SAVE_SCREENSHOTS_LOCAL,
    SCREENSHOT_MODE,
    SCREENSHOTS_DIR,
    TEST_DELAY,
)
from core.driver_factory import crear_driver
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.signup_page import SignupPage
from utils.logger import get_logger

logger = get_logger(__name__)

_RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
_VALID_SCREENSHOT_MODES = {"every_step", "always", "on_failure", "none"}
_MAX_SEGMENT_LEN = 35
_WINDOWS_MAX_PATH = 259


def _sanitizar_nombre(texto: str, max_len: int = _MAX_SEGMENT_LEN) -> str:
    """Limpia un texto para usarlo como nombre de carpeta o archivo en Windows."""
    limpio = re.sub(r"[^A-Za-z0-9_-]+", "_", texto or "")
    limpio = re.sub(r"_+", "_", limpio).strip("_-")
    if not limpio:
        limpio = "item"
    return limpio[:max_len].rstrip("_-") or "item"


def _construir_carpeta_escenario(nodeid: str, scenario_name: str) -> Path:
    """Genera una ruta corta (<35 chars por segmento) y unica por escenario."""
    hash_corto = hashlib.sha1(nodeid.encode("utf-8")).hexdigest()[:6]
    max_base = _MAX_SEGMENT_LEN - len(hash_corto) - 1
    base = _sanitizar_nombre(scenario_name, max_len=max_base)
    carpeta_escenario = f"{base}_{hash_corto}"
    return PROJECT_ROOT / SCREENSHOTS_DIR / _RUN_TIMESTAMP / carpeta_escenario


def _construir_nombre_archivo(step_idx: int, status: str, step_name: str) -> str:
    """Construye un nombre de archivo .png de maximo 35 caracteres."""
    prefijo = f"{step_idx:02d}_{status}_"
    extension = ".png"
    max_slug = _MAX_SEGMENT_LEN - len(prefijo) - len(extension)
    slug = _sanitizar_nombre(step_name, max_len=max(1, max_slug))
    return f"{prefijo}{slug}{extension}"


def _hay_alerta_abierta(driver: WebDriver) -> bool:
    """Comprueba sin modificarla si existe una alerta JS activa en el navegador."""
    try:
        _ = driver.switch_to.alert
        return True
    except NoAlertPresentException:
        return False
    except WebDriverException:
        return False


def _obtener_driver_activo(item: pytest.Item) -> WebDriver | None:
    """Obtiene la instancia activa de WebDriver del test sin forzar su creacion."""
    driver_activo = getattr(item, "_active_driver", None)
    if driver_activo is not None:
        return driver_activo

    funcargs = getattr(item, "funcargs", None)
    if isinstance(funcargs, dict):
        return funcargs.get("driver")
    return None


def _capturar_evidencia(
    item: pytest.Item, step_idx: int, status: str, label: str
) -> bool:
    """Toma captura de pantalla, la adjunta a Allure y la guarda localmente."""
    if SCREENSHOT_MODE not in _VALID_SCREENSHOT_MODES or SCREENSHOT_MODE == "none":
        return False

    driver = _obtener_driver_activo(item)
    if driver is None:
        return False

    if _hay_alerta_abierta(driver):
        logger.debug(
            "Se omite captura en '%s' porque hay una alerta JS activa.", label
        )
        return False

    try:
        png_bytes = driver.get_screenshot_as_png()
    except (
        UnexpectedAlertPresentException,
        InvalidSessionIdException,
        WebDriverException,
    ) as exc:
        logger.warning("No se pudo capturar pantalla (%s): %s", label, exc)
        return False

    nombre_archivo = _construir_nombre_archivo(step_idx, status, label)
    allure.attach(
        png_bytes,
        name=nombre_archivo,
        attachment_type=allure.attachment_type.PNG,
    )

    if SAVE_SCREENSHOTS_LOCAL:
        carpeta = getattr(item, "_screenshot_dir", None)
        if isinstance(carpeta, Path):
            ruta_destino = carpeta / nombre_archivo
            if len(str(ruta_destino)) >= _WINDOWS_MAX_PATH:
                logger.warning(
                    "Ruta excede limite MAX_PATH (%d chars): %s",
                    len(str(ruta_destino)),
                    ruta_destino,
                )
                return True
            carpeta.mkdir(parents=True, exist_ok=True)
            ruta_destino.write_bytes(png_bytes)

    return True


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    """Provee un WebDriver aislado por escenario con teardown blindado."""
    webdriver_instance = crear_driver()
    request.node._active_driver = webdriver_instance
    try:
        yield webdriver_instance
    finally:
        request.node._active_driver = None
        try:
            webdriver_instance.quit()
        except (InvalidSessionIdException, WebDriverException, Exception) as exc:
            logger.warning("Error controlado al cerrar WebDriver: %s", exc)
        if TEST_DELAY > 0:
            time.sleep(TEST_DELAY)


@pytest.fixture(scope="function")
def context() -> dict[str, Any]:
    """Contexto mutable por escenario para compartir datos entre steps."""
    return {}


@pytest.fixture(scope="function")
def home_page(driver: WebDriver) -> HomePage:
    """Instancia de HomePage asociada al driver del escenario."""
    return HomePage(driver)


@pytest.fixture(scope="function")
def signup_page(driver: WebDriver) -> SignupPage:
    """Instancia de SignupPage asociada al driver del escenario."""
    return SignupPage(driver)


@pytest.fixture(scope="function")
def login_page(driver: WebDriver) -> LoginPage:
    """Instancia de LoginPage asociada al driver del escenario."""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def product_page(driver: WebDriver) -> ProductPage:
    """Instancia de ProductPage asociada al driver del escenario."""
    return ProductPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver: WebDriver) -> CartPage:
    """Instancia de CartPage asociada al driver del escenario."""
    return CartPage(driver)


def pytest_bdd_before_scenario(
    request: pytest.FixtureRequest, feature: Any, scenario: Any
) -> None:
    """Inicializa contadores y carpeta local de capturas para el escenario."""
    node = request.node
    node._step_counter = 0
    node._failure_screenshot_taken = False
    node._screenshot_dir = _construir_carpeta_escenario(
        node.nodeid, getattr(scenario, "name", node.name)
    )


def pytest_bdd_after_step(
    request: pytest.FixtureRequest,
    feature: Any,
    scenario: Any,
    step: Any,
    step_func: Any,
    step_func_args: dict[str, Any],
) -> None:
    """Captura evidencia despues de cada step exitoso cuando SCREENSHOT_MODE=every_step."""
    node = request.node
    node._step_counter = getattr(node, "_step_counter", 0) + 1
    if SCREENSHOT_MODE == "every_step":
        _capturar_evidencia(
            node,
            step_idx=node._step_counter,
            status="PASS",
            label=getattr(step, "name", "step"),
        )


def pytest_bdd_step_error(
    request: pytest.FixtureRequest,
    feature: Any,
    scenario: Any,
    step: Any,
    step_func: Any,
    step_func_args: dict[str, Any],
    exception: Exception,
) -> None:
    """Captura evidencia inmediata cuando falla un step BDD."""
    node = request.node
    node._step_counter = getattr(node, "_step_counter", 0) + 1
    if SCREENSHOT_MODE in {"every_step", "always", "on_failure"}:
        capturada = _capturar_evidencia(
            node,
            step_idx=node._step_counter,
            status="FAIL",
            label=getattr(step, "name", "step_error"),
        )
        if capturada:
            node._failure_screenshot_taken = True


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    """Respalda la captura al finalizar el test segun SCREENSHOT_MODE."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    step_idx = getattr(item, "_step_counter", 0) + 1
    if report.failed and SCREENSHOT_MODE in {"every_step", "always", "on_failure"}:
        if not getattr(item, "_failure_screenshot_taken", False):
            _capturar_evidencia(item, step_idx=step_idx, status="FAIL", label="final")
    elif report.passed and SCREENSHOT_MODE == "always":
        _capturar_evidencia(item, step_idx=step_idx, status="PASS", label="final")
