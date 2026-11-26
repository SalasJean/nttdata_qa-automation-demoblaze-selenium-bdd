Feature: Catalogo, Carrito y Compra en Demoblaze

  Como usuario autenticado de Demoblaze
  Quiero seleccionar productos por categoria, agregarlos al carrito y completar la orden
  Para realizar compras exitosas y validar los controles obligatorios del checkout

  Background:
    Given el usuario abre la aplicacion Demoblaze
    And existe un usuario nuevo registrado con credenciales validas desde la configuracion
    And el usuario inicia sesion con las mismas credenciales registradas
    And al navegar a la pagina principal la URL debe corresponder a index.html

  @HappyPath @smoke @regression
  Scenario Outline: Compra exitosa de producto por categoria (<categoria> - <producto>)
    When selecciona la categoria "<categoria>"
    And selecciona el producto "<producto>"
    And agrega el producto al carrito
    Then debe mostrarse la alerta con el mensaje "Product added."
    When acepta la alerta actual
    And accede al carrito de compras
    Then debe visualizar el producto "<producto>" listado en el carrito
    When inicia la orden de compra con Place Order
    And completa el formulario de compra con nombre "<nombre>", pais "<pais>", ciudad "<ciudad>", tarjeta "<tarjeta>", mes "<mes>" y anio "<anio>"
    And confirma la compra con Purchase
    Then debe mostrarse la confirmacion "Thank you for your purchase!" con el nombre "<nombre>"
    When acepta el modal de confirmacion con OK
    Then el flujo de compra finaliza correctamente

    Examples:
      | categoria | producto   | nombre     | pais | ciudad | tarjeta          | mes | anio |
      | Phones    | HTC One M9 | Jean Salas | Peru | Lima   | 4111111111111111 | 11  | 2026 |

  @NegativePath @regression
  Scenario Outline: Intento de compra con datos obligatorios incompletos (<caso>)
    When selecciona la categoria "<categoria>"
    And selecciona el producto "<producto>"
    And agrega el producto al carrito
    Then debe mostrarse la alerta con el mensaje "Product added."
    When acepta la alerta actual
    And accede al carrito de compras
    And inicia la orden de compra con Place Order
    And completa el formulario de compra con nombre "<nombre>", pais "<pais>", ciudad "<ciudad>", tarjeta "<tarjeta>", mes "<mes>" y anio "<anio>"
    And confirma la compra con Purchase
    Then debe mostrarse la alerta con el mensaje "<mensaje_alerta>"

    Examples:
      | caso                    | categoria | producto   | nombre     | pais | ciudad | tarjeta          | mes | anio | mensaje_alerta                       |
      | Nombre vacio            | Phones    | HTC One M9 |            | Peru | Lima   | 4111111111111111 | 11  | 2026 | Please fill out Name and Creditcard. |
      | Tarjeta vacia           | Phones    | HTC One M9 | Jean Salas | Peru | Lima   |                  | 11  | 2026 | Please fill out Name and Creditcard. |
      | Nombre y tarjeta vacios | Phones    | HTC One M9 |            | Peru | Lima   |                  | 11  | 2026 | Please fill out Name and Creditcard. |
