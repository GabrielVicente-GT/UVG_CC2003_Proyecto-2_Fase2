from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from neo4j.work.simple import Query

class App:
  def __init__(self, uri, user, password):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))
  def close(self):
    self.driver.close()
  def create_relationship(self, person1_name, game1_name):
    with self.driver.session() as session:
        result = session.write_transaction(
            self._create_and_return_relationship, person1_name, game1_name)
        for row in result:
            print("Creacion de relacion exitosa entre: {p1}, {g1}".format(p1=row['p1'], g1=row['g1']))
  '''def create_Videogames():
    query = (
      "CREATE (FO:Game { name: Fortnite, Tipo: FPS})"
      "(GI:Game { name: Genshin Impact,  Tipo: ARPG-Mundo Abierto})"
      "(LL:Game { name: League of Legends, Tipo: MOBA})"
      "(MK:Game { name: Mario Kart 8 Deluxe, Tipo: Carreras})"
      "(AU:Game { name: Among Us, Tipo: Party/Estrategia})"
      "(WZ:Game { name: Call of Duty: Warzone, Tipo: FPS-Battle Royale})"
      "(MC:Game { name: Minecraft, Tipo: Mundo Abierto-Survival-Creative})"
      "(FG:Game { name: Fall Guys: Ultimate Knockout, Tipo: BattleRoyale})"
      "(RL:Game { name: Rocket League, Tipo: Carreras/Deportes})"
      "(GV:Game { name: GTA V, Tipo: Accion-Aventura})"
      "(RG:Company { name: Riot Games, from: California, USA})"
      "(EG:Company { name: Epic Games, from: MaryLand, USA})"
      "(NN:Company { name: Nintendo, from: Kyoto, Japon})"
      "(MH:Company { name: miHoyo, from: Shangai, China})"
      "(IT:Company { name: InnerSloth, from: Washington, USA})"
      "(AV:Company { name: Activision, from: California, USA})"
      "(MT:Company { name: Mediatonic, from: Londres, UK})"
      "(MG:Company { name: Mojang Studios, from: Estocolmo, Suecia})"
      "(RK:Company { name: Rockstar Games, from: Nueva York , USA})"
      "(PX:Company { name: Psyonix, from: California del norte, USA})"
      "(MP:Modo { name: Multiplayer})"
      "(SP:Modo { name: Singleplayer})"
      "(OL:CONEXION { name: Online})"
      "(OF:CONEXION { name: Offline})"
      "(VA)-[:DESARROLLADO {since: 2019}]->(RG),(LL)-[:DESARROLLADO {since: 2009}]->(RG)"
      "(FO)-[:DESARROLLADO {since: 2017}]->(EG),(GI)-[:DESARROLLADO {since: 2020}]->(MH)"
      "(MK)-[:DESARROLLADO {since: 2014}]->(NN),(AU)-[:DESARROLLADO {since: 2018}]->(IT)"
      "(WZ)-[:DESARROLLADO {since: 2020}]->(AV),(MC)-[:DESARROLLADO {since: 2011}]->(MG)"
      "(FG)-[:DESARROLLADO {since: 2019}]->(MT),(RL)-[:DESARROLLADO {since: 2015}]->(PX)"
      "(GV)-[:DESARROLLADO {since: 2013}]->(RK),(VA)-[:MODO]->(MP)"
      "(FO)-[:MODO]->(MP)"
      "(GI)-[:MODO]->(MP)"
      "(GI)-[:MODO]->(SP)"
      "(LL)-[:MODO]->(MP)"
      "(MK)-[:MODO]->(MP)"
      "(MK)-[:MODO]->(SP)"
      "(AU)-[:MODO]->(MP)"
      "(WZ)-[:MODO]->(MP)"
      "(MC)-[:MODO]->(MP)"
      "(FG)-[:MODO]->(MP)"
      "(RL)-[:MODO]->(MP)"
      "(RL)-[:MODO]->(SP)"
      "(GV)-[:MODO]->(MP)"
      "(GV)-[:MODO]->(SP)"
      "(VA)-[:CONEXION]->(OL)"
      "(FO)-[:CONEXION]->(OL)"
      "(GI)-[:CONEXION]->(OL)"
      "(LL)-[:CONEXION]->(OL)"
      "(MK)-[:CONEXION]->(OL)"
      "(MK)-[:CONEXION]->(OF)"
      "(AU)-[:CONEXION]->(OL)"
      "(WZ)-[:CONEXION]->(OL)"
      "(MC)-[:CONEXION]->(OL)"
      "(MC)-[:CONEXION]->(OF)"
      "(FG)-[:CONEXION]->(OL)"
      "(RL)-[:CONEXION]->(OL)"
      "(GV)-[:CONEXION]->(OL)"
    )
    print("Listo, base creada")'''
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
        raise
  def find_person(self, person_name):
    with self.driver.session() as session:
        result = session.read_transaction(self._find_and_return_person, person_name)
        for row in result:
            print("Found person: {row}".format(row=row))
  @staticmethod
  def _find_and_return_person(tx, person_name):
    query = (
        "MATCH (p:Person) "
        "WHERE p.name = $person_name "
        "RETURN p.name AS name"
    )
    result = tx.run(query, person_name=person_name)
    return [row["name"] for row in result]
if __name__ == "__main__":
  bolt_url = "bolt://54.159.202.221:7687"
  user = "neo4j"
  password = "sleeve-twists-stopper"
  app = App(bolt_url, user, password)
  #app.create_Videogames()
  app.create_relationship("Carlos", "Valorant")
  app.find_person("Carlos")
  app.close()
