"""
limpiar_seguimientos.py
=======================
Borra TODOS los cortes de la pestaña "Seguimiento" (tablas
autodx_seguimiento y autodx_seguimiento_detalle) para dejar esa sección
limpia. Esto quita el error de "Duplicate column names" que provocan los
cortes de prueba con nombres repetidos.

NO toca nada más: tu autodiagnóstico, plan de acción, usuarios, evidencias,
etc. quedan intactos. Solo borra los "cortes" de Seguimiento.

CÓMO USARLO
-----------
1. Pon este archivo en la carpeta  C:\\CNBPEO_actualizacion  (la raíz, donde
   está app.py y la base de datos).
2. En la terminal de VS Code, con la app DETENIDA (Ctrl+C), ejecuta:
       python limpiar_seguimientos.py
3. Vuelve a arrancar la app:  python -m streamlit run app.py
"""

import os
import sqlite3

AQUI = os.path.dirname(os.path.abspath(__file__))

# La app usa cnbpe.db; se limpia también CNBPEO.db si existe, por si acaso.
candidatas = [os.path.join(AQUI, n) for n in ("cnbpe.db", "CNBPEO.db")
              if os.path.exists(os.path.join(AQUI, n))]

if not candidatas:
    print("❌ No encontré 'cnbpe.db' ni 'CNBPEO.db' en esta carpeta.")
    print("   Coloca este script en C:\\CNBPEO_actualizacion (donde está app.py).")
    raise SystemExit(1)

total = 0
for db in candidatas:
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        n = cur.execute("SELECT COUNT(*) FROM autodx_seguimiento").fetchone()[0]
        cur.execute("DELETE FROM autodx_seguimiento_detalle")
        cur.execute("DELETE FROM autodx_seguimiento")
        conn.commit()
        total += n
        print(f"✅ {os.path.basename(db)}: {n} corte(s) de seguimiento eliminado(s).")
    except sqlite3.OperationalError as exc:
        # La tabla puede no existir en una BD que nunca abrió esa pestaña.
        print(f"ℹ️  {os.path.basename(db)}: sin tabla de seguimientos ({exc}).")
    finally:
        conn.close()

print(f"\n🎉 Listo. Se eliminaron {total} corte(s) en total.")
print("Vuelve a la app (python -m streamlit run app.py) y entra a 'Seguimiento':")
print("ya no debe salir el error. Empieza a registrar tus cortes reales.")
