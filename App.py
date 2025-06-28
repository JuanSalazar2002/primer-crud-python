from tkinter import *
from tkinter import messagebox
import sqlite3 as sq

# 1. primero creamos la raiz y ajustamos el tamaño que tendra
root = Tk()
root.title("Aplicacion CRUD")
root.geometry("300x400")
root.resizable(False,False)

# 2. creamos el menu principal y le decimos a la raiz que ese sera su menu
barraMenu = Menu(root)
root.config(menu=barraMenu)

# 8. Declaramos la variables para que pueda almacenar lo que ingresamos, ya que las variables por si solo no se puede obtener
inp_id_var = StringVar()
inp_name_var = StringVar()
inp_pass_var = StringVar()
inp_ape_var = StringVar()
inp_dir_var = StringVar()

# 11. creamos variables para almacenar lo que obtengamos de resultado en BUSCAR depaso que con estos datos seteamos lo que se mostrar en pantalla
bd_id = ""
bd_name = ""
bd_pass = ""
bd_ape = ""
bd_dir = ""
bd_txt = ""

optionBuscar = IntVar()
optionVista = IntVar(value=0)

# 10. creamos las variables para la conexion
miConexion = 0

def borrarTodo():
    inp_id_var.set("")
    inp_name_var.set("")
    inp_pass_var.set("")
    inp_ape_var.set("")
    inp_dir_var.set("")
    txt_com.delete("1.0",END)

def conectarBD():
    global miConexion
    miConexion = sq.connect("GestionUsuarios")
    cursor = miConexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuarios(
    id CHAR(4) PRIMARY KEY, 
    nombre VARCHAR(50),
    password VARCHAR(50),
    apellido VARCHAR(50),
    direccion VARCHAR(50),
    texto TEXT
    )
    """)
    miConexion.commit()
    
    messagebox.showinfo("Conexion","Se establecio una conexion con la base de datos")

def guardar():
    try:
        global miConexion

        if not miConexion: # <- esto es para decir que si no esta conectado entonces que suelte un error
            raise ConnectionError("No hay conexión activa a la base de datos.")

        miCursor = miConexion.cursor()
        miCursor.execute("INSERT INTO Usuarios VALUES (?, ?, ?, ?, ?, ?)", (inp_id_var.get(), 
                                                                            inp_name_var.get(), 
                                                                            inp_pass_var.get(), 
                                                                            inp_ape_var.get(), 
                                                                            inp_dir_var.get(), 
                                                                            txt_com.get("1.0",END).strip()))
        miConexion.commit()

        messagebox.showinfo("Guardado","Se llego a guardar correctamente este registro")
    except ConnectionError as ce:
        print(ce)
    except sq.IntegrityError as ie:
        messagebox.showerror("Error", "Ya hay un registro con ese ID")

def buscar(n_id):
    global bd_id, bd_name, bd_pass, bd_ape, bd_dir, bd_txt

    try:
        global miConexion
         
        if not miConexion:
            raise ConnectionError("No hay conexión activa a la base de datos.")
        
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM Usuarios WHERE id = ?",(n_id,))
        miConexion.commit()

        usuario = miCursor.fetchone() # <- fecthone nos dice que solo va a devolver directamente solo una tupla o un NONE
        
        if usuario != None: # <- esto es para asegurarnos de que estamos recibien datos sino hay nada entonces que de el mensaje
            bd_id,bd_name,bd_pass,bd_ape,bd_dir,bd_txt = usuario

            # aca vamos a ingresar los resultados en pantalla
            inp_name_var.set(bd_name)
            inp_pass_var.set(bd_pass)
            inp_ape_var.set(bd_ape)
            inp_dir_var.set(bd_dir)
            txt_com.delete("1.0",END) # <- esto es para borrar el texto anterior y que no se vaya acumulando
            txt_com.insert("1.0",str(bd_txt))
        else:
            print("No hay ningun usuario registrado con ese ID")

    except ConnectionError as ce:
        print(ce)

def eliminar(n_id):
    global miConexion
    try:
        if not miConexion:
            raise ConnectionError("Error en la conexion con la base de datos")
        
        cursor = miConexion.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE id = ?",(n_id,))
        miConexion.commit()

        borrarTodo()

        messagebox.showinfo("Eliminacion", "Se elimino correctamente el registro")

    except ConnectionError as ce:
        messagebox.showerror("Error","No se puedo eliminar el registro")

def actualizar():
    global miConexion

    try:
        if not miConexion:
            raise ConnectionError("Error en la conexion con la base de datos")

        cursor = miConexion.cursor()
        cursor.execute("UPDATE Usuarios SET nombre = ?, password = ?, apellido = ?, direccion = ?, texto = ? WHERE id = ? ", (inp_name_var.get(), inp_pass_var.get(), inp_ape_var.get(), inp_dir_var.get(), txt_com.get("1.0", END), inp_id_var.get()))
        miConexion.commit()

        messagebox.showinfo("Actualizacion","La actualizacion se realizo con exito")

    except ConnectionError as ce:
        messagebox.showerror("Error", "Error con la conexion con la base de datos")

def salir():
    global miConexion

    if miConexion:
        miConexion.close()
    root.destroy()
    print("===Se Cerro Exitosamente===")

def registros():
    global miConexion
    raiz = Toplevel()
    raiz.geometry("800x400")

    # primero hacemos que se cree el espacio donde iran los encabazados
    encabezados = Frame(raiz)
    encabezados.pack()
    
    # aca ira los datos que tomemos
    elFrame = Frame(raiz)
    elFrame.pack()

    columnas = ["ID", "NOMBRE", "CONTRASEÑA", "APELLIDO", "DIRECCION", "TEXTO"]
    for idx, titulo in enumerate(columnas):
        Label(encabezados, text=titulo, borderwidth=1, relief="solid", width=15).grid(row=0, column=idx, padx=5, pady=5)

    try:
        cursor = miConexion.cursor()

        cursor.execute("SELECT * FROM Usuarios")
        miConexion.commit()
        usuarios = cursor.fetchall()

        if usuarios:
            for i,j in enumerate(usuarios):
                Label(elFrame, text=f"{j[0]}", width=15).grid(row=i, column=0, padx=5, pady=5)
                Label(elFrame, text=f"{j[1]}", width=15).grid(row=i, column=1, padx=5, pady=5)
                Label(elFrame, text=f"{j[2]}", width=15).grid(row=i, column=2, padx=5, pady=5)
                Label(elFrame, text=f"{j[3]}", width=15).grid(row=i, column=3, padx=5, pady=5)
                Label(elFrame, text=f"{j[4]}", width=15).grid(row=i, column=4, padx=5, pady=5)
                Label(elFrame, text=f"{j[5]}", width=15).grid(row=i, column=5, padx=5, pady=5)
        else:
            Label(elFrame, text="No hay datos disponibles").pack()
    except AttributeError as ae:
        Label(elFrame, text="No se establecio una conexion a la base de datos").pack()
        # print("Error : ", ae)

    raiz.mainloop()

def idAutoincremental():
    global miConexion
    cursor = miConexion.cursor()    
    
    cursor.execute("SELECT * FROM Usuarios WHERE ROWID IN (SELECT max(ROWID) FROM Usuarios)")
    miConexion.commit()
    valor = cursor.fetchone()

    if valor is not None:
        ultimo_dato = valor[0] # <- U007

        # valPri = ultimo_dato[:1]
        ultimo_numero = str(int(ultimo_dato[1:]) + 1)
        valor_id = "U"

        for i in range(4):
            if len(valor_id) + len(ultimo_numero) < 4:
                valor_id = valor_id + "0"

        nuevo_id = valor_id + ultimo_numero
    else:
        nuevo_id = "U001"
    
    return nuevo_id # <- es un str

def habilitar_entry():
    global miConexion

    try:
        if not miConexion:
            raise ConnectionError("No hay conexión activa a la base de datos.")

        if optionBuscar.get() == 1:
            inp_id.config(state="disabled")
            inp_id_var.set(idAutoincremental())
        else:
            inp_id.config(state="normal") 
            inp_id_var.set("")
    except ConnectionError as ce:
        print(ce)

def vistaContra():
    if optionVista.get() == 1:
        inp_pass.config(show="")
    else:
        inp_pass.config(show="*")

# 4. creamos los submenus que tendra nuestra opcion BBDD y creamos sus submenus
# Opcion Barra BBDD
barraBBDD = Menu(barraMenu, tearoff=0)
barraBBDD.add_cascade(label="Conectar", command=conectarBD)
barraBBDD.add_cascade(label="Salir", command=salir)

# Opcion Barra OPCIONES
barraOpciones = Menu(barraMenu, tearoff=0)
barraOpciones.add_cascade(label="Limpiar Pantalla", command= borrarTodo)
barraOpciones.add_cascade(label="Mostrar Registros", command=registros)

# 3. añadimos los elementos que tendra nuestro menu
# 5. en "menu" enlazamos a su correspondiente menu
barraMenu.add_cascade(label="BBDD", menu=barraBBDD)
barraMenu.add_cascade(label="Opciones", menu=barraOpciones)

# 6. creamos nuestro frame
miFrame = Frame()
miFrame.pack()

# 7. creamos los mensajes e insertamos los entry para poder añadir los campos
Label(miFrame, text="ID").grid(row=0, column=0)
inp_id = Entry(miFrame, textvariable=inp_id_var)
inp_id.grid(row=0, column=1, padx=5, pady=5)

Checkbutton(miFrame, text="ID", variable=optionBuscar, onvalue=1, offvalue=0, command=habilitar_entry).grid(row=0, column=2)

Label(miFrame, text="NOMBRE").grid(row=1, column=0)
inp_name = Entry(miFrame, textvariable=inp_name_var)
inp_name.grid(row=1, column=1, padx=5, pady=5)

Label(miFrame, text="PASSWORD").grid(row=2, column=0)
inp_pass = Entry(miFrame, textvariable=inp_pass_var, show="*")
inp_pass.grid(row=2, column=1, padx=5, pady=5)
Checkbutton(miFrame, text="VISTA", variable=optionVista, onvalue=1, offvalue=0, command=vistaContra).grid(row=2, column=2) # <- aqui hay que crear para que sea visible la contraseña


Label(miFrame, text="APELLIDO").grid(row=3, column=0)
inp_ape = Entry(miFrame, textvariable=inp_ape_var)
inp_ape.grid(row=3, column=1, padx=5, pady=5)

Label(miFrame, text="DIRECCION").grid(row=4, column=0)
inp_dir = Entry(miFrame, textvariable=inp_dir_var)
inp_dir.grid(row=4, column=1, padx=5, pady=5)

Label(miFrame, text="COMENTARIO").grid(row=5, column=0)
txt_com = Text(miFrame, width=15, height=5)
txt_com.grid(row=5, column=1, padx=5, pady=5)

# 9. creamos los botones
botonGuardar = Button(miFrame, text="Guardar", command=guardar)
botonGuardar.grid(row=6, column=0, padx=5, pady=5)

botonBuscar = Button(miFrame, text="Buscar", command=lambda:buscar(inp_id_var.get()))
botonBuscar.grid(row=6, column=1, padx=5, pady=5)

botonEliminar = Button(miFrame, text="Eliminar", command= lambda: eliminar(inp_id_var.get()))
botonEliminar.grid(row=7, column=0, padx=5, pady=5)

botonEliminar = Button(miFrame, text="Actualizar", command=actualizar)
botonEliminar.grid(row=7, column=1, padx=5, pady=5)
root.mainloop()