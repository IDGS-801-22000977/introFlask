from datetime import datetime
from flask import Flask, render_template, request
import forms 

app=Flask(__name__) 

@app.route("/")
def index():
    titulo="IDGS801"
    lista=["pedro", "juan", "luis"]
    return render_template("index.html",titulo=titulo, lista=lista)

@app.route("/ejemplo1")
def ejemplo1():
   return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
   return render_template("ejemplo2.html")


@app.route("/hola")
def hola():
   return "<h1>Hello World -- Hola we</h1>"

@app.route("/user/<string:user>")
def user(user):
   return f"<h1>Hola, {user}! </h1>"

@app.route("/numero/<int:n>")
def numero(n):
   return f"<h1>El numero es: {n}! </h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
   return f"<h1>Hola, {username}: Tu id es {id} </h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
   return f"<h1>La suma es: {n1+n2}</h1>"

@app.route("/default/")
@app.route("/default/<string:param>") 
def func(param="Juan"):
   return f"<h1>Hola, {param} </h1>"

@app.route("/ope")
def o():
   return '''
    <form>
        <label for="name">Name:</label>
<input type="text" id="name" name="name" required>

<label for="Password">Password:</label>
<input type="text" id="Password" name="Password" required>


        </label>
    </form>

'''
@app.route("/OperasBas", methods=["GET", "POST"])
def operas():
    resultado = None  # Inicializar la variable resultado

    if request.method == "POST":
        n1 = int(request.form.get("n1"))
        n2 = int(request.form.get("n2"))
        operacion = request.form.get("operacion")

        if operacion == "suma":
            resultado = f"{n1} + {n2} = {n1 + n2}"
        elif operacion == "resta":
            resultado = f"{n1} - {n2} = {n1 - n2}"
        elif operacion == "multiplicacion":
            resultado = f"{n1} * {n2} = {n1 * n2}"
        elif operacion == "division":
            if n2 != 0:
                resultado = f"{n1} / {n2} = {n1 / n2}"
            else:
                resultado = "Error: No se puede dividir por cero."

    return render_template("OperasBas.html", resultado=resultado)
 
 

@app.route("/Alumnos",methods=["GET","POST"])
def alumnos():
    mat=''
    nom=''
    ape=''
    correo=''
    alumno_clas=forms.UserForm(request.form)
    if request.method == 'POST':
        mat = alumno_clas.matricula.data
        nom = alumno_clas.nombre.data
        ape = alumno_clas.apellido.data
        correo = alumno_clas.correo.data


    return render_template("Alumnos.html",form=alumno_clas,mat=mat,nom=nom,ape=ape,correo=correo)
 # CINEPÓLIS -------------------------------------------------------------------------------------



class Cine:
    precio_boleto = 12
    ventas = []

    def calcular_descuento(self, total, boletos):
        if boletos > 5:
            return total * 0.85
        elif 3 <= boletos <= 5:
            return total * 0.90
        else:
            return total

    def validar_boletos(self, personas, boletos):
        return boletos <= personas * 7

    def guardar_venta(self, nombre, total):
        self.ventas.append((nombre, total))

    def mostrar_resumen_ventas(self):
        if not self.ventas:
            return "No se realizaron ventas."
        else:
            resumen = ""
            total_general = 0
            for nombre, total in self.ventas:
                resumen += f"{nombre}: ${total:.2f}<br>"
                total_general += total
            resumen += f"Total General: ${total_general:.2f}"
            return resumen

cine = Cine()

@app.route("/cinepolis", methods=["GET", "POST"])
def cinepolis():
    resultado = None

    if request.method == "POST":
        nombre = request.form.get("nombre")
        personas = int(request.form.get("personas"))
        boletos = int(request.form.get("boletos"))
        metodo_pago = request.form.get("metodo_pago")

        if cine.validar_boletos(personas, boletos):
            total = cine.precio_boleto * boletos
            total_con_descuento = cine.calcular_descuento(total, boletos)

            # Aplicar descuento adicional si el método de pago es tarjeta
            if metodo_pago == "tarjeta":
                total_con_descuento *= 0.90

            cine.guardar_venta(nombre, total_con_descuento)
            resultado = f"Total a pagar: ${total_con_descuento:.2f}<br>"
        else:
            resultado = "Cantidad de boletos no válida (máximo 7 por persona)."

    return render_template("cinepolis.html", resultado=resultado)

# ZODIACO CHINO --------------------------------------------------------------------------------------

def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def obtener_signo_zodiaco_chino(anio):
    signos = ["Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey", "Tigre", "Conejo", "Dragon", "Serpiente", "Caballo", "Cabra"]
    return signos[anio % 12].lower()  


@app.route("/zodiaco", methods=["GET", "POST"])
def zodiaco():
    resultado = None
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido_paterno = request.form.get("apellido_paterno")
        apellido_materno = request.form.get("apellido_materno")
        dia = int(request.form.get("dia"))
        mes = int(request.form.get("mes"))
        anio = int(request.form.get("anio"))
        sexo = request.form.get("sexo")

        fecha_nacimiento = datetime(anio, mes, dia)
        edad = calcular_edad(fecha_nacimiento)
        signo = obtener_signo_zodiaco_chino(anio)

        resultado = {
            "nombre_completo": f"{nombre} {apellido_paterno} {apellido_materno}",
            "edad": edad,
            "signo": signo,
            "sexo": sexo
        }

    return render_template("zodiacoChino.html", resultado=resultado)





#levantar el servidor 
if __name__=="__main__":
    app.run(debug=True,port=3000)

