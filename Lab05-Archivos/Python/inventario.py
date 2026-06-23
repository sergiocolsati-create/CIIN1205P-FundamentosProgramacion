	# ============================================================
# LABORATORIO N° 5 - FUNDAMENTOS DE PROGRAMACIÓN
# Tema: Persistencia de Datos con Archivos de Texto y Binarios
# Ejemplo: Sistema de Gestión de Inventario
# Lenguaje: Python
# Alumno: Sergio Colan Sanchez
# Fecha: Junio 2026
# ============================================================

# "import" en Python es igual que "using" en C#
# Importamos las librerías que necesitamos

import os       # Para verificar si archivos/carpetas existen
                # Equivalente a: File.Exists() y Directory.Exists() en C#

import pickle   # Para serialización BINARIA de objetos Python
                # Equivalente a: BinaryFormatter en C#
                # pickle convierte objetos Python → bytes → archivo .bin
                # y también bytes → objetos Python (deserializar)


# ══════════════════════════════════════════════════════════════
# RUTAS DE ARCHIVOS
# ══════════════════════════════════════════════════════════════
# __file__ = ruta completa de este script (inventario.py)
# os.path.dirname() = extrae solo la carpeta donde está el script
# os.path.join() = une rutas de forma segura (como Path.Combine en C#)
# ".." = sube una carpeta

# Ruta base: sube desde Python\ hasta Lab05-Archivos\
BASE = os.path.dirname(os.path.abspath(__file__))  
DATOS = os.path.join(BASE, "..", "Datos")          # Lab05-Archivos\Datos\

RUTA_TXT = os.path.join(DATOS, "inventario.txt")  # archivo de texto
RUTA_BIN = os.path.join(DATOS, "inventario.bin")  # archivo binario


# ══════════════════════════════════════════════════════════════
# ¿QUÉ ES UNA CLASE EN PYTHON?
# ══════════════════════════════════════════════════════════════
# En C# teníamos:
#   class Producto { public int Id { get; set; } ... }
#
# En Python es más simple, no necesita [Serializable]
# porque pickle puede serializar CUALQUIER objeto Python
# automáticamente sin necesidad de marcarlo
# ══════════════════════════════════════════════════════════════

class Producto:
    """
    Representa un producto del inventario.
    Equivalente a la clase Producto en C# pero sin [Serializable]
    porque pickle lo maneja automáticamente.
    """

    # __init__ = constructor (se ejecuta al crear un objeto)
    # Equivalente a: public Producto(int id, string nombre...) en C#
    # "self" = referencia al objeto mismo (como "this" en C#)
    def __init__(self, id, nombre, categoria, stock, precio):
        self.id        = id        # Número único del producto
        self.nombre    = nombre    # Nombre del producto
        self.categoria = categoria # Categoría (Electrónica, Ropa, etc.)
        self.stock     = stock     # Cantidad disponible
        self.precio    = precio    # Precio en soles

    # __str__ = método especial que define cómo se ve el objeto como texto
    # Equivalente a: override string ToString() en C#
    # Se llama automáticamente cuando hacemos print(producto) o str(producto)
    def __str__(self):
        # f"..." = f-string, como $"..." en C#
        # :.2f = formato con 2 decimales (como :F2 en C#)
        return f"{self.id},{self.nombre},{self.categoria},{self.stock},{self.precio:.2f}"


# ══════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL - MENÚ
# En Python no hay Main() obligatorio, pero usamos
# el patrón: if __name__ == "__main__" que significa
# "ejecutar esto solo si corres este archivo directamente"
# ══════════════════════════════════════════════════════════════

def mostrar_menu():
    """Limpia la pantalla y muestra el menú principal."""
    os.system('cls' if os.name == 'nt' else 'clear')  # cls en Windows, clear en Mac/Linux
    print("╔══════════════════════════════════════════╗")
    print("║    LAB 05 - SISTEMA DE INVENTARIO        ║")
    print("║    Python - Archivos .txt y .bin         ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Agregar producto     → escribe .txt  ║")
    print("║  2. Ver inventario       → lee .txt      ║")
    print("║  3. Buscar producto      → procesa .txt  ║")
    print("║  4. Resumen de stock     → procesa .txt  ║")
    print("║  5. Guardar en binario   → crea .bin     ║")
    print("║  6. Leer desde binario   → lee .bin      ║")
    print("║  7. Salir                                ║")
    print("╚══════════════════════════════════════════╝")


# ══════════════════════════════════════════════════════════════
# HELPER - ASEGURAR QUE LA CARPETA DATOS/ EXISTE
# Equivalente a AsegurarDirectorio() en C#
# ══════════════════════════════════════════════════════════════

def asegurar_directorio():
    """Crea la carpeta Datos/ si no existe."""
    # os.makedirs() = crea la carpeta y subcarpetas si no existen
    # exist_ok=True = no lanza error si ya existe
    # Equivalente a: Directory.CreateDirectory() en C#
    os.makedirs(DATOS, exist_ok=True)


# ══════════════════════════════════════════════════════════════
# HELPER - OBTENER SIGUIENTE ID
# Cuenta las líneas del .txt para asignar el próximo ID
# ══════════════════════════════════════════════════════════════

def obtener_siguiente_id():
    """Cuenta líneas del .txt y devuelve el siguiente ID disponible."""
    if not os.path.exists(RUTA_TXT):  # Si no existe el archivo
        return 1                       # Empieza en 1
    
    # open() abre un archivo - equivalente a StreamReader/StreamWriter en C#
    # 'r'  = modo lectura (read)   → como StreamReader en C#
    # 'w'  = modo escritura        → como StreamWriter(append:false) en C#
    # 'a'  = modo añadir (append)  → como StreamWriter(append:true) en C#
    # 'rb' = lectura binaria       → como FileStream en C#
    # 'wb' = escritura binaria     → como FileStream en C#
    #
    # encoding='latin-1' = para soportar tildes y caracteres especiales
    with open(RUTA_TXT, 'r', encoding='latin-1') as archivo:
        # readlines() lee TODAS las líneas de una vez como lista
        # len() cuenta cuántos elementos tiene la lista
        lineas = archivo.readlines()
    
    return len(lineas) + 1  # Siguiente ID = total de líneas + 1


# ══════════════════════════════════════════════════════════════
# OPCIÓN 1 - AGREGAR PRODUCTO
# Pasos 3, 4 y 6 de la guía:
#   Paso 3: ingresar datos por teclado
#   Paso 4: escribir en archivo de texto
#   Paso 6: añadir SIN sobrescribir (modo 'a')
# ══════════════════════════════════════════════════════════════

def agregar_producto():
    """Pide datos al usuario y los guarda en el archivo .txt."""
    print("\n AGREGAR NUEVO PRODUCTO AL INVENTARIO")
    print("─" * 40)

    nuevo_id = obtener_siguiente_id()
    print(f"ID asignado automáticamente: {nuevo_id}")

    # input() en Python = Console.ReadLine() en C#
    nombre    = input("Nombre del producto : ")
    categoria = input("Categoría           : ")
    
    # int() convierte texto a entero = int.Parse() en C#
    # float() convierte texto a decimal = double.Parse() en C#
    stock  = int(input("Stock (cantidad)    : "))
    precio = float(input("Precio (soles)      : "))

    # Validación básica
    if not nombre.strip() or not categoria.strip():
        print("\n El nombre y la categoría son obligatorios.")
        return  # Sale de la función sin guardar

    # Crear el objeto Producto
    p = Producto(nuevo_id, nombre, categoria, stock, precio)

    # ──────────────────────────────────────────────────────
    # ESCRIBIR EN ARCHIVO DE TEXTO - MODO APPEND
    # ──────────────────────────────────────────────────────
    # "with open(...) as archivo:" es el equivalente Python de:
    # "using (StreamWriter sw = new StreamWriter(ruta, append:true))"
    #
    # El bloque "with" garantiza que el archivo se CIERRA
    # automáticamente al terminar, aunque haya un error.
    # Cumple el PASO 10: cerrar archivos correctamente.
    #
    # 'a' = append → añade al final SIN borrar lo anterior
    #               Cumple PASO 6 de la guía
    asegurar_directorio()
    with open(RUTA_TXT, 'a', encoding='latin-1') as archivo:
        # str(p) llama automáticamente a __str__()
        # produce: "1,Laptop Dell,Electrónica,5,2500.00"
        # \n = salto de línea (como WriteLine en C#)
        archivo.write(str(p) + '\n')
    # ← aquí el archivo se cierra automáticamente

    print(f"\n✅ Producto guardado correctamente:")
    print(f"   ID:{nuevo_id} | {nombre} | {categoria} | Stock:{stock} | S/.{precio:.2f}")
    print(f" Guardado en: {os.path.abspath(RUTA_TXT)}")


# ══════════════════════════════════════════════════════════════
# OPCIÓN 2 - MOSTRAR INVENTARIO
# Paso 5 de la guía: leer y mostrar línea por línea
# ══════════════════════════════════════════════════════════════

def mostrar_inventario():
    """Lee el archivo .txt línea por línea y muestra el inventario."""
    print("\n INVENTARIO COMPLETO (leyendo desde .txt)")
    print("─" * 60)

    if not os.path.exists(RUTA_TXT):
        print("  Archivo no encontrado. Agrega productos primero.")
        return

    # Encabezado de tabla con formato fijo
    # {:<5} = alinear izquierda en 5 caracteres (como ,-5 en C#)
    # {:>8} = alinear derecha en 8 caracteres  (como ,8 en C#)
    print(f"{'ID':<5} {'Nombre':<20} {'Categoría':<15} {'Stock':>7} {'Precio':>10}")
    print("─" * 60)

    total = 0

    # LEER LÍNEA POR LÍNEA
    # 'r' = modo lectura (read) → equivalente a StreamReader en C#
    with open(RUTA_TXT, 'r', encoding='latin-1') as archivo:
        for linea in archivo:              # Itera línea por línea automáticamente
            linea = linea.strip()          # strip() elimina \n y espacios al inicio/fin
            if not linea:                  # Si la línea está vacía, la saltamos
                continue

            # split(',') divide "1,Laptop,Electrónica,5,2500.00"
            # en lista: ["1","Laptop","Electrónica","5","2500.00"]
            # Equivalente a: linea.Split(',') en C#
            partes = linea.split(',')

            if len(partes) == 5:           # Verificar que tenga 5 campos
                id_p  = partes[0]
                nom   = partes[1]
                cat   = partes[2]
                stk   = partes[3]
                pre   = float(partes[4])

                print(f"{id_p:<5} {nom:<20} {cat:<15} {stk:>7} S/.{pre:>8.2f}")
                total += 1

    print("─" * 60)
    print(f"Total de productos en inventario: {total}")


# ══════════════════════════════════════════════════════════════
# OPCIÓN 3 - BUSCAR PRODUCTO
# Paso 7: leer, PROCESAR (búsqueda) y mostrar
# ══════════════════════════════════════════════════════════════

def buscar_producto():
    """Busca productos por nombre o categoría en el archivo .txt."""
    print("\n🔍 BUSCAR PRODUCTO EN INVENTARIO")
    print("─" * 40)
    busqueda = input("Nombre o categoría a buscar: ").lower()
    # .lower() convierte a minúsculas para buscar sin importar mayúsculas
    # Equivalente a: .ToLower() en C#

    if not os.path.exists(RUTA_TXT):
        print("⚠️  Archivo no encontrado.")
        return

    encontrado = False

    with open(RUTA_TXT, 'r', encoding='latin-1') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(',')
            if len(partes) == 5:
                # "in" en Python = .Contains() en C#
                # Busca en nombre (partes[1]) Y categoría (partes[2])
                if busqueda in partes[1].lower() or busqueda in partes[2].lower():
                    if not encontrado:
                        print(f"\n{'ID':<5} {'Nombre':<20} {'Categoría':<15} {'Stock':>7} {'Precio':>10}")
                        print("─" * 60)
                    print(f"{partes[0]:<5} {partes[1]:<20} {partes[2]:<15} {partes[3]:>7} S/.{float(partes[4]):>8.2f}")
                    encontrado = True

    if encontrado:
        print("\n Búsqueda completada.")
    else:
        print(f"\n No se encontró '{busqueda}' en el inventario.")


# ══════════════════════════════════════════════════════════════
# OPCIÓN 4 - RESUMEN DE STOCK
# Paso 7: leer, PROCESAR (conteo/suma) y mostrar
# ══════════════════════════════════════════════════════════════

def contar_y_resumir():
    """Procesa el .txt y muestra estadísticas del inventario."""
    print("\n📊 RESUMEN DEL INVENTARIO")
    print("─" * 40)

    if not os.path.exists(RUTA_TXT):
        print("  Archivo no encontrado.")
        return

    total_productos  = 0
    total_unidades   = 0
    valor_total      = 0.0
    precio_mas_alto  = 0.0
    producto_mas_caro = ""

    with open(RUTA_TXT, 'r', encoding='latin-1') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(',')
            if len(partes) == 5:
                stock  = int(partes[3])
                precio = float(partes[4])

                total_productos  += 1
                total_unidades   += stock
                valor_total      += precio * stock

                if precio > precio_mas_alto:
                    precio_mas_alto   = precio
                    producto_mas_caro = partes[1]

    print(f"  Productos distintos : {total_productos}")
    print(f"  Total de unidades   : {total_unidades}")
    print(f"  Valor del inventario: S/. {valor_total:.2f}")
    print(f"  Producto más caro   : {producto_mas_caro} (S/. {precio_mas_alto:.2f})")


# ══════════════════════════════════════════════════════════════
# OPCIÓN 5 - GUARDAR EN BINARIO
# Paso 8: serializar objetos a archivo .bin con pickle
#
# pickle en Python = BinaryFormatter en C#
# La diferencia clave:
#   C#     → necesita [Serializable] en la clase
#   Python → pickle serializa CUALQUIER objeto automáticamente
# ══════════════════════════════════════════════════════════════

def guardar_en_binario():
    """Serializa todos los productos del .txt a un archivo .bin con pickle."""
    print("\n💾 GUARDAR INVENTARIO EN ARCHIVO BINARIO")
    print("─" * 40)

    if not os.path.exists(RUTA_TXT):
        print("  No hay datos en .txt para convertir a .bin")
        return

    # Primero cargamos todos los productos del .txt
    lista = cargar_productos_desde_txt()

    # ──────────────────────────────────────────────────────
    # SERIALIZAR A BINARIO CON PICKLE
    # 'wb' = write binary (escritura binaria)
    #        Equivalente a: FileStream(ruta, FileMode.Create) en C#
    #
    # pickle.dump(objeto, archivo) = serializa el objeto a bytes
    #        Equivalente a: BinaryFormatter.Serialize(fs, lista) en C#
    # ──────────────────────────────────────────────────────
    asegurar_directorio()
    with open(RUTA_BIN, 'wb') as archivo:
        pickle.dump(lista, archivo)
    # ← archivo cerrado automáticamente (PASO 10)

    tam_txt = os.path.getsize(RUTA_TXT)  # Tamaño en bytes del .txt
    tam_bin = os.path.getsize(RUTA_BIN)  # Tamaño en bytes del .bin

    print(f" {len(lista)} producto(s) serializados a binario.")
    print(f" Archivo .bin: {os.path.abspath(RUTA_BIN)}")
    print(f"\n📏 Comparación de tamaños:")
    print(f"   inventario.txt → {tam_txt} bytes (legible)")
    print(f"   inventario.bin → {tam_bin} bytes (binario)")


# ══════════════════════════════════════════════════════════════
# OPCIÓN 6 - LEER DESDE BINARIO
# Paso 8: deserializar objetos desde archivo .bin con pickle
# ══════════════════════════════════════════════════════════════

def leer_desde_binario():
    """Deserializa los productos desde el archivo .bin y los muestra."""
    print("\n LEER INVENTARIO DESDE ARCHIVO BINARIO")
    print("─" * 40)

    if not os.path.exists(RUTA_BIN):
        print("⚠️  Archivo .bin no existe. Usa la opción 5 primero.")
        return

    # ──────────────────────────────────────────────────────
    # DESERIALIZAR DESDE BINARIO CON PICKLE
    # 'rb' = read binary (lectura binaria)
    #        Equivalente a: FileStream(ruta, FileMode.Open) en C#
    #
    # pickle.load(archivo) = convierte bytes → objeto Python
    #        Equivalente a: BinaryFormatter.Deserialize(fs) en C#
    # ──────────────────────────────────────────────────────
    with open(RUTA_BIN, 'rb') as archivo:
        lista = pickle.load(archivo)
    # ← archivo cerrado automáticamente

    print(f"{'ID':<5} {'Nombre':<20} {'Categoría':<15} {'Stock':>7} {'Precio':>10}")
    print("─" * 60)

    # Recorrer la lista de objetos Producto recuperados del .bin
    # Equivalente a: foreach (Producto p in lista) en C#
    for p in lista:
        print(f"{p.id:<5} {p.nombre:<20} {p.categoria:<15} {p.stock:>7} S/.{p.precio:>8.2f}")

    print("─" * 60)
    print(f" {len(lista)} producto(s) recuperados exitosamente desde .bin")


# ══════════════════════════════════════════════════════════════
# HELPER - CARGAR PRODUCTOS DESDE TXT
# Lee el .txt y devuelve una lista de objetos Producto
# ══════════════════════════════════════════════════════════════

def cargar_productos_desde_txt():
    """Lee el archivo .txt y devuelve lista de objetos Producto."""
    lista = []  # Lista vacía → equivalente a new List<Producto>() en C#

    with open(RUTA_TXT, 'r', encoding='latin-1') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(',')
            if len(partes) == 5:
                # Reconstruir el objeto Producto desde el texto CSV
                p = Producto(
                    id        = int(partes[0]),
                    nombre    = partes[1],
                    categoria = partes[2],
                    stock     = int(partes[3]),
                    precio    = float(partes[4])
                )
                lista.append(p)  # append() = .Add() en C#

    return lista


# ══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA DEL PROGRAMA
# "if __name__ == '__main__':" significa:
# "Ejecutar esto SOLO si corres este archivo directamente"
# (no si lo importas desde otro script)
# Equivalente conceptual al método Main() en C#
# ══════════════════════════════════════════════════════════════

if __name__ == '__main__':

    salir = False  # Variable que controla el bucle del menú

    while not salir:  # "mientras salir sea False, seguir mostrando el menú"
        mostrar_menu()

        opcion = input("\n Elige una opción: ")

        # En Python no hay switch, usamos if/elif/else
        # Equivalente al switch(opcion) en C#
        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            mostrar_inventario()
        elif opcion == '3':
            buscar_producto()
        elif opcion == '4':
            contar_y_resumir()
        elif opcion == '5':
            guardar_en_binario()
        elif opcion == '6':
            leer_desde_binario()
        elif opcion == '7':
            salir = True
        else:
            print("\n⚠️  Opción no válida. Intenta de nuevo.")

        if not salir:
            input("\nPresiona ENTER para volver al menú...")

    print("\n Programa cerrado. Datos guardados en disco.")
