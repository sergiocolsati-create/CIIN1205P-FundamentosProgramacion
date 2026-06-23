// ============================================================
// LABORATORIO N° 5 - FUNDAMENTOS DE PROGRAMACIÓN
// Tema: Persistencia de Datos con Archivos de Texto y Binarios
// Ejemplo: Sistema de Gestión de Inventario
// Lenguaje: C#
// Alumno: Sergio Isaac Colan Sanchez
// Fecha: Junio 2026
// ============================================================


using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Net;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Threading.Tasks;

namespace GestionInventario
{
    [Serializable]// ← Le decimos a C# que esta clase puede ser serializada

    class Producto {
        // Propiedades del producto (los campos de nuestra "tabla")
        //{get:set} significa que se puede modificar desde afuera
        public int id { get; set; } //Id del producto
        public string Nombre {  get; set; } // Nombre del Producto
        public string Categoria { get; set; } // Categoria del Producto
        public int Stock { get; set; } // Cantidad Disponible del Producto en Almacen
        public double Precio { get; set; } // Precio Unitario en Soles

        // To String es un metodo especial que C# llama automaticamente cuando necesita impirimir o convertir un texto
        // Lo que hace override es sobreescribir para definirlo como queremos y poder guardarlo en .txt
        public override string ToString() => $"{id},{Nombre},{Categoria},{Stock},{Precio}";
            }

    internal class Program
    {
        // Declaramos variables estaticas para que existan durante toda la ejecuacion para que sean accesible  desde 
        //Cualquier metodo
        // Ruta del archivo (.txt)
        //Ya no se necesita subir el txt, el programa los crea solo
        static string rutaTxt = @"..\..\..\..\Datos\inventario.txt";
        // Ruta del archivo (.bin)
        static string rutaBin = @"..\..\..\..\Datos\inventario.txt";
        static void Main(string[] args)
        {
            // Permite moistrar caracteres especiales
            Console.OutputEncoding = System.Text.Encoding.UTF8;


            bool salir = false;   // Variable que controla el bucle del menu

            //Bucle princial: El menu se repite hasta el usuario elija salir
            while (!salir) {
                MostrarMenu(); //Muestra el menu

                string opcion = Console.ReadLine();// Lee lo que escriba el usuario

                // Menu switch de seleccion de opcion

                switch (opcion)
                { 
                    case "1": AgregarProducto();
                        break;
                    case "2":
                        MostrarInventario();
                        break;
                    case "3":
                        BuscarProducto();
                        break;
                    case "4":
                        ContaryResumirStock();
                        break;
                    case "5":
                        GuardarenBinario();
                        break;
                    case "6":
                        LeerdesdeBinario();
                        break;
                    case "7":
                        salir=true;
                        break;
                    default:
                        // Si el usuario escribe un numero diferente
                        Console.WriteLine("\n Opcion no valida. Intenta denuevo");
                        break;
                // Pausa entre funciones para ordenar y leer resultados
                }
                if (!salir)
                {
                    Console.WriteLine("\n Presiona Enter para volver al menu");
                    Console.ReadLine(); // Esperand que el usuario presione Enter para nueva tarea
                }
        }
            Console.WriteLine("\n Programa Cerrado Datos guardados en Disco");
            }

        static void MostrarMenu() { // Menu Visual mostrado en consola para ver la funciones disponibles
        
        Console.Clear();// Limpia la consola antes de mostrar el menu
            Console.WriteLine("╔══════════════════════════════════════════╗");
            Console.WriteLine("╔══════════════════════════════════════════╗");
            Console.WriteLine("║    LAB 05 - SISTEMA DE INVENTARIO        ║");
            Console.WriteLine("║    Persistencia con .txt y .bin          ║");
            Console.WriteLine("╠══════════════════════════════════════════╣");
            Console.WriteLine("║  1. Agregar producto     → escribe .txt  ║");
            Console.WriteLine("║  2. Ver inventario       → lee .txt      ║");
            Console.WriteLine("║  3. Buscar producto      → procesa .txt  ║");
            Console.WriteLine("║  4. Resumen de stock     → procesa .txt  ║");
            Console.WriteLine("║  5. Guardar en binario   → crea .bin     ║");
            Console.WriteLine("║  6. Leer desde binario   → lee .bin      ║");
            Console.WriteLine("║  7. Salir                                ║");
            Console.WriteLine("╚══════════════════════════════════════════╝");
            Console.Write("\n Elige una opción: ");

        }

        // funciones 

        // OPCION 1 - AGREGAR PRODUCTO

        static void AgregarProducto() {
            Console.WriteLine("\n AGREGAR NUEVO PRODUCTO AL INVENTARIO");
            Console.WriteLine("────────────────────────────────────────");

            int nuevoId = ObtenerSiguienteID();
            Console.WriteLine($"Id asignado automaticamente: {nuevoId}");

            Console.Write("Nombre del producto: ");
            string nombre= Console.ReadLine(); // Lee texto desde el teclado

            Console.Write("Categoria: ");
            string categoria= Console.ReadLine();

            Console.Write("Stock(cantidad): ");
            int stock= int.Parse(Console.ReadLine());// convierte texto en un int

            Console.Write("Precio(soles): ");
            double precio= double.Parse(Console.ReadLine());// convierte texto en un decimal

            if (string.IsNullOrEmpty(nombre) || string.IsNullOrEmpty(categoria)){

                Console.WriteLine("\n El nombre y la categoria son obligatorios");
            }

            //Crea el producto con los datos asignados
            Producto p = new Producto
            { 
                    id= nuevoId,
                    Nombre=nombre,
                    Categoria=categoria,
                    Stock=stock,
                    Precio=precio
                                          
            };

            // Escribir en archivo de texto
            //Asegura Directorio para crear la carpeta Datos/ si no existe

            AsegurarDirectorio(rutaTxt);

            // StreamWriter clase de C# para escibir en archivos de texto
            //append: true añade al final del archivo
            using (StreamWriter sw= new StreamWriter(rutaTxt, append: true)){ 
                // Escribe una linea + salto automatico de linea
                // con el To string producimos la linea para txt
                sw.WriteLine(p.ToString());
            }

            Console.WriteLine("\n Producto Guardado Correctamente: ");
            Console.WriteLine($"ID:{nuevoId}|{nombre}|{categoria}|Stock:{stock}| S/. {precio:F2}");// F2 muestra solo dos decimales
            Console.WriteLine($"guardado en: {Path.GetFullPath(rutaTxt)} ");
        }
             
             

        // OPCION 2 - mostrar inventario

        static void MostrarInventario() {
            Console.WriteLine("\n INVENTARIO COMPLETO(leyendo desde .txt)");
            Console.WriteLine("────────────────────────────────────────────");


            // Verificar la existencia del archivo
            if (!File.Exists(rutaTxt)) {

                Console.WriteLine("  Archivo no encontrado. Agrega productos primero.");
            }

            Console.WriteLine($"{"ID",-5}{"Nombre",-20}{"Categoria",-15}{"Stock",7}{"Precio",10}");
            Console.WriteLine(new string('-',62));
        
        int totalProductos=0; // Contador de filas leidas

            using (StreamReader sr = new StreamReader(rutaTxt)) {

                string linea;

                while ((linea = sr.ReadLine()) != null)
                {
                    string[] partes = linea.Split(',');

                    if (partes.Length == 5) { 
                    
                        int id= int.Parse(partes[0]);
                        string nombre = partes[1];
                        string categ = partes[2];
                        int stock = int.Parse(partes[3]);
                        double precio = double.Parse(partes[4]);

                        Console.WriteLine($"{id,-5}{nombre,-20}{categ,-15}{stock,7}  S/.{precio,8:F2}");
                        totalProductos++;
                    
                    }
                   
                }
            
            }
            Console.WriteLine(new string('-',62));
            Console.WriteLine($"Total de productos en inventario:{totalProductos}");

        }

        // OPCION 3 - Buscar Producto

        static void BuscarProducto()
        {
            Console.WriteLine("\n BUSCAR PRODUCTO EN INVENTARIO");
            Console.WriteLine("──────────────────────────────────");
            Console.WriteLine("Nombre o categoría a buscar: ");

            string busqueda= Console.ReadLine()?.ToLower();// tolower nos permite comparar sin atender mayusculas

            if (!File.Exists(rutaTxt)) { 
            
                    Console.WriteLine("Archivos no encontrados");
                return;
            }
            bool encontrado = false;

            using (StreamReader sr = new StreamReader(rutaTxt)) {
                string linea;
                while ((linea = sr.ReadLine()) != null)
                {
                    string[] partes = linea.Split(',');
                    if (partes.Length == 5) {
                        //.Contains()= nos ayuda a verificar si el texto contiene lo que buscamos
                        // buscamos en nombre (parte[1] y en categoria(partes[2]))

                        bool coincide = partes[1].ToLower().Contains(busqueda) || partes[2].ToLower().Contains(busqueda);

                        if (coincide) {

                            if (!encontrado) {
                                Console.WriteLine($"\n{"ID",-5} {"Nombre",-20} {"Categoría",-15} {"Stock",7} {"Precio",10}");
                                Console.WriteLine(new string('─', 62));
                            }
                            Console.WriteLine($"{partes[0],-5} {partes[1],-20} {partes[2],-15} {partes[3],7} S/.{double.Parse(partes[4]),8:F2}");
                            encontrado = true;
                        }


                    }
                
                
                }
            
            
            
            }
            Console.WriteLine(encontrado
            ? "\n✅ Búsqueda completada."
            : $"\n❌ No se encontró '{busqueda}' en el inventario.");



        }

        // OPCION 4 - Contar y resumir Stock

        static void ContaryResumirStock() {

            Console.WriteLine("\n RESUMEN DEL INVENTARIO");
            Console.WriteLine("──────────────────────────");

            if (!File.Exists(rutaTxt))
            {
                Console.WriteLine("  Archivo no encontrado.");
                return;
            }

            int totalProductos = 0;    // Cuántos productos distintos hay
            int totalUnidades = 0;    // Suma de todos los stocks
            double valorTotal = 0;    // Suma de (precio × stock) de cada producto
            double precioMasAlto = 0;    // El precio unitario más caro
            string productoMasCaro = "";   // Nombre del producto más caro

            using (StreamReader sr = new StreamReader(rutaTxt))
            {
                string linea;
                while ((linea = sr.ReadLine()) != null)
                {
                    string[] partes = linea.Split(',');
                    if (partes.Length == 5)
                    {
                        int stock = int.Parse(partes[3]);
                        double precio = double.Parse(partes[4]);

                        totalProductos++;
                        totalUnidades += stock;                  // Suma acumulada de stock
                        valorTotal += precio * stock;         // Valor total por producto

                        // Detectar el producto más caro
                        if (precio > precioMasAlto)
                        {
                            precioMasAlto = precio;
                            productoMasCaro = partes[1];
                        }
                    }
                }
            }

            // Mostrar resumen procesado
            Console.WriteLine($"  Productos distintos : {totalProductos}");
            Console.WriteLine($"  Total de unidades   : {totalUnidades}");
            Console.WriteLine($"  Valor del inventario: S/. {valorTotal:F2}");
            Console.WriteLine($"  Producto más caro   : {productoMasCaro} (S/. {precioMasAlto:F2})");


        }

        // OPCION 5 - GuardarenBinario
        // ¿Por qué binario?
        //   .txt → legible por humanos, fácil de editar/ver
        //   .bin → no legible directamente, más compacto,
        //          ideal para estructuras complejas y mayor seguridad

        static void GuardarenBinario() {
            Console.WriteLine("\n GUARDAR INVENTARIO EN ARCHIVO BINARIO");
            Console.WriteLine("─────────────────────────────────────────");

            if (!File.Exists(rutaTxt))
            {
                Console.WriteLine("  No hay datos en .txt para convertir a .bin");
                return;
            }

            // Primero cargamos todos los productos desde el .txt
            List<Producto> lista = CargarProductosDesdeTxt();

            // Asegurar que la carpeta Datos/ existe
            AsegurarDirectorio(rutaBin);

            // ──────────────────────────────────────────────────────
            // SERIALIZAR A BINARIO
            // FileStream: abre/crea un archivo a nivel de bytes (binario)
            //   FileMode.Create → crea nuevo o SOBREESCRIBE si ya existe
            // BinaryFormatter: convierte objetos C# ↔ bytes
            // ──────────────────────────────────────────────────────
            using (FileStream fs = new FileStream(rutaBin, FileMode.Create))
            {
#pragma warning disable SYSLIB0011 // Desactiva advertencia de obsolescencia
                BinaryFormatter bf = new BinaryFormatter();

                // Serialize = OBJETO → BYTES → ARCHIVO
                // Toma la lista completa de objetos Producto y la convierte
                // a una secuencia de bytes que se graba en el archivo .bin
                bf.Serialize(fs, lista);
#pragma warning restore SYSLIB0011
            } // ← FileStream se cierra automáticamente (PASO 10)

            // Comparar tamaños para ver la diferencia .txt vs .bin
            long tamTxt = new FileInfo(rutaTxt).Length;
            long tamBin = new FileInfo(rutaBin).Length;

            Console.WriteLine($"✅ {lista.Count} producto(s) serializados a binario.");
            Console.WriteLine($"📁 Archivo .bin: {Path.GetFullPath(rutaBin)}");
            Console.WriteLine($"\n📏 Comparación de tamaños:");
            Console.WriteLine($"   inventario.txt → {tamTxt} bytes (legible)");
            Console.WriteLine($"   inventario.bin → {tamBin} bytes (binario)");
        }

        // OPCION 6 - Leer desde binario

        static void LeerdesdeBinario() {

            Console.WriteLine("\n LEER INVENTARIO DESDE ARCHIVO BINARIO");
            Console.WriteLine("─────────────────────────────────────────");

            if (!File.Exists(rutaBin))
            {
                Console.WriteLine("⚠️  Archivo .bin no existe. Usa la opción 5 primero.");
                return;
            }

            List<Producto> lista;

            using (FileStream fs = new FileStream(rutaBin, FileMode.Open))
            {
#pragma warning disable SYSLIB0011
                BinaryFormatter bf = new BinaryFormatter();

                // Deserialize = BYTES → OBJETO
                // Lee los bytes del .bin y los reconstruye como objetos Producto
                // El cast (List<Producto>) le dice a C# qué tipo de objeto esperar
                lista = (List<Producto>)bf.Deserialize(fs);
#pragma warning restore SYSLIB0011
            }

            Console.WriteLine($"{"ID",-5} {"Nombre",-20} {"Categoría",-15} {"Stock",7} {"Precio",10}");
            Console.WriteLine(new string('─', 62));

            // Recorremos la lista de objetos recuperados del .bin
            foreach (Producto p in lista)
            {
                Console.WriteLine($"{p.id,-5} {p.Nombre,-20} {p.Categoria,-15} {p.Stock,7} S/.{p.Precio,8:F2}");
            }

            Console.WriteLine(new string('─', 62));
            Console.WriteLine($"✅ {lista.Count} producto(s) recuperados exitosamente desde .bin");
        }


        // METODOS AUXILIARES (Helpers)
        // Funciones reutilizables que usan los metodos principales

        static int ObtenerSiguienteID()
        {
            if(!File.Exists(rutaTxt)) return 1;

            int count =0;
            using(StreamReader sr = new StreamReader(rutaTxt))
                while(sr.ReadLine()!=null) count++; // cuenta cada linea
                    
            return count +1; // Aumenta el numero de id +1
        
        }

        static List<Producto> CargarProductosDesdeTxt() {

            var lista = new List<Producto>();

            using (StreamReader sr = new StreamReader(rutaTxt)) {
                string linea;
                while ((linea = sr.ReadLine()) != null)
                {
                    string[] p = linea.Split(',');
                    if (p.Length == 5)
                    {
                        lista.Add(new Producto
                        {
                            id= int.Parse(p[0]),
                            Nombre = p[1],
                            Categoria = p[2],
                            Stock = int.Parse(p[3]),
                            Precio = double.Parse(p[4]),

                        });
                                }
                       
            }

                return lista; 

        }

       
    }

        static void AsegurarDirectorio(string ruta)
        {
            // Path.GetFullPath → convierte ruta relativa a absoluta
            // Path.GetDirectoryName → extrae solo la carpeta
            string dir = Path.GetDirectoryName(Path.GetFullPath(ruta));

            // Si la carpeta no existe la crea
            if (!Directory.Exists(dir)) Directory.CreateDirectory(dir);

        }

    }
}

