import pandas as pd
import mysql.connector
from teamData import TeamData
from season import Season

class Engine:
    # Private attributes
    __seasons = []

    # Public attributes
    seasons = []
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "db_modelacion",
        port = 3306
    )
    #1433 for SQL
    SQL = """
        SELECT *
        FROM teamStats
    """

    def constructor(self, simulations):
        df = pd.read_sql_query(SQL, db)
        stats = df.values.tolist()
        data = []
        
        for item in stats:
            data.append(TeamData(item))
        
        for index in range(simulations):
            self.__seasons.append(Season(data))

        self.seasons = self.__seasons.copy()

    
