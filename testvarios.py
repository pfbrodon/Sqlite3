import re

cadena = "La temperatura es 55,400.00 grados Celsius"

# Buscar los dígitos en la cadena utilizando una expresión regular
digitos = re.findall(r'\d\.\d+|\d+', cadena)

# Convertir los dígitos en float
numeros_float = [float(d) for d in digitos]
print (digitos)
print(numeros_float)

for numeros in digitos:
    nuevaCadena= numeros
    print(nuevaCadena)