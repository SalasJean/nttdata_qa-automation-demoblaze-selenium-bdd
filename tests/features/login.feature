Feature: Inicio de Sesion (Login) en Demoblaze

  Como usuario registrado de Demoblaze
  Quiero iniciar sesion con mis credenciales
  Para acceder de forma autenticada a la tienda

  Background:
    Given el usuario abre la aplicacion Demoblaze

  @HappyPath @smoke
  Scenario: Inicio de sesion exitoso con usuario previamente registrado
    Given existe un usuario nuevo registrado con credenciales validas desde la configuracion
    When el usuario abre el modal de Login
    And inicia sesion con las mismas credenciales registradas
    Then el navbar debe mostrar el saludo de bienvenida con el usuario registrado
    And al navegar a la pagina principal la URL debe corresponder a index.html

  @NegativePath @regression
  Scenario Outline: Inicio de sesion fallido en Login (<caso>)
    When el usuario abre el modal de Login
    And ingresa en Login el usuario "<username>" y contrasena "<password>"
    And confirma el inicio de sesion en Login
    Then debe mostrarse la alerta con el mensaje "<mensaje_alerta>"

    Examples:
      | caso                  | username                   | password           | mensaje_alerta                         |
      | Usuario inexistente   | usuario_inexistente_qa_999 | ClaveDemo123       | User does not exist.                   |
      | Contrasena incorrecta | admin                      | ClaveIncorrecta999 | Wrong password.                        |
      | Usuario vacio         |                            | ClaveDemo123       | Please fill out Username and Password. |
      | Contrasena vacia      | admin                      |                    | Please fill out Username and Password. |
      | Ambos campos vacios   |                            |                    | Please fill out Username and Password. |
