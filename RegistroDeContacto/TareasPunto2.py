# import csv

# def menu():
#     print("\nGestor de Contactos")
#     print("1. Agregar un contacto")
#     print("2. Mostrar contactos")
#     print("3. Buscar un contacto")
#     print("4. Eliminar un contacto")
#     print("5. Guardar contactos en archivo CSV")
#     print("6. Cargar contactos desde archivo CSV")
#     print("7. Salir")
#     return input("Seleccione una opción: ")

# def validar_datos(contactos, nombre, telefono, correo):
#     for contacto in contactos:
#         if contacto["Nombre"].lower() == nombre.lower():
#             print("Error: El nombre ya está en la lista de contactos.")
#             return False
#         if contacto["Teléfono"] == telefono:
#             print("Error: El teléfono ya está en la lista de contactos.")
#             return False
#         if contacto["Correo"].lower() == correo.lower():
#             print("Error: El correo ya está en la lista de contactos.")
#             return False
#     return True

# def agregar_contacto(contactos):
#     nombre = input("Nombre: ")
#     telefono = input("Teléfono: ")
#     correo = input("Correo electrónico: ")

#     if validar_datos(contactos, nombre, telefono, correo):
#         contactos.append({"Nombre": nombre, "Teléfono": telefono, "Correo": correo})
#         print("Contacto agregado con éxito.")

# def mostrar_contactos(contactos):
#     if not contactos:
#         print("No hay contactos para mostrar.")
#         return
#     print("\nLista de contactos:")
#     print("{:<20} {:<15} {:<25}".format("Nombre", "Teléfono", "Correo"))
#     print("-" * 60)
#     for contacto in contactos:
#         print("{:<20} {:<15} {:<25}".format(contacto["Nombre"], contacto["Teléfono"], contacto["Correo"]))

# def buscar_contacto(contactos):
#     criterio = input("Buscar por (nombre/teléfono/correo): ").lower()
#     valor = input("Ingrese el valor a buscar: ")
#     resultados = [c for c in contactos if c[criterio.capitalize()] == valor]
#     if resultados:
#         print("\nContactos encontrados:")
#         print("{:<20} {:<15} {:<25}".format("Nombre", "Teléfono", "Correo"))
#         print("-" * 60)
#         for contacto in resultados:
#             print("{:<20} {:<15} {:<25}".format(contacto["Nombre"], contacto["Teléfono"], contacto["Correo"]))
#     else:
#         print("No se encontraron contactos que coincidan con el criterio.")

# def eliminar_contacto(contactos):
#     criterio = input("Eliminar por (nombre/teléfono/correo): ").lower()
#     valor = input("Ingrese el valor a buscar: ")
#     for contacto in contactos:
#         if contacto[criterio.capitalize()] == valor:
#             contactos.remove(contacto)
#             print("Contacto eliminado con éxito.")
#             return
#     print("No se encontró un contacto que coincida con el criterio.")

# def guardar_en_csv(contactos, archivo):
#     with open(archivo, mode="w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=["Nombre", "Teléfono", "Correo"])
#         writer.writeheader()
#         writer.writerows(contactos)
#     print(f"Contactos guardados en {archivo}.")

# def cargar_desde_csv(contactos, archivo):
#     try:
#         with open(archivo, mode="r", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             contactos.clear()
#             contactos.extend(reader)
#         print(f"Contactos cargados desde {archivo}.")
#     except FileNotFoundError:
#         print(f"El archivo {archivo} no existe.")

# def main():
#     contactos = []
#     archivo_csv = "contactos.csv"

#     while True:
#         opcion = menu()

#         if opcion == "1":
#             agregar_contacto(contactos)
#         elif opcion == "2":
#             mostrar_contactos(contactos)
#         elif opcion == "3":
#             buscar_contacto(contactos)
#         elif opcion == "4":
#             eliminar_contacto(contactos)
#         elif opcion == "5":
#             guardar_en_csv(contactos, archivo_csv)
#         elif opcion == "6":
#             cargar_desde_csv(contactos, archivo_csv)
#         elif opcion == "7":
#             print("Saliendo del programa. ¡Hasta luego!")
#             break
#         else:
#             print("Opción no válida, intente de nuevo.")

# if __name__ == "__main__":
#     main()