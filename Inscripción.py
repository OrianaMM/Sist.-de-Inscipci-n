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
   


def guardar_inscripcion(alumno, datos, arch):
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



menu = {
    "1": lambda: inscripcion("Curso de Inglés"),
    "2": lambda: inscripcion("Curso de Portugués"),
    "3": lambda: inscripcion("Curso de Informática"),
    "4": lambda: inscripcion("Curso de Electricidad"),
    "5": lambda: inscripcion("Taller de Pintura"),
    "6": lambda: inscripcion("Taller de Escritura"),
    "7": lambda: inscripcion("Taller de Lecto Comprensión"),
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

