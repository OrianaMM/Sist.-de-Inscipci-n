def inscripcion():
    nombre= str(input("Indique sus Nombres sin el apellido: "))
    apellido= str(input("Indique su Apellido: "))
    conocimiento= str(input("Indique su conocimiento sobre la materia (Alto, Medio Nulo): "))

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
opcion= int(input("Introduzca su opción: "))
if opcion == 1:
    print("Elijio el Curso de Inglés, por favor rellene sus datos")
    inscripcion()
elif opcion ==2:
    print("Elijio el Curso de Portugués, por favor rellene sus datos")
    inscripcion()