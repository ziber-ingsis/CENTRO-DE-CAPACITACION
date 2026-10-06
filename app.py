from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
RUTA_BD = 'bd_instituto.db'

# === INICIALIZAR BASE DE DATOS ===
def crear_tablas():
    conn = sqlite3.connect(RUTA_BD)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT,
            telefono TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY,
            nombre_curso TEXT NOT NULL,
            duracion_horas INTEGER,
            precio REAL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY,
            fecha_inscripcion TEXT NOT NULL,
            estudiante_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# === RUTAS PRINCIPALES ===
@app.route('/')
def index():
    return redirect(url_for('lista_inscripciones'))

# --- ESTUDIANTES ---
@app.route('/estudiantes')
def lista_estudiantes():
    conn = sqlite3.connect(RUTA_BD)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM estudiantes")
    datos = c.fetchall()
    conn.close()
    return render_template('estudiantes.html', estudiantes=datos)

@app.route('/estudiantes/nuevo', methods=['GET','POST'])
def nuevo_estudiante():
    if request.method == 'POST':
        conn = sqlite3.connect(RUTA_BD)
        c = conn.cursor()
        c.execute("""
            INSERT INTO estudiantes (nombre, apellido, correo, telefono)
            VALUES (?, ?, ?, ?)
        """, (
            request.form['nombre'],
            request.form['apellido'],
            request.form['correo'],
            request.form['telefono']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('lista_estudiantes'))
    return render_template('form_estudiante.html')

@app.route('/estudiantes/eliminar/<int:id>')
def eliminar_estudiante(id):
    conn = sqlite3.connect(RUTA_BD)
    c = conn.cursor()
    c.execute("DELETE FROM estudiantes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('lista_estudiantes'))

# --- CURSOS ---
@app.route('/cursos')
def lista_cursos():
    conn = sqlite3.connect(RUTA_BD)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM cursos")
    datos = c.fetchall()
    conn.close()
    return render_template('cursos.html', cursos=datos)

@app.route('/cursos/nuevo', methods=['GET','POST'])
def nuevo_curso():
    if request.method == 'POST':
        conn = sqlite3.connect(RUTA_BD)
        c = conn.cursor()
        c.execute("""
            INSERT INTO cursos (nombre_curso, duracion_horas, precio)
            VALUES (?, ?, ?)
        """, (
            request.form['nombre_curso'],
            request.form['duracion_horas'],
            request.form['precio']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('lista_cursos'))
    return render_template('form_curso.html')

@app.route('/cursos/eliminar/<int:id>')
def eliminar_curso(id):
    conn = sqlite3.connect(RUTA_BD)
    c = conn.cursor()
    c.execute("DELETE FROM cursos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('lista_cursos'))

# --- INSCRIPCIONES ---
@app.route('/inscripciones')
def lista_inscripciones():
    conn = sqlite3.connect(RUTA_BD)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT i.id, i.fecha_inscripcion, 
               e.nombre || ' ' || e.apellido AS estudiante,
               c.nombre_curso AS curso
        FROM inscripciones i
        JOIN estudiantes e ON i.estudiante_id = e.id
        JOIN cursos c ON i.curso_id = c.id
    """)
    datos = c.fetchall()
    conn.close()
    return render_template('inscripciones.html', inscripciones=datos)

@app.route('/inscripciones/nuevo', methods=['GET','POST'])
def nueva_inscripcion():
    conn = sqlite3.connect(RUTA_BD)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if request.method == 'POST':
        c.execute("""
            INSERT INTO inscripciones (fecha_inscripcion, estudiante_id, curso_id)
            VALUES (?, ?, ?)
        """, (
            request.form['fecha_inscripcion'],
            request.form['estudiante_id'],
            request.form['curso_id']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('lista_inscripciones'))
    
    # Cargar listas para desplegables
    c.execute("SELECT * FROM estudiantes")
    estudiantes = c.fetchall()
    c.execute("SELECT * FROM cursos")
    cursos = c.fetchall()
    conn.close()
    return render_template('form_inscripcion.html', estudiantes=estudiantes, cursos=cursos)

@app.route('/inscripciones/eliminar/<int:id>')
def eliminar_inscripcion(id):
    conn = sqlite3.connect(RUTA_BD)
    c = conn.cursor()
    c.execute("DELETE FROM inscripciones WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('lista_inscripciones'))

# === EJECUCIÓN ===
if __name__ == '__main__':
    crear_tablas()
    app.run(debug=True)