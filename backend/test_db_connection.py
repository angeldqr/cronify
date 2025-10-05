import psycopg2

try:
    conn = psycopg2.connect(
        dbname="cronify_db",
        user="postgres",
        password="tu_contraseña",  # Cambia esto
        host="localhost",
        port="5432",
        options="-c client_encoding=UTF8"
    )
    print("Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
