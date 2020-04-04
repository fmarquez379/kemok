"""
  KemokDanceRobot ver 1.0
  Author: Felix Marquez  nivel.fmarquez@uneg.edu.ve
  Business Intelligence and Data Analytics
  http://www.kemok.io/

"""
import argparse
from kemokDanceRobot import KemokRobot

"""
 Parametros:  consultar -h
"""
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
parser.add_argument("-l", "--log", help="Archivo log de pasos ejecutados por"
                                        "kemok-dance-robot")
parser.add_argument("-i", "--pasoinicio",
                    help="Paso de inicio desde el cual comenzará a bailar "
                         "KemokRobot el robot", type=int)
parser.add_argument("-k", "--pasok", help="paso final", type=int)

try:
    args = parser.parse_args()
except:
    parser.print_help()
    exit(0)

print("KemokDanceRobot ver 1.0")

if args.verbose:
    print("modo mostrar pasos activado")

if args.log:
    print("  Nombre Archivo de pasos: " + args.log+".log")

if args.pasoinicio:
    print("  Inicio:", args.pasoinicio)

if args.pasoinicio:
    if args.pasoinicio < 4:
        print("paso inicio corrida debe ser mayor 4")
        print("los pasos 1 2 3 son pasos de aprendizaje")
        exit(0)
else:
    args.pasoinicio = 4
    print("  Inicio: "+str(args.pasoinicio)+"(por decfecto). use "
                                            "--pasoinicio PASOINICIO")

if args.pasok:
    print("  k     :", args.pasok)
else:
    print("Error Parametro paso k -h to help")
    exit(0)


robot = KemokRobot(args)
robot.Bailar()
print("  Paso Final:"+str(robot.getPasoFinal()))

if args.verbose:
    robot.PrintPasos()
