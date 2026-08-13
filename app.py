from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    numeros = []

    for numero in range(1, 101):
        numeros.append(f"{numero:04d}")

    return render_template(
        "index.html",
        numeros=numeros
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
