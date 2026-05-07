from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Persistencia.Postgres.Pool.DBPool import db


class ControladorIncidencia:

    def __init__(self, pantalla):
        self.__pantalla = pantalla
        self.__repo = RepositorioImpl(CRUDimp())

        # Para saber qué incidencia estás editando
        self.__id_actual = None

    # =========================================
    # 📌 OBTENER INCIDENCIAS (USA LA VISTA)
    # =========================================
    def obtener_incidencias(
        self,
        texto: str = "",
        fecha_inicio=None,
        fecha_fin=None,
        tipo: str = "Todos",
        estado: str = "Todos",
        limit: int = 10,
        offset: int = 0
    ):
        filtros = {}
        or_filtros = []

        texto = (texto or "").strip()
        if texto:
            or_filtros = [
                {"nombre_completo__like": texto},
                {"identificador__like": texto},
                {"matricula__like": texto},
                {"n_plaza__like": texto},
            ]

        if tipo and tipo != "Todos":
            filtros["tipo_usuario"] = tipo.upper()

        if estado == "Pendiente":
            filtros["estado"] = "PENDIENTE"
        elif estado == "Resuelto":
            filtros["estado"] = "RESUELTA"

        if fecha_inicio:
            filtros["fecha__gte"] = fecha_inicio
        if fecha_fin:
            filtros["fecha__lte"] = fecha_fin

        datos = self.__repo.obtener_avanzado(
            nombre_tabla="vista_incidencias",
            filtros=filtros,
            or_filtros=or_filtros if or_filtros else None,
            order_by=[("fecha", "DESC")],
            limit=limit,
            offset=offset
        )

        total = self.__repo.contar_avanzado(
            nombre_tabla="vista_incidencias",
            filtros=filtros,
            or_filtros=or_filtros if or_filtros else None
        )

        resultado = []
        for d in datos:
            resultado.append({
                "id": d["id_incidencia"],
                "nombre": d["nombre_completo"],
                "identificador": d.get("matricula") or d.get("n_plaza") or d.get("identificador"),
                "tipo_usuario": d["tipo_usuario"],
                "carrera": d.get("nombre_carrera") or "-",
                "semestre": d.get("semestre") or "-",
                "categoria": d["motivo"],
                "descripcion": d["descripcion"],
                "lugar": d["lugar"],
                "fecha": d["fecha"].strftime("%d/%m/%Y %H:%M"),
                "tipo": d["tipo"],
                "estado": d["estado"],
                "comentario": d.get("comentario") or "",
                "institucion": d.get("nombre_institucion") or "-"
            })

        return resultado, total

    def guardar_dialogo(self, e):
        try:
            comentario = self.__pantalla.modal_comentario.value

            if not self.__id_actual:
                print("No hay incidencia seleccionada")
                return

            with db.get_connection() as conn:
                query = """
                    UPDATE incidencia
                    SET comentario = %s
                    WHERE id_incidencia = %s
                """
                conn.execute(query, (comentario, self.__id_actual))

            print("Comentario actualizado")

        except Exception as ex:
            print("Error:", ex)

        self.__pantalla.cerrar_dialogo(e)

       # refrescar lista 
        self.__pantalla.cargar_datos(e=True)
        self.__pantalla.update()

    # CUANDO se abre  MODAL
    def seleccionar_incidencia(self, id_incidencia):
        self.__id_actual = id_incidencia

    #  CAMBIAR ESTADO
    def cambiar_estado(self, id_incidencia, nuevo_estado):
        try:
            with db.get_connection() as conn:
                query = """
                    UPDATE incidencia
                    SET estado = %s
                    WHERE id_incidencia = %s
                """
                conn.execute(query, (nuevo_estado, id_incidencia))

        except Exception as ex:
            print("Error:", ex)

        self.__pantalla.actualizar()