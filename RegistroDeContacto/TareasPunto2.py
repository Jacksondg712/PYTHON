import json
from datetime import datetime

class Tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        self.completada = False

    def marcar_completada(self):
        self.completada = True

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha_vencimiento": self.fecha_vencimiento.strftime("%Y-%m-%d"),
            "completada": self.completada
        }

    @staticmethod
    def from_dict(data):
        tarea = Tarea(data["titulo"], data["descripcion"], data["fecha_vencimiento"])
        tarea.completada = data["completada"]
        return tarea

class SistemaGestionTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, titulo, descripcion, fecha_vencimiento):
        self.tareas.append(Tarea(titulo, descripcion, fecha_vencimiento))

    def mostrar_tareas(self):
        tareas_ordenadas = sorted(self.tareas, key=lambda x: x.fecha_vencimiento)
        for idx, tarea in enumerate(tareas_ordenadas, start=1):
            estado = "Completada" if tarea.completada else "Pendiente"
            print(f"{idx}. {tarea.titulo} - {tarea.descripcion} - {tarea.fecha_vencimiento.strftime('%Y-%m-%d')} - {estado}")

    def marcar_tarea_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].marcar_completada()
        else:
            print("Índice fuera de rango.")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
        else:
            print("Índice fuera de rango.")

    def buscar_tareas(self, termino):
        resultados = [tarea for tarea in self.tareas if termino.lower() in tarea.titulo.lower() or termino.lower() in tarea.descripcion.lower()]
        for tarea in resultados:
            estado = "Completada" if tarea.completada else "Pendiente"
            print(f"{tarea.titulo} - {tarea.descripcion} - {tarea.fecha_vencimiento.strftime('%Y-%m-%d')} - {estado}")

    def guardar_tareas(self, archivo):
        with open(archivo, "w") as f:
            json.dump([tarea.to_dict() for tarea in self.tareas], f)

    def cargar_tareas(self, archivo):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                if not isinstance(datos, list):
                    raise ValueError("Formato de archivo incorrecto")
                self.tareas = [Tarea.from_dict(tarea) for tarea in datos]
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            print("No se pudo cargar el archivo de tareas. Iniciando con una lista vacía.")
            self.tareas = []

if __name__ == "__main__":
    sistema = SistemaGestionTareas()
    sistema.cargar_tareas("tareas.json")

    while True:
        print("\nSistema de Gestión de Tareas")
        print("1. Agregar tarea")
        print("2. Mostrar tareas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar tarea")
        print("5. Buscar tareas")
        print("6. Guardar y salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            descripcion = input("Descripción: ")
            fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
            sistema.agregar_tarea(titulo, descripcion, fecha_vencimiento)
        elif opcion == "2":
            sistema.mostrar_tareas()
        elif opcion == "3":
            indice = int(input("Índice de la tarea a completar: ")) - 1
            sistema.marcar_tarea_completada(indice)
        elif opcion == "4":
            indice = int(input("Índice de la tarea a eliminar: ")) - 1
            sistema.eliminar_tarea(indice)
        elif opcion == "5":
            termino = input("Buscar por título o descripción: ")
            sistema.buscar_tareas(termino)
        elif opcion == "6":
            sistema.guardar_tareas("tareas.json")
            print("Tareas guardadas. ¡Adiós!")
            break
        else:
            print("Opción no válida. Intenta de nuevo...")
