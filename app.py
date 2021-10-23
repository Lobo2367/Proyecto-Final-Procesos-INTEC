#Importación e instalación de librerías y módulos
from flask import Flask, config
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from pymysql.cursors import Cursor
from datetime import datetime
import os

#Implementacion de flask
app= Flask(__name__)

# Declaración de la base de datos
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

#Declaración de carpeta uploads para el manejo de imágenes

CARPETA= os.path.join(r'C:/Users/kingd/Desktop/proyecto/uploads')
app.config['CARPETA']=CARPETA



#Dirección Index/Función Principal
@app.route('/')
#Método index
def index():

	#Llamada y activación de la base de datos
	sql="SELECT * FROM `estudiantes`;"
	conn= mysql.connect()
	cursor=conn.cursor()
	cursor.execute(sql)
	estudiantes=cursor.fetchall()
	print(estudiantes)
	conn.commit()

	#Renderización de la plantilla "index.html, a partir de los datos suministrados"
	return render_template('est/index.html', estudiantes=estudiantes)



# Dirección destroy (Eliminación de una entidad)
@app.route('/destroy/<int:id>')
#Método destroy
def destroy(id):

	#Llamada y eliminacion de una entidad de la base de datos
	conn= mysql.connect()
	cursor=conn.cursor()
	cursor.execute("DELETE FROM estudiantes WHERE id=%s",(id))
	conn.commit()

	#Retorno a  "Index"
	return redirect('/')


#Dirección edit (Editar una entidad "estudiante" de la base de datos)
@app.route('/edit/<int:id>')
#Método edit
def edit(id):

	#Llamada y actualización de una determinada tabla de la base de datos.
	conn= mysql.connect()
	cursor=conn.cursor()
	cursor.execute("SELECT * FROM estudiantes WHERE id=%s", (id))
	estudiantes=cursor.fetchall()
	conn.commit()
	
	#Renderización de la plantilla 'edit'(formulario) con los datos suministrados.
	return render_template('est/edit.html', estudiantes= estudiantes)
	

@app.route('/update', methods=['POST'])
def update():

	_nombre=request.form["txtNombre"]
	_correo=request.form["txtCorreo"]
	_foto=request.files["txtFoto"]
	_materias=request.form["txtMateria"]
	id=request.form["txtID"]

	sql="UPDATE `estudiantes` SET `nombre`=%s, `correo`=%s, `Materias`=%s WHERE id=%s ;"
	datos=(_nombre,_correo,_materias,id)


	conn= mysql.connect()
	cursor=conn.cursor()

	now= datetime.now()
	tiempo=now.strftime("%Y%H%M%S")
	
	if _foto.filename != '':
		
		nuevoNombreFoto=tiempo+_foto.filename
		_foto.save(r'uploads/'+nuevoNombreFoto)

		cursor.execute("SELECT foto FROM estudiantes WHERE id=%s",id)
		fila=cursor.fetchall()

		cursor.execute("UPDATE estudiantes SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
		conn.commit()

	cursor.execute(sql,datos)
	conn.commit()



	return redirect("/")



@app.route('/create')
def create():
	return render_template('est/create.html')

@app.route('/store', methods=['POST'])
def storage():
	_nombre=request.form["txtNombre"]
	_correo=request.form["txtCorreo"]
	_foto=request.files["txtFoto"]
	_materia=request.form["txtMateria"]
	nuevoNombreFoto = _foto.filename
	now= datetime.now()
	tiempo=now.strftime("%Y%H%M%S")
	
	if _foto.filename != '':
		nuevoNombreFoto=tiempo+_foto.filename
		_foto.save("uploads/"+nuevoNombreFoto)



	sql="INSERT INTO `estudiantes` (`id`, `nombre`, `correo`, `calificación`, `Materias`) VALUES (NULL, %s,%s, %s, %s);"
	
	datos=(_nombre,_correo,nuevoNombreFoto,_materia)
	conn= mysql.connect()
	cursor=conn.cursor()
	cursor.execute(sql,datos)
	conn.commit()
	return redirect("/")


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)