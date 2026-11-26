"""Configuracion centralizada del framework de automatizacion."""

import os
from pathlib import Path


def _env_bool(name: str, default: bool) -> bool:
    """Convierte una variable de entorno a booleano de forma segura."""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "si", "on"}


# Rutas base del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# URLs de la aplicacion bajo prueba (Demoblaze)
BASE_URL = os.getenv("BASE_URL", "https://www.demoblaze.com/").strip()
_CLEAN_BASE_URL = BASE_URL.rstrip("/")
HOME_URL = os.getenv("HOME_URL", f"{_CLEAN_BASE_URL}/index.html")
CART_URL = os.getenv("CART_URL", f"{_CLEAN_BASE_URL}/cart.html")

# Configuracion del navegador
BROWSER = os.getenv("BROWSER", "chrome").strip().lower()
HEADLESS = _env_bool("HEADLESS", False)
DETACH = _env_bool("DETACH", False)

# Timeouts en segundos
IMPLICIT_WAIT = float(os.getenv("IMPLICIT_WAIT", "0"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

# Control de ejecucion
TEST_DELAY = float(os.getenv("TEST_DELAY", "0"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").strip().upper()

# Capturas de pantalla y reportes
# Modos validos: every_step | always | on_failure | none
SCREENSHOT_MODE = os.getenv("SCREENSHOT_MODE", "every_step").strip().lower()
SAVE_SCREENSHOTS_LOCAL = _env_bool("SAVE_SCREENSHOTS_LOCAL", True)
SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "reports/screenshots")
ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")

# Credenciales de prueba (defaults locales solo para entorno de desarrollo)
TEST_USERNAME = os.getenv("TEST_USERNAME", "jeanxyz")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "JeanDemo123!")
