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

  # Creación de relación (Revisar y modificar para que funcione como queremos)
  '''def create_relationship(self, person1_name, game1_name):
    with self.driver.session() as session:
        result = session.write_transaction(
            self._create_and_return_relationship, person1_name, game1_name)
        for row in result:
            print("Creacion de relacion exitosa entre: {p1}, {g1}".format(
                p1=row['p1'], g1=row['g1']))

  @staticmethod
  def _create_and_return_relationship(tx, person1_name, game1_name):
    query = (
        "CREATE (p1:Person { name: $person1_name }) "
        "CREATE (g1:Game { name: $game1_name }) "
        "CREATE (p1)-[:DISFRUTA]->(g1) "
        "RETURN p1, g1"
        )
    result = tx.run(query, person1_name=person1_name, game1_name=game1_name)
    try:
        return [{"p1": row["p1"]["name"], "g1": row["g1"]["name"]}
            for row in result]
    except ServiceUnavailable as exception:
        logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
        raise'''

  # Búsqueda de persona por nombre
  def find_person(self, person_name):
    with self.driver.session() as session:
        result = session.read_transaction(self._find_and_return_person, person_name)
        for row in result:
          print("Found person: {row}".format(row=row))

  # Query para buscar a la persona por nombre
  @staticmethod
  def _find_and_return_person(tx, person_name):
    query = (
        "MATCH (p:Person) "
        "WHERE p.name = $person_name "
        "RETURN p.name AS name"
    )
    result = tx.run(query, person_name=person_name)
    return [row["name"] for row in result]

  # Búsqueda de juegos por tipo
  def find_game_by_type(self, game_type):
    with self.driver.session() as session:
      result = session.read_transaction(self._find_and_return_game_by_Type, game_type)
      for row in result:
        print("Juegos recomendados que coinciden con el tipo seleccionado: {row}".format(row=row))

  # Query para buscar juegos por tipo
  @staticmethod
  def _find_and_return_game_by_Type(tx, game_type):
    query = (
        "MATCH (G:Game) "
        "WHERE G.Tipo = $game_type "
        "RETURN G.name AS name"
    )
    result = tx.run(query, game_type=game_type)
    return [row["name"] for row in result]

  # Búsqueda de juegos por dispositivo
  def find_game_by_device(self, device_type):
    with self.driver.session() as session:
      result = session.read_transaction(self._find_and_return_game_by_Device, device_type)
      for row in result:
       print("Juegos recomendados que coinciden con el dispositivo seleccionado: {row}".format(row=row))

  # Query para buscar juegos por dispositivo
  @staticmethod
  def _find_and_return_game_by_Device(tx, device_type):
    query = (
      "MATCH (D:Device {name: $device_type})<-[:DISPONIBLE_EN]-(games)"
      "RETURN games.name AS name"
    )
    result = tx.run(query,device_type=device_type)
    return [row["name"] for row in result]

  # Búsqueda de juegos por compañia
  def find_game_by_company(self, company_type):
    with self.driver.session() as session:
      result = session.read_transaction(self._find_and_return_game_by_Company, company_type)
      for row in result:
        print("Juegos recomendados que coinciden con la compañia seleccionado: {row}".format(row=row))

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
      result = session.read_transaction(self._find_and_return_game_by_Conection, conection_type)
      for row in result:
        print("Juegos recomendados que coinciden con la conexión seleccionado: {row}".format(row=row))

  # Query para buscar juegos por conexión
  @staticmethod
  def _find_and_return_game_by_Conection(tx, conection_type):
    query = (
      "MATCH (D:CONEXION {name: $conection_type})<-[:CONEXION]-(games)"
      "RETURN games.name AS name"
    )
    result = tx.run(query, conection_type=conection_type)
    return [row["name"] for row in result]

  # Búsqueda de juegos por modo
  def find_game_by_mode(self, mode_type):
    with self.driver.session() as session:
      result = session.read_transaction(self._find_and_return_game_by_Mode, mode_type)
      for row in result:
        print("Juegos recomendados que coinciden con el modo seleccionado: {row}".format(row=row))

  # Query para buscar juegos por modo
  @staticmethod
  def _find_and_return_game_by_Mode(tx, mode_type):
    query = (
      "MATCH (D:Modo {name: $mode_type})<-[:MODO]-(games)"
      "RETURN games.name AS name"
    )
    result = tx.run(query, mode_type=mode_type)
    return [row["name"] for row in result]

if __name__ == "__main__":

  bolt_url = "bolt://3.231.33.43:7687"
  user = "neo4j"
  password = "knock-ration-limitations"
  app = App(bolt_url, user, password)
  # app.create_relationship("Pedro", "Mario Bros")
  # app.find_person("Pedro")
  # app.find_game_by_type("FPS")

  def no_option(Verificacion):
    print('La opción que ingresó no existe')
    Verificacion = False

  print('______________________-----------------------------------______________________')
  print('______________________----------Sistema ChrIGaJ----------______________________')
  print('______________________-----------------------------------______________________')
  print()

  Verificador = False
  Palabra_clave = ''

  while Verificador != True:
    try:
        print()
        print('Seleccione una accion a realizar con la base de datos')
        print()
        print('--------------------')
        print('... Elegir juego ...')
        print('--------------------')
        print('1) Por Tipo / Genero')
        print('2) Por Dispositivo')
        print('3) Por Compania')
        print('4) Por Conexion')
        print('5) Por Jugabilidad')
        print()
        print('----------------------')
        print('... Otras opciones ...')
        print('----------------------')
        print('6) Agregar relacion')
        print('7) Quitar relacion')
        print('8) Salir')
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
            else:
              print()
              print('Genero no encontrado')
              print()
              no_option(Verificador)
              Palabra_clave = ''
            if Palabra_clave != '':
              print()
              app.find_game_by_type(Palabra_clave)
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
            print ('En que dispositivo?')
            print ('1) Playstation 4-5')
            print ('2) Xbox One S-Series X')
            print ('3) Android/IOS')
            print ('4) PC')
            print ('5) Nintendo Switch')

            print ()
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
              print ()
              print ('Dispositivo no encontrado')
              print ()
              no_option(Verificador)
              Palabra_clave = ''
                    
            if Palabra_clave != '':
              print ()
              app.find_game_by_device(Palabra_clave)
            else:
              print('esto no esta en la base')
              print()
                  
          except:
            print ('La opción que ingresó no existe')
            print ()
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
            else:
              print()
              print('Compania no encontrado')
              print()
              no_option(Verificador)
              Palabra_clave = ''
            if Palabra_clave != '':
              print()
              app.find_game_by_company(Palabra_clave)
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
            print ('Tipo de conexion?')
            print ('1) Conexion Online')
            print ('2) Conexion Offline')
            
            print()
            disp = int(input('Ingrese una opción: '))
            if disp == 1:
              Palabra_clave = 'Online'
            elif disp == 2:                  
              Palabra_clave = 'Offline'   
            else:
              print ()
              print ('Conexion no encontrado')
              print ()
              no_option(Verificador)
              Palabra_clave = ''
            if Palabra_clave != '':
              print()
              app.find_game_by_conection(Palabra_clave)
            else:
              print('Esto no esta en la base')
              print()
              
          except:
            print ('La opción que ingresó no existe')
            print ()
            Verificador = False
                  
        elif Menu == 5:
          try:
            print()
            print ('Modo de jugabilidad?')
            print ('1) Singleplayer')
            print ('2) Multiplayer')
            
            print()
            disp = int(input('Ingrese una opción: '))
            if disp == 1:
              Palabra_clave = 'Singleplayer'
            elif disp == 2:                  
              Palabra_clave = 'Multiplayer'   
            else:
              print ()
              print ('Conexion no encontrado')
              print ()
              no_option(Verificador)
              Palabra_clave = ''
            if Palabra_clave != '':
              print()
              app.find_game_by_mode(Palabra_clave)
            else:
              print('Esto no esta en la base')
              print()
              
          except:
            print ('La opción que ingresó no existe')
            print ()
            Verificador = False

        elif Menu == 6:
          print()
          print('esta es la opcion de crear relacion')
              
          Verificador = False
        elif Menu == 7:
          print()
          print('esta es la opcion de eliminar')
            
          Verificador = False
        elif Menu == 8:
          print ('Adios!')
          print ()
          app.close()
          Verificador = True

        else:
          print ()
          print ('La opción que ingresó no existe')
          print ()
          no_option(Verificador)        
    except:
      print ('La opción que ingresó no existe')
      print ()
      Verificador = False
  app.close()
