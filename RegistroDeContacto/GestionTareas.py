import csv
import os
from datetime import datetime

class Tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        self.completada = False

    def marcar_completada(self):
        self.completada = True

    def to_list(self):
        return [
            self.titulo,
            self.descripcion,
            self.fecha_vencimiento.strftime("%Y-%m-%d"),
            self.completada
        ]

    @staticmethod
    def from_list(data):
        tarea = Tarea(data[0], data[1], data[2])
        tarea.completada = data[3] == 'True'
        return tarea
    
class SistemaGestionTareas:
    def __init__(self):
        self.tareas = []
        self.archivo = os.path.join(os.path.dirname(__file__), "tareas.csv")

    def agregar_tarea(self, titulo, descripcion, fecha_vencimiento):
        self.tareas.append(Tarea(titulo, descripcion, fecha_vencimiento))

    def mostrar_tareas(self):
        if not self.tareas:
            print("No hay tareas registradas.")
            return
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
        if not resultados:
            print("No se encontraron tareas que coincidan con el término.")
            return
        for tarea in resultados:
            estado = "Completada" if tarea.completada else "Pendiente"
            print(f"{tarea.titulo} - {tarea.descripcion} - {tarea.fecha_vencimiento.strftime('%Y-%m-%d')} - {estado}")

    def guardar_tareas(self):
        with open(self.archivo, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Titulo", "Descripcion", "FechaVencimiento", "Completada"])
            for tarea in self.tareas:
                writer.writerow(tarea.to_list())
        print("Tareas guardadas exitosamente en el archivo.")

    def cargar_tareas(self):
        try:
            with open(self.archivo, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  
                self.tareas = [Tarea.from_list(row) for row in reader]
                print("Tareas cargadas exitosamente.")
        except FileNotFoundError:
            print("No se encontró el archivo de tareas. Iniciando con una lista vacía.")
            self.tareas = []
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            self.tareas = []

if __name__ == "__main__":
    sistema = SistemaGestionTareas()
    sistema.cargar_tareas()

    
    if sistema.tareas:
        print("\nTareas cargadas desde el archivo:")
        sistema.mostrar_tareas()
    else:
        print("\nNo hay tareas registradas en el archivo inicial.")

    while True:
        print("\nSistema de Gestión de Tareas")
        print("1. Agregar una tarea")
        print("2. Mostrar tareas agregadas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar una tarea")
        print("5. Buscar una tarea")
        print("6. Guardar tareas en formato csv")
        print("7. Salir del programa")
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
            sistema.guardar_tareas()
        elif opcion == "7":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo...")
