"""
  kemokDanceRobot ver 1.0
  Author: Felix Marquez  nivel.fmarquez@uneg.edu.ve
  Business Intelligence and Data Analytics
  http://www.kemok.io/

"""

"""
Planteamiento:Inicialmente el robot se encuentra en la posición 0 (cero).
- En el primer paso ( P 1 ), el robot se mueve 1 pasos, es decir, un
paso hacia adelante, quedando en la posición 1.
- En el segundo paso ( P 2 ), el robot se mueve -3 pasos, es decir,
tres pasos hacia atrás(note que el signo negativo indica movimientos
hacia atrás), quedando en la posición -2.
- Para los siguientes ( P k ), el robot se desplaza el resultado de la
resta del último paso dado y el penúltimo ( P k−1 − P k−2 ).
Por ejemplo, P 3 = (-3) - (1) = -4 y P 4 = (-4) - (-3) = -1.
Por ejemplo2, P 3 = (-2) - (1) = -3 y P 4 = (-3) - (-2) = -1.
en el ejemplo2  p k-esimo - 1 es -2 y no -3 de este modo se ajusta a
planteamiento pk = P k−1 − P k−2
EL algoritmo se realizó coniderando el ajuste (ejemplo2) en caso que el
plantemiento.
"""


class KemokRobot(object):

    def __init__(self, args__):
        self.args = args__

        if self.args.pasoinicio >= 4:
            self.paso_inicio_corrida = int(self.args.pasoinicio or 0)

        self.paso_k = int(self.args.pasok or 0)

        if self.args.log:
            self.f = open(self.args.log+".log", "w")

        """ indica movibiento hacia adelante, variación positiva en posición
            actual
        """
        self.mov_adelante = 1

        """ indica movibiento hacia atras, variación positiva en posición
        actual
        """
        self.mov_atras = -3
        """ vector posición del robot, esta versión considera maximo 10000
            posiciones
        """
        self.p = [0] * 10000
        self.posicion_inicial = 0
        """
           PasoInicial(pos_inicio): es utilizada para dar movimiento inicial
           al robot en condiciones normales se debe ejecuta PasoInicial(4)
           - PasoInicial es utilizada para mover el robot a una posicion de
             partida superior 10,40 o para el caso planteado  p2020  parametro
             pos_inicio=2020. Esta funcion dejará al robot en la posición de
             partida según parametro pos_inicio
             calculando la posición p que tendrá el robot una vez calculados
             los pos_inicio movientos.
        """
        """ el archivo pasado en parámetro --log es un archivo log por
            convención se le coloca extensión .log
        """

    def GuardarPaso(self, cad):
        if self.args.log:
            self.f.write(cad)

    def PasoInicial(self):

        posicion_inicio = self.paso_inicio_corrida

        """  primeros tres moviemientos"""
        self.p[1] = 0
        self.p[2] = self.p[1] + self.mov_adelante
        self.p[3] = self.p[2] + self.mov_atras

        if self.args.verbose:
            print("1", ';', self.p[1])
            print("2", ';', self.p[2])
            print("3", ';', self.p[3])
        """ en caso que el moviento soliitado sea superior a 4
            caso ejecucion p2020"""

        if posicion_inicio >= 4:
            k = 4
            while k <= posicion_inicio:
                """ ecuacion de movimiento pk"""
                self.p[k] = self.p[k-1] - self.p[k-2]
                if self.args.verbose:
                    print(k, ';', self.p[k])
                self.GuardarPaso(str(k) + ";" + str(self.p[k]) + '\n')
                k += 1

        else:
            print("posión inicial debe ser mayor a 3")

    """
    Dance(k): Función que movera el valor hasta la posión pk considerando la
    encuación pk partiendo de la posicion_inicial previamente calculada.
    """

    def Bailar(self):

        self.PasoInicial()

        if self.paso_inicio_corrida < self.paso_k:
            k = self.paso_inicio_corrida + 1
            """ calculo movimiento  """
            while k <= self.paso_k:
                self.p[k] = self.p[k-1] - self.p[k-2]
                if self.args.verbose:
                    print(k, ';', self.p[k])
                self.GuardarPaso(str(k) + ";" + str(self.p[k]) + '\n')
                k += 1

        self.f.close()

    def PrintPasos(self):
        for i in range(0, self.paso_k):
            print(str(self.p[i])+"\n")

    def getPasoFinal(self):
        return self.p[self.paso_k]
