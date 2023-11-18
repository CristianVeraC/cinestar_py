from flask import Flask, render_template, request

import mysql.connector
app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'CineStar',
    'port': 3306,
}


@app.route('/index')
def index():
   return render_template('index.html')

@app.route('/pelicula')
def get_pelicula():
    try:
        id = request.args.get('id')
        connection = mysql.connector.connect(*db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM pelicula WHERE id = %s', (id,))
        movie_data = cursor.fetchone()
        cursor.close()
        connection.close()
        if movie_data:
            return render_template('pelicula.html')
        else:
            return 'No se encontró película'
    except mysql.connector.Error as e:
        return f"Error al obtener datos: {str(e)}"
    
@app.route('/cines')
def get_cines():
    try:
        connection = mysql.connector.connect(db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM cine') 
        cines = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('cines.html', cines=cines)
    except mysql.connector.Error as e:
        return f"Error al obtener los datos: {str(e)}"

@app.route('/peliculas')
def mostrar_peliculas():
    try:
        connection = mysql.connector.connect(db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM pelicula')
        peliculas = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('peliculas.html', peliculas=peliculas)
    except mysql.connector.Error as e:
        return f"Error de peliculas: {str(e)}"
    
@app.route('/cine')
def get_cine():
    try:
        id = request.args.get('id')
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Cine WHERE id = %s', (id,))
        cine_data = cursor.fetchone()
        cursor.execute('SELECT * FROM CineTarifa WHERE idCine = %s', (id,))
        tarifas_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('cine.html', cine=cine_data, tarifas=tarifas_data)
    except mysql.connector.Error as e:
        return f"Error al obtener datos del cine: {str(e)}"
   
if __name__=='__main__':
    app.run(debug=True, port=5000)
