"""Step definitions del feature de Catalogo, Carrito y Compra en Demoblaze."""

from pytest_bdd import parsers, scenarios, then, when

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from tests.step_defs.common_steps import *  # noqa: F401, F403

scenarios("purchase.feature")


@when(parsers.parse('selecciona la categoria "{categoria}"'))
def seleccionar_categoria(home_page: HomePage, categoria: str) -> None:
    """Selecciona la categoria indicada en el catalogo."""
    home_page.seleccionar_categoria(categoria)


@when(parsers.parse('selecciona el producto "{producto}"'))
def seleccionar_producto(home_page: HomePage, producto: str) -> None:
    """Selecciona el producto indicado dentro del catalogo."""
    home_page.seleccionar_producto(producto)


@when("agrega el producto al carrito")
def agregar_producto_al_carrito(product_page: ProductPage) -> None:
    """Presiona el boton Add to cart en el detalle del producto."""
    product_page.agregar_al_carrito()


@when("accede al carrito de compras")
def acceder_al_carrito(home_page: HomePage) -> None:
    """Navega al carrito desde el navbar."""
    home_page.ir_al_carrito()


@then(parsers.parse('debe visualizar el producto "{producto}" listado en el carrito'))
def verificar_producto_en_carrito(cart_page: CartPage, producto: str) -> None:
    """Verifica que el producto esperado aparezca en la tabla del carrito."""
    productos = cart_page.obtener_productos_en_carrito()
    assert producto in productos, (
        f"Producto '{producto}' no encontrado en el carrito: {productos}"
    )


@when("inicia la orden de compra con Place Order")
def iniciar_place_order(cart_page: CartPage) -> None:
    """Abre el modal de Place Order."""
    cart_page.abrir_modal_orden()


@when(
    parsers.re(
        r'completa el formulario de compra con nombre "(?P<nombre>[^"]*)", '
        r'pais "(?P<pais>[^"]*)", ciudad "(?P<ciudad>[^"]*)", '
        r'tarjeta "(?P<tarjeta>[^"]*)", mes "(?P<mes>[^"]*)" y anio "(?P<anio>[^"]*)"'
    )
)
def completar_formulario_compra(
    cart_page: CartPage,
    nombre: str,
    pais: str,
    ciudad: str,
    tarjeta: str,
    mes: str,
    anio: str,
) -> None:
    """Completa los campos del modal Place Order."""
    cart_page.completar_formulario_orden(
        nombre=nombre,
        pais=pais,
        ciudad=ciudad,
        tarjeta=tarjeta,
        mes=mes,
        anio=anio,
    )


@when("confirma la compra con Purchase")
def confirmar_compra(cart_page: CartPage) -> None:
    """Envia la orden de compra haciendo clic en Purchase."""
    cart_page.confirmar_compra()


@then(
    parsers.parse(
        'debe mostrarse la confirmacion "{titulo_esperado}" con el nombre "{nombre_esperado}"'
    )
)
def verificar_confirmacion_compra(
    cart_page: CartPage, titulo_esperado: str, nombre_esperado: str
) -> None:
    """Valida el titulo de confirmacion y que incluya el nombre del comprador."""
    titulo_actual = cart_page.obtener_titulo_confirmacion()
    detalle_actual = cart_page.obtener_detalle_confirmacion()
    assert titulo_actual == titulo_esperado, (
        f"Titulo esperado '{titulo_esperado}', obtenido '{titulo_actual}'"
    )
    assert f"Name: {nombre_esperado}" in detalle_actual, (
        f"Se esperaba 'Name: {nombre_esperado}' en el detalle:\n{detalle_actual}"
    )


@when("acepta el modal de confirmacion con OK")
def aceptar_modal_confirmacion(cart_page: CartPage) -> None:
    """Cierra el modal de confirmacion haciendo clic en OK."""
    cart_page.aceptar_confirmacion()


@then("el flujo de compra finaliza correctamente")
def verificar_fin_compra(home_page: HomePage) -> None:
    """Verifica que la sesion del navegador sigue activa tras completar la compra."""
    url_actual = home_page.obtener_url_actual()
    assert "demoblaze.com" in url_actual, (
        f"URL inesperada tras completar compra: '{url_actual}'"
    )
