from Persistencia.conexion import get_conn


def obtener_carreras():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id_carrera, nombre_carrera FROM Carrera ORDER BY nombre_carrera")
    data = cur.fetchall()
    conn.close()
    return data


def obtener_semestres():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id_semestre, semestre FROM Semestre ORDER BY id_semestre")
    data = cur.fetchall()
    conn.close()
    return data

def obtener_grupos_por_semestre(id_semestre):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_grupo, grupo
        FROM Grupo
        WHERE id_semestre = %s
        ORDER BY grupo
    """, (id_semestre,))
    data = cur.fetchall()
    conn.close()
    return data

def obtener_grupos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id_grupo, grupo FROM Grupo ORDER BY grupo")
    data = cur.fetchall()
    conn.close()
    return data

def obtener_grupos_filtrados(id_carrera, id_semestre):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id_grupo, grupo
        FROM Grupo
        WHERE id_carrera = %s AND id_semestre = %s
        ORDER BY grupo
    """, (id_carrera, id_semestre))

    data = cur.fetchall()
    conn.close()
    return data

def obtener_instituciones():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id_institucion, nombre_institucion FROM Institucion ORDER BY nombre_institucion")
    data = cur.fetchall()
    conn.close()
    return data