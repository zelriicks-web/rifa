import os

import psycopg2
from flask import Flask, render_template

app = Flask(__name__)


def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def inicializar_base_de_datos():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS numeros (
            id SERIAL PRIMARY KEY,
            numero INTEGER UNIQUE NOT NULL,
            estado VARCHAR(20) NOT NULL DEFAULT 'disponible'
        )
    """)

    for numero in range(1, 101):
        cursor.execute("""
            INSERT INTO numeros (numero, estado)
            VALUES (%s, 'disponible')
            ON CONFLICT (numero) DO NOTHING
        """, (numero,))

    conn.commit()
    cursor.close()
    conn.close()


@app.route("/")
def inicio():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT numero, estado
        FROM numeros
        ORDER BY numero
    """)

    numeros = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        numeros=numeros
    )


inicializar_base_de_datos()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
