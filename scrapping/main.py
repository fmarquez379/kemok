import argparse
from scraper import ScrapeBot

"""
 Parametros:  consultar -h
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
    parser.add_argument("-a", "--anual", help="scrip anual",
                        action="store_true")
    parser.add_argument("-d", "--diario", help="scrip diario",
                        action="store_true")
    parser.add_argument("-u", "--usuario", help="scrip diario")

    try:
        args = parser.parse_args()

    except:
        parser.print_help()
        exit(0)

    print("kemok-scrapping ver 1.0")
    if args.verbose:
        print("modo mostrar salida activado")

    if args.usuario:
        usuario = args.usuario
    else:
        usuario = 'Kemokbot'

    scrapingbot = ScrapeBot(args, usuario)
    scrapingbot.PrepararDB()
    if args.diario:
        scrapingbot.scraper1()
        if args.verbose:
            scrapingbot.leer_data()

    if args.anual:
        scrapingbot.scraper2()
        if args.verbose:
            scrapingbot.leer_data()
