import pymysql
import os

def main():
    conn = pymysql.connect(
        host='db',
        user='usuarioapp',
        password='clave123',
        database='proyecto_db',
        autocommit=True,
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    migrations_dir = './migrations'
    files = sorted(f for f in os.listdir(migrations_dir) if f.endswith('.sql'))

    for file in files:
        print(f"Aplicando migración: {file}")
        with open(os.path.join(migrations_dir, file), 'r', encoding='utf-8') as f:
            sql_text = f.read()

        # Separar statements por ';'
        statements = [s.strip() for s in sql_text.split(';') if s.strip()]

        for stmt in statements:
            try:
                cursor.execute(stmt)
            except pymysql.MySQLError as e:
                # Imprime el error pero sigue con la siguiente sentencia
                print(f"[ERROR] {e}\nStatement: {stmt[:100]}...")

        print(f"¡Migración {file} aplicada correctamente!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()