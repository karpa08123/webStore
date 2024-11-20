from flask import Flask, render_template
from flask import request
from bd import GetDatabase
import crud

app = Flask(__name__)

db = GetDatabase()
coleccion='producto'

@app.route("/")
def index():
    return render_template("kioskTerminal.html")

@app.route("/article/")
@app.route("/article/<idOnWeb>")
def article(idOnWeb = "67377e582b8385850b42f808"):
    arti = crud.ReadDocById(db,coleccion,idOnWeb)
    arti = crud.ClearFormat(arti)
    return render_template("article.html", articleName=arti['nombre'], articleDescription=arti['descripcion'])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)