'''
Todo:
    - A el formulairo de registro (campo password y email) si valida que esten llenos apropiadamente pero no muestra mensaje de error si no lo estan
    - El campo email no valida si el correo es de un dominio de correos real o reconocido
    - Hacer que durante le registro, si ya hay una cuenta usando ese correo, no permita generar registro
'''

from flask import Flask, render_template
from flask import request
from bd import getDatabase
from flask import make_response
from flask import session
from flask import url_for
from flask import redirect
import crud
import registerForm
import json

app = Flask(__name__)
app.secret_key = 'papasconchile'

db = getDatabase()

@app.route("/")
def index():
    panaderia = crud.readDoc(db,'producto',{})
    largo = len(panaderia)
    return render_template("kt.html", article=panaderia, largo=largo)

@app.route("/article/<idOnWeb>", methods=['GET','POST'])
def article(idOnWeb):
    arti = crud.readDocById(db,'producto',idOnWeb)
    arti = crud.clearFormat(arti)

    sellingForm = registerForm.Selling(request.form)
    if request.method == 'POST' and sellingForm.validate() and 'username' in session:
         session.get('carrito', [])
         carrito = []
         artiqlo={'_id':sellingForm.articleId.data, 'quantity':sellingForm.quantity.data}
         carrito.append(artiqlo)
         session['carrito'] = carrito
         print(session['carrito'])
    return render_template("article.html", articulo=arti, form=sellingForm)

@app.route("/register/", methods=['GET','POST'])
def register():
    formulario = registerForm.Register(request.form)
    if request.method == 'POST' and formulario.validate():
            newUser={
                'username':formulario.username.data,
                'mail':formulario.mail.data,
                'nombre':formulario.names.data,
                'apellido':formulario.lastNames.data,
                'password':formulario.password.data,
                'direccion':formulario.address.data,
                'rfc':formulario.rfc.data
            }
            crud.createOneDoc(db,'usuarios',newUser)
    return render_template("register.html", form=formulario)

@app.route("/login/", methods=['GET','POST'])
def login():
     formulario = registerForm.Login(request.form)
     if request.method == 'POST' and formulario.validate():
        checkUser={'username':formulario.username.data,'password':formulario.password.data}
        validateUser = crud.readDoc(db,'usuarios',{'username':checkUser['username']})
        validateUser = crud.clearFormat(validateUser)
        if(validateUser):
            if(checkUser['password']==validateUser['password']):
                session['username']=checkUser['username']
                print("Login hecho exitosamente")
     return render_template("login.html", form=formulario)

@app.route("/logout/")
def logout():
     if 'username' in session:
          session.pop('username', None)
          print('username borrado')
     if 'carrito' in session:
          session.pop('carrito', None)
          print('carrito borrado')
     return redirect(url_for('index'))

@app.route("/user/", methods=['GET','POST'])
def user():
    formulario = registerForm.Register(request.form)
    if request.method == 'POST' and formulario.validate():
            newUser={
                'username':formulario.username.data,
                'mail':formulario.mail.data,
                'nombre':formulario.names.data,
                'apellido':formulario.lastNames.data,
                'password':formulario.password.data,
                'direccion':formulario.address.data,
                'rfc':formulario.rfc.data
            }
            crud.createOneDoc(db,'usuarios',newUser)
    return render_template("user.html", form=formulario)

@app.route("/cart/")
def cart():
     return render_template("cart.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)