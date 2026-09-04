"""
crear_anneurys.py — Crea (o resetea) el usuario 'anneurys' sin pedir nada.
Ejecutar en la carpeta del proyecto:   python crear_anneurys.py
"""
from data.database import inicializar_base_datos, obtener_conexion
from security.auth import registrar_usuario, resetear_password_admin

USUARIO = "anneurys"
CLAVE = "CNBPEO2026$"   # 8+ caracteres, mayúscula, número y símbolo

inicializar_base_datos()
try:
    registrar_usuario(USUARIO, CLAVE, rol="administrador")
    print(f"\n[OK] Usuario '{USUARIO}' creado como administrador.")
except Exception:
    conn = obtener_conexion()
    fila = conn.execute("SELECT id FROM usuarios WHERE username = ?", (USUARIO,)).fetchone()
    if fila:
        conn.execute("UPDATE usuarios SET activo = 1 WHERE id = ?", (fila[0],))
        conn.commit()
        conn.close()
        resetear_password_admin(fila[0], CLAVE)
        print(f"\n[OK] Usuario '{USUARIO}' ya existía: reactivado y clave reseteada.")
    else:
        conn.close()
        raise
print(f"     Entra con:  usuario = {USUARIO}   contrasena = {CLAVE}")
