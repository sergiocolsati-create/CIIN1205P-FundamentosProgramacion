# CIIN1205P-FundamentosProgramacion
Laboratorios del curso Fundamentos de Programación - UPN

Laboratorio N° 5 — Persistencia de Datos con Archivos

**Curso:** Fundamentos de Programación — CIIN1205P  
**Alumno:** Sergio Colan Sanchez
**Fecha:** Junio 2026  

---

## Objetivo

Aplicar operaciones de apertura, lectura, escritura y cierre de archivos
de texto y binarios para lograr almacenamiento persistente usando C# y Python.
---

## Estructura del proyecto
Lab05-Archivos/

├── CSharp/

│   └── GestionInventario/

│       └── Program.cs       ← Sistema de inventario en C#

├── Python/

│   └── inventario.py        ← Sistema de inventario en Python 

├── Datos/

│   └── .gitkeep             ← Los archivos .txt y .bin se generan aquí al ejecutar

└── README.md

---

## Cómo ejecutar

### C#
1. Abrir `CSharp/GestionInventario.sln` en Visual Studio
2. Presionar `F5`
3. Seguir el menú en consola

### Python
1. Abrir terminal en la carpeta `Python/`
2. Ejecutar: `python inventario.py`

---

## Archivos generados al ejecutar (no incluidos en el repo)

| Archivo | Tipo | Descripción |
|---|---|---|
| `Datos/inventario.txt` | Texto | Registros en formato CSV legible |
| `Datos/inventario.bin` | Binario | Registros serializados en bytes |

---

## Conceptos aplicados

| Concepto | C# | Python |
|---|---|---|
| Escribir archivo | `StreamWriter` | `open('a')` |
| Leer archivo | `StreamReader` | `open('r')` |
| Modo append | `append: true` | modo `'a'` |
| Serialización binaria | `BinaryFormatter` | `pickle` |
| Clase serializable | `[Serializable]` | automático en pickle |
