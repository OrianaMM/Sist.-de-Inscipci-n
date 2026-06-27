import json

def guardar_inscripcion(alumno, datos, arch):
 datos.append(alumno)
 with open(arch, "w", encoding="utf-8") as archivo: #guardado del alumno
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
 print("¡Ya estás inscripto!")  

def obtenerInscriptosValidacion(curso, datos):
  cupos= 25
  inscriptos_curso= 0
  for d in datos:
      if d.get("Nombre de Curso/Taller") == curso: #busca cupos en los curso
         inscriptos_curso = inscriptos_curso + 1    
 
  if inscriptos_curso >= cupos:
    print(f"\n Lo sentimos, no quedan más lugares para el {curso}")
    inscriptos_curso -= 1
    return -1 #esto indica que el curso está lleno
  return inscriptos_curso
      

def inscripcion(curso):
    arch= "inscriptos.json"
    try:
        with open(arch,"r", encoding="utf-8") as archivo: #apertura del archivo en esc/lec
            datos= json.load(archivo) #cargo datos
    except (FileNotFoundError, json.JSONDecodeError):
             datos=[] #empiezo una lista nueva 

    incriptosActu= obtenerInscriptosValidacion(curso, datos)
    if incriptosActu == -1: #indica que esta lleno y detiene la fn
     return 
    
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

print("Elija el curso o Taller al que se quiere inscribir")
print("Cursos Disponibles:")
print("""
1- Curso de Inglés
2- Curso de Portugués
3- Curso de Informatica
4- Curso de Electricidad
""")
print("Talleres Disponibles:")
print("""
5- Taller de Pintura
6- Taller de Escritura 
7- Taller de Comprensión Lectora
""") 

opcion =input("Introduzca su opción: ")
accion = menu.get(opcion)
if accion:
   accion()
else:
    print("Esa opcion no es valida. Intente nuevamente")  
   


