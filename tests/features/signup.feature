Feature: Registro de Usuario (Sign up) en Demoblaze

  Como nuevo visitante de Demoblaze
  Quiero registrarme en la plataforma
  Para poder contar con una cuenta e iniciar sesion posteriormente

  Background:
    Given el usuario abre la aplicacion Demoblaze

  @HappyPath @smoke
  Scenario: Registro exitoso de un nuevo usuario
    When el usuario abre el modal de Sign up
    And registra un usuario nuevo con credenciales validas generadas desde la configuracion
    Then debe mostrarse la alerta con el mensaje "Sign up successful."
    When acepta la alerta actual
    Then el registro finaliza correctamente sin errores

  @NegativePath @regression
  Scenario Outline: Registro fallido en Sign up (<caso>)
    When el usuario abre el modal de Sign up
    And ingresa en Sign up el usuario "<username>" y contrasena "<password>"
    And confirma el registro en Sign up
    Then debe mostrarse la alerta con el mensaje "<mensaje_alerta>"

    Examples:
      | caso                 | username        | password     | mensaje_alerta                         |
      | Usuario ya existente | admin           | ClaveDemo123 | This user already exist.               |
      | Usuario vacio        |                 | ClaveDemo123 | Please fill out Username and Password. |
      | Contrasena vacia     | usuario_demo_qa |              | Please fill out Username and Password. |
      | Ambos campos vacios  |                 |              | Please fill out Username and Password. |
