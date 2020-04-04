"""
  kemok-dance-robot ver 1.0
  Author: Felix Marquez  nivel.fmarquez@uneg.edu.ve
  Business Intelligence and Data Analytics
  http://www.kemok.io/

"""
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

"""
 Parametros:  consultar -h
"""


class ScrapeBot(object):

    def __init__(self, args__, usuario__):
        self.args = args__
        self.usuario = usuario__

    def PrepararDB(self):
        self.conn = sqlite3.connect('kemok-log.db')
        self.c = self.conn.cursor()
        if self.args.verbose:
            if self.c.connection:
                print("DB conected")
        self.create_table()

    def CerraDB(self):
        self.c.close()
        self.conn.close()

    def create_table(self):
        # c.execute("drop TABLE scraper_log")
        self.c.execute("CREATE TABLE IF NOT EXISTS scraper_log(fecha DATE, "
                       "tasa REAL,ejecucion DATE,usuario TEXT,"
                       "observacion TEXT)")
        self.conn.commit()

    def data_entry(self, fecha, tasa, usuario, observacion):
        ejecucion = str(datetime.today())
        ejecucion_fecha = ejecucion.split(" ")[0].split("-")
        ejecucion_hora = ejecucion.split(" ")[1].split("-")
        ejecucion_fecha = "/".join(reversed(ejecucion_fecha))
        ejecucion = ejecucion_fecha + ' ' + ejecucion_hora[0][:8]
        cad = "'" + fecha + "'," + tasa + ",'" + ejecucion + "','" +\
              self.usuario + "','" + observacion + "'"
        if self.args.verbose:
            print(cad)
        self.c.execute("INSERT INTO scraper_log VALUES("+cad+")")
        self.conn.commit()

    def leer_data(self):
        print('scraper log display....')
        if self.args.verbose:
            for row in self.c.execute('SELECT * FROM scraper_log ORDER BY'
                                      ' ejecucion'):
                print(row)
            self.c.execute("SELECT COUNT(*) as CANTIDAD FROM  scraper_log")
            print(self.c.fetchone())

    def consultar_tabla_url(self, url):
        try:
            respuesta = urllib.request.urlopen(url)
            if self.args.verbose:
                print(respuesta)

            return (respuesta)
        except:
            print("No se logro la conexión")
            ejecucion = str(datetime.today())
            ejecucion_fecha = ejecucion.split(" ")[0].split("-")
            ejecucion_hora = ejecucion.split(" ")[1].split("-")
            ejecucion_fecha = "/".join(reversed(ejecucion_fecha))
            ejecucion = ejecucion_fecha + ' ' + ejecucion_hora[0][:8]
            observacion = 'falla conexion:' + url
            cad = "'" + ejecucion_fecha + "'," + '0' + ",'" + ejecucion + \
                  "','" + self.usuario + "','" + observacion + "'"
            if self.args.verbose:
                print(cad)
            self.c.execute("INSERT INTO scraper_log VALUES(" + cad + ")")
            self.conn.commit()
            exit(0)

    def scraper1(self):
        """
        estrategia:preprocesamiento + scanner + registro en la db sqllite3
        preprocesamiento del códico html.
        Considerando que el html puede tener particularidades sintactivcas
        fuera del w3c es necesario limpiar ese tipo de inconsistencia y
        estandarizar la cadena html.
        scanner:
        Se identificaron frases claves en el html que dan cuenta de una unica
        ocurriencia.
        estas claves son ['Tipo de Cambio de Referencia vigente para el','<b>']
        la primer para determinar el dia mes año y el segundo para la tasa.
        """

        pagina = self.consultar_tabla_url('http://banguat.gob.gt/cambio/'
                                          'default.asp')
        soup = BeautifulSoup(pagina, 'html.parser')
        claves = {
          "clavefecha": "Tipo de Cambio de Referencia vigente para el",
          "clavetasa": "<b>"}
        mes_numero = {
            'enero': '1', 'febrero': '2', 'marzo': '3', 'abril': '4',
            'mayo': '5', 'junio': '6', 'julio': '7',
            'agosto': '8', 'septiembre': '9', 'ocubre': '10',
            'noviembre': '11', 'diciembre': '12'
        }

        cad = soup.prettify()
        pos = cad.find(claves.get('clavefecha'))

        """
        la presicion: cantidad de digitos que tiene la mantiza
        del numero  mas el punto (.) ej: 7.69881  6 + 1
        """
        dia = ''
        mes = ''
        anio = ''
        tasa = ''
        observacion = ''
        precision = 7
        if pos != -1:
            k = pos + 44
            cadena2 = cad[k:k+250]
            x = cadena2.split()
            dia = x[1]
            mes = x[3]
            anio = x[4]
            pos2 = cadena2.find(claves.get('clavetasa'))
            mes = mes[: mes.find(',')]
            mes = mes_numero.get(mes.lower())
            # print('fecha:', dia,mes,anio)
            if pos2 != -1:
                k = pos2+13
                tasa = cadena2[k:k+precision]
                if self.args.verbose:
                    print(tasa)
                    print(dia, mes, anio)
                observacion = 'diario'
            else:
                observacion = 'falló clavetasa:'+claves.get('clavetasa')

        else:
            observacion = 'falla clavefecha:'+claves.get('clavefecha')

        if observacion == 'diario':
            self.data_entry(dia + '/' + mes + '/' + anio, tasa, self.usuario,
                            observacion)
        else:
            self.data_entry('null', str(0), self.usuario, observacion)

    def scraper2(self):
        """
         estrategia: preprocesamiento + scanner +registra db sqllite3
         Script lee todo el documento en el enlace indicado.
         no se preparó la propuesta opcion considerando que la propuesta
         en particular busca un vaciado completo de la página,
         de modo que para buscar las tasas entre intervalos esta a nivel
         de sql.
         Este proceso es mas costoso buscar en la página por parametro
         cada vez que se necesite (request + scraper) que
         consultar el intervalo de fechas en base de datos donde la busqueda
         es a nivel de nlogn.
        """
        cad = 'http://banguat.gob.gt/cambio/historico.asp?kmoneda=02&' \
              'ktipo=5&kdia=01&kmes=01&kanio=2020&kdia1=31&kmes1=12&' \
              'kanio1=2020&submit1=Consultar'
        pagina = self.consultar_tabla_url(cad)
        soup = BeautifulSoup(pagina, 'html.parser')
        cad = soup.prettify()
        table_body = soup.find_all('tr')
        estado = 0
        observacion = 'Anual '
        for row in table_body:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            if estado == 0 and cols[0] == '1/1/2020':
                estado = 1
            if estado == 1:
                falla = 0
                fecha = str(cols[0])
                try:
                    dia, mes, anio = fecha.split('/')
                except:
                    falla = 1

                if falla == 0:
                    tasa = str(cols[1])
                    self.data_entry(dia + '/' + mes + '/' + anio, tasa,
                                    self.usuario, observacion)
                    self.conn.commit()

            if estado == 1 and (len(cols[0]) == 0 or len(cols[0]) > 10):
                estado = 2
