import flet as ft
from Presentacion.main import run
from Negocio.Modelo.Alumno import Alumno
from datetime import date
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
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