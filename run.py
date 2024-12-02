'''
Todo:
    - A el formulairo de registro (campo password y email) si valida que esten llenos apropiadamente pero no muestra mensaje de error si no lo estan
    - El campo email no valida si el correo es de un dominio de correos real o reconocido
    - Hacer que durante le registro, si ya hay una cuenta usando ese correo, no permita generar registro
'''

from flask import Flask, render_template
from flask import request
from bd import getDatabase
from flask import session
from flask import url_for
from flask import redirect
from bson.objectid import ObjectId
import crud
import registerForm

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
        if 'carrito' not in session:
            session.get('carrito', [])
            print('Se genero un carrito')
            carrito = []
        elif 'carrito' in session:
            carrito = session.get('carrito')
            print('se extrajo un carrito')
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
                session['id']=str(validateUser['_id'])
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
    query =[]
    carro = session.get('carrito', [])
    for item in carro:
         flag1 = crud.readDocById(db,'producto',item['_id'])
         flag1 = crud.clearFormat(flag1)
         query.append(flag1)
    largo = len(query)

    sumatoria=0
    for i in range(0,largo,1):
        sumatoria = sumatoria + ((float(query[i]['precio'])-(float(query[i]['descuento'])*float(query[i]['precio'])))*float(carro[i]['quantity']))
    iva = sumatoria + (sumatoria*0.16)
    return render_template("cart.html", bigData=query, littleData=carro, largo=largo, sumatoria=sumatoria, IVA=iva)

@app.route("/checkout/", methods=['GET','POST'])
def checkout():
    from datetime import datetime
    subtotal = request.form.get('total')
    total = request.form.get('iva')

    productos = []
    i = 0
    while True:
        product_id = request.form.get(f"products[{i}][id]")
        quantity = request.form.get(f"products[{i}][quantity]")
        price = request.form.get(f"products[{i}][price]")
        discount = request.form.get(f"products[{i}][discount]")

        if not product_id:
            break
        productos.append({
            "idArticulo": product_id,
            "cantidad": int(quantity),
            "precio": float(price),
            "descuento": float(discount)
        })
        i += 1

    userdata = crud.readDocById(db,'usuarios',session['id'])
    userdata = crud.clearFormat(userdata)
    vendedorData = crud.readDocById(db,'usuarios','674d806dbb06e34cda70056c')
    vendedorData = crud.clearFormat(vendedorData)

    venta = {
        'idUsuario':str(userdata['_id']),
        'domicilio':str(userdata['direccion']),
        'articulos':productos,
        'subtotal':subtotal,
        'metodoPago':'efectivo',
        'totalIva':total
    }

    crud.createOneDoc(db,'ventas',venta)
    print("venta generada")

    ventaData = crud.readDoc(db,'ventas',venta)
    ventaData = crud.clearFormat(ventaData)

    xmlGenerales={
        'folio':str(ObjectId()),
        'version':4,
        'noDeVenta':ventaData['_id'],
        'fechaEmision':str(datetime.now()),
        'lugarExpedicion':vendedorData['direccion'],
    }
    xmlVenta={
        'articulos':productos,
        'subTotal':subtotal,
        'totalIva':total,
        'metodoPago':'efectivo'
    }
    xmlVendedor={
        'rfc':vendedorData['rfc'],
        'nombre':vendedorData['nombre'],
    }

    compradorNombre = userdata['nombre'] + " "+ userdata['apellido']
    xmlComprador={
        'rfc':userdata['rfc'],
        'nombre':compradorNombre,
        'domicilio':userdata['direccion']
    }

    xml={
        'generales':xmlGenerales,
        'venta':xmlVenta,
        'vendedor':xmlVendedor,
        'comprador':xmlComprador         
    }

    crud.createOneDoc(db,'xml',xml)
    print('xml generado!!!!!!!')

    return render_template("checkout.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)