# ================================================================
# PROYECTO: SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ
# Descripcion: Gestion de clientes, servicios y reservas.
# ================================================================

# Importamos ABC y abstractmethod para crear clases abstractas.
from abc import ABC, abstractmethod

# Importamos logging para registrar eventos y errores.
import logging

# Importamos datetime para trabajar con fechas y horas.
from datetime import datetime

# Importamos os para trabajar con archivos y rutas.
import os


# ================================================================
# CONFIGURACION DEL ARCHIVO DE LOGS
# ================================================================

# Obtenemos la carpeta donde está guardado el programa.
CARPETA_PROGRAMA = os.path.dirname(os.path.abspath(__file__))

# Creamos la ruta del archivo de registros en esa carpeta.
RUTA_LOG = os.path.join(CARPETA_PROGRAMA, "software_fj.log")

# Configuramos el archivo donde se guardarán los eventos y errores.
logging.basicConfig(
    filename=RUTA_LOG,  # Guarda el archivo junto al programa.
    level=logging.INFO,  # Nivel de información que se guardará.
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato de los registros.
    encoding="utf-8"  # Permite guardar caracteres especiales.
)


# ================================================================
# EXCEPCIONES PERSONALIZADAS
# ================================================================

# Creamos una excepcion general para el sistema.
class ErrorSistema(Exception):
    pass  # Permite identificar errores propios del proyecto.


# Creamos una excepcion para errores de clientes.
class ErrorCliente(ErrorSistema):
    pass  # Hereda de la excepcion general.


# Creamos una excepcion para errores de servicios.
class ErrorServicio(ErrorSistema):
    pass  # Hereda de la excepcion general.


# Creamos una excepcion para errores de reservas.
class ErrorReserva(ErrorSistema):
    pass  # Hereda de la excepcion general.


# Creamos una excepcion para operaciones con estados incorrectos.
class EstadoReservaInvalido(ErrorReserva):
    pass  # Hereda de la excepcion de reservas.


# ================================================================
# CLASE ABSTRACTA GENERAL: ENTIDAD
# ================================================================

# Creamos una clase abstracta que representa las entidades del sistema.
class Entidad(ABC):

    # Inicializamos el identificador de cada entidad.
    def __init__(self, identificador):

        # Validamos que el identificador no este vacio.
        if not identificador or not str(identificador).strip():

            # Generamos un error si el identificador no es valido.
            raise ValueError("El identificador no puede estar vacio.")

        # Guardamos el identificador como atributo protegido.
        self._identificador = str(identificador).strip()

    # Creamos una propiedad para consultar el identificador.
    @property
    def identificador(self):

        # Devolvemos el identificador almacenado.
        return self._identificador

    # Obligamos a las clases hijas a implementar este metodo.
    @abstractmethod
    def describir(self):

        # La implementacion se realiza en las clases derivadas.
        pass


# ================================================================
# CLASE CLIENTE
# ================================================================

# Creamos la clase Cliente heredando de Entidad.
class Cliente(Entidad):

    # Inicializamos los datos personales del cliente.
    def __init__(self, identificador, nombre, correo, telefono):

        # Inicializamos el identificador desde la clase padre.
        super().__init__(identificador)

        # Asignamos el nombre utilizando su propiedad de validacion.
        self.nombre = nombre

        # Asignamos el correo utilizando su propiedad de validacion.
        self.correo = correo

        # Asignamos el telefono utilizando su propiedad de validacion.
        self.telefono = telefono

        # Registramos la creacion del cliente en el archivo de logs.
        logging.info("Cliente registrado: %s", self.identificador)

    # Creamos una propiedad para consultar el nombre.
    @property
    def nombre(self):

        # Devolvemos el nombre privado.
        return self.__nombre

    # Creamos el metodo para modificar y validar el nombre.
    @nombre.setter
    def nombre(self, valor):

        # Comprobamos que el nombre sea texto y tenga minimo tres caracteres.
        if not isinstance(valor, str) or len(valor.strip()) < 3:

            # Generamos una excepcion si el nombre no es valido.
            raise ErrorCliente("El nombre debe tener al menos tres caracteres.")

        # Guardamos el nombre sin espacios externos.
        self.__nombre = valor.strip()

    # Creamos una propiedad para consultar el correo.
    @property
    def correo(self):

        # Devolvemos el correo privado.
        return self.__correo

    # Creamos el metodo para modificar y validar el correo.
    @correo.setter
    def correo(self, valor):

        # Comprobamos que el correo tenga un formato basico valido.
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:

            # Generamos una excepcion si el correo es incorrecto.
            raise ErrorCliente("El correo electronico no tiene un formato valido.")

        # Guardamos el correo sin espacios externos.
        self.__correo = valor.strip()

    # Creamos una propiedad para consultar el telefono.
    @property
    def telefono(self):

        # Devolvemos el telefono privado.
        return self.__telefono

    # Creamos el metodo para modificar y validar el telefono.
    @telefono.setter
    def telefono(self, valor):

        # Convertimos el telefono a texto y eliminamos espacios.
        telefono_limpio = str(valor).strip()

        # Comprobamos que contenga numeros y minimo siete digitos.
        if not telefono_limpio.isdigit() or len(telefono_limpio) < 7:

            # Generamos una excepcion si el telefono es incorrecto.
            raise ErrorCliente("El telefono debe contener al menos siete digitos.")

        # Guardamos el telefono validado.
        self.__telefono = telefono_limpio

    # Implementamos el metodo abstracto de la clase Entidad.
    def describir(self):

        # Devolvemos la informacion del cliente.
        return f"Cliente: {self.nombre} | Correo: {self.correo} | Telefono: {self.telefono}"


# ================================================================
# CLASE ABSTRACTA SERVICIO
# ================================================================

# Creamos la clase abstracta Servicio que hereda de Entidad.
class Servicio(Entidad, ABC):

    # Inicializamos los datos generales de cada servicio.
    def __init__(self, identificador, nombre, tarifa_base):

        # Inicializamos el identificador desde la clase padre.
        super().__init__(identificador)

        # Validamos que el nombre del servicio sea correcto.
        if not isinstance(nombre, str) or not nombre.strip():

            # Generamos un error cuando el nombre esta vacio.
            raise ErrorServicio("El nombre del servicio es obligatorio.")

        # Validamos que la tarifa sea numerica y positiva.
        if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool) or tarifa_base <= 0:

            # Generamos un error si la tarifa no es valida.
            raise ErrorServicio("La tarifa base debe ser mayor que cero.")

        # Guardamos el nombre del servicio.
        self._nombre = nombre.strip()

        # Guardamos la tarifa como numero decimal.
        self._tarifa_base = float(tarifa_base)

        # Inicializamos el servicio como disponible.
        self._disponible = True

    # Creamos una propiedad para consultar el nombre.
    @property
    def nombre(self):

        # Devolvemos el nombre del servicio.
        return self._nombre

    # Creamos una propiedad para consultar la disponibilidad.
    @property
    def disponible(self):

        # Devolvemos el estado de disponibilidad.
        return self._disponible

    # Creamos un metodo para cambiar la disponibilidad.
    def cambiar_disponibilidad(self, estado):

        # Comprobamos que el estado sea verdadero o falso.
        if not isinstance(estado, bool):

            # Generamos un error si el valor no es booleano.
            raise ErrorServicio("La disponibilidad debe ser un valor booleano.")

        # Actualizamos la disponibilidad.
        self._disponible = estado

        # Registramos el cambio en el archivo de logs.
        logging.info("Disponibilidad del servicio %s: %s", self.identificador, estado)

    # Obligamos a las clases hijas a implementar el calculo de costos.
    @abstractmethod
    def calcular_costo(self, duracion, *args, **kwargs):

        # Cada servicio tendra su propia formula de calculo.
        pass

    # Obligamos a las clases hijas a validar los parametros.
    @abstractmethod
    def validar_parametros(self, duracion):

        # Cada servicio realizara sus propias validaciones.
        pass

    # Obligamos a las clases hijas a describir sus caracteristicas.
    @abstractmethod
    def describir(self):

        # Cada servicio implementara su descripcion.
        pass


# ================================================================
# SERVICIO ESPECIALIZADO: RESERVA DE SALAS
# ================================================================

# Creamos la clase ServicioSala heredando de Servicio.
class ServicioSala(Servicio):

    # Inicializamos los datos propios de una sala.
    def __init__(self, identificador, nombre, tarifa_base, capacidad):

        # Inicializamos los datos generales del servicio.
        super().__init__(identificador, nombre, tarifa_base)

        # Validamos que la capacidad sea un numero entero positivo.
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:

            # Generamos un error cuando la capacidad es incorrecta.
            raise ErrorServicio("La capacidad debe ser un entero positivo.")

        # Guardamos la capacidad maxima de la sala.
        self.capacidad = capacidad

    # Validamos la duracion de la reserva de la sala.
    def validar_parametros(self, duracion):

        # Comprobamos que la duracion sea numerica y positiva.
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:

            # Generamos un error si la duracion no es valida.
            raise ErrorServicio("La duracion debe ser mayor que cero.")

        # Comprobamos que no supere doce horas.
        if duracion > 12:

            # Generamos un error si supera el limite permitido.
            raise ErrorServicio("La sala no se puede reservar por mas de doce horas.")

    # Calculamos el costo de la reserva de sala.
    def calcular_costo(self, duracion, *args, **kwargs):

        # Validamos primero la duracion.
        self.validar_parametros(duracion)

        # Obtenemos la cantidad de personas o utilizamos una por defecto.
        personas = kwargs.get("personas", 1)

        # Obtenemos el impuesto o utilizamos el diecinueve por ciento.
        impuesto = kwargs.get("impuesto", 0.19)

        # Obtenemos el descuento o utilizamos cero por defecto.
        descuento = kwargs.get("descuento", 0)

        # Validamos que las personas no superen la capacidad.
        if not isinstance(personas, int) or isinstance(personas, bool) or personas < 1 or personas > self.capacidad:

            # Generamos un error si la cantidad de personas no es valida.
            raise ErrorServicio("La cantidad de personas supera la capacidad de la sala.")

        # Validamos que el impuesto este entre cero y uno.
        if not isinstance(impuesto, (int, float)) or isinstance(impuesto, bool) or not 0 <= impuesto <= 1:

            # Generamos un error si el impuesto es incorrecto.
            raise ErrorServicio("El impuesto debe estar entre cero y uno.")

        # Validamos que el descuento este entre cero y uno.
        if not isinstance(descuento, (int, float)) or isinstance(descuento, bool) or not 0 <= descuento <= 1:

            # Generamos un error si el descuento es incorrecto.
            raise ErrorServicio("El descuento debe estar entre cero y uno.")

        # Calculamos el costo antes de impuestos y descuentos.
        subtotal = self._tarifa_base * duracion

        # Aplicamos el descuento y posteriormente el impuesto.
        total = subtotal * (1 - descuento) * (1 + impuesto)

        # Devolvemos el costo final con dos decimales.
        return round(total, 2)

    # Implementamos la descripcion especifica de la sala.
    def describir(self):

        # Devolvemos las caracteristicas principales de la sala.
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas | Tarifa por hora: ${self._tarifa_base:.2f}"


# ================================================================
# SERVICIO ESPECIALIZADO: ALQUILER DE EQUIPOS
# ================================================================

# Creamos la clase ServicioEquipo heredando de Servicio.
class ServicioEquipo(Servicio):

    # Inicializamos los datos propios de los equipos.
    def __init__(self, identificador, nombre, tarifa_base, unidades_disponibles):

        # Inicializamos los datos generales del servicio.
        super().__init__(identificador, nombre, tarifa_base)

        # Validamos que las unidades sean un entero igual o mayor que cero.
        if not isinstance(unidades_disponibles, int) or isinstance(unidades_disponibles, bool) or unidades_disponibles < 0:

            # Generamos un error cuando las unidades son incorrectas.
            raise ErrorServicio("Las unidades disponibles deben ser un entero igual o mayor que cero.")

        # Guardamos la cantidad de equipos disponibles.
        self.unidades_disponibles = unidades_disponibles

    # Validamos la duracion del alquiler.
    def validar_parametros(self, duracion):

        # Comprobamos que la duracion sea numerica y positiva.
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:

            # Generamos un error si la duracion no es valida.
            raise ErrorServicio("La duracion del alquiler debe ser mayor que cero.")

        # Comprobamos que no supere treinta dias.
        if duracion > 30:

            # Generamos un error si supera el limite permitido.
            raise ErrorServicio("El alquiler no puede superar treinta dias.")

    # Calculamos el costo del alquiler de equipos.
    def calcular_costo(self, duracion, *args, **kwargs):

        # Validamos primero la duracion del alquiler.
        self.validar_parametros(duracion)

        # Obtenemos la cantidad solicitada o utilizamos una unidad.
        cantidad = kwargs.get("cantidad", 1)

        # Obtenemos el impuesto o utilizamos el diecinueve por ciento.
        impuesto = kwargs.get("impuesto", 0.19)

        # Obtenemos el descuento o utilizamos cero por defecto.
        descuento = kwargs.get("descuento", 0)

        # Validamos que la cantidad sea un entero positivo.
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1:

            # Generamos un error cuando la cantidad no es valida.
            raise ErrorServicio("La cantidad de equipos debe ser un entero positivo.")

        # Comprobamos que existan suficientes equipos.
        if cantidad > self.unidades_disponibles:

            # Generamos un error si no hay equipos suficientes.
            raise ErrorServicio("No hay suficientes equipos disponibles.")

        # Validamos que el impuesto este entre cero y uno.
        if not isinstance(impuesto, (int, float)) or isinstance(impuesto, bool) or not 0 <= impuesto <= 1:

            # Generamos un error si el impuesto es incorrecto.
            raise ErrorServicio("El impuesto debe estar entre cero y uno.")

        # Validamos que el descuento este entre cero y uno.
        if not isinstance(descuento, (int, float)) or isinstance(descuento, bool) or not 0 <= descuento <= 1:

            # Generamos un error si el descuento es incorrecto.
            raise ErrorServicio("El descuento debe estar entre cero y uno.")

        # Calculamos el costo segun los dias y equipos solicitados.
        subtotal = self._tarifa_base * duracion * cantidad

        # Aplicamos el descuento y posteriormente el impuesto.
        total = subtotal * (1 - descuento) * (1 + impuesto)

        # Devolvemos el costo final con dos decimales.
        return round(total, 2)

    # Implementamos la descripcion especifica del equipo.
    def describir(self):

        # Devolvemos las caracteristicas principales del equipo.
        return f"Equipo: {self.nombre} | Unidades disponibles: {self.unidades_disponibles} | Tarifa diaria: ${self._tarifa_base:.2f}"


# ================================================================
# SERVICIO ESPECIALIZADO: ASESORIAS
# ================================================================

# Creamos la clase ServicioAsesoria heredando de Servicio.
class ServicioAsesoria(Servicio):

    # Inicializamos los datos propios de la asesoria.
    def __init__(self, identificador, nombre, tarifa_base, especialidad):

        # Inicializamos los datos generales del servicio.
        super().__init__(identificador, nombre, tarifa_base)

        # Validamos que la especialidad no este vacia.
        if not isinstance(especialidad, str) or not especialidad.strip():

            # Generamos un error cuando falta la especialidad.
            raise ErrorServicio("La especialidad de la asesoria es obligatoria.")

        # Guardamos la especialidad de la asesoria.
        self.especialidad = especialidad.strip()

    # Validamos la duracion de la asesoria.
    def validar_parametros(self, duracion):

        # Comprobamos que la duracion sea numerica y positiva.
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:

            # Generamos un error si la duracion no es valida.
            raise ErrorServicio("La duracion de la asesoria debe ser mayor que cero.")

        # Comprobamos que no supere ocho horas.
        if duracion > 8:

            # Generamos un error si supera el limite permitido.
            raise ErrorServicio("La asesoria no puede superar ocho horas.")

    # Calculamos el costo de la asesoria.
    def calcular_costo(self, duracion, *args, **kwargs):

        # Validamos primero la duracion de la asesoria.
        self.validar_parametros(duracion)

        # Obtenemos la modalidad o utilizamos virtual por defecto.
        modalidad = kwargs.get("modalidad", "virtual")

        # Obtenemos el impuesto o utilizamos el diecinueve por ciento.
        impuesto = kwargs.get("impuesto", 0.19)

        # Obtenemos el descuento o utilizamos cero por defecto.
        descuento = kwargs.get("descuento", 0)

        # Comprobamos que la modalidad sea virtual o presencial.
        if modalidad not in ("virtual", "presencial"):

            # Generamos un error cuando la modalidad no es permitida.
            raise ErrorServicio("La modalidad debe ser virtual o presencial.")

        # Validamos que el impuesto este entre cero y uno.
        if not isinstance(impuesto, (int, float)) or isinstance(impuesto, bool) or not 0 <= impuesto <= 1:

            # Generamos un error si el impuesto es incorrecto.
            raise ErrorServicio("El impuesto debe estar entre cero y uno.")

        # Validamos que el descuento este entre cero y uno.
        if not isinstance(descuento, (int, float)) or isinstance(descuento, bool) or not 0 <= descuento <= 1:

            # Generamos un error si el descuento es incorrecto.
            raise ErrorServicio("El descuento debe estar entre cero y uno.")

        # Aplicamos un veinte por ciento adicional si la modalidad es presencial.
        factor_modalidad = 1.20 if modalidad == "presencial" else 1.00

        # Calculamos el subtotal segun duracion y modalidad.
        subtotal = self._tarifa_base * duracion * factor_modalidad

        # Aplicamos el descuento y posteriormente el impuesto.
        total = subtotal * (1 - descuento) * (1 + impuesto)

        # Devolvemos el costo final con dos decimales.
        return round(total, 2)

    # Implementamos la descripcion especifica de la asesoria.
    def describir(self):

        # Devolvemos las caracteristicas principales de la asesoria.
        return f"Asesoria: {self.nombre} | Especialidad: {self.especialidad} | Tarifa por hora: ${self._tarifa_base:.2f}"


# ================================================================
# CLASE RESERVA
# ================================================================

# Se crea la clase Reserva, que hereda de la clase abstracta Entidad.
class Reserva(Entidad):

    # Se define el metodo constructor para crear una reserva.
    def __init__(self, identificador, cliente, servicio, duracion, **opciones):

        # Se inicializa el identificador heredado de la clase Entidad.
        super().__init__(identificador)

        # Se verifica que el cliente sea un objeto de la clase Cliente.
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("El cliente seleccionado no es valido.")

        # Se verifica que el servicio pertenezca a la clase Servicio.
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("El servicio seleccionado no es valido.")

        # Se validan los parametros de duracion del servicio.
        servicio.validar_parametros(duracion)

        # Se guarda el cliente asociado a la reserva.
        self.cliente = cliente

        # Se guarda el servicio seleccionado para la reserva.
        self.servicio = servicio

        # Se almacena la duracion solicitada.
        self.duracion = duracion

        # Se guardan las opciones adicionales del servicio.
        self.opciones = opciones

        # Se establece el estado inicial de la reserva.
        self.estado = "Pendiente"

        # Se inicializa el costo de la reserva en cero.
        self.costo = 0.0

        # Se registra en el archivo de logs la creacion de la reserva.
        logging.info("Reserva %s creada correctamente.", self.identificador)

    # Se define el metodo para confirmar una reserva.
    def confirmar(self):

        # Se verifica que la reserva se encuentre pendiente.
        if self.estado != "Pendiente":
            raise EstadoReservaInvalido("La reserva no se encuentra pendiente.")

        # Se verifica que el servicio este disponible.
        if not self.servicio.disponible:
            raise ErrorReserva("El servicio seleccionado no esta disponible.")

        # Se inicia el bloque para calcular y confirmar la reserva.
        try:

            # Se calcula el costo utilizando el metodo del servicio correspondiente.
            self.costo = self.servicio.calcular_costo(self.duracion, **self.opciones)

            # Se verifica que el costo sea numerico y mayor que cero.
            if not isinstance(self.costo, (int, float)) or self.costo <= 0:
                raise ErrorServicio("El costo calculado no es valido.")

            # Se cambia el estado de la reserva a confirmada.
            self.estado = "Confirmada"

            # Se registra la confirmacion en el archivo de logs.
            logging.info("Reserva %s confirmada.", self.identificador)

        # Se capturan los errores relacionados con el sistema.
        except ErrorSistema as error:

            # Se registra el error ocurrido durante la confirmacion.
            logging.exception("Error al confirmar la reserva %s.", self.identificador)

            # Se genera una nueva excepcion conservando el error original.
            raise ErrorReserva("La reserva no pudo ser confirmada.") from error

    # Se define el metodo para cancelar una reserva.
    def cancelar(self):

        # Se verifica que la reserva pueda ser cancelada.
        if self.estado not in ("Pendiente", "Confirmada"):
            raise EstadoReservaInvalido("No se puede cancelar esta reserva.")

        # Se cambia el estado de la reserva a cancelada.
        self.estado = "Cancelada"

        # Se registra la cancelacion en el archivo de logs.
        logging.info("Reserva %s cancelada.", self.identificador)

    # Se define el metodo para procesar una reserva.
    def procesar(self):

        # Se verifica que la reserva este confirmada.
        if self.estado != "Confirmada":
            raise EstadoReservaInvalido("Solo se pueden procesar reservas confirmadas.")

        # Se cambia el estado de la reserva a procesada.
        self.estado = "Procesada"

        # Se registra el procesamiento en el archivo de logs.
        logging.info("Reserva %s procesada.", self.identificador)

    # Se define el metodo para mostrar la informacion de la reserva.
    def describir(self):

        # Se devuelve una descripcion con los datos principales de la reserva.
        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duracion: {self.duracion} | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo:,.2f}"
        )


# ================================================================
# CLASE PRINCIPAL DEL SISTEMA
# ================================================================

# Se crea la clase principal que administra el sistema Software FJ.
class SistemaSoftwareFJ:

    # Se define el constructor de la clase principal.
    def __init__(self):

        # Se crea una lista para almacenar los clientes registrados.
        self.clientes = []

        # Se crea una lista para almacenar los servicios disponibles.
        self.servicios = []

        # Se crea una lista para almacenar las reservas realizadas.
        self.reservas = []

        # Se registra el inicio del sistema en el archivo de logs.
        logging.info("Sistema Software FJ iniciado correctamente.")

    # Se define el metodo para registrar un cliente.
    def registrar_cliente(self, cliente):

        # Se verifica que el objeto recibido sea un cliente.
        if not isinstance(cliente, Cliente):
            raise ErrorCliente("El objeto recibido no corresponde a un cliente.")

        # Se verifica que no exista otro cliente con el mismo identificador.
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ErrorCliente("Ya existe un cliente con ese identificador.")

        # Se agrega el cliente a la lista de clientes.
        self.clientes.append(cliente)

        # Se registra la operacion en el archivo de logs.
        logging.info("Cliente %s registrado correctamente.", cliente.nombre)

        # Se devuelve un mensaje de confirmacion.
        return "Cliente registrado correctamente."

    # Se define el metodo para agregar un servicio.
    def agregar_servicio(self, servicio):

        # Se verifica que el objeto recibido sea un servicio.
        if not isinstance(servicio, Servicio):
            raise ErrorServicio("El objeto recibido no corresponde a un servicio.")

        # Se verifica que no exista otro servicio con el mismo identificador.
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ErrorServicio("Ya existe un servicio con ese identificador.")

        # Se agrega el servicio a la lista de servicios.
        self.servicios.append(servicio)

        # Se registra la operacion en el archivo de logs.
        logging.info("Servicio %s agregado correctamente.", servicio.nombre)

        # Se devuelve un mensaje de confirmacion.
        return "Servicio agregado correctamente."

    # Se define el metodo para crear una nueva reserva.
    def crear_reserva(self, identificador, cliente, servicio, duracion, **opciones):

        # Se verifica que el cliente este registrado en el sistema.
        if cliente not in self.clientes:
            raise ErrorReserva("El cliente no esta registrado en el sistema.")

        # Se verifica que el servicio este registrado en el sistema.
        if servicio not in self.servicios:
            raise ErrorReserva("El servicio no esta registrado en el sistema.")

        # Se crea el objeto de reserva con los datos recibidos.
        reserva = Reserva(identificador, cliente, servicio, duracion, **opciones)

        # Se agrega la reserva a la lista de reservas.
        self.reservas.append(reserva)

        # Se registra la creacion en el archivo de logs.
        logging.info("Reserva %s agregada al sistema.", identificador)

        # Se devuelve el objeto de reserva creado.
        return reserva

    # Se define el metodo para buscar una reserva por su identificador.
    def buscar_reserva(self, identificador):

        # Se recorre la lista de reservas para encontrar la solicitada.
        for reserva in self.reservas:

            # Se compara el identificador de cada reserva.
            if reserva.identificador == identificador:

                # Se devuelve la reserva encontrada.
                return reserva

        # Se genera un error cuando no se encuentra la reserva.
        raise ErrorReserva("No se encontro una reserva con ese identificador.")

    # Se define el metodo para mostrar un resumen del sistema.
    def mostrar_resumen(self):

        # Se muestra el titulo del resumen.
        print("\n========== RESUMEN DEL SISTEMA SOFTWARE FJ ==========")

        # Se muestra la cantidad total de clientes registrados.
        print(f"Clientes registrados: {len(self.clientes)}")

        # Se muestra la cantidad total de servicios disponibles.
        print(f"Servicios registrados: {len(self.servicios)}")

        # Se muestra la cantidad total de reservas realizadas.
        print(f"Reservas registradas: {len(self.reservas)}")

        # Se muestra un encabezado para la informacion de las reservas.
        print("\nDETALLE DE LAS RESERVAS:")

        # Se recorre la lista de reservas para mostrar su informacion.
        for reserva in self.reservas:

            # Se imprime la descripcion de cada reserva.
            print(reserva.describir())

        # Se muestra una linea de cierre del resumen.
        print("=====================================================")


# ================================================================
# FUNCION PARA EJECUTAR Y CONTROLAR LAS PRUEBAS
# ================================================================

# Se define una funcion para ejecutar pruebas y controlar los posibles errores.
def ejecutar_prueba(nombre, funcion):

    # Se muestra el nombre de la prueba que se va a ejecutar.
    print(f"\n[PRUEBA] {nombre}")

    # Se inicia el bloque para controlar posibles excepciones.
    try:

        # Se ejecuta la funcion recibida como parametro.
        resultado = funcion()

    # Se capturan los errores personalizados del sistema.
    except ErrorSistema as error:

        # Se muestra el mensaje del error encontrado.
        print(f"Error controlado: {error}")

        # Se registra el error en el archivo de logs.
        logging.error("Prueba '%s': %s", nombre, error)

    # Se capturan errores de tipo o de valor.
    except (TypeError, ValueError) as error:

        # Se muestra el mensaje del error encontrado.
        print(f"Error de datos: {error}")

        # Se registra el error en el archivo de logs.
        logging.error("Prueba '%s': %s", nombre, error)

    # Se capturan otros errores inesperados.
    except Exception as error:

        # Se muestra el mensaje del error inesperado.
        print(f"Error inesperado: {error}")

        # Se registra el error inesperado en el archivo de logs.
        logging.exception("Prueba '%s' produjo un error inesperado.", nombre)

    # Se ejecuta cuando no se presento ninguna excepcion.
    else:

        # Se muestra el resultado de la operacion exitosa.
        print(f"Resultado: {resultado}")

    # Se ejecuta siempre, haya ocurrido un error o no.
    finally:

        # Se muestra un mensaje indicando que termino la prueba.
        print("Finalizacion de la prueba.")


# ================================================================
# FUNCION PRINCIPAL DEL PROGRAMA
# ================================================================

# Se define la funcion principal del programa.
def main():

    # Se muestra el nombre del sistema en pantalla.
    print("==============================================")
    print("       SISTEMA INTEGRAL SOFTWARE FJ")
    print(" Gestion de clientes, servicios y reservas")
    print("==============================================")

    # Se crea una instancia del sistema principal.
    sistema = SistemaSoftwareFJ()

    # Se crean los clientes que participaran en las pruebas.
    cliente1 = Cliente("C001", "Juan Perez", "juan@gmail.com", "3001234567")
    cliente2 = Cliente("C002", "Maria Gomez", "maria@gmail.com", "3101234567")
    cliente3 = Cliente("C003", "Carlos Ruiz", "carlos@gmail.com", "3201234567")

    # Se registran los clientes en el sistema.
    ejecutar_prueba("Registrar cliente Juan", lambda: sistema.registrar_cliente(cliente1))
    ejecutar_prueba("Registrar cliente Maria", lambda: sistema.registrar_cliente(cliente2))
    ejecutar_prueba("Registrar cliente Carlos", lambda: sistema.registrar_cliente(cliente3))

    # Se intenta registrar un cliente duplicado.
    ejecutar_prueba("Registrar cliente duplicado", lambda: sistema.registrar_cliente(cliente1))

    # Se crean los servicios disponibles con los parametros correctos.
    sala = ServicioSala("S001", "Sala de reuniones", 50000, 10)
    equipo = ServicioEquipo("S002", "Alquiler de computador", 20000, 5)

    # La especialidad debe ser texto; no se debe enviar True.
    asesoria = ServicioAsesoria("S003", "Asesoria tecnologica", 80000, "Tecnologia")

    # Se agregan los servicios al sistema.
    ejecutar_prueba("Agregar servicio de sala", lambda: sistema.agregar_servicio(sala))
    ejecutar_prueba("Agregar servicio de equipos", lambda: sistema.agregar_servicio(equipo))
    ejecutar_prueba("Agregar servicio de asesoria", lambda: sistema.agregar_servicio(asesoria))

    # Se intenta agregar un servicio duplicado.
    ejecutar_prueba("Agregar servicio duplicado", lambda: sistema.agregar_servicio(sala))

    # Se crea y confirma una reserva de sala.
    reserva1 = sistema.crear_reserva("R001", cliente1, sala, 2)
    ejecutar_prueba("Confirmar reserva de sala", reserva1.confirmar)

    # Se procesa la reserva de sala.
    ejecutar_prueba("Procesar reserva de sala", reserva1.procesar)

    # Se crea y confirma una reserva de equipos.
    reserva2 = sistema.crear_reserva("R002", cliente2, equipo, 3, cantidad=2)
    ejecutar_prueba("Confirmar reserva de equipos", reserva2.confirmar)

    # Se crea y confirma una reserva de asesoria.
    reserva3 = sistema.crear_reserva("R003", cliente3, asesoria, 4, modalidad="virtual")
    ejecutar_prueba("Confirmar reserva de asesoria", reserva3.confirmar)

    # Se cancela la reserva de asesoria.
    ejecutar_prueba("Cancelar reserva de asesoria", reserva3.cancelar)

    # Se intenta procesar una reserva cancelada.
    ejecutar_prueba("Procesar reserva cancelada", reserva3.procesar)

    # Se intenta confirmar nuevamente una reserva procesada.
    ejecutar_prueba("Confirmar reserva procesada", reserva1.confirmar)

    # Se intenta crear una reserva con un cliente no registrado.
    ejecutar_prueba(
        "Crear reserva con cliente no registrado",
        lambda: sistema.crear_reserva(
            "R004",
            Cliente("C004", "Pedro", "pedro@gmail.com", "3000000000"),
            sala,
            2
        )
    )

    # Se intenta crear una reserva con duracion invalida.
    ejecutar_prueba(
        "Crear reserva con duracion invalida",
        lambda: sistema.crear_reserva("R005", cliente1, sala, -2)
    )

    # Se crea un servicio de sala que inicialmente no estara disponible.
    servicio_no_disponible = ServicioSala("S004", "Sala ocupada", 40000, 5)

    # Se cambia la disponibilidad usando el metodo definido en la clase Servicio.
    servicio_no_disponible.cambiar_disponibilidad(False)

    # Se agrega el servicio no disponible al sistema.
    sistema.agregar_servicio(servicio_no_disponible)

    # Se crea una reserva con el servicio no disponible.
    reserva4 = sistema.crear_reserva("R006", cliente1, servicio_no_disponible, 2)

    # Se intenta confirmar la reserva del servicio no disponible.
    ejecutar_prueba("Confirmar servicio no disponible", reserva4.confirmar)

    # Se intenta buscar una reserva inexistente.
    ejecutar_prueba("Buscar reserva inexistente", lambda: sistema.buscar_reserva("R999"))

    # Se crea una reserva con una cantidad de equipos invalida.
    reserva_encadenada = sistema.crear_reserva("R007", cliente2, equipo, 2, cantidad=0)

    # Se inicia el bloque para demostrar el encadenamiento de excepciones.
    try:

        # Se intenta confirmar la reserva con una cantidad invalida.
        reserva_encadenada.confirmar()

    # Se captura el error generado durante la confirmacion.
    except ErrorReserva as error:

        # Se muestra el error principal.
        print(f"\nError principal: {error}")

        # Se verifica si existe una excepcion original.
        if error.__cause__ is not None:

            # Se muestra el error original encadenado.
            print(f"Error original encadenado: {error.__cause__}")

        # Se registra el encadenamiento de excepciones en el archivo de logs.
        logging.exception("Prueba de encadenamiento de excepciones.")

    # Se ejecuta cuando no ocurre ningun error.
    else:

        # Se muestra un mensaje de confirmacion.
        print("La reserva se confirmo sin errores.")

    # Se ejecuta siempre al finalizar la prueba.
    finally:

        # Se informa que termino la prueba.
        print("Finalizo la prueba de encadenamiento.")

    # Se prueba el calculo del costo de alquiler de equipos.
    ejecutar_prueba(
        "Calcular costo de alquiler de equipos",
        lambda: equipo.calcular_costo(2, cantidad=2)
    )

    # Se prueba la descripcion del servicio de sala.
    ejecutar_prueba("Describir servicio de sala", sala.describir)

    # Se muestra el resumen general del sistema.
    sistema.mostrar_resumen()

    # Se registra la finalizacion del programa.
    logging.info("Programa Software FJ finalizado correctamente.")

    # Se muestra el mensaje final en pantalla.
    print("\nEl sistema Software FJ termino su ejecucion correctamente.")


# Se verifica que el archivo se este ejecutando directamente.
if __name__ == "__main__":

    # Se llama a la funcion principal para iniciar el programa.
    main()
