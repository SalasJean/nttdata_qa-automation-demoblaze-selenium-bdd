# Demoblaze E2E Test Automation Framework (Python + POM + BDD + Allure)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.54.0-43B02A?logo=selenium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.2.0-0A9EDC?logo=pytest&logoColor=white)
![Pytest-BDD](https://img.shields.io/badge/BDD-Gherkin%20%2F%20pytest--bdd-2B9E4B)
![Allure](https://img.shields.io/badge/Report-Allure%20Single--File-FF6B00)
![CI](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)

Framework de automatización web **End-to-End (E2E)** para **[Demoblaze](https://www.demoblaze.com/)**, diseñado con arquitectura **Page Object Model (POM)**, pruebas orientadas al comportamiento (**BDD / Gherkin** con `pytest-bdd`), evidencias paso a paso estilo Serenity (**Allure Reports + capturas PNG**) e integración continua con **GitHub Actions**.

---

## Cobertura Funcional (15 Escenarios Automatizados)

Los escenarios están organizados por **dominio funcional** con etiquetas `@HappyPath`, `@NegativePath`, `@smoke` y `@regression`:

| Dominio | Feature | Cobertura |
|---|---|---|
| **Registro (`Sign up`)** | [`signup.feature`](tests/features/signup.feature) | Alta exitosa de usuario único + `Scenario Outline` (usuario existente, usuario vacío, contraseña vacía, ambos vacíos). |
| **Autenticación (`Login`)** | [`login.feature`](tests/features/login.feature) | Inicio de sesión con el usuario recién registrado, verificación de saludo `Welcome <usuario>` y `index.html` + `Scenario Outline` (usuario inexistente, contraseña incorrecta, campos vacíos). |
| **Catálogo, Carrito y Compra** | [`purchase.feature`](tests/features/purchase.feature) | Selección dinámica por categoría y producto (`Phones` → `HTC One M9`), carrito, formulario `Place Order`, confirmación `Thank you for your purchase!` y validaciones negativas de campos obligatorios. |

---

## Arquitectura del Proyecto

```text
├── .github/
│   └── workflows/
│       └── qa-e2e.yml             # Pipeline CI/CD: ejecuta pytest headless y publica reporte Allure
├── config/
│   └── settings.py                # Configuración centralizada vía variables de entorno (os.getenv)
├── core/
│   ├── base_page.py               # Esperas explícitas (WebDriverWait) sin assertions ni time.sleep()
│   └── driver_factory.py          # Inicialización de Chrome (headless, detach, mitigación webdriver)
├── pages/
│   ├── home_page.py               # Navbar, catálogo y selectores dinámicos de categoría/producto
│   ├── signup_page.py             # Modal de registro (Sign up)
│   ├── login_page.py              # Modal de inicio de sesión (Login)
│   ├── product_page.py            # Detalle de producto y Add to cart
│   └── cart_page.py               # Carrito, Place Order y modal SweetAlert de confirmación
├── reports/                       # Evidencias locales, allure-results y reporte HTML (ignorado en git)
├── tests/
│   ├── conftest.py                # Fixtures (driver, context, Page Objects) + hooks de capturas
│   ├── features/                  # Especificaciones Gherkin por dominio
│   └── step_defs/                 # Step definitions desacoplados y reutilizables
├── utils/
│   └── logger.py                  # Logger centralizado sin duplicación de handlers
├── pytest.ini                     # Configuración de pytest-bdd, markers y Allure
└── requirements.txt               # Dependencias con versiones fijadas
```

### Decisiones Técnicas Clave
- **POM estricto:** Los Page Objects encapsulan localizadores (priorizando `By.ID` y CSS sobre XPath frágiles) e interacciones anotadas con `@allure.step`. Las aserciones viven únicamente en `tests/step_defs/`.
- **Resiliencia ante AJAX y Modales Bootstrap:** `BasePage` usa `WebDriverWait` ignorando `NoSuchElementException`, `StaleElementReferenceException` y `ElementClickInterceptedException`, eliminando `time.sleep()`.
- **Evidencias Estilo Serenity (`every_step`):** Cada paso captura pantalla en PNG, la adjunta a Allure y la guarda localmente en `reports/screenshots/<timestamp>/<escenario>/`.
- **Protección de Alertas JS:** Antes de capturar pantalla tras un step, `conftest.py` detecta si existe un `alert()` activo para no interferir con la validación del mensaje (adjuntando el texto de la alerta a Allure).
- **Compatibilidad Windows (`MAX_PATH < 260`):** Nombres sanitizados y truncados a `<= 35` caracteres con hash corto único de 6 caracteres por `nodeid` para evitar colisiones en `Scenario Outline`.

---

## Requisitos e Instalación Local

- **Python 3.12+**
- **Google Chrome** instalado
- **Allure CLI** *(opcional para generar reportes HTML localmente)*

```powershell
# 1. Clonar el repositorio
git clone https://github.com/SalasJean/nttdata_qa-automation-demoblaze-selenium-bdd.git
cd nttdata_qa-automation-demoblaze-selenium-bdd

# 2. Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependencias con versiones fijadas
python -m ensurepip --upgrade
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuración por Variables de Entorno

| Variable | Por defecto | Descripción |
|---|---|---|
| `BASE_URL` | `https://www.demoblaze.com/` | URL base de la aplicación |
| `HEADLESS` | `false` | Ejecución sin interfaz gráfica (`true` / `false`) |
| `DETACH` | `false` | Mantiene abierto Chrome al finalizar (`true` / `false`) |
| `EXPLICIT_WAIT` | `15` | Timeout de `WebDriverWait` (segundos) |
| `PAGE_LOAD_TIMEOUT` | `30` | Timeout de carga de página (segundos) |
| `SCREENSHOT_MODE` | `every_step` | `every_step` \| `always` \| `on_failure` \| `none` |
| `SAVE_SCREENSHOTS_LOCAL` | `true` | Guarda copias `.png` en `reports/screenshots/` |
| `TEST_USERNAME` | `jeanxyz` | Prefijo base para generar usuarios únicos de prueba |
| `TEST_PASSWORD` | `JeanDemo123!` | Contraseña base para pruebas locales |

---

## Ejecución de Pruebas y Reporte Allure

```powershell
# Ejecutar toda la suite (15 escenarios)
pytest

# Ejecutar por markers
pytest -m HappyPath
pytest -m NegativePath
pytest -m smoke
pytest -m regression

# Ejecutar en modo headless
$env:HEADLESS = "true"; pytest

# Validar únicamente colección de escenarios (sin abrir navegador)
pytest --collect-only -o addopts=""
```

### Generar reporte HTML único de Allure

```powershell
allure generate --single-file reports/allure-results -o reports/allure-report --clean
Start-Process "reports\allure-report\index.html"
```

---

## CI/CD y Reporte Web Público (GitHub Actions + GitHub Pages)

El workflow [`.github/workflows/qa-e2e.yml`](.github/workflows/qa-e2e.yml) se ejecuta automáticamente en cada `push` o `pull_request` hacia `main` (y manualmente desde la pestaña **Actions** eligiendo el marker deseado):

1. Configura Python 3.12, Google Chrome y dependencias.
2. Valida la colección BDD (`pytest --collect-only`).
3. Ejecuta la suite en modo `HEADLESS=true` generando capturas `every_step`.
4. Genera el reporte `single-file` de Allure (`reports/allure-report/index.html`) incluso si algún escenario falla (`if: always()`).
5. Publica **3 Artifacts** descargables (`allure-report-html`, `allure-results-raw`, `screenshots-evidencia`).
6. Despliega automáticamente el reporte HTML en **GitHub Pages** para verlo en la web sin descargar nada:
   - **URL pública del reporte:** `https://salasjean.github.io/nttdata_qa-automation-demoblaze-selenium-bdd/` *(requiere habilitar una única vez en GitHub: `Settings → Pages → Source: GitHub Actions`)*.
