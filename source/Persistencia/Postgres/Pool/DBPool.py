import atexit
import logging
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

class DBPool:
    def __init__(self, conninfo: str):
        self._pool = ConnectionPool(
            conninfo,
            min_size=2,
            max_size=4,
            max_idle=600, # 10 minutos de inactividad antes de reducir las conexiones
            check=ConnectionPool.check_connection, # Verificar que la conexión esté viva
            kwargs={"row_factory": dict_row} #para devolver diccionarios en lugar de tuplas
        )
        #Luego lo quitaré, es sólo para validar la conexión
        print("Pool de base de datos creado correctamente")
        print(conninfo)


        # Asegurar el cierre en caso de que se detenga la app
        atexit.register(self.close_pool)

    def get_connection(self):
        #se retorna una instancia de la conexión
        return self._pool.connection()

    def close_pool(self):
        # cerrando ek pool
        if not self._pool.closed:
            self._pool.close()
            print("Pool de base de datos cerrado correctamente.")

# instancia de manera global, para la inyección de dependencias 
#lo cambiaré por un archivo para que la información de la bd no esté en el código
db = DBPool("dbname=nombre user=usuario password=contraseña")