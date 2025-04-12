from flask import Flask, request, render_template
import psycopg2
import os

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
DB_HOST = os.environ.get('DB_HOST', '129.213.105.247')
DB_NAME = os.environ.get('DB_NAME', 'registro_restaurante')
DB_USER = os.environ.get('DB_USER', 'reportesiga')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'fRB3raM6pu')
DB_PORT = os.environ.get('DB_PORT', '5432')

@app.route('/', methods=['GET', 'POST'])
def registro_comensales():
    mensaje = None
    error = False
    if request.method == 'POST':
        fecha = request.form['fecha']
        comensales_manana = request.form['comensales_manana']
        comensales_tarde = request.form['comensales_tarde']

        conn = None  # Inicializa la conexión como None
        cur = None   # Inicializa el cursor como None

        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            cur = conn.cursor()
            query = "INSERT INTO registro_comensales (fecha, comensales_manana, comensales_tarde) VALUES (%s, %s, %s)"
            cur.execute(query, (fecha, comensales_manana, comensales_tarde))
            conn.commit()
            mensaje = "Registro guardado exitosamente."

        except psycopg2.Error as e:
            error = True
            mensaje = f"Error de base de datos: {e}"
            if conn:
                conn.rollback()
        except Exception as e:
            error = True
            mensaje = f"Error inesperado: {e}"
            if conn:
                conn.rollback()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template('formulario_ingreso.html', mensaje=mensaje, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')