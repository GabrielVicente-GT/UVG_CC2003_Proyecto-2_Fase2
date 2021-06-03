# Christopher García 20541
# Isabel Solano 20504
# Gabriel Vicente 20498
# Jessica Ortíz 20192
# Algoritmos y estructura de datos CC2003
# Sección 10

from typing import List
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from neo4j.work.simple import Query


class App:

    # Inicio de la sesion, se conecta a la base de Neo4j
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # Termina la sesión
    def close(self):
        self.driver.close()

    # Creación de relación
    def create_relationship(self, person1_name, game1_name, Type_name, Device_name, Company_name, Modo_name, Conexion_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_relationship, person1_name, game1_name, Type_name, Device_name, Company_name, Modo_name, Conexion_name)
            for row in result:
                print("Creacion de relacion exitosa entre: {p1}".format(
                    p1=row['p1'])+", el juego: {g1}".format(g1=row['g1'])+" y sus caracteristicas")

    # Creación de relación
    @staticmethod
    def _create_and_return_relationship(tx, person1_name, game1_name, Type_name, Device_name, Company_name, Modo_name, Conexion_name):
        query = (
            "MATCH (t1:Type { name: '%s' }) "
            "MATCH (d1:Device { name: '%s' }) "
            "MATCH (co1:Conection { name: '%s' }) "
            "MATCH (m1:Modo { name: '%s' })  "
            "CREATE (p1:Person { name: '%s' }) "
            "CREATE (g1:Game { name: '%s' }) "
            "CREATE (c1:Company { name: '%s' }) "
            "CREATE (g1)-[:GENERO]->(t1) "
            "CREATE (g1)-[:DISPONIBLE_EN]->(d1) "
            "CREATE (g1)-[:DESARROLLADO]->(c1) "
            "CREATE (g1)-[:MODO]->(m1) "
            "CREATE (g1)-[:CONEXION]->(co1) "
            "CREATE (p1)-[:RECOMIENDA]->(g1) "
            "RETURN p1, g1"
            % (Type_name, Device_name, Conexion_name, Modo_name, person1_name, game1_name, Company_name))
        result = tx.run(query, person1_name=person1_name,
                        game1_name=game1_name)
        try:
            return [{"p1": row["p1"]["name"], "g1": row["g1"]["name"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    # Eliminación de relación
    def delete_relationship(self, person1_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._delete_and_return_relationship, person1_name)
            for row in result:
                print(
                    "Eliminación de recomendaciones por el usuario y de relaciones exitosa")

    # Eliminación de relación
    @staticmethod
    def _delete_and_return_relationship(tx, person1_name):
        query = (
            "MATCH (p1:Person {name: $person1_name}) "
            "DETACH DELETE p1"
        )
        result = tx.run(query, person1_name=person1_name)
        try:
            return [{"p1": row["p1"]["name"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    # Búsqueda de juegos por tipo
    def find_game_by_type(self, game_type):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_game_by_Type, game_type)
            for row in result:
                print("Juegos recomendados que coinciden con el tipo seleccionado: {row}".format(
                    row=row))

    # Query para buscar juegos por tipo
    @staticmethod
    def _find_and_return_game_by_Type(tx, game_type):
        query = (
            "MATCH (T:Type {name: $game_type})<-[:GENERO]-(Games)"
            "RETURN Games.name AS name"
        )
        result = tx.run(query, game_type=game_type)
        return [row["name"] for row in result]

    # Búsqueda de juegos por dispositivo
    def find_game_by_device(self, device_type):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_game_by_Device, device_type)
            for row in result:
                print("Juegos recomendados que coinciden con el dispositivo seleccionado: {row}".format(
                    row=row))

    # Query para buscar juegos por dispositivo
    @staticmethod
    def _find_and_return_game_by_Device(tx, device_type):
        query = (
            "MATCH (D:Device {name: $device_type})<-[:DISPONIBLE_EN]-(games)"
            "RETURN games.name AS name"
        )
        result = tx.run(query, device_type=device_type)
        return [row["name"] for row in result]

    # Búsqueda de juegos por compañia
    def find_game_by_company(self, company_type):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_game_by_Company, company_type)
            for row in result:
                print("Juegos recomendados que coinciden con la compañia seleccionado: {row}".format(
                    row=row))

    # Query para buscar juegos por compañia
    @staticmethod
    def _find_and_return_game_by_Company(tx, company_type):
        query = (
            "MATCH (D:Company {name: $company_type})<-[:DESARROLLADO]-(games)"
            "RETURN games.name AS name"
        )
        result = tx.run(query, company_type=company_type)
        return [row["name"] for row in result]

    # Búsqueda de juegos por conexión
    def find_game_by_conection(self, conection_type):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_game_by_Conection, conection_type)
            for row in result:
                print("Juegos recomendados que coinciden con la conexión seleccionado: {row}".format(
                    row=row))

    # Query para buscar juegos por conexión
    @staticmethod
    def _find_and_return_game_by_Conection(tx, conection_type):
        query = (
            "MATCH (D:Conection {name: $conection_type})<-[:CONEXION]-(games)"
            "RETURN games.name AS name"
        )
        result = tx.run(query, conection_type=conection_type)
        return [row["name"] for row in result]

    # Búsqueda de juegos por modo
    def find_game_by_mode(self, mode_type):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_and_return_game_by_Mode, mode_type)
            for row in result:
                print("Juegos recomendados que coinciden con el modo seleccionado: {row}".format(
                    row=row))

    # Query para buscar juegos por modo
    @staticmethod
    def _find_and_return_game_by_Mode(tx, mode_type):
        query = (
            "MATCH (D:Modo {name: $mode_type})<-[:MODO]-(games)"
            "RETURN games.name AS name"
        )
        result = tx.run(query, mode_type=mode_type)
        return [row["name"] for row in result]

    # Búsqueda de todas las personas
    def find_persons(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_persons)
            for row in result:
                print("Personas que recomendaron algun videojuego y se agrego a la base de datos: {row}".format(
                    row=row))

    # Query para buscar todas las personas
    @staticmethod
    def _find_and_return_persons(tx):
        query = (
            "MATCH (P:Person) "
            "RETURN P.name AS name"
        )
        result = tx.run(query)
        # print(list(result))
        return [row["name"] for row in result]

    # Recomendaciones de dos categorias
    def find_game_by_Two_Categories(self, Relation_one, Type_One, category_1, Relation_two, Type_Two, category_2):
        with self.driver.session() as session:
            result = session.read_transaction(
                self._find_game_by_Two_Categories, Relation_one, Type_One, category_1, Relation_two, Type_Two, category_2)
            for row in result:
                print("Juegos recomendados que coinciden con las categorias seleccionadas: {row}".format(
                    row=row))

    # Query para recomendar por medio de dos categorías
    @staticmethod
    def _find_game_by_Two_Categories(tx, Relation_one, Type_One, category_1, Relation_two, Type_Two, category_2):
        query = (
            "MATCH (n:Game)-[:%s]->(x:%s { name: '%s' }) "
            "MATCH (n)-[:%s]->(y:%s { name: '%s' }) "
            "RETURN n.name AS name"
            % (Relation_one, Type_One, category_1, Relation_two, Type_Two, category_2))
        #print(query)
        result = tx.run(query, Relation_one=Relation_one, Type_One=Type_One, category_1=category_1,
                        Relation_two=Relation_two, Type_Two=Type_Two, category_2=category_2)
        #print(list(result))
        return [row["name"] for row in result]


if __name__ == "__main__":

    bolt_url = "bolt://3.83.243.101:7687"
    user = "neo4j"
    password = "trip-rudder-miner"
    app = App(bolt_url, user, password)

    def no_option(Verificacion):
        print('La opción que ingresó no existe')
        Verificacion = False

    Verificador = False
    print('______________________-----------------------------------______________________')
    print('______________________----------Sistema ChrIGaJ----------______________________')
    print('______________________-----------------------------------______________________')
    print()
    while Verificador != True:
        print()
        print('Bienvenido(a) a este sistema de recomendaciones')
        print('Para empezar deberas seleccionar una de las opciones disponibles')
        print()
        print('1) Recomendaciones de Videojuegos generales')
        print('2) Recomendaciones de Videojuegos especificas')
        print('3) Agregar recomendacion')
        print('4) Eliminar recomendacion')
        print('5) Salir')

        print()
        VerificadorInicio = False
        MenuInicio = int(input('Ingrese una opción: '))
        
        if MenuInicio == 1:
            try:
                Verificador = False
                Palabra_clave = ''
                
                try:
                        print()
                        print('Seleccione una accion a realizar con la base de datos')
                        print()
                        print('--------------------')
                        print('... Elegir categoria ...')
                        print('--------------------')
                        print('1) Por Tipo / Genero')
                        print('2) Por Dispositivo')
                        print('3) Por Compania')
                        print('4) Por Conexion')
                        print('5) Por Jugabilidad')
                        print('6) Salir')
                        print()

                        Menu = int(input('Ingrese una opción: '))

                        if Menu == 1:
                            try:
                                print()
                                print('Que genero desea?')
                                print()
                                print('1) FPS')
                                print('2) ARPG')
                                print('3) MOBA')
                                print('4) Mundo abierto')
                                print('5) Carreras')
                                print('6) Party')
                                print('7) Estrategia')
                                print('8) Deportes')
                                print('9) Accion')
                                print('10) Aventura')
                                print('11) Peleas')
                                print('12) Battle Royale')
                                print('13) Terror')
                                print('14) Peleas')

                                print()
                                genero = int(input('Ingrese una opción: '))
                                if genero == 1:
                                    Palabra_clave = 'FPS'
                                elif genero == 2:
                                    Palabra_clave = 'ARPG'
                                elif genero == 3:
                                    Palabra_clave = 'MOBA'
                                elif genero == 4:
                                    Palabra_clave = 'Mundo abierto'
                                elif genero == 5:
                                    Palabra_clave = 'Carreras'
                                elif genero == 6:
                                    Palabra_clave = 'Party'
                                elif genero == 7:
                                    Palabra_clave = 'Estrategia'
                                elif genero == 8:
                                    Palabra_clave = 'Deportes'
                                elif genero == 9:
                                    Palabra_clave = 'Accion'
                                elif genero == 10:
                                    Palabra_clave = 'Aventura'
                                elif genero == 11:
                                    Palabra_clave = 'Peleas'
                                elif genero == 12:
                                    Palabra_clave = 'Battle Royale'
                                elif genero == 13:
                                    Palabra_clave = 'Terror'
                                elif genero == 14:
                                    Palabra_clave = 'Peleas'
                                else:
                                    print()
                                    print('Genero no encontrado')
                                    print()
                                    no_option(Verificador)
                                    Palabra_clave = ''
                                if Palabra_clave != '':
                                    print()
                                    app.find_game_by_type(Palabra_clave)
                                    Verificador = False
                                else:
                                    print('Esto no esta en la base')
                                    print()

                            except:
                                print('La opción que ingresó no existe')
                                print()
                                Verificador = False

                        elif Menu == 2:
                            try:
                                print()
                                print('En que dispositivo?')
                                print('1) Playstation 4-5')
                                print('2) Xbox One S-Series X')
                                print('3) Android/IOS')
                                print('4) PC')
                                print('5) Nintendo Switch')

                                print()
                                disp = int(input('Ingrese una opción: '))
                                if disp == 1:
                                    Palabra_clave = 'Playstation 4-5'
                                elif disp == 2:
                                    Palabra_clave = 'Xbox One S-Series X'
                                elif disp == 3:
                                    Palabra_clave = 'Android/IOS'
                                elif disp == 4:
                                    Palabra_clave = 'PC'
                                elif disp == 5:
                                    Palabra_clave = 'Nintendo Switch'
                                else:
                                    print()
                                    print('Dispositivo no encontrado')
                                    print()
                                    no_option(Verificador)
                                    Palabra_clave = ''

                                if Palabra_clave != '':
                                    print()
                                    app.find_game_by_device(Palabra_clave)
                                    Verificador = False
                                else:
                                    print('esto no esta en la base')
                                    print()

                            except:
                                print('La opción que ingresó no existe')
                                print()
                                Verificador = False

                            Verificador = False

                        elif Menu == 3:
                            try:
                                print()
                                print('Que compania desea?')
                                print()
                                print('1) Riot Games')
                                print('2) Supercell')
                                print('3) Epic Games')
                                print('4) Nintendo')
                                print('5) miHoyo')
                                print('6) InnerSloth')
                                print('7) Activision')
                                print('8) Mediatonic')
                                print('9) Mojang Studios')
                                print('10) Rockstar Games')
                                print('11) Psyonix')
                                print('12) Electronics Arts')
                                print('13) Valve Corporation')
                                print('14) Blizzard Entertainment')
                                print('15) NetherRealm Studios')
                                print('16) Capcom')

                                print()
                                ceo = int(input('Ingrese una opción: '))
                                if ceo == 1:
                                    Palabra_clave = 'Riot Games'
                                elif ceo == 2:
                                    Palabra_clave = 'Supercell'
                                elif ceo == 3:
                                    Palabra_clave = 'Epic Games'
                                elif ceo == 4:
                                    Palabra_clave = 'Nintendo'
                                elif ceo == 5:
                                    Palabra_clave = 'miHoyo'
                                elif ceo == 6:
                                    Palabra_clave = 'InnerSloth'
                                elif ceo == 7:
                                    Palabra_clave = 'Activision'
                                elif ceo == 8:
                                    Palabra_clave = 'Mediatonic'
                                elif ceo == 9:
                                    Palabra_clave = 'Mojang Studios'
                                elif ceo == 10:
                                    Palabra_clave = 'Rockstar Games'
                                elif ceo == 11:
                                    Palabra_clave = 'Psyonix'
                                elif ceo == 12:
                                    Palabra_clave = 'Electronics Arts'
                                elif ceo == 13:
                                    Palabra_clave = 'Valve Corporation'
                                elif ceo == 14:
                                    Palabra_clave = 'Blizzard Entertainment'
                                elif ceo == 15:
                                    Palabra_clave = 'NetherRealm Studios'
                                elif ceo == 16:
                                    Palabra_clave = 'Capcom'

                                else:
                                    print()
                                    print('Compania no encontrado')
                                    print()
                                    no_option(Verificador)
                                    Palabra_clave = ''
                                if Palabra_clave != '':
                                    print()
                                    app.find_game_by_company(Palabra_clave)
                                    Verificador = False
                                else:
                                    print('Esto no esta en la base')
                                    print()

                            except:
                                print('La opción que ingresó no existe')
                                print()
                                Verificador = False

                        elif Menu == 4:
                            try:
                                print()
                                print('Tipo de conexion?')
                                print('1) Conexion Online')
                                print('2) Conexion Offline')

                                print()
                                disp = int(input('Ingrese una opción: '))
                                if disp == 1:
                                    Palabra_clave = 'Online'
                                elif disp == 2:
                                    Palabra_clave = 'Offline'
                                else:
                                    print()
                                    print('Conexion no encontrada')
                                    print()
                                    no_option(Verificador)
                                    Palabra_clave = ''
                                if Palabra_clave != '':
                                    print()
                                    app.find_game_by_conection(Palabra_clave)
                                    Verificador = False
                                else:
                                    print('Esto no esta en la base')
                                    print()

                            except:
                                print('La opción que ingresó no existe')
                                print()
                                Verificador = False

                        elif Menu == 5:
                            try:
                                print()
                                print('Modo de jugabilidad?')
                                print('1) Singleplayer')
                                print('2) Multiplayer')

                                print()
                                disp = int(input('Ingrese una opción: '))
                                if disp == 1:
                                    Palabra_clave = 'Singleplayer'
                                elif disp == 2:
                                    Palabra_clave = 'Multiplayer'
                                else:
                                    print()
                                    print('Jugabilidad no encontrada')
                                    print()
                                    no_option(Verificador)
                                    Palabra_clave = ''
                                if Palabra_clave != '':
                                    print()
                                    app.find_game_by_mode(Palabra_clave)
                                    Verificador = False
                                else:
                                    print('Esto no esta en la base')
                                    print()

                            except:
                                print('La opción que ingresó no existe')
                                print()
                                Verificador = False
                        elif Menu == 6:
                            print('Adios!')
                            print()
                            app.close()
                            Verificador = True

                        else:
                            print()
                            print('La opción que ingresó no existe')
                            print()
                            no_option(Verificador)
                except:
                    print('La opción que ingresó no existe')
                    print()
                    Verificador = False

            except:
                print('La opción que ingresó no existe')
                print()
                VerificadorInicio = False

        elif MenuInicio == 2:
            try:
                print()
                print(
                    'Deberas de seleccionar las categorias de tu interes para esta opcion (2 maximo)')
                print('------------------------------------------------------------')
                print('| Si en dado caso no aparece ningun videojuego recomendado  |\n| muy probablemente es porque no existe en la base de datos |\n| un videojuego con todas las caracteristicas               |')
                print('------------------------------------------------------------')
                print()

                print('---Categorias disponibles---')
                print('A) Por Tipo / Genero')
                print('\t1) FPS')
                print('\t2) ARPG')
                print('\t3) MOBA')
                print('\t4) Mundo abierto')
                print('\t5) Carreras')
                print('\t6) Party')
                print('\t7) Estrategia')
                print('\t8) Deportes')
                print('\t9) Accion')
                print('\t10) Aventura')
                print('\t11) Peleas')
                print('\t12) Battle Royale')
                print('\t13) Terror')
                print('\t14) Peleas')

                print('B) Por Dispositivo')
                print('\t1) Playstation 4-5')
                print('\t2) Xbox One S-Series X')
                print('\t3) Android/IOS')
                print('\t4) PC')
                print('\t5) Nintendo Switch')

                print('C) Por Conexion')
                print('\t1) Conexion Online')
                print('\t2) Conexion Offline')

                print('D) Por Jugabilidad')
                print('\t1) Singleplayer')
                print('\t2) Multiplayer')

                print()

                category_1 = ''
                Relacion_1 = ''
                Tipo_1 = ''
                category_2 = ''
                Relacion_2 = ''
                Tipo_2 = ''

                try:
                    print(
                        'Ingresar codigo de categoria (Ejemplo: Conexion Online = D1 || Siempre en mayúsculas)')
                    print()
                    Cate1 = input('Categoria#1: ')
                    if Cate1 == 'A1':
                        category_1 = 'FPS'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A2':
                        category_1 = 'ARPG'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A3':
                        category_1 = 'MOBA'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A4':
                        category_1 = 'Mundo abierto'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A5':
                        category_1 = 'Carreras'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A6':
                        category_1 = 'Party'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A7':
                        category_1 = 'Estrategia'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A8':
                        category_1 = 'Deportes'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A9':
                        category_1 = 'Accion'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A10':
                        category_1 = 'Aventura'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A11':
                        category_1 = 'Peleas'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'
                    elif Cate1 == 'A12':
                        category_1 = 'Battle Royale'
                        Relacion_1 = 'GENERO'
                        Tipo_1 = 'Type'

                    elif Cate1 == 'B1':
                        category_1 = 'Playstation 4-5'
                        Relacion_1 = 'DISPONIBLE_EN'
                        Tipo_1 = 'Device'
                    elif Cate1 == 'B2':
                        category_1 = 'Xbox One S-Series X'
                        Relacion_1 = 'DISPONIBLE_EN'
                        Tipo_1 = 'Device'
                    elif Cate1 == 'B3':
                        category_1 = 'Android/IOS'
                        Relacion_1 = 'DISPONIBLE_EN'
                        Tipo_1 = 'Device'
                    elif Cate1 == 'B4':
                        category_1 = 'PC'
                        Relacion_1 = 'DISPONIBLE_EN'
                        Tipo_1 = 'Device'
                    elif Cate1 == 'B5':
                        category_1 = 'Nintendo Switch'
                        Relacion_1 = 'DISPONIBLE_EN'
                        Tipo_1 = 'Device'

                    elif Cate1 == 'C1':
                        category_1 = 'Online'
                        Relacion_1 = 'CONEXION'
                        Tipo_1 = 'Conection'
                    elif Cate1 == 'C2':
                        category_1 = 'Offline'
                        Relacion_1 = 'CONEXION'
                        Tipo_1 = 'Conection'

                    elif Cate1 == 'D1':
                        category_1 = 'Singleplayer'
                        Relacion_1 = 'MODO'
                        Tipo_1 = 'Modo'
                    elif Cate1 == 'D2':
                        category_1 = 'Multiplayer'
                        Relacion_1 = 'MODO'
                        Tipo_1 = 'Modo'

                    Cate2 = input('Categoria#2: ')
                    if Cate2 == 'A1':
                        category_2 = 'FPS'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A2':
                        category_2 = 'ARPG'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A3':
                        category_2 = 'MOBA'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A4':
                        category_2 = 'Mundo abierto'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A5':
                        category_2 = 'Carreras'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A6':
                        category_2 = 'Party'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A7':
                        category_2 = 'Estrategia'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A8':
                        category_2 = 'Deportes'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A9':
                        category_2 = 'Accion'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A10':
                        category_2 = 'Aventura'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A11':
                        category_2 = 'Peleas'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'
                    elif Cate2 == 'A12':
                        category_2 = 'Battle Royale'
                        Relacion_2 = 'GENERO'
                        Tipo_2 = 'Type'

                    elif Cate2 == 'B1':
                        category_2 = 'Playstation 4-5'
                        Relacion_2 = 'DISPONIBLE_EN'
                        Tipo_2 = 'Device'
                    elif Cate2 == 'B2':
                        category_2 = 'Xbox One S-Series X'
                        Relacion_2 = 'DISPONIBLE_EN'
                        Tipo_2 = 'Device'
                    elif Cate2 == 'B3':
                        category_2 = 'Android/IOS'
                        Relacion_2 = 'DISPONIBLE_EN'
                        Tipo_2 = 'Device'
                    elif Cate2 == 'B4':
                        category_2 = 'PC'
                        Relacion_2 = 'DISPONIBLE_EN'
                        Tipo_2 = 'Device'
                    elif Cate2 == 'B5':
                        category_2 = 'Nintendo Switch'
                        Relacion_2 = 'DISPONIBLE_EN'
                        Tipo_2 = 'Device'

                    elif Cate2 == 'C1':
                        category_2 = 'Online'
                        Relacion_2 = 'CONEXION'
                        Tipo_2 = 'Conection'
                    elif Cate2 == 'C2':
                        category_2 = 'Offline'
                        Relacion_2 = 'CONEXION'
                        Tipo_2 = 'Conection'

                    elif Cate2 == 'D1':
                        category_2 = 'Singleplayer'
                        Relacion_2 = 'MODO'
                        Tipo_2 = 'Modo'
                    elif Cate2 == 'D2':
                        category_2 = 'Multiplayer'
                        Relacion_2 = 'MODO'
                        Tipo_2 = 'Modo'

                    print()
                    print('Categorias seleccionadas: ')
                    print('Categoria#1: '+category_1)
                    print('Categoria#2: '+category_2)
                    print()
                    print('Relaciones que representan: ')
                    print('Relacion#1: '+Relacion_1)
                    print('Relacion#2: '+Relacion_2)
                    print()
                    print('Tipo que representan: ')
                    print('Tipo#1: '+Tipo_1)
                    print('Tipo#2: '+Tipo_2)
                    print()

                    app.find_game_by_Two_Categories(
                        Relacion_1, Tipo_1, category_1, Relacion_2, Tipo_2, category_2)

                except:
                    print()
                    print('Algo ha salido mal')

            except:
                print('La opción que ingresó no existe')
                print()
                VerificadorInicio = False

        elif MenuInicio == 3:
            try:
                print()
                print('Para ingresar una nueva relacion necesito algunos datos')
                print('Esta relación será de recomendación, por lo que debe de ingresar un videojuego de su agrado y algunos datos adicionales')
                print('Se utilizan apodos para poder proteger la identidad de cada usuario')
                print()
                Apodo = input('Apodo del usuario: ')
                Game = input('Nombre del videojuego: ')
                Company = input('Compañia que desarrollo el videojuego: ')

                print()
                Type = ''
                try:
                    print('Genero del videojuego (1):')
                    print('1) FPS')
                    print('2) ARPG')
                    print('3) MOBA')
                    print('4) Mundo abierto')
                    print('5) Carreras')
                    print('6) Party')
                    print('7) Estrategia')
                    print('8) Deportes')
                    print('9) Accion')
                    print('10) Aventura')
                    print('11) Peleas')
                    print('12) Battle Royale')

                    print()
                    genero = int(input('Ingrese una opción: '))
                    if genero == 1:
                        Type = 'FPS'
                    elif genero == 2:
                        Type = 'ARPG'
                    elif genero == 3:
                        Type = 'MOBA'
                    elif genero == 4:
                        Type = 'Mundo abierto'
                    elif genero == 5:
                        Type = 'Carreras'
                    elif genero == 6:
                        Type = 'Party'
                    elif genero == 7:
                        Type = 'Estrategia'
                    elif genero == 8:
                        Type = 'Deportes'
                    elif genero == 9:
                        Type = 'Accion'
                    elif genero == 10:
                        Type = 'Aventura'
                    elif genero == 11:
                        Type = 'Peleas'
                    elif genero == 12:
                        Type = 'Battle Royale'
                    else:
                        print()
                        print('Genero no encontrado')
                        print()
                        no_option(VerificadorInicio)
                        Type = ''
                        print('Esto no esta en la base')
                        print()
                except:
                    print('La opción que ingresó no existe')
                    print()
                    VerificadorInicio = False
                print()

                Device = ''
                try:
                    print('Dispositivo en el que se pueda jugar el videojuego (1): ')
                    print('1) Playstation 4-5')
                    print('2) Xbox One S-Series X')
                    print('3) Android/IOS')
                    print('4) PC')
                    print('5) Nintendo Switch')
                    print()
                    disp = int(input('Ingrese una opción: '))
                    if disp == 1:
                        Device = 'Playstation 4-5'
                    elif disp == 2:
                        Device = 'Xbox One S-Series X'
                    elif disp == 3:
                        Device = 'Android/IOS'
                    elif disp == 4:
                        Device = 'PC'
                    elif disp == 5:
                        Device = 'Nintendo Switch'
                    else:
                        print()
                        print('Dispositivo no encontrado')
                        print()
                        no_option(VerificadorInicio)
                        Device = ''
                        print('esto no esta en la base')
                        print()
                except:
                    print('La opción que ingresó no existe')
                    print()
                    VerificadorInicio = False
                print()

                Modo = ''
                try:
                    print('Modo de jugabilidad?')
                    print('1) Singleplayer')
                    print('2) Multiplayer')
                    print()
                    disp = int(
                        input('Modalidad del videojuego (Multiplayer o Singleplayer) (1): '))
                    if disp == 1:
                        Modo = 'Singleplayer'
                    elif disp == 2:
                        Modo = 'Multiplayer'
                    else:
                        print()
                        print('Jugabilidad no encontrada')
                        print()
                        no_option(VerificadorInicio)
                        Modo = ''
                        print('Esto no esta en la base')
                        print()
                except:
                    print('La opción que ingresó no existe')
                    print()
                    VerificadorInicio = False
                print()

                Conexion = ''
                try:
                    print('Tipo de conexion?')
                    print('1) Conexion Online')
                    print('2) Conexion Offline')
                    print()
                    disp = int(
                        input('Conexion del videojuego (Online u Offline) (1): '))
                    if disp == 1:
                        Conexion = 'Online'
                    elif disp == 2:
                        Conexion = 'Offline'
                    else:
                        print()
                        print('Conexion no encontrada')
                        print()
                        no_option(VerificadorInicio)
                        Conexion = ''
                        print('Esto no esta en la base')
                        print()
                except:
                    print('La opción que ingresó no existe')
                    print()
                    VerificadorInicio = False

                print()
                app.create_relationship(
                    Apodo, Game, Type, Device, Company, Modo, Conexion)
                print()

            except:
                print('La opción que ingresó no existe')
                print()
                Verificador = False

        elif MenuInicio == 4:
            try:
                print()
                print('Para eliminar una nueva relacion necesito algunos datos')
                print('Esta eliminación será unicamente de otras recomendaciones para no afectar la base de datos original')
                print(
                    'Se mostraran todos los usuarios que han realizado alguna recomendacion')
                print()

                app.find_persons()

                print()
                NombU = input(
                    'Apodo del usuario que realizo recomendaciones (Escriba el nombre correctamente): ')
                print()
                app.delete_relationship(NombU)
            except:
                print('La opción que ingresó no existe')
                print()
                Verificador = False

        elif MenuInicio == 5:
            try:
                print('Adios!')
                print()
                Verificador = True
            except:
                print('La opción que ingresó no existe')
                print()
                Verificador = True

        

        app.close()
