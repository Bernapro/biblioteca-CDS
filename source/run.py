import sys
import os
import flet as ft

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from Presentacion.main import run
from Persistencia.Postgres.Pool.DBPool import db




if __name__ == "__main__":
    """
    usr= Alumno(id_usuario= 1234, nombre= "Bernapro", ap_paterno= "Vargas", ap_materno="Cruz", fecha_nacimiento=date.today(), tipo_usuario= "ALUMNO", identificador= "100025781", grupo= 1)
    print(usr.get_columns())
    rep = RepositorioImpl(crud= CRUDimp(db))
    rep.guardar(usr)
    """
    run()
    print("saliendo ...")
    db.close_pool()

    
