import json
import time


def carga_espera(mensaje="Cargando", segundos=5, num_puntos=3): #ayuda de IA gemini para  creacion de esta funcion
    #Muestra un mensaje con puntos suspensivos animados en la consola
    for _ in range(segundos):
        for i in range(num_puntos + 1):
            puntos = "." * i
            espacios = " " * (num_puntos - i)
            print(f"\r{mensaje}{puntos}{espacios}", end="", flush=True)
            time.sleep(0.5)  # Pausa de medio segundo
    print()

def guardar_inscripcion(alumno, datos, arch):
    for linea in datos:
        if (linea.get("Nombre").lower() == alumno["Nombre"].lower() and
            linea.get("Apellido").lower() == alumno["Apellido"].lower() and
            linea.get("Nombre de Curso/Taller") == alumno["Nombre de Curso/Taller"]):
            print("Ese alumno ya está inscripto en ese curso.")
            return
        
    datos.append(alumno)
    with open(arch, "w", encoding="utf-8") as archivo: #guardado del alumno
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print("¡Ya estás inscripto!🤓")  

def obtenerInscriptosValidacion(curso, datos):
  cupos= 25
  inscriptos_curso= 0
  for d in datos:
      if d.get("Nombre de Curso/Taller") == curso: #busca cupos en los curso
         inscriptos_curso = inscriptos_curso + 1    
 
  if inscriptos_curso >= cupos:
    print(f"\n Lo sentimos, no quedan más lugares para el {curso} 🫤")
    inscriptos_curso -= 1
    return -1 #esto indica que el curso está lleno
  return inscriptos_curso
      
def ListaEspera(alumnoEspera, curso):
    arch = "espera.json"

    try:
        with open(arch, "r", encoding="utf-8") as archivo:
            espera = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        espera = []

    # Verificar duplicados en lista de espera
    for alumno in espera:

        if (alumno.get("Nombre").lower() == alumnoEspera["Nombre"].lower() and
            alumno.get("Apellido").lower() == alumnoEspera["Apellido"].lower() and
            alumno.get("Nombre de Curso/Taller") == curso):

            print("Ya estás anotado en la lista de espera.")
            return

    alumnosEnEspera = 0

    for e in espera:
        if e.get("Nombre de Curso/Taller") == curso:
            alumnosEnEspera += 1

    lugar_espera = alumnosEnEspera + 1

    datosAlumno = {
        "Nombre": alumnoEspera["Nombre"],
        "Apellido": alumnoEspera["Apellido"],
        "Nivel de Conocimiento": alumnoEspera["Nivel de Conocimiento"],
        "Nombre de Curso/Taller": curso,
        "Lugar": lugar_espera
    }

    espera.append(datosAlumno)

    with open(arch, "w", encoding="utf-8") as archivo:
        json.dump(espera, archivo, indent=4, ensure_ascii=False)

    print("¡Te añadimos a la lista de espera! Si hay alguna vacante te avisaremos 😄")

def validar_nombre_apellido(mensaje):
    while True:
        dato = input(mensaje).strip()

        if dato.replace(" ", "").isalpha():
            return dato

        print("Solo se permiten letras.")

def validar_conocimiento():
    while True:
        conocimiento = input(
            "Indique su conocimiento sobre la materia (Alto, Medio, Nulo): "
        ).capitalize()

        if conocimiento in ["Alto", "Medio", "Nulo"]:
            return conocimiento

        print(" Debe ingresar Alto, Medio o Nulo.")

def inscripcion(curso):
    arch= "inscriptos.json"
    try:
        with open(arch,"r", encoding="utf-8") as archivo: #apertura del archivo en esc/lec
            datos= json.load(archivo) #cargo datos
    except (FileNotFoundError, json.JSONDecodeError):
             datos=[] #empiezo una lista nueva 

    incriptosActu= obtenerInscriptosValidacion(curso, datos)
    
    if incriptosActu == -1: 
        inscribir= input("¿Querés inscribirte en la lista de espera? Ingresa 'si', si no quieres ingresa otro caracter")
        if inscribir != "si":
            print("Su inscripción ha sido cancelada ❌")
            return
        print("\n")
        print("Vamos a tomar sus datos para la lista de espera ✍️✍️")
        print("\n")
        print("Está inscribiendose al ", curso)
        nombre=  validar_nombre_apellido("Indique sus Nombres sin el apellido: ")
        apellido= validar_nombre_apellido("Indique su Apellido: ")
        conocimiento= validar_conocimiento()
        alumnoEspera= { #registro de esperas
            "Nombre": nombre, "Apellido": apellido, "Nivel de Conocimiento": conocimiento,
            "Nombre de Curso/Taller": curso
            }
        ListaEspera(alumnoEspera, curso)
    else:
      print("\n")
      print("Está inscribiendose al ", curso)
      nombre= validar_nombre_apellido("Indique sus Nombres sin el apellido: ")
      apellido= validar_nombre_apellido("Indique su Apellido: ")
      conocimiento= validar_conocimiento()
      lugar_curso= incriptosActu + 1
      
      alumno = {
          "Nombre": nombre, "Apellido": apellido, "Nivel de Conocimiento": conocimiento,
          "Nombre de Curso/Taller": curso, "Lugar": lugar_curso,
      } #este es el armado del registro de cada inscripto 
      guardar_inscripcion(alumno, datos, arch)

def estadisticas():
    try:
        with open("inscriptos.json","r",encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hay alumnos inscriptos.")
        return
    cursos = [
            "Curso de Inglés",
            "Curso de Portugués",
            "Curso de Informática",
            "Curso de Electricidad",
            "Taller de Pintura",
            "Taller de Escritura",
            "Taller de Lecto Comprensión"
            ]
    for curso in cursos:
            cont = 0
            for alumno in datos:
                if alumno.get("Nombre de Curso/Taller") == curso:
                    cont +=1
            print("Cantidad de inscriptos a", curso, "es: ", cont,"/25 alumnos")

def buscar_alumno():
    try:
        with open("inscriptos.json","r",encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hay alumnos inscriptos.")
        return
    nombre = validar_nombre_apellido("Ingrese el nombre del inscripto: ")
    apellido = validar_nombre_apellido("Ingrese el apellido del inscripto: ")
    for alumno in datos:
            if (alumno.get("Nombre").lower() == nombre.lower() and alumno.get("Apellido").lower() == apellido.lower()):
                print(nombre,apellido)
                print(alumno.get("Nombre de Curso/Taller"))
                return
    print("No existe alumno inscripto con ese nombre o apellido")   

def actualizar_lugares(datos, curso):
    lugar = 1
    for alumno in datos:
        if alumno.get("Nombre de Curso/Taller") == curso:
            alumno["Lugar"] = lugar
            lugar += 1

def dar_de_baja():
    try:
        with open("inscriptos.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hay alumnos inscriptos.")
        return

    nombre = validar_nombre_apellido(
        "Ingrese el nombre del inscripto: "
    )

    apellido = validar_nombre_apellido(
        "Ingrese el apellido del inscripto: "
    )

    for alumno in datos:

        if (alumno.get("Nombre").lower() == nombre.lower() and
            alumno.get("Apellido").lower() == apellido.lower()):

            curso = alumno.get("Nombre de Curso/Taller")

            datos.remove(alumno)

            actualizar_lugares(datos, curso)

            with open("inscriptos.json", "w", encoding="utf-8") as archivo:
                json.dump(
                    datos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            print("Alumno dado de baja correctamente.")

            promover_lista_espera(curso)

            return

    print("No existe un alumno con ese nombre y apellido.")

def mostrar_cupos():
    try:
        with open("inscriptos.json","r",encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except:
        datos = []

    cursos = [
        "Curso de Inglés",
        "Curso de Portugués",
        "Curso de Informática",
        "Curso de Electricidad",
        "Taller de Pintura",
        "Taller de Escritura",
        "Taller de Lecto Comprensión"
    ]

    print("\nCUPOS DISPONIBLES")

    for curso in cursos:
        inscriptos = 0

        for alumno in datos:
            if alumno["Nombre de Curso/Taller"] == curso:
                inscriptos += 1

        disponibles = 25 - inscriptos

        print(curso, ":", disponibles, "lugares")

def mostrar_lista_espera():
    try:
        with open("espera.json","r",encoding="utf-8") as archivo:
            espera = json.load(archivo)
    except:
        print("No hay lista de espera.")
        return

    for alumno in espera:
        print(
            alumno["Nombre"],
            alumno["Apellido"],
            "-",
            alumno["Nombre de Curso/Taller"],
            "- Lugar:",
            alumno["Lugar"]
        )
def curso_mas_demandado():
    try:
        with open("inscriptos.json","r",encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except:
        print("No hay datos.")
        return

    contador = {}

    for alumno in datos:
        curso = alumno["Nombre de Curso/Taller"]

        if curso not in contador:
            contador[curso] = 0

        contador[curso] += 1

    if not contador:
        print("No hay alumnos inscriptos.")
        return

    mayor = max(contador, key=contador.get)

    print("Curso más demandado:")
    print(mayor, "-", contador[mayor], "inscriptos")

def estadisticas_conocimiento():
    try:
        with open("inscriptos.json","r",encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hay alumnos inscriptos.")
        return

    cursos = [
        "Curso de Inglés",
        "Curso de Portugués",
        "Curso de Informática",
        "Curso de Electricidad",
        "Taller de Pintura",
        "Taller de Escritura",
        "Taller de Lecto Comprensión"
    ]

    for curso in cursos:

        alto = 0
        medio = 0
        nulo = 0

        for alumno in datos:

            if alumno["Nombre de Curso/Taller"] == curso:

                if alumno["Nivel de Conocimiento"] == "Alto":
                    alto += 1

                elif alumno["Nivel de Conocimiento"] == "Medio":
                    medio += 1

                elif alumno["Nivel de Conocimiento"] == "Nulo":
                    nulo += 1

        print("\n", curso)
        print("Alto:", alto)
        print("Medio:", medio)
        print("Nulo:", nulo)
  
def promover_lista_espera(curso):
    try:
        with open("espera.json", "r", encoding="utf-8") as archivo:
            espera = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return

    try:
        with open("inscriptos.json", "r", encoding="utf-8") as archivo:
            inscriptos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        inscriptos = []

    alumno_promovido = None

    for alumno in espera:
        if alumno.get("Nombre de Curso/Taller") == curso and alumno.get("Lugar") == 1:
            alumno_promovido = alumno
            break

    if alumno_promovido is None:
        return

    espera.remove(alumno_promovido)

    lugar = 1
    for alumno in inscriptos:
        if alumno.get("Nombre de Curso/Taller") == curso:
            lugar += 1

    nuevo_alumno = {
        "Nombre": alumno_promovido["Nombre"],
        "Apellido": alumno_promovido["Apellido"],
        "Nivel de Conocimiento": alumno_promovido["Nivel de Conocimiento"],
        "Nombre de Curso/Taller": curso,
        "Lugar": lugar
    }

    inscriptos.append(nuevo_alumno)

    posicion = 1
    for alumno in espera:
        if alumno.get("Nombre de Curso/Taller") == curso:
            alumno["Lugar"] = posicion
            posicion += 1

    with open("inscriptos.json", "w", encoding="utf-8") as archivo:
        json.dump(inscriptos, archivo, indent=4, ensure_ascii=False)

    with open("espera.json", "w", encoding="utf-8") as archivo:
        json.dump(espera, archivo, indent=4, ensure_ascii=False)

    print(
        f"Se liberó una vacante en {curso}. "
        f"{nuevo_alumno['Nombre']} {nuevo_alumno['Apellido']} "
        f"ha sido promovido desde la lista de espera."
    )        

def salir():
    print("Gracias por utilizar nuestro sistema, vuelva pronto 😄")
    exit()
        
menu = {
    "1": lambda: inscripcion("Curso de Inglés"),
    "2": lambda: inscripcion("Curso de Portugués"),
    "3": lambda: inscripcion("Curso de Informática"),
    "4": lambda: inscripcion("Curso de Electricidad"),
    "5": lambda: inscripcion("Taller de Pintura"),
    "6": lambda: inscripcion("Taller de Escritura"),
    "7": lambda: inscripcion("Taller de Lecto Comprensión"),
    "8": estadisticas,
    "9": buscar_alumno,
    "10": dar_de_baja,
    "11": mostrar_cupos,
    "12": mostrar_lista_espera,
    "13": curso_mas_demandado,
    "14": estadisticas_conocimiento,
    "15": salir
    }

while True:
 print("Elija el curso o Taller al que se quiere inscribir ")
 print("Cursos Disponibles:")
 print("""
 1- Curso de Inglés 🇺🇲
 2- Curso de Portugués 🇧🇷
 3- Curso de Informatica 💻
 4- Curso de Electricidad 🔌
 """)
 print("Talleres Disponibles:")
 print("""
 5- Taller de Pintura 🎨
 6- Taller de Escritura ✒️ 
 7- Taller de Comprensión Lectora 📖
 """)
 print("""
 8- Estadisticas de inscriptos a cada curso
 9- Buscar alumno inscripto
 10- Dar de baja alumno inscripto
 11- Mostrar cupos disponibles
 12- Mostrar lista de espera
 13- Mostrar curso más demandado
 14- Estadisticas de conocimiento de los alumnos
 15- Salir del programa
 """) 
 opcion =input("Introduzca su opción: ")
 accion = menu.get(opcion)
 
 
 if accion:
    accion()
    print("\n")
    carga_espera("Volviendo a Menu principal", 2)
 else:
   print("Esa opcion no es valida 🫤. Intente nuevamente")  
   print("\n")
   carga_espera("Volviendo a Menu principal", 2)
   print("\n")
