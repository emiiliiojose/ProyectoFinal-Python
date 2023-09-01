from tkinter import *
from tkinter import ttk
import psycopg2
import tkinter.messagebox as m
from operator import itemgetter
#from cryptography.fernet import Fernet
#import base64
#import bcrypt
import tkinter as tk
import speech_recognition as sr
import pyperclip
import random
import array

mainWindow = Tk()
mainWindow.title("Keyper")
mainWindow.geometry("1000x600")
mainWindow.iconbitmap (r"C:\Users\nelso\Downloads\PF - Python\keyper_icon.ico")
mainWindow.resizable(False, False)

welcome_frame = Frame(mainWindow, bg="#2D364C")
welcome_frame.pack()
welcome_frame.pack_propagate(False)
welcome_frame.configure(width=1000, height=600)

logo_keyper_welcome = PhotoImage(file=r"C:\Users\nelso\Downloads\PF - Python\logo_keyper_menu2.png")
logo_menu_welcome = Label(welcome_frame, image = logo_keyper_welcome)
logo_menu_welcome.place(x=350, y=15)

lb_welcome = Label(welcome_frame, text="Bienvenido/a\n", font=("Roboto", 30, "bold"), fg="#ffffff", bg="#2D364C").place(x=285, y=180)
lb_welcomeText = Label(welcome_frame, text="Este es el baúl de contraseñas Keyper!", font=("Roboto", 40), fg="#ffffff", bg="#2D364C").place(x=50, y=300)

def conexion():
    con = psycopg2.connect(
                dbname="prypassword",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
    return con

#Método para hacer el logeo
def Login():
    loginWindow = Tk()
    loginWindow.title("Keyper")
    loginWindow.geometry("1000x600")
    loginWindow.resizable(False, False)
    loginWindow.iconbitmap (r"C:\Users\nelso\Downloads\PF - Python\keyper_icon.ico")
    
    login_frame = Frame(loginWindow, bg="#2D364C")
    login_frame.pack()
    login_frame.pack_propagate(False)
    login_frame.configure(width=1000, height=600)

    lb_login = Label(login_frame, text="Inicio de sesión\n", font=("Roboto", 24, "bold"), fg="#ffffff", bg="#2D364C")
    lb_login.place(x=285, y=180)
    
    con=conexion()
    cursor = con.cursor()
    conn=conexion()
    cursor2 = conn.cursor()

    emai = Label(loginWindow, text="Nombre de usuario:", bg="#2D364C", fg="#ffffff")
    emai.place(x=220, y=300)
    
    password = Label(loginWindow, text="Contraseña:",bg="#2D364C", fg="#ffffff")
    password.place(x=220, y=350)

    e1 = Entry(loginWindow, width="40", highlightthickness=2)
    e1.place(x=350, y=300)
    e2 = Entry(loginWindow, width="40", highlightthickness=2, show="*")
    e2.place(x=350, y=350)

    #Comprobación del usuario para permitir el acceso
    def check ():
        sqlCommand1 = "select username from users"
        sqlCommand2 = "select password_hash from users"

        cursor.execute(sqlCommand1)
        cursor2.execute(sqlCommand2)
        email = e1.get()
        password = encriptar_replace(e2.get())
        e=[]
        p=[]
        for i in cursor:
            e.append(i)
        for j in cursor2:
            p.append(j)
        res=list(map(itemgetter(0),e))
        res2=list(map(itemgetter(0),p))
        k = len(res)
        i=0
        while i<k:
            if res[i]==email and res2[i]==password:
                m.showinfo(title="Ingreso al sistema",message="Ha ingresado al sistema correctamente")
                #Vacío entrys luego de ingresar datos   
                e1.delete(0,"end")
                e2.delete(0,"end")
                ventanalogeado(email)#Envio nombre de usuario para obtener el id y que sea multiusuario
                break
            i+=1
        else:
            #Vacío entrys luego de ingresar datos   
            e1.delete(0,"end")
            e2.delete(0,"end")
            m.showinfo(title="error",message="Error al iniciar sesión")
        
     
    #Método que agrega el nuevo usuario en la base       
    def insertar_usuario():
        
        if e1.get() == "":
            m.showinfo(title="Error al crear cuenta",message="Ingrese datos !!!!!!!")
        else:
            v1=str(e1.get())
            v2=str(encriptar_replace(e2.get()))
            #v3=hash_password(v2)
            cursor.execute(
                    "insert into users (username,password_hash) VALUES (%s, %s)",
                    #(e1.get(),e2.get())
                    #(v1,v3) para encriptación
                    (v1,v2)
                )
            m.showinfo(title="Crear cuenta",message="Cuenta creada exitosamente")
            con.commit()
            #Vacío entrys luego de ingresar datos
            e1.delete(0,"end")
            e2.delete(0,"end")

    #Botón para iniciar sesión
    login = Button(loginWindow, text="Iniciar sesión", font=("Roboto", 11, "bold"),
                        fg= "#2D364C", bd=0, bg="#FFFFFF", cursor="hand2", border=2, width=24, command=check)
    login.place(x=150, y=450)
    
    #Botón para crear cuenta
    crearcuenta = Button(loginWindow, text="Crear cuenta", font=("Roboto", 11, "bold"),
                        fg= "#2D364C", bd=0, bg="#FFFFFF", cursor="hand2", border=2, width=24, command=insertar_usuario)
    crearcuenta.place(x=400, y=450)
    mainWindow.destroy() 
    loginWindow.mainloop()
      
#Método para cargar los combos de categorías
def cargarcombocategorias():
    con=conexion()
    con = psycopg2.connect(
                dbname="prypassword",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
        )
    cursor = con.cursor()

    cursor.execute("SELECT categoria_nombre FROM categorias")

    result=cursor.fetchall()
    val=[]
    for f in result:
        print(f[0])
        val.append(f[0])

    return val

#Método para obtener el id del usuario en base al nombre y con eso hacerle multiusuario
def obteneruserid(user):
    con=conexion()
    cursor = con.cursor()

    cursor.execute(
                "select user_id from users WHERE username = %s",([user])
        )
    result=cursor.fetchone()
    return result

#Encriptación de contraseñas
def encriptar_replace(texto):
    char_to_replace = {'a':'Q','b':'$','c':'6','d':'1','e':'=','f':'m','g':'R','h':'#','i':'(','j':'S','k':'n','l':'7','m':'&','n':'<','o':'¡','p':'+','q':'l','r':'8',
's':'-','t':'2','u':'!','v':'|','w':'k','x':',','y':'{','z':'_','A':'5','B':'.','C':'%','D':')','E':'x','F':'}','G':'y','H':'o','I':'[','J':'O',
'K':'?','L':'j','M':'¿','N':'w','O':'9','P':'p','Q':'3','R':'>','S':'0','T':'i','U':'4','V':']','W':'T','X':'q','Y':'~','Z':'z','1':'H','2':'v',
'3':'K','4':'g','5':'U','6':'G','7':'V','8':'P','9':'h','0':'L','!':'B','#':'f','$':'u','%':'W','&':'b','(':'E',')':'M','=':'r','?':'I','¡':'e',
'¿':'N','+':'t','{':'F','}':'c','[':'X',']':'C',',':'A','.':'s','-':'Y','_':'J','|':'a','~':'D','<':'Z','>':'d'}
 
    texto = texto.translate(str.maketrans(char_to_replace))    
    return texto

#Desencripta contraseñas
def desencriptar_replace(texto):
    char_to_replace = {'Q':'a','$':'b','6':'c','1':'d','=':'e','m':'f','R':'g','#':'h','(':'i','S':'j','n':'k','7':'l','&':'m','<':'n','¡':'o','+':'p','l':'q','8':'r',
'-':'s','2':'t','!':'u','|':'v','k':'w',',':'x','{':'y','_':'z','5':'A','.':'B','%':'C',')':'D','x':'E','}':'F','y':'G','o':'H','[':'I','O':'J',
'?':'K','j':'L','¿':'M','w':'N','9':'O','p':'P','3':'Q','>':'R','0':'S','i':'T','4':'U',']':'V','T':'W','q':'X','~':'Y','z':'Z','H':'1','v':'2',
'K':'3','g':'4','U':'5','G':'6','V':'7','P':'8','h':'9','L':'0','B':'!','f':'#','u':'$','W':'%','b':'&','E':'(','M':')','r':'=','I':'?','e':'¡',
'N':'¿','t':'+','F':'{','c':'}','X':'[','C':']','A':',','s':'.','Y':'-','J':'_','a':'|','D':'~','Z':'<','d':'>'}
    
    texto = texto.translate(str.maketrans(char_to_replace))    
    return texto

#Página logeado
def ventanalogeado(username):
    raiz = Tk()
    raiz.geometry("1500x600")
    raiz.title("Keyper")
    raiz.iconbitmap (r"C:\Users\nelso\Downloads\PF - Python\keyper_icon.ico")
    raiz.resizable(False, False)
    print(obteneruserid(username))
    print(username)

    #Página 1: Mis contraseñas
    def baul_page():
        baul_frame = Frame(main_frame)
        baul_frame.place(x=0, y=0)
        baul_frame.config(width=1000, height=600)

        lb_baul = Label(baul_frame, text="Mis contraseñas\n", font=("Roboto", 24, "bold"), fg="#2D364C").place(x=185, y=20)
        
        #Definición de variables para entrada de datos
        buscar_categ = StringVar()
        servicio_digital = StringVar()
        usuario = StringVar()

        #Campo buscar categoría
        buscar_categ_lbl = Label(baul_frame, text="Selecciona la categoría:").place(x=100, y=100)
        #Cargo el combo de categorías
        combo_nueva_categ = ttk.Combobox(baul_frame, state="readonly", values=cargarcombocategorias())
        combo_nueva_categ.config(width="37")
        combo_nueva_categ.current(0)#Muestro el primer valor del combo por defecto
        combo_nueva_categ.place(x=240, y=100)
        
        #Muestra la categoría seleccionada
        def show_selection_cat():         
            selection = combo_nueva_categ.get()
            val=str(selection)
            return val
        
        #Método que trae los datos de la categoría seleccionada y el usuario que se logeo
        def buscar_categoria():
            con=conexion()
            my_conn = con.cursor()
            input=show_selection_cat()
            my_conn.execute("select username,website_name,url,notas,encrypted_password,categoria_nombre,favorito from passwords p inner join categorias c on p.categoria_id=c.categoria_id inner join users u on p.user_id=u.user_id WHERE categoria_nombre = %s and username = %s",([input,username]))
            result=my_conn.fetchall()
            
            #Copiar al portapepeles
            def item_selected(event):
                item_id = tree_cat.identify("item", event.x, event.y)
                column_id = tree_cat.identify("column", event.x, event.y)
                data = tree_cat.set(item_id, column_id)
                pyperclip.copy(data)
                m.showinfo(title="Copiar", message=f"{data} copiado al portapapeles")
            
            #Presento el resultado de la consulta en el TreeView
            tree_cat = ttk.Treeview(baul_frame,columns=7, height=10)
            tree_cat.place(x=4, y=180)
        
            tree_cat['columns'] = ('username', 'website_name', 'url', 'notas','encrypted_password','categoria_nombre','favorito')
        
            tree_cat.column('#0', width=0, stretch=NO)
            tree_cat.column('username', width=60, anchor=CENTER)
            tree_cat.column('website_name', width=100, anchor=CENTER)
            tree_cat.column('url', anchor=CENTER, width=150)
            tree_cat.column('notas', width=100, anchor=CENTER)
            tree_cat.column('encrypted_password', width=100, anchor=CENTER)
            tree_cat.column('categoria_nombre', width=100, anchor=CENTER)  
            tree_cat.column('favorito', width=60, anchor=CENTER)        
        
            tree_cat.heading('username', text='Usuario')
            tree_cat.heading('website_name', text='Sitio web')
            tree_cat.heading('url', text='Url')
            tree_cat.heading('notas', text='Notas')
            tree_cat.heading('encrypted_password', text='Contraseña')
            tree_cat.heading('categoria_nombre', text='Categoría')
            tree_cat.heading('favorito', text='Favorito')
            tree_cat.bind("<1>", item_selected)

            #Ingreso los datos en el TreeView
            for user in result:
                tree_cat.insert(parent="", index="end", values=(user[0], user[1], user[2], user[3],desencriptar_replace(user[4]), user[5], user[6]))#desencripta(user[4])
               
        #Botón que obtiene los datos de la categoría seleccionada
        consultar_btn = Button(baul_frame, text="Obtener contraseñas", font=("Roboto", 11, "bold"),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2", border=2, width=24, command=buscar_categoria)
        consultar_btn.place(x=190, y=130)
        
        baul_frame.place(pady=20)

    #Página 2: Categorías
    def categ_page():

        categ_frame = Frame(main_frame)
        categ_frame.place(x=0, y=0)
        categ_frame.config(width=610, height=600)

        lb_categ = Label(categ_frame, text="Categorías\n", font=("Roboto", 24, "bold"), fg="#2D364C").place(x=215, y=20)

        con=conexion()
        my_conn = con.cursor()
        my_conn.execute("select categoria_nombre, categoria_descripcion  from categorias")#e3.get() input
        result=my_conn.fetchall()
        
        #Ingreso los datos de las categorías en el TreeView
        tree = ttk.Treeview(categ_frame,columns=6, height=10)
        tree.place(x=175, y=70)
        
        tree['columns'] = ('categoria_nombre', 'categoria_descripcion')
        
        tree.column('#0', width=0, stretch=NO)
        tree.column('categoria_nombre', width=100, anchor=CENTER)
        tree.column('categoria_descripcion', width=200, anchor=CENTER)
        
        tree.heading('categoria_nombre', text='Categoría')
        tree.heading('categoria_descripcion', text='Descripción de la categoría')
        for user in result:
            print(user)
            tree.insert(parent="", index="end", values=(user[0], user[1]))
                
        #Definición de variables para entrada de datos
        nombre_categ = StringVar()
        desc_categ = Text()

        #Sección agregar nueva categoría
        lb_agregar_categ = Label(categ_frame, text="Agregar nueva categoría\n", font=("Roboto", 16, "bold"), fg="#2D364C").place(x=180, y=300)

        #Agrega la nueva categoría
        def agg_categoria():
            
            my_conn2 = con.cursor()
            my_conn2.execute(
                "insert into categorias (categoria_nombre,categoria_descripcion) VALUES (%s, %s)",
                (nombre_categ_entry.get(),desc_categ_entry.get())
            )
            m.showinfo(title="Categoría",message="Categoría creada exitosamente")
            con.commit()
            #Vacío los entrys luego de ingresar la categoría
            nombre_categ_entry.delete(0,"end")
            desc_categ_entry.delete(0,"end")

        #Campo nombre categoría
        nombre_categ_lbl = Label(categ_frame, text="Nombre categoría:").place(x=130, y=350)
        nombre_categ_entry = Entry(categ_frame,textvariable = nombre_categ, width="40", highlightthickness=2)
        nombre_categ_entry.place(x=240, y=350)
        #Campo descripción categoría
        desc_categ_lbl = Label(categ_frame, text="Descripción:").place(x=130, y=400)
        desc_categ_entry = Entry(categ_frame,textvariable = desc_categ, width="40", highlightthickness=2)
        desc_categ_entry.place(x=240, y=400)

        #Botón agregar categoría
        add_categ_btn = Button(categ_frame, text="Agregar", font=("Roboto", 11, "bold"),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2", border=2, width=24,command=agg_categoria).place(x=190, y=450)

        categ_frame.place(pady=20)

    #Página 3: Ingresar nueva Contraseña
    def nueva_page():
    
        nueva_frame = Frame(main_frame)
        nueva_frame.place(x=0, y=0)
        nueva_frame.config(width=1000, height=600)

        lb_nueva = Label(nueva_frame, text="Nueva Contraseña\n", font=("Roboto", 24, "bold"), fg="#2D364C").place(x=185, y=20)

        #Definición de variables para entrada de datos
        nueva_website = StringVar()
        nueva_url = StringVar()
        nueva_nota = Text()
        nueva_contra = StringVar()
        nueva_categ = StringVar()

        #Campo Sitio web
        nueva_website_lbl = Label(nueva_frame, text="Sitio web:*").place(x=130, y=100)
        nueva_website_entry = Entry(nueva_frame,textvariable = nueva_website, width="40", highlightthickness=2)
        nueva_website_entry.place(x=240, y=100)
        
        #Campo URL
        nueva_url_lbl = Label(nueva_frame, text="URL:*").place(x=130, y=150)
        nueva_url_entry = Entry(nueva_frame,textvariable = nueva_url, width="40", highlightthickness=2)
        nueva_url_entry.place(x=240, y=150)
        
        #Campo Nota
        nueva_nota_lbl = Label(nueva_frame, text="Nota:").place(x=130, y=200)
        nueva_nota_entry = Entry(nueva_frame,textvariable = nueva_nota, width="40", highlightthickness=2)
        nueva_nota_entry.place(x=240, y=200)

        #Campo contraseña
        nueva_contra_lbl = Label(nueva_frame, text="Contraseña:*").place(x=130, y=250)
        nueva_contra_entry = Entry(nueva_frame,textvariable = nueva_contra, width="25", highlightthickness=2)
        nueva_contra_entry.place(x=240, y=250)
        
        #Selecciona el nivel de complejidad de la contraseña
        def nivelclave():
            nueva_contra_entry.delete(0,"end")#Vacío el Entry para que no se sobreescriba
            selection = combo_dificultad_clave.get()
            m.showinfo(message=f"Contraseña generada con nivel: {selection}",title="Selección")
            
            DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
            LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']
 
            UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                     'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                     'Z']
 
            SYMBOLS = ['!','#','$','%','&','(',')','=','?','¡','¿','+','{','}','[',']',',','.','-','_','|','~','<','>']
            #Primera selección aleatoria de las clases de caracteres
            rand_digit = random.choice(DIGITS)
            rand_upper = random.choice(UPCASE_CHARACTERS)
            rand_lower = random.choice(LOCASE_CHARACTERS)
            rand_symbol = random.choice(SYMBOLS)
            password = ""
            #Niveles de complejidad según el combobox
            if selection=='Bajo':
                temp_pass = rand_digit+rand_lower
                longitud=6
                clave_baja=rand_digit+rand_lower
                for x in range(longitud):#8 dígitos
                    temp_pass = temp_pass + random.choice(clave_baja)
                    temp_pass_list = array.array('u', temp_pass)
                    random.shuffle(temp_pass_list)
                                   
                for x in temp_pass_list:
                    password = password + x
                    
            elif selection=='Medio':
                temp_pass_media = rand_digit+rand_lower+rand_upper
                longitud_media=9
                clave_media=rand_digit+rand_lower+rand_upper
                for x in range(longitud_media):#12 dígitos
                    temp_pass_media = temp_pass_media + random.choice(clave_media)
                    temp_pass_list_media = array.array('u', temp_pass_media)
                    random.shuffle(temp_pass_list_media)
                    
                for x in temp_pass_list_media:
                    password = password + x
            else:
                temp_pass_alta = rand_digit+rand_lower+rand_upper+rand_symbol
                longitud_alta=11
                clave_alta=rand_digit+rand_lower+rand_upper+rand_symbol
                for x in range(longitud_alta):#15 dígitos
                    temp_pass_alta = temp_pass_alta + random.choice(clave_alta)
                    temp_pass_list_alta = array.array('u', temp_pass_alta)
                    random.shuffle(temp_pass_list_alta)
                    
                for x in temp_pass_list_alta:
                    password = password + x

            nueva_contra_entry.insert(0,password)
            return password
        
            
        #Generar contraseña según la dificultad
        generar_btn = Button(nueva_frame, text="Generar", font=("Roboto", 10, "bold"),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2", border=2, width=10,command=nivelclave)
        generar_btn.place(x=720, y=250)
        
        dificultad_clave_lbl = Label(nueva_frame, text="Nivel de complejidad: ")
        dificultad_clave_lbl.place(x=420, y=250)
        
        #Combo para niveles de complejidad
        combo_dificultad_clave = ttk.Combobox(nueva_frame, textvariable="comboclave", values=["Alto", "Medio", "Bajo"])
        combo_dificultad_clave.current(0)#Para mostrar valor por defecto combobox
        combo_dificultad_clave.place(x=550, y=250)

        #cargar combo Categoría
        nueva_categ_lbl = Label(nueva_frame, text="Categoría:").place(x=130, y=300)
        combo_nueva_categ = ttk.Combobox(nueva_frame,
            state="readonly",
            values=cargarcombocategorias())
        combo_nueva_categ.current(0)#Para mostrar valor por defecto combobox
        combo_nueva_categ.config(width="37")
        combo_nueva_categ.place(x=240, y=300)
        
        def show_selection():
            con=conexion()
            cursor = con.cursor()            
            selection = combo_nueva_categ.get()
            val=str(selection)
            m.showinfo(
            message=f"La categoría seleccionada es: {selection}",title="Selección")
            #Obtengo el id de la categoría según lo seleccionado para insertar en la tabla passwords
            cursor.execute("SELECT categoria_id FROM categorias WHERE categoria_nombre = %s",([val]))
            result=cursor.fetchone()
            result2=str(result)
            result3=result2.replace('(','')
            result4=result3.replace(',)','')
            print(result4)
            return result4
        
        con=conexion()
        cursor = con.cursor()
        #Insertar la nueva contraseña en la tabla passwords
        def agg_clave():
            userid=obteneruserid(username)
            fav=True;#Para que se ingrese la contraseña a 'Mis favoritos' por defecto
            cursor.execute(
                "insert into passwords (user_id,website_name,categoria_id,url,notas,encrypted_password,favorito) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (userid,nueva_website_entry.get(),int(show_selection()),nueva_url_entry.get(),nueva_nota_entry.get(),encriptar_replace(nueva_contra_entry.get()),fav)#encripta(nueva_contra_entry.get())
            )
            m.showinfo(title="Crear contraseña",message="Contraseña ingresada exitosamente")
            con.commit()
            #Vacío los entrys luego de ingresar la contraseña
            nueva_website_entry.delete(0,"end")
            nueva_url_entry.delete(0,"end")
            nueva_nota_entry.delete(0,"end")
            nueva_contra_entry.delete(0,"end")
            
            
        #Botón Guardar contraseña
        consultar_btn = Button(nueva_frame, text="Guardar", font=("Roboto", 11, "bold"),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2", border=2, width=24,command=agg_clave)
        consultar_btn.place(x=190, y=450)

        nueva_frame.place(pady=20)   

    #Página 4 Mis Favoritos. Por defecto todas las contraseñas se ingresan como Mis Favoritos y aquí se puede quitar
    def favoritos():
        frame_favoritos = Frame(main_frame)
        frame_favoritos.place(x=0, y=0)
        frame_favoritos.config(width=1000, height=600)
        
        lb_favoritos = Label(frame_favoritos, text="Mis favoritos\n", font=("Roboto", 24, "bold"), fg="#2D364C")
        lb_favoritos.place(x=185, y=20)
        
        con=conexion()
        my_conn = con.cursor()
        my_conn.execute("select username,website_name,url,notas,encrypted_password,categoria_nombre,favorito from passwords p inner join categorias c on p.categoria_id=c.categoria_id inner join users u on p.user_id=u.user_id WHERE username= %s and favorito=%s",([username,'True']))
        result=my_conn.fetchall()
        
        #Método para copiar al portapapeles lo que se seleccione del Tree View    
        def item_selected(event):
            item_id = tree_fav.identify("item", event.x, event.y)
            column_id = tree_fav.identify("column", event.x, event.y)
            data = tree_fav.set(item_id, column_id)
            pyperclip.copy(data)
            #spam = pyperclip.paste()
            m.showinfo(title="Copiar", message=f"{data} copiado al portapapeles")
        
        #TreeView para mostrar los datos de Mis Favoritos
        tree_fav = ttk.Treeview(frame_favoritos,columns=7, height=10)
        tree_fav.place(x=4, y=80)
        
        tree_fav['columns'] = ('username', 'website_name', 'url', 'notas','encrypted_password','categoria_nombre','favorito')
        
        tree_fav.column('#0', width=0, stretch=NO)
        tree_fav.column('username', width=60, anchor=CENTER)
        tree_fav.column('website_name', width=100, anchor=CENTER)
        tree_fav.column('url', anchor=CENTER, width=150)
        tree_fav.column('notas', width=100, anchor=CENTER)
        tree_fav.column('encrypted_password', width=100, anchor=CENTER)
        tree_fav.column('categoria_nombre', width=100, anchor=CENTER)  
        tree_fav.column('favorito', width=60, anchor=CENTER)        
        
        tree_fav.heading('username', text='Usuario')
        tree_fav.heading('website_name', text='Sitio web')
        tree_fav.heading('url', text='Url')
        tree_fav.heading('notas', text='Notas')
        tree_fav.heading('encrypted_password', text='Contraseña')
        tree_fav.heading('categoria_nombre', text='Categoría')
        tree_fav.heading('favorito', text='Favorito')
        #Copia al portapapeles lo seleccionado
        tree_fav.bind("<1>", item_selected)
        
        for user in result:
            tree_fav.insert(parent="", index="end", values=(user[0], user[1], user[2], user[3],desencriptar_replace(user[4]), user[5], user[6])) 
         
        #Método para eliminar una contraseña de mis favoritos   
        def eliminarfavorito():
            con=conexion()
            my_conn = con.cursor()
            my_conn.execute("UPDATE passwords SET favorito= %s WHERE website_name=%s and user_id=%s",(['False',nueva_nota_entry.get(),obteneruserid(username)]))
            m.showinfo(message=f"El sitio web: {nueva_nota_entry.get()} fue eliminado de mis favoritos correctamente.",title='Eliminar favorito')
            con.commit()  
            #Vacío el entry
            nueva_nota_entry.delete(0,"end")
                     
            
        lb_eliminar_favoritos = Label(frame_favoritos, text="¿Eliminar de mis favoritos?\n", font=("Roboto", 24, "bold"), fg="#2D364C")
        lb_eliminar_favoritos.place(x=185, y=350)    
        
        lb_website_eliminar_favoritos = Label(frame_favoritos, text="Sitio web a eliminar: \n", font=("Roboto",10, "bold"), fg="#2D364C")
        lb_website_eliminar_favoritos.place(x=20, y=400)  
        
        #Ingreso el sitio web que quiero quitar de mis favoritos
        nueva_nota_entry = Entry(frame_favoritos,textvariable = lb_website_eliminar_favoritos, width="40", highlightthickness=2)
        nueva_nota_entry.place(x=180, y=400)
        
        #Botón para eliminar de mis favoritos
        consultar_btn = Button(frame_favoritos, text="Eliminar", font=("Roboto", 11, "bold"),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2", border=2, width=15,command=eliminarfavorito)
        consultar_btn.place(x=450, y=400) 
       
    #Página para búsqueda por voz
    def busquedavoz():
        frame_busqueda = Frame(main_frame)
        frame_busqueda.place(x=0, y=0)
        frame_busqueda.config(width=1000, height=600)

        lb_nueva = Label(frame_busqueda, text="Búsqueda por voz del sitio web\n", font=("Roboto", 24, "bold"), fg="#2D364C").place(x=185, y=20) 
        
        #Captura el audio
        def capture_audio():
                recognizer = sr.Recognizer()
    
                with sr.Microphone() as source:
                    print("Habla algo...")
                    audio = recognizer.listen(source)
        
                try:
                    text = recognizer.recognize_google(audio, language="es-ES")
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, text)
                    result_text2.delete(0, END)
                    result_text2.insert(0, text)
                except sr.UnknownValueError:
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, "No se pudo entender el audio")
                except sr.RequestError as e:
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END, f"Error en la solicitud: {e}")
    
        # Etiqueta y botón
        label = tk.Label(frame_busqueda, text="Presiona el botón y habla:")
        label.place(x=185, y=70)
        #Botón para capturar la voz
        capture_button = tk.Button(frame_busqueda,text="Capturar Voz", command=capture_audio)
        capture_button.place(x=185, y=100) 
        
        result_text = tk.Text(frame_busqueda, height=5, width=40)
        result_text.place(x=185, y=150)

        #Muestra el resultado de lo que captura la voz
        result_text2 = Entry(frame_busqueda, bg="white", width=50, borderwidth=2)
        result_text2.place(x=185,y=250)
        
        buscar = Label(frame_busqueda, text="Sitio web a Buscar: ")
        buscar.place(x=80, y=250)
        
        #Obtiene los registros del sitio web que captura el audio
        def buscar():
            con=conexion()
            my_conn = con.cursor()
            input=result_text2.get()#'1.0', 'end'
            print(input)
            my_conn.execute("select username,website_name,url,notas,encrypted_password,categoria_nombre,favorito from passwords p inner join categorias c on p.categoria_id=c.categoria_id inner join users u on p.user_id=u.user_id WHERE website_name = %s and username= %s",([result_text2.get(),username]))#e3.get() input
            result=my_conn.fetchall()

            #Copiar al portapapeles
            def item_selected(event):
                item_id = tree.identify("item", event.x, event.y)
                column_id = tree.identify("column", event.x, event.y)
                data = tree.set(item_id, column_id)
                pyperclip.copy(data)
                m.showinfo(title="Copiar", message=f"{data} copiado al portapapeles")
            
            #Muestro los datos del sitio web que captura la voz
            tree = ttk.Treeview(frame_busqueda,columns=7, height=10)
            tree.place(x=4, y=350)
        
            tree['columns'] = ('username', 'website_name', 'url', 'notas','encrypted_password','categoria_nombre','favorito')
        
            tree.column('#0', width=0, stretch=NO)
            tree.column('username', width=60, anchor=CENTER)
            tree.column('website_name', width=100, anchor=CENTER)
            tree.column('url', anchor=CENTER, width=150)
            tree.column('notas', width=100, anchor=CENTER)
            tree.column('encrypted_password', width=100, anchor=CENTER)
            tree.column('categoria_nombre', width=100, anchor=CENTER)  
            tree.column('favorito', width=60, anchor=CENTER)        
        
            tree.heading('username', text='Usuario')
            tree.heading('website_name', text='Sitio web')
            tree.heading('url', text='Url')
            tree.heading('notas', text='Notas')
            tree.heading('encrypted_password', text='Contraseña')
            tree.heading('categoria_nombre', text='Categoría')
            tree.heading('favorito', text='Favorito')
            tree.bind("<1>", item_selected)

            for user in result:
                tree.insert(parent="", index="end", values=(user[0], user[1], user[2], user[3],desencriptar_replace(user[4]), user[5], user[6]))
        
        #Botón para buscar lo capturado por voz        
        buttonsearchdata = ttk.Button(frame_busqueda,text="Buscar", command=buscar)
        buttonsearchdata.place(x=200, y=300)
        
    #Función para visualizar el botón del menú lateral como inactivo
    def est_inactivo():
        baul_activo.config(bg="#2D364C")
        categ_activo.config(bg="#2D364C")
        nueva_activo.config(bg="#2D364C")

    #Función para limpiar páginas cuando selecciono una opción del menú lateral
    def limpiar_pag():
        for frame in main_frame.winfo_children():
            frame.destroy()

    
    #Función para visualizar el botón del menú lateral como activo
    def est_activo(lb, page):
        est_inactivo()
        lb.config(bg="#FF8519")
        limpiar_pag()
        page()

    lateral_frame = Frame(raiz, bg="#2D364C")

    #Se inserta el logo de Keyper en el menú lateral
    logo_keyper = PhotoImage(file=r"C:\Users\nelso\Downloads\PF - Python\logo_keyper_menu2.png")
    logo_menu_lat = Label(lateral_frame, image = logo_keyper)
    #logo_menu_lat.pack()
    logo_menu_lat.place(x=40, y=15)

    #Menú Lateral: Botón "Mis Contraseñas"
    baul_btn = Button(lateral_frame, text="Mis Contraseñas", font=("Roboto", 14),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2",
                            command = lambda: est_activo(baul_activo, baul_page))

    baul_btn.place(x=10, y=150)

        #Indicador botón activo
    baul_activo = Label(lateral_frame, text="", bg="#2D364C")
    baul_activo.place(x=3, y=150, width=5, height=40)

    #Menú Lateral: Botón "Categorías"
    categ_btn = Button(lateral_frame, text="Categorías", font=("Roboto", 14),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2",
                            command = lambda: est_activo(categ_activo, categ_page))

    categ_btn.place(x=10, y=200)

        #Indicador botón activo
    categ_activo = Label(lateral_frame, text="", bg="#2D364C")
    categ_activo.place(x=3, y=200, width=5, height=40)

    #Menú Lateral: Botón "Nueva Contraseña"
    nueva_btn = Button(lateral_frame, text="Nueva Contraseña", font=("Roboto", 14),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2",
                            command = lambda: est_activo(nueva_activo, nueva_page))

    nueva_btn.place(x=10, y=250)

        #Indicador botón activo
    nueva_activo = Label(lateral_frame, text="", bg="#2D364C")
    nueva_activo.place(x=3, y=250, width=5, height=40)
    
    #Menú Lateral: Botón "Busqueda por voz"
    bus_voz_btn = Button(lateral_frame, text="Búsqueda por voz", font=("Roboto", 14),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2",
                            command = lambda: est_activo(nueva_activo, busquedavoz))

    bus_voz_btn.place(x=10, y=300)

        #Indicador botón activo
    bus_voz_activo = Label(lateral_frame, text="", bg="#2D364C")
    bus_voz_activo.place(x=3, y=300, width=5, height=40)
    
    #Menú Lateral: Botón mis favoritos
    favoritos_btn = Button(lateral_frame, text="Mis favoritos", font=("Roboto", 14),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2",
                            command = lambda: est_activo(nueva_activo, favoritos))

    favoritos_btn.place(x=10, y=350)
    favoritos_activo = Label(lateral_frame, text="", bg="#2D364C")
    favoritos_activo.place(x=3, y=350, width=5, height=40)
    
    #Menú Lateral: Botón "Cerrar Sesión"
    salir_btn = Button(lateral_frame, text="Cerrar Sesión", font=("Roboto", 14),
                            fg= "#FFFFFF", bd=0, bg="#2D364C", cursor="hand2",command=raiz.destroy) 

    salir_btn.place(x=10, y=550)

    main_frame = Frame(raiz) #,highlightbackground="black",
                        #highlightthickness=2)

    #Frame del menú lateral

    lateral_frame.pack(side=LEFT)
    lateral_frame.pack_propagate(False)
    lateral_frame.configure(width=190, height=600)



    main_frame.pack(side=LEFT)
    main_frame.pack_propagate(False)
    main_frame.configure(width=1000, height=600)

    raiz.mainloop()
 
#Botón para ingresar al sistema   
goToLogin = Button(welcome_frame,text="Ingresar al sistema",fg= "#2D364C", bd=0, bg="#FFFFFF", cursor="hand2", border=2, width=24, font=("Roboto", 15, "bold"),command=Login)
goToLogin.place(x=300, y=450)

mainWindow.mainloop()