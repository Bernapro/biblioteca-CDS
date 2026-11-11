import bcrypt
# ¡ACTUALIZADO! Apuntamos a 'DBPool' y usamos la variable 'db' que tú creaste
from Persistencia.Postgres.Pool.DBPool import db

class ControladorLogin:
    @staticmethod
    def validar_credenciales(usuario: str, pass_ingresada: str) -> tuple[bool, dict | None]:
        usuario_limpio = (usuario or "").strip()
        if not usuario_limpio or not pass_ingresada:
            return False, None

        try:
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_admin, usuario, password_hash, nombre_completo, rol FROM Administrador WHERE usuario = %s",
                        (usuario_limpio,)
                    )
                    resultado = cursor.fetchone()

                    if resultado:
                        hash_guardado = resultado['password_hash']
                        
                        # bcrypt compara lo que escribiste en la pantalla con el texto raro guardado
                        if bcrypt.checkpw(pass_ingresada.encode('utf-8'), hash_guardado.encode('utf-8')):
                            datos_usuario = {
                                "id_admin": resultado["id_admin"],
                                "usuario": resultado["usuario"],
                                "nombre_completo": resultado["nombre_completo"],
                                "rol": resultado["rol"]
                            }
                            return True, datos_usuario
                            
            return False, None # Si el usuario no existe o la contraseña está mal
        except Exception as e:
            # Si hay un error se imprime aquí
            print(f"Error al validar credenciales en BD: {e}")
            return False, None

    @staticmethod
    def registrar_administrador(
        nombre_completo: str,
        usuario: str,
        pass_plana: str,
        rol: str = "BIBLIOTECARIO"
    ) -> tuple[bool, str]:
        nombre_limpio = (nombre_completo or "").strip()
        usuario_limpio = (usuario or "").strip()
        rol_limpio = (rol or "BIBLIOTECARIO").strip()

        if not nombre_limpio or not usuario_limpio or not pass_plana:
            return False, "Por favor, llena todos los campos."

        if len(usuario_limpio) > 50:
            return False, "El usuario no puede exceder los 50 caracteres."

        if len(nombre_limpio) > 100:
            return False, "El nombre completo no puede exceder los 100 caracteres."

        try:
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM Administrador WHERE usuario = %s",
                        (usuario_limpio,)
                    )
                    if cursor.fetchone() is not None:
                        return False, "El nombre de usuario ya existe."

                    hash_seguro = bcrypt.hashpw(
                        pass_plana.encode('utf-8'),
                        bcrypt.gensalt()
                    ).decode('utf-8')

                    cursor.execute(
                        "INSERT INTO Administrador (usuario, password_hash, nombre_completo, rol) VALUES (%s, %s, %s, %s)",
                        (usuario_limpio, hash_seguro, nombre_limpio, rol_limpio)
                    )
                conn.commit()
            return True, "Usuario creado correctamente"
        except Exception as e:
            print(f"Error al registrar administrador en BD: {e}")
            return False, f"Error al crear el usuario: {e}"