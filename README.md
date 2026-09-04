# CNBPEO — Autodiagnóstico de Calidad de la Producción Estadística

**Oficina Nacional de Estadística (ONE) · República Dominicana**

---

## ¿Qué es?

CNBPEO es una aplicación web institucional para realizar el **Autodiagnóstico de Calidad** de la producción estadística, basado en el **Código Nacional de Buenas Prácticas para las Estadísticas Oficiales (CNBPEO)**. Convierte la matriz de autodiagnóstico en Excel en una herramienta guiada, con evidencias, estadísticas automáticas y descargas listas para presentar.

Está construida sobre **Python + Streamlit + SQLite**. Cada institución guarda su propio autodiagnóstico por separado.

---

## La matriz del autodiagnóstico

El autodiagnóstico se organiza en **3 niveles de gestión**, con un total de **15 principios**, **67 requisitos** y **252 elementos de verificación**:

| Nivel | Código | Qué evalúa |
|---|---|---|
| Gestión del Entorno Institucional | **GEI** | El marco institucional que garantiza la calidad (independencia, mandato, recursos…) |
| Gestión del Proceso Estadístico | **GPE** | Cómo se producen las estadísticas (metodología, recolección, procesamiento…) |
| Gestión de Resultados Estadísticos | **GRE** | La calidad del producto final (pertinencia, precisión, accesibilidad…) |

---

## Cómo se usa (pestañas)

Al entrar a **Autodiagnóstico** primero se elige la **institución** que hace el diagnóstico. Luego hay 5 pestañas:

### ✅ Marcar cumplimiento
Se selecciona un nivel de gestión (GEI/GPE/GRE) y se van completando los elementos, uno por uno. Cada elemento tiene un formulario con:

- **¿Cumple con el elemento?** (SI / NO / N/A)
- **Nivel de cumplimiento** (No Iniciado, Iniciado, Cumplimiento Parcial, Cumplimiento Total)
- **Evidencia actual** y **anterior** (texto + enlace + archivo adjunto)
- **Comentario**, **Acción de mejora**, **Responsable** y **Fecha de cumplimiento**

Cada campo tiene un **signo de ayuda (?)** que, al pasar el mouse, explica qué poner y da un ejemplo.

Arriba aparece la tabla **"Herramienta de autodiagnóstico"**, que lista **todos** los elementos con una columna de **Estado** (✔ Lleno / ⬜ Pendiente), se puede filtrar por nivel/principio/requisito y descargar en **CSV** y **Excel**. La evidencia adjunta se descarga desde la misma fila.

### 📊 Estadísticas
Muestra el **% de cumplimiento** por nivel y por principio, calculado igual que la hoja RESULTADOS del Excel oficial (solo cuenta lo que está en **Cumplimiento Total**, sobre los elementos que aplican). Permite descargar:

- **Excel** y **PDF** de resultados.
- **📦 Informe completo**: un solo Excel con las hojas *Autodiagnóstico*, *Plan de acción*, *Estadísticas*, *Puntaje por nivel* y **Descripción de campos** (documentación de cada columna), más una versión en CSV.

### 📋 Plan de acción
Tabla del plan de acción por requerimiento (con sus actividades, insumos, responsables, riesgos, etc.), con descarga en Excel y CSV.

### 📈 Seguimiento
Vista de avance del autodiagnóstico de la institución.

### 📤 Cargar CSV/JSON/Excel
Permite **importar la matriz Excel (V3)** con las hojas GEI/GPE/GRE, el Plan de acción y los resultados. Al cargarla, se llenan todos los elementos y las estadísticas coinciden con la hoja RESULTADOS del Excel.

---

## Acceso y seguridad

- **Login por usuario y contraseña**, con roles (administrador y otros).
- La sesión **se mantiene al refrescar la página (F5)**: te quedas en la misma pantalla. La única forma de salir es el botón **"Cerrar Sesión"** (o que expire por inactividad).
- Contraseñas protegidas con **bcrypt**; bloqueo temporal tras varios intentos fallidos; verificación en dos pasos (2FA/TOTP) disponible.
- Tema visual institucional azul de la ONE aplicado a toda la app.

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Interfaz web | Streamlit |
| Base de datos | SQLite (archivo local `cnbpe.db`) |
| Autenticación | bcrypt + 2FA (pyotp) |
| Análisis de datos | pandas |
| Exportación Excel | openpyxl |
| Generación PDF | fpdf2 |
| Gráficos | Plotly |

---

## Cómo arrancar la aplicación

```bash
# 1. Instalar dependencias
python -m pip install -r requirements.txt

# 2. (Solo la primera vez) crear el usuario administrador
python -m security.crear_admin

# 3. Levantar la aplicación
python -m streamlit run app.py
```

La aplicación queda disponible en `http://localhost:8501`.

> Nota: si el comando `streamlit` solo no funciona en Windows, usa siempre
> `python -m streamlit run app.py` (así se ejecuta a través de Python
> aunque `streamlit` no esté en el PATH).

---

## Estructura del proyecto (resumen)

```
CNBPEO_actualizacion/
├── app.py                     # Punto de entrada: login, menú, tema visual, sesión
├── config.py                  # Configuración (ruta de la base de datos, etc.)
├── data/
│   ├── database.py            # Base de datos y migraciones
│   ├── diccionario_datos.py   # Hoja "Descripción de campos" del Informe completo
│   └── autodiagnostico_catalogo.py  # Catálogo de niveles/principios/elementos
├── models/                    # Lógica de datos (crud_autodiagnostico, etc.)
├── views/
│   └── autodiagnostico.py     # Toda la pantalla de Autodiagnóstico
├── security/                  # Autenticación, roles, 2FA, hardening
├── utils/                     # Utilidades (backup, mensajes, etc.)
└── cnbpe.db                   # Base de datos (tus datos)
```

---

*Sistema desarrollado por Anneurys M. Medina para la Oficina Nacional de Estadística (ONE) · República Dominicana.*
