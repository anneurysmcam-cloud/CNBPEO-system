"""
resetear_clave.py — Recupera el acceso reseteando la clave de un usuario.
Ejecutar en la carpeta del proyecto:   python resetear_clave.py
"""
from data.database import inicializar_base_datos, obtener_conexion
from security.auth import resetear_password_admin

# >>> Cambia aquí si tu usuario u otra clave <<<
USUARIO = "anneurys"
NUEVA_CLAVE = "CNBPEO2026$"   # requisitos: 8+ caracteres, una mayúscula, un número y un símbolo

inicializar_base_datos()
conn = obtener_conexion()
try:
    print("Usuarios en la base de datos:")
    for u in conn.execute("SELECT id, username, rol, activo FROM usuarios ORDER BY id").fetchall():
        print(f"  id={u[0]}  usuario='{u[1]}'  rol={u[2]}  activo={u[3]}")
    fila = conn.execute("SELECT id FROM usuarios WHERE username = ?", (USUARIO,)).fetchone()
    if not fila:
        print(f"\n>>> No existe un usuario llamado '{USUARIO}'.")
        print(">>> Mira la lista de arriba y pon el nombre correcto en la variable USUARIO.")
        uid = None
    else:
        uid = fila[0]
        conn.execute("UPDATE usuarios SET activo = 1 WHERE id = ?", (uid,))
        conn.commit()
finally:
    conn.close()

if uid is not None:
    resetear_password_admin(uid, NUEVA_CLAVE)
    print(f"\n[OK] Usuario '{USUARIO}' reactivado y clave nueva: {NUEVA_CLAVE}")
    print("     Entra con ese usuario y esa clave; luego puedes cambiarla.")
