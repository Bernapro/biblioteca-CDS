def registrar_usuario(data):
    conn = get_conn()
    cur = conn.cursor()

    try:
        # =========================
        # 1. INSERT USUARIO
        # =========================
        cur.execute("""
            INSERT INTO Usuario (
                nombre, ap_paterno, ap_materno,
                fecha_nacimiento, tipo_usuario, identificador
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_usuario
        """, (
            data["nombre"],
            data["ap_paterno"],
            data["ap_materno"],
            data["fecha"],
            data["tipo"],
            data["identificador"]
        ))

        id_usuario = cur.fetchone()[0]

        # =========================
        # 2. INSERT SEGÚN TIPO
        # =========================

        if data["tipo"] == "ALUMNO":
            cur.execute("""
                INSERT INTO Alumno (id_usuario, matricula, id_grupo)
                VALUES (%s, %s, %s)
            """, (
                id_usuario,
                data["matricula"],
                data["id_grupo"]   # 🔥 CLAVE
            ))

        elif data["tipo"] == "PERSONAL":
            cur.execute("""
                INSERT INTO Personal (id_usuario, n_plaza)
                VALUES (%s, %s)
            """, (
                id_usuario,
                data["n_plaza"]
            ))

        elif data["tipo"] == "VISITANTE":
            cur.execute("""
                INSERT INTO Visitante (id_usuario, id_institucion)
                VALUES (%s, %s)
            """, (
                id_usuario,
                data["id_institucion"]
            ))

        conn.commit()
        return "✅ Usuario registrado correctamente"

    except Exception as e:
        conn.rollback()
        return f"❌ Error: {e}"

    finally:
        conn.close()