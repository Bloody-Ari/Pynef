from lib import pynef

####################################################################
# Nota: al script no utilizar GUI los objetos en el archivo de CAD #
# se va a desactivar su visibilidad, solo basta con seleccionarlos #
# y presionar espacio o clickear el ojo a su izquierda en el arbol #
####################################################################

# Abre pynef/cad_files/defaultNozzle.FCStd
pynef.openDefaultFile()

# Modifica el sktech en el archivo, la logica es que al FreeCAD ser
# paramétrico, mientras que no se ponga ningún valor "extraño" todo va 
# a actualizarse chetuki. 
# Si el resultado esta mal hay que revisar esto.
#
# updateNozzle(
#   chamber_radius_mm
#   chamber_cone_length_mm
#   throat_radius_mm
#   exit_radius_mm
#   exit_cone_length_mm
# )
pynef.updateNozzle(6.375, 3.370, 3.005, 3.7505, 2.781)

# Exporta el archivo con el nombre del primer argumento, el tipo del
# segundo y, (opcional) el path del tercero.
# Si se deja el path vacio se manda el archivo a documentos.
# Para utilizar el directorio actual ingresar "."
# Los tipos que se verificaron son stl y 3mf, pero todo tipo
# soportado por FreeCAD para exportar un cuerpo debería ser válido.
#
# exportNozzle(
#   file_name
#   file_type
#   target_dir (default = user documents)
pynef.exportNozzle("NewNozzle", "stl", None)
