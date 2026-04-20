import json

archivo = "tareas.json"

def cargar_tareas():
    try:
        with open(archivo, "r") as f:
            return json.load(f)
    except:
        return []

def guardar_tareas(tareas):
    with open(archivo, "w") as f:
        json.dump(tareas, f)

tareas = cargar_tareas()

def agregar_tarea():
    tarea = input("Nueva tarea: ").strip()
    if tarea and tarea not in tareas:
        tareas.append(tarea)
        guardar_tareas(tareas)
        print("Tarea agregada.")
    else:
        print("Tarea inválida o ya existe.")

def mostrar_tareas():
    if len(tareas) == 0:
        print("No hay tareas.")
    else:
        print("\nLista de tareas:")
        for i, t in enumerate(tareas, 1):
            print(f"{i}. {t}")

def eliminar_tarea():
    mostrar_tareas()
    try:
        num = int(input("Número de tarea a eliminar: "))
        if 1 <= num <= len(tareas):
            tarea = tareas.pop(num - 1)
            guardar_tareas(tareas)
            print(f"Eliminada: {tarea}")
        else:
            print("Número inválido.")
    except:
        print("Entrada inválida.")

# LOOP PRINCIPAL
while True:
    print("\n--- MENÚ ---")
    print("1. Ver tareas")
    print("2. Agregar tarea")
    print("3. Eliminar tarea")
    print("4. Salir")

    opcion = input("Elegí una opción: ")

    if opcion == "1":
        mostrar_tareas()
    elif opcion == "2":
        agregar_tarea()
    elif opcion == "3":
        eliminar_tarea()
    elif opcion == "4":
        print("Chau 👋")
        break
    else:
        print("Opción inválida.")