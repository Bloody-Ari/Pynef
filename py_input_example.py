from lib import pynef
import math

chamber_radius = (float(input("Ingrese el diametro de la camara: ")))/2
ac_at = float(input("Ingrese relacion Ac/At (default: 4.5): "))
ae_at = float(input("Ingrese relacion Ae/At: "))

file_name = input("Ingrese el nombre para el archivo (sin tipo): ")
file_type = input("Ingrese el tipo del archivo (sin puntos): ")

chamber_area = math.pi * (chamber_radius**2)
throat_area = chamber_area / ac_at
throat_radius = math.sqrt(throat_area / math.pi)

exit_area = throat_area * ae_at
exit_radius = math.sqrt(exit_area / math.pi)

chamber_cone_length = (chamber_radius - throat_radius)  / 0.26794919243 #tan(15°)
exit_cone_length = (exit_radius - throat_radius) / 0.26794919243

print(f"\nchamber_radius: {chamber_radius:8.5f}")
print(f"chamber_cone_length: {chamber_cone_length:8.5f}")
print(f"throat_radius: {throat_radius:8.5f}")
print(f"exit_radius: {exit_radius:8.5f}")
print(f"exit_cone_length {exit_cone_length:8.5f}\n")

pynef.openDefaultFile()
pynef.updateNozzle(chamber_radius, chamber_cone_length, throat_radius, exit_radius, exit_cone_length)
pynef.exportNozzle(file_name, file_type)
