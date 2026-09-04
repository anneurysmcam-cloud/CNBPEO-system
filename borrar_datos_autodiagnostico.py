"""
borrar_datos_autodiagnostico.py
===============================
Borra TODOS los datos llenados del autodiagnóstico para empezar de cero:
  - Evaluaciones (¿Cumple?, nivel, evidencia, comentario, acción, responsable, fecha)
  - Enlaces y archivos de evidencia adjuntos
  - Filas del Plan de acción
  - Cortes de Seguimiento

NO borra: la matriz de los 252 elementos (niveles, principios, requisitos,
elementos), la lista de instituciones, ni los usuarios. Después de correrlo,
todas las instituciones quedan en 0% y listas para llenar de nuevo.

⚠️ Esto NO se puede deshacer. Pide una confirmación escrita antes de borrar.

CÓMO USARLO
-----------
1. Pon este archivo en  C:\\CNBPEO_actualizacion  (la raíz, donde está app.py).
2. Con la app DETENIDA (Ctrl+C), en la terminal ejecuta:
       python borrar_datos_autodiagnostico.py
3. Te mostrará cuántos datos hay y te pedirá escribir BORRAR para confirmar.
4. Vuelve a arrancar:  python -m streamlit run app.py
"""

import os
import sqlite3

AQUI = os.path.dirname(os.path.abspath(__file__))

# Tablas con datos LLENADOS (se vacían). El catálogo, instituciones y usuarios
# NO están aquí, así que no se tocan.
TABLAS_DATOS = [
    "autodx_evaluaciones_inst",   # ¿Cumple?, nivel, evidencia, comentario, etc.
    "autodx_evidencia_extra",     # enlaces y archivos adjuntos
    "autodx_plan_accion",         # plan de acción
    "autodx_seguimiento_detalle", # detalle de cortes
    "autodx_seguimiento",         # cortes de seguimiento
]

candidatas = [os.path.join(AQUI, n) for n in ("cnbpe.db", "CNBPEO.db")
              if os.path.exists(os.path.join(AQUI, n))]

if not candidatas:
    print("❌ No encontré 'cnbpe.db' ni 'CNBPEO.db' en esta carpeta.")
    print("   Coloca este script en C:\\CNBPEO_actualizacion (donde está app.py).")
    raise SystemExit(1)

# Mostrar cuántos datos hay antes de borrar.
print("Se borrarán los DATOS LLENADOS de estas bases de datos:\n")
for db in candidatas:
    print("📂", os.path.basename(db))
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    for t in TABLAS_DATOS:
        try:
            n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            print(f"   - {t}: {n} registro(s)")
        except sqlite3.OperationalError:
            print(f"   - {t}: (no existe, se omite)")
    conn.close()

print("\n⚠️  Esto NO se puede deshacer. La matriz de 252 elementos, las")
print("    instituciones y los usuarios NO se tocan; solo se borra lo llenado.")
resp = input('\nEscribe BORRAR (en mayúsculas) para confirmar, o Enter para cancelar: ').strip()

if resp != "BORRAR":
    print("\nCancelado. No se borró nada.")
    raise SystemExit(0)

total = 0
for db in candidatas:
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    for t in TABLAS_DATOS:
        try:
            n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            cur.execute(f"DELETE FROM {t}")
            total += n
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()
    print(f"✅ {os.path.basename(db)}: datos borrados.")

print(f"\n🎉 Listo. Se borraron {total} registro(s) en total.")
print("Todas las instituciones quedan en 0%, listas para llenar de nuevo.")
print("Arranca la app:  python -m streamlit run app.py")
