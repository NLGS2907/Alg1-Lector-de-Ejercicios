def cargar_guia(carpeta: str="guia/2c2019") -> dict:

    guia = dict()

    for unidad in range(1, 18):

        dic_unidad = dict()
        lista_ej = list()
        nombre_ej = ''

        with open(f"{carpeta}/guia_{unidad}.txt", encoding="utf-8") as archivo:

            for linea in archivo:

                if any((not linea, linea == '\n', linea[0] == '#')):

                    continue

                llave, *valor = linea.rstrip().split('=', 1)
                valor = ''.join(valor)

                if llave == "titulo":

                    dic_unidad[llave] = valor

                elif valor == '<': # Empezar a leer ejercicio

                    nombre_ej = llave
                    lista_ej = list()

                elif llave in ('t', 'n', 'tn', ''): # Para formatear lineas

                    tab = '\t' if llave in ('t', "tn") else ''
                    new_line = '\n' if llave in ('n', "tn") else ''

                    lista_ej.append(f"{tab}{valor}{new_line}")

                elif llave == '>': # Termina de leer ejercicio

                    dic_unidad[nombre_ej] = '\n'.join(lista_ej)

                else:

                    lista_ej.append(llave)

        guia[str(unidad)] = dic_unidad

    return guia