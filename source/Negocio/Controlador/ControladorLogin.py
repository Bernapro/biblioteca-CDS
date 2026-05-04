import bcrypt
# ¡ACTUALIZADO! Apuntamos a 'DBPool' y usamos la variable 'db' que tú creaste
from Persistencia.Postgres.Pool.DBPool import db

class ControladorLogin:
    @staticmethod
    def validar_credenciales(usuario: str, pass_ingresada: str) -> bool:
        try:
            # Usamos tu variable 'db' para conectarnos
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Buscamos la contraseña encriptada (hash) en la base de datos
                    cursor.execute("SELECT password_hash FROM Administrador WHERE usuario = %s", (usuario,))
                    resultado = cursor.fetchone()

                    if resultado:
                        # Extraemos el hash guardado en Postgres
                        hash_guardado = resultado['password_hash']
                        
                        # bcrypt compara lo que escribiste en la pantalla con el texto raro guardado
                        if bcrypt.checkpw(pass_ingresada.encode('utf-8'), hash_guardado.encode('utf-8')):
                            return True # ¡Contraseña correcta!
                            
            return False # Si el usuario no existe o la contraseña está mal
        except Exception as e:
            # Si hay un error (como que no exista la tabla), se imprime aquí
            print(f"Error al validar credenciales en BD: {e}")
            return False