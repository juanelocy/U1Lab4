import datetime
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase


class VacacionesEcuador(HolidayBase):
    """
    Una clase para representar un feriado en Ecuador por provincia (Vacaciones Ecuador) 
    Tiene como objetivo que determinar si una fecha específica es un feriado 
    de la manera más rápida y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase VacacionesEcuador)
    ----------
    prueba: calle
        código de provincia según ISO3166-2
    Métodos
    -------
    __init__(self, placa, fecha, tiempo, online=Falso):
        Construye todos los atributos necesarios para el objeto HolidayEcuador.
    _populate(self, anio):
        Devoluciones si una fecha es feriado o no
    """     
    # ISO 3166-2 codigos de la principal subdivision, 
    # Provincias llamadas
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCIAS = ["EC-P"]  # TODO añadir mas provincias

    def __init__(self, **kwargs):
        """
        Construye todos los atributos necesarios para el objeto HolidayEcuador.
        """         
        self.pais = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, anio):
        """
        Verifica si la fecha es vacacion o no
        
        Parametros
        ----------
        anio : str
            anio de la fecha
        Retorna
        -------
        Devuelve verdadero si una fecha es un día festivo, de lo contrario,
        se muestra como verdadero.
        """                    
        #Dia de anio nuevo 
        self[datetime.date(anio, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(anio, DEC, 25)] = "Navidad [Christmas]"
        
        #Semana Santa
        self[easter(anio) + rd(diaLab=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(anio)] = "Día de Pascuas [Easter dia]"
        
        # Carnaval
        cuaresma = 46
        self[easter(anio) - datetime.timedelta(dias=cuaresma+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(anio) - datetime.timedelta(dias=cuaresma+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Dia del trabajo
        nombre = "Día Nacional del Trabajo [Labour dia]"
        # (Ley 858/Ley Reformatoria a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al viernes o lunes inmediato anterior
        # respectivamente
        if anio > 2015 and datetime.date(anio, MAY, 1).diaLab() in (5,1):
            self[datetime.date(anio, MAY, 1) - datetime.timedelta(dias=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) si el feriado cae en domingo
         # el descanso obligatorio sera para el lunes siguiente
        elif anio > 2015 and datetime.date(anio, MAY, 1).diaLab() == 6:
            self[datetime.date(anio, MAY, 1) + datetime.timedelta(dias=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
         # se moverá al viernes de esa semana
        elif anio > 2015 and  datetime.date(anio, MAY, 1).diaLab() in (2,3):
            self[datetime.date(anio, MAY, 1) + rd(diaLab=FR)] = nombre
        else:
            self[datetime.date(anio, MAY, 1)] = nombre
        
        # Batalla de Pichincha, las reglas son las mismas que el día del trabajo
        nombre = "Batalla del Pichincha [Pichincha Battle]"
        if anio > 2015 and datetime.date(anio, MAY, 24).diaLab() in (5,1):
            self[datetime.date(anio, MAY, 24).diaLab() - datetime.timedelta(dias=1)] = nombre
        elif anio > 2015 and datetime.date(anio, MAY, 24).diaLab() == 6:
            self[datetime.date(anio, MAY, 24) + datetime.timedelta(dias=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, MAY, 24).diaLab() in (2,3):
            self[datetime.date(anio, MAY, 24) + rd(diaLab=FR)] = nombre
        else:
            self[datetime.date(anio, MAY, 24)] = nombre        
        
        # Primer Grito de Independencia, las reglas son las mismas que el día del trabajo  
        nombre = "Primer Grito de la Independencia [First Cry of Independence]"
        if anio > 2015 and datetime.date(anio, AUG, 10).diaLab() in (5,1):
            self[datetime.date(anio, AUG, 10)- datetime.timedelta(dias=1)] = nombre
        elif anio > 2015 and datetime.date(anio, AUG, 10).diaLab() == 6:
            self[datetime.date(anio, AUG, 10) + datetime.timedelta(dias=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, AUG, 10).diaLab() in (2,3):
            self[datetime.date(anio, AUG, 10) + rd(diaLab=FR)] = nombre
        else:
            self[datetime.date(anio, AUG, 10)] = nombre       
        
        # Guayaquil's independence, the rules are the same as the labor dia
        nombre = "Independencia de Guayaquil [Guayaquil's Independence]"
        if anio > 2015 and datetime.date(anio, OCT, 9).diaLab() in (5,1):
            self[datetime.date(anio, OCT, 9) - datetime.timedelta(dias=1)] = nombre
        elif anio > 2015 and datetime.date(anio, OCT, 9).diaLab() == 6:
            self[datetime.date(anio, OCT, 9) + datetime.timedelta(dias=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, MAY, 1).diaLab() in (2,3):
            self[datetime.date(anio, OCT, 9) + rd(diaLab=FR)] = nombre
        else:
            self[datetime.date(anio, OCT, 9)] = nombre        
        
        # Dia de muertos y 
        nombredd = "Día de los difuntos [dia of the Dead]" 
        # Independencia de cuenca
        nombreic = "Independencia de Cuenca [Independence of Cuenca]"
        #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906))
        #Para festivos nacionales y/o locales que coincidan en días corridos,
        #se aplicarán las siguientes reglas:
        if (datetime.date(anio, NOV, 2).diaLab() == 5 and  datetime.date(anio, NOV, 3).diaLab() == 6):
            self[datetime.date(anio, NOV, 2) - datetime.timedelta(dias=1)] = nombredd
            self[datetime.date(anio, NOV, 3) + datetime.timedelta(dias=1)] = nombreic     
        elif (datetime.date(anio, NOV, 3).diaLab() == 2):
            self[datetime.date(anio, NOV, 2)] = nombredd
            self[datetime.date(anio, NOV, 3) - datetime.timedelta(dias=2)] = nombreic
        elif (datetime.date(anio, NOV, 3).diaLab() == 3):
            self[datetime.date(anio, NOV, 3)] = nombreic
            self[datetime.date(anio, NOV, 2) + datetime.timedelta(dias=2)] = nombredd
        elif (datetime.date(anio, NOV, 3).diaLab() == 5):
            self[datetime.date(anio, NOV, 2)] =  nombredd
            self[datetime.date(anio, NOV, 3) - datetime.timedelta(dias=2)] = nombreic
        elif (datetime.date(anio, NOV, 3).diaLab() == 0):
            self[datetime.date(anio, NOV, 3)] = nombreic
            self[datetime.date(anio, NOV, 2) + datetime.timedelta(dias=2)] = nombredd
        else:
            self[datetime.date(anio, NOV, 2)] = nombredd
            self[datetime.date(anio, NOV, 3)] = nombreic  
            
        #Fundacion de Quito, aplica solo en la provincia de Pichincha
        # las reglas son las mismas que el día del trabajo
        name = "Fundación de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if anio > 2015 and datetime.date(anio, DEC, 6).diaLab() in (5,1):
                self[datetime.date(anio, DEC, 6) - datetime.timedelta(dias=1)] = name
            elif anio > 2015 and datetime.date(anio, DEC, 6).diaLab() == 6:
                self[(datetime.date(anio, DEC, 6).diaLab()) + datetime.timedelta(dias=1)] =name
            elif anio > 2015 and  datetime.date(anio, DEC, 6).diaLab() in (2,3):
                self[datetime.date(anio, DEC, 6) + rd(diaLab=FR)] = name
            else:
                self[datetime.date(anio, DEC, 6)] = name

class PicoPlaca:
    """
    Una clase para representar un vehículo.
    medida de restricción (Pico y Placa) 
    - ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    Atributos
    ----------
    placa : str 
        El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
        caracteres que identifican e individualizan el vehículo respecto de los demás;
        
        El formato utilizado es
        XX-YYYY o XXX-YYYY,
        donde X es una letra mayúscula e Y es un dígito.
    fecha : str
        Fecha en la que el vehículo pretende transitar
        esta siguiendo el
        Formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
    hora : str
        tiempo en que el vehículo pretende transitar
        esta siguiendo el formato
        HH:MM: por ejemplo, 08:35, 19:30
    online: boolean, opcional
        if online == Cierto, se utilizará la API abstracta de días festivos
    Metodos
    -------
    __init__(self, placa, fecha, hora, online=False):
        Construye todos los atributos necesarios.
        para el objeto PicoPlaca.
    placa(self):
        Obtiene el valor del atributo de placa
    placa(self, value):
        Establece el valor del atributo de la placa
    fecha(self):
        Obtiene el valor del atributo de fecha
    fecha(self, value):
        Establece el valor del atributo de fecha
    hora(self):
        Obtiene el valor del atributo de tiempo
    hora(self, value):
        Establece el valor del atributo de tiempo
    __EncontrarDia(self, fecha):
        Devuelve el día a partir de la fecha: por ejemplo, miércoles
    __horaProhibida(self, VerificarHora):
        Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, Falso
    __feriado:
        Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, Falso
    predecir(self):
        Devuelve True si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora especificadas, de lo contrario, Falso
    """ 
    #Dias de la semana
    __dias = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"]

    # Diccionario que contiene las restricciones de la forma {día: último dígito prohibido}
    __restricciones = {
            "Monday": [1, 2],
            "Tuesday": [3, 4],
            "Wednesday": [5, 6],
            "Thursday": [7, 8],
            "Friday": [9, 0],
            "Saturday": [],
            "Sunday": []}

    def __init__(self, placa, fecha, tiempo, online=False):
        """
        Construye todos los atributos necesarios para el objeto PicoPlaca.
        
        Parámetros
        ----------
            placa : calle
                El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
                caracteres que identifican e individualizan el vehículo respecto de los demás;
                El formato utilizado es AA-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito.
            fecha: calle
                Fecha en la que el vehículo pretende transitar
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
            tiempo: calle
                tiempo en que el vehículo pretende transitar
                Sigue el formato HH:MM: por ejemplo, 08:35, 19:30
            en línea: booleano, opcional
                si en línea == Verdadero, se usará la API de días festivos abstractos (el valor predeterminado es Falso)               
        """                
        self.placa = placa
        self.fecha = fecha
        self.tiempo = tiempo
        self.online = online


    @property
    def placa(self):
        """Tiene el atributo de la placa un valor"""
        return self._placa


    @placa.setter
    def placa(self, valor):
        """
        Establece el valor del atributo de la placa
        Parámetros
        ----------
        valor: str
        
        aumenta
        ------
        ValorError
            Si la cadena de valor no tiene el formato
            XX-YYYY o XXX-YYYY,
            donde X es una letra mayúscula e Y es un dígito
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', valor):
            raise ValueError(
                'La placa debe tener el siguiente formato: XX-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito')
        self._placa = valor


    @property
    def fecha(self):
        """Tiene valor el atrivuto fecha"""
        return self._fecha


    @fecha.setter
    def fecha(self, valor):
        """
        Establece el valor del atributo de fecha
        Parámetros
        ----------
        valor : str
        
        aumenta
        ------
        ValorError
            Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021-04-02)
        """
        try:
            if len(valor) != 10:
                raise ValueError
            datetime.datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
        self._date = valor
        

    @property
    def tiempo(self):
        """Tiene valor el atrivuto tiempo"""
        return self._tiempo


    @tiempo.setter
    def tiempo(self, valor):
        """
        Establece el valor del atributo de tiempo
        Parámetros
        ----------
        valor: str
        
        aumenta
        ------
        ValorError
            Si la cadena de valor no tiene el formato HH:MM (por ejemplo, 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', valor):
            raise ValueError(
                'La hora debe tener el siguiente formato: HH:MM (por ejemplo, 08:31, 14:22, 00:01)')
        self._tiempo = valor


    def __find_dia(self, fecha):
        """
        Encuentra el día a partir de la fecha: por ejemplo, miércoles
        Parámetros
        ----------
        fecha: str
            Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        Devoluciones
        -------
        Devuelve el día a partir de la fecha como una cadena
        """        
        d = datetime.datetime.strptime(fecha, '%Y-%m-%d').diaLab()
        return self.__dias[d]


    def __is_forbidden_time(self, check_time):
        """
        Comprueba si el tiempo proporcionado está dentro de las horas pico prohibidas,
        donde las horas pico son: 07:00 - 09:30 y 16:00 - 19:30
        Parámetros
        ----------
        verificarHora : str
            Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
        Devoluciones
        -------
        Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, False
        """           
        t = datetime.datetime.strptime(check_time, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __is_holiday(self, fecha, online):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador
        si en línea == Verdadero, utilizará una API REST, de lo contrario, generará los días festivos del año examinado
        
        Parámetros
        ----------
        fecha: str
            Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        en línea: booleano, opcional
            si online == Verdadero, se utilizará la API de días festivos abstractos
        Devoluciones
        -------
        Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
        """            
        y, m, d = fecha.split('-')

        if online:
            #API de vacaciones abstractapi, versión gratuita: 1000 solicitudes por mes
            #1 solicitud por segundo
            #recuperar la clave API de la variable de entorno
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&dia={}".format(key, y, m, d))
            if (response.status_code == 401):
                # Esto significa que falta una clave API
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # si no hay vacaciones, obtenemos una matriz vacía
                return False
            # Arreglar el Jueves Santo incorrectamente denotado como feriado
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = VacacionesEcuador(prov='EC-P')
            return fecha in ecu_holidays


    def predecir(self):
        """
        Comprueba si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora proporcionada según las reglas de Pico y Placa:
        http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
        Devoluciones
        -------
        Devoluciones
        Verdadero si el vehículo con
        la placa especificada puede estar en el camino
        en la fecha y hora especificadas, de lo contrario Falso
        """
        # Comprobar si la fecha es un día festivo
        if self.__is_holiday(self.fecha, self.online):
            return True

        # Consultar vehículos excluidos de la restricción según la segunda letra de la placa o si se utilizan sólo dos letras
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.placa[1] in 'AUZEXM' or len(self.placa.split('-')[0]) == 2:
            return True

        # Compruebe si el tiempo proporcionado no está en las horas pico prohibidas
        if not self.__is_forbidden_time(self.tiempo):
            return True

        dia = self.__find_dia(self.fecha)  # Buscar el día de la semana a partir de la fecha
        # Verifique si el último dígito de la placa no está restringido en este día en particular
        if int(self.placa[-1]) not in self.__restricciones[dia]:
            return True

        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Predictor Pico y Placa Quito: Verifique si el vehículo con la placa proporcionada puede estar en la carretera en la fecha y hora proporcionada')
    parser.add_argument(
        '-o',
        '--online',
        action='store_true',
        help='use abstract\'s Public Holidays API')
    parser.add_argument(
        '-p',
        '--plate',
        required=True,
        help='la placa del vehículo: XXX-YYYY o XX-YYYY, donde X es una letra mayúscula e Y es un dígito')
    parser.add_argument(
        '-d',
        '--date',
        required=True,
        help='la fecha a comprobar: AAAA-MM-DD')
    parser.add_argument(
        '-t',
        '--time',
        required=True,
        help='la hora a comprobar: HH:MM')
    args = parser.parse_args()


    pyp = PicoPlaca(args.placa, args.fecha, args.tiempo, args.online)

    if pyp.predecir():
        print(
            'El vehículo con placa {} PUEDE estar en la carretera el {} a las {}.'.format(
                args.placa,
                args.fecha,
                args.tiempo))
    else:
        print(
            'El vehículo con placa {} NO PUEDE estar en la carretera el {} a las {}.'.format(
                args.placa,
                args.fecha,
                args.tiempo))