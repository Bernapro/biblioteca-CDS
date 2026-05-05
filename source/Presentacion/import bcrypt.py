import bcrypt
mi_contrasena = "a"

# Python la encripta
hash_seguro = bcrypt.hashpw(mi_contrasena.encode('utf-8'), bcrypt.gensalt())

# pip uninstall psycopg2 psycopg2-binary -yImprime el resultado
print("\n--- COPIA EL TEXTO ---")
print(hash_seguro.decode('utf-8'))
print("------------------------------------\n")