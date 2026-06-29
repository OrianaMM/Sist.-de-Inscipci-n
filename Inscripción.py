import json
import time


def carga_espera(mensaje="Cargando", segundos=3, num_puntos=3): #ayuda de IA gemini para  creacion de esta funcion
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
    arch= "espera.json"
    try:
        with open(arch,"r", encoding="utf-8") as archivo:
           espera= json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
           espera= []
    
    alumnosEnEspera= 0
    for e in espera:
        if e.get("Nombre de Curso/Taller") == curso:
           alumnosEnEspera += 1
    lugar_espera= alumnosEnEspera + 1 
    datosAlumno= { #asignacion de campos al registro del archivo
        "Nombre": alumnoEspera["Nombre"], "Apellido": alumnoEspera["Apellido"], "Nivel de Conocimiento": alumnoEspera["Nivel de Conocimiento"],
        "Nombre de Curso/Taller": curso, "Lugar": lugar_espera
    }
    espera.append(datosAlumno)

    with open(arch, "w", encoding="utf-8") as archivo:
        json.dump(espera, archivo, indent=4, ensure_ascii=False)
        print("¡Te añadimos a la lista de espera! Si hay alguna vacante te avisaremos 😄")

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
        nombre= str(input("Indique sus Nombres sin el apellido: "))
        apellido= str(input("Indique su Apellido: "))
        conocimiento= str(input("Indique su conocimiento sobre la materia (Alto, Medio Nulo): "))  
        alumnoEspera= { #registro de esperas
            "Nombre": nombre, "Apellido": apellido, "Nivel de Conocimiento": conocimiento,
            "Nombre de Curso/Taller": curso
            }
        ListaEspera(alumnoEspera, curso)
    else:
      print("\n")
      print("Está inscribiendose al ", curso)
      nombre= str(input("Indique sus Nombres sin el apellido: "))
      apellido= str(input("Indique su Apellido: "))
      conocimiento= str(input("Indique su conocimiento sobre la materia (Alto, Medio Nulo): "))
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
    nombre = str(input("Ingrese el nombre del inscripto: "))
    apellido = str(input("Ingrese el apellido del inscripto: "))
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
    nombre = str(input("Ingrese el nombre del inscripto: "))
    apellido = str(input("Ingrese el apellido del inscripto: "))
    for alumno in datos:
        if alumno.get("Nombre").lower() == nombre.lower() and alumno.get("Apellido").lower() == apellido.lower():
            curso = alumno.get("Nombre de Curso/Taller")
            datos.remove(alumno)
            actualizar_lugares(datos,curso)
            with open("inscriptos.json", "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            print("Alumno dado de baja correctamente.")
            return
    print("No existe un alumno con ese nombre y apellido.")
        
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
    "10": dar_de_baja
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
