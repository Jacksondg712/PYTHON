import json
from datetime import datetime

class Tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento, completada=False):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        self.completada = completada

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_vencimiento": self.fecha_vencimiento.strftime("%Y-%m-%d"),
            "completada": self.completada,
        }

    @staticmethod
    def from_dict(data):
        return Tarea(
            data["titulo"],
            data["descripcion"],
            data["fecha_vencimiento"],
            data["completada"],
        )


class GestorTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, titulo, descripcion, fecha_vencimiento):
        tarea = Tarea(titulo, descripcion, fecha_vencimiento)
        self.tareas.append(tarea)
        print("Tarea agregada con éxito.")

    def mostrar_tareas(self):
        if not self.tareas:
            print("No hay tareas registradas.")
            return

        tareas_ordenadas = sorted(self.tareas, key=lambda tarea: tarea.fecha_vencimiento)
        for tarea in tareas_ordenadas:
            estado = "Completada" if tarea.completada else "Pendiente"
            print(f"Título: {tarea.titulo}")
            print(f"Descripción: {tarea.descripcion}")
            print(f"Fecha de vencimiento: {tarea.fecha_vencimiento.strftime('%Y-%m-%d')}")
            print(f"Estado: {estado}")
            print("-" * 20)

    def marcar_completada(self, titulo):
        for tarea in self.tareas:
            if tarea.titulo == titulo:
                tarea.completada = True
                print("Tarea marcada como completada.")
                return
        print("Tarea no encontrada.")

    def eliminar_tarea(self, titulo):
        for tarea in self.tareas:
            if tarea.titulo == titulo:
                self.tareas.remove(tarea)
                print("Tarea eliminada con éxito.")
                return
        print("Tarea no encontrada.")

    def buscar_tarea(self, termino):
        resultados = [
            tarea
            for tarea in self.tareas
            if termino.lower() in tarea.titulo.lower() or termino.lower() in tarea.descripcion.lower()
        ]
        if not resultados:
            print("No se encontraron tareas.")
        else:
            for tarea in resultados:
                estado = "Completada" if tarea.completada else "Pendiente"
                print(f"Título: {tarea.titulo}")
                print(f"Descripción: {tarea.descripcion}")
                print(f"Fecha de vencimiento: {tarea.fecha_vencimiento.strftime('%Y-%m-%d')}")
                print(f"Estado: {estado}")
                print("-" * 20)

    def guardar_tareas(self, archivo):
        with open(archivo, "w") as f:
            json.dump([tarea.to_dict() for tarea in self.tareas], f)
        print("Tareas guardadas con éxito.")

    def cargar_tareas(self, archivo):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                self.tareas = [Tarea.from_dict(dato) for dato in datos]
            print("Tareas cargadas con éxito.")
        except FileNotFoundError:
            print("Archivo no encontrado. No se cargaron tareas.")
        except json.JSONDecodeError:
            print("El archivo no tiene un formato válido.")


def mostrar_menu():
    print("\nMenú de Gestión de Tareas")
    print("1. Agregar tarea")
    print("2. Mostrar tareas")
    print("3. Marcar tarea como completada")
    print("4. Eliminar tarea")
    print("5. Buscar tareas")
    print("6. Guardar tareas")
    print("7. Cargar tareas")
    print("8. Salir")


if __name__ == "__main__":
    gestor = GestorTareas()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            descripcion = input("Descripción: ")
            fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
            try:
                datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
                gestor.agregar_tarea(titulo, descripcion, fecha_vencimiento)
            except ValueError:
                print("Fecha no válida. Usa el formato YYYY-MM-DD.")

        elif opcion == "2":
            gestor.mostrar_tareas()

        elif opcion == "3":
            titulo = input("Título de la tarea a completar: ")
            gestor.marcar_completada(titulo)

        elif opcion == "4":
            titulo = input("Título de la tarea a eliminar: ")
            gestor.eliminar_tarea(titulo)

        elif opcion == "5":
            termino = input("Ingrese un término para buscar: ")
            gestor.buscar_tarea(termino)

        elif opcion == "6":
            archivo = input("Nombre del archivo para guardar las tareas (e.g., tareas.json): ")
            gestor.guardar_tareas(archivo)

        elif opcion == "7":
            archivo = input("Nombre del archivo para cargar las tareas (e.g., tareas.json): ")
            gestor.cargar_tareas(archivo)

        elif opcion == "8":
            print("Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")
