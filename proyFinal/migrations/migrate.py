import pymysql
import os
import re

def split_by_tables(sql_text):
    # Divide el SQL por tablas usando el comentario "-- Estructura de tabla para la tabla `NombreTabla`"
    bloques = re.split(r'--\s+Estructura de tabla para la tabla `([^`]+)`', sql_text)
    # bloques[0] es lo que viene antes del primer CREATE TABLE, lo ignoramos
    # después cada par [nombre_tabla, sql_bloque]
    resultados = []
    for i in range(1, len(bloques), 2):
        tabla = bloques[i]
        contenido = bloques[i+1]
        resultados.append((tabla, contenido))
    return resultados

def execute_statements(cursor, sql_text):
    # Arreglo rápido para separar sentencias SQL (mejorar según necesidad)
    statements = [s.strip() for s in sql_text.split(';') if s.strip()]
    for stmt in statements:
        cursor.execute(stmt + ';')

def execute_drop_statements(cursor, sql_text):
    # Buscar todas las sentencias DROP TABLE IF EXISTS y ejecutarlas
    drop_statements = re.findall(r'DROP TABLE IF EXISTS .*?;', sql_text, re.IGNORECASE | re.DOTALL)
    for drop_sql in drop_statements:
        try:
            print(f"Ejecutando drop: {drop_sql.strip()}")
            cursor.execute(drop_sql)
        except Exception as e:
            print(f"Error ejecutando drop: {e}")

def main():
    conn = pymysql.connect(
        host='db',
        user='usuarioapp',
        password='clave123',
        database='proyecto_db',
        autocommit=False,
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS migrations_applied (
        filename VARCHAR(255) PRIMARY KEY,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

    migrations_dir = './migrations'
    files = sorted(f for f in os.listdir(migrations_dir) if f.endswith('.sql'))

    for file in files:
        cursor.execute("SELECT COUNT(*) FROM migrations_applied WHERE filename=%s", (file,))
        if cursor.fetchone()[0] == 0:
            print(f"Applying migration {file}")

            with open(os.path.join(migrations_dir, file), 'r', encoding='utf-8') as f:
                sql = f.read()

            # Primero ejecuto los drops (si existen)
            execute_drop_statements(cursor, sql)

            # Después sigo con el split por tablas y el resto normal
            tablas = split_by_tables(sql)

            for tabla, contenido in tablas:
                print(f"Procesando tabla {tabla}")

                # Verifico si tabla existe (después de drops probablemente no exista)
                cursor.execute(f"SHOW TABLES LIKE '{tabla}';")
                tabla_existe = cursor.fetchone() is not None

                # Extraigo el bloque CREATE TABLE
                match_create = re.search(r'(CREATE TABLE.*?;)', contenido, re.DOTALL | re.IGNORECASE)
                if match_create and not tabla_existe:
                    create_sql = match_create.group(1)
                    try:
                        print(f"Creando tabla {tabla}")
                        cursor.execute(create_sql)
                    except Exception as e:
                        print(f"Error creando tabla {tabla}: {e}")

                # Extraigo bloque INSERT para esta tabla
                inserts = re.findall(r'(INSERT INTO `?' + re.escape(tabla) + r'`?.*?;)', contenido, re.DOTALL | re.IGNORECASE)
                for insert_sql in inserts:
                    try:
                        print(f"Insertando datos en {tabla}")
                        cursor.execute(insert_sql)
                    except Exception as e:
                        print(f"Error insertando datos en {tabla}: {e}")

            # Marcar migración como aplicada
            cursor.execute("INSERT INTO migrations_applied (filename) VALUES (%s)", (file,))
            conn.commit()

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
