"""
views/autodiagnostico.py
=========================
Autodiagnóstico de Calidad — Código Nacional de Buenas Prácticas para las
Estadísticas Oficiales (ONE). Refleja la Matriz original tal cual:

    Nivel (GEI/GPE/GRE) > Principio (15) > Requisito (67) > Verificación (252)

POR INSTITUCIÓN: arriba se elige la institución pública (de una lista o
escribiendo una nueva) y todo lo que se marca/importa/exporta/plan/seguimiento
pertenece a esa institución. Pestañas: Marcar cumplimiento, Estadísticas,
Plan de acción, Seguimiento y Excel automático.
"""

import datetime
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

from data import database as db_mod
from models import crud_autodiagnostico as crud_adx

_COLOR_NIVEL_CUMPLIMIENTO: dict[str, str] = {
    "No aplica": "#9CA3AF", "No Iniciado": "#D9534F", "Iniciado": "#F0AD4E",
    "Cumplimiento Parcial": "#FFC72C", "Cumplimiento Total": "#002F6C",
}
_ORDEN_NIVEL_CUMPLIMIENTO = list(_COLOR_NIVEL_CUMPLIMIENTO.keys())
_COLOR_SCORE_ESCALA = "Blues"
_LETRA_NIVEL = {"GEI": "A", "GPE": "B", "GRE": "C"}
_OPCION_NUEVA = "➕ Escribir otra institución…"


def _grafico_descargable(fig, nombre_archivo: str, alto: int | None = None) -> None:
    if alto:
        fig.update_layout(height=alto)
    st.plotly_chart(
        fig, width="stretch",
        config={"displaylogo": False,
                "toImageButtonOptions": {"format": "png", "filename": nombre_archivo, "scale": 2}},
    )


def _selector_institucion() -> int | None:
    """Selector de institución activa (lista + opción de escribir una nueva).
    Guarda la institución elegida en session_state y devuelve su id."""
    instituciones = crud_adx.listar_instituciones()
    if not instituciones:
        st.error("No hay instituciones cargadas.")
        return None
    por_nombre = {i["nombre"]: i["id"] for i in instituciones}
    nombres = list(por_nombre.keys()) + [_OPCION_NUEVA]

    actual_id = st.session_state.get("adx_institucion_id") or crud_adx.id_institucion_por_defecto()
    indice = 0
    for pos, nombre in enumerate(nombres[:-1]):
        if por_nombre[nombre] == actual_id:
            indice = pos
            break

    col_sel, col_info = st.columns([3, 2])
    with col_sel:
        sel = st.selectbox("🏛️ Institución que hace el autodiagnóstico", nombres,
                           index=indice, key="adx_inst_sel")

    if sel == _OPCION_NUEVA:
        with col_info:
            st.caption(" ")
        c1, c2 = st.columns([3, 1])
        nueva = c1.text_input("Nombre de la institución nueva", key="adx_inst_nueva",
                              placeholder="Ej. Ayuntamiento del Distrito Nacional")
        c2.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if c2.button("➕ Agregar", key="adx_inst_add", width="stretch"):
            nid, msg = crud_adx.crear_o_obtener_institucion(nueva)
            if nid:
                st.session_state["adx_institucion_id"] = nid
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        return st.session_state.get("adx_institucion_id") or crud_adx.id_institucion_por_defecto()

    iid = por_nombre[sel]
    st.session_state["adx_institucion_id"] = iid
    with col_info:
        resumen = crud_adx.calcular_resumen(iid)
        st.metric("% General de esta institución",
                  f"{resumen['general']}%" if resumen["general"] is not None else "—")
    return iid


_NOMBRE_NIVEL = {
    "GEI": "A. Gestión del entorno institucional",
    "GPE": "B. Gestión del Proceso Estadístico",
    "GRE": "C. Gestión de resultados estadísticos",
}


def mostrar_autodiagnostico_gei() -> None:
    mostrar_autodiagnostico(nivel_forzado="GEI")


def mostrar_autodiagnostico_gpe() -> None:
    mostrar_autodiagnostico(nivel_forzado="GPE")


def mostrar_autodiagnostico_gre() -> None:
    mostrar_autodiagnostico(nivel_forzado="GRE")


def mostrar_autodiagnostico(nivel_forzado: str | None = None) -> None:
    # El signo (?) de ayuda de Streamlit hereda un gris muy tenue que casi no
    # se ve sobre el fondo azul oscuro. Lo forzamos a un color brillante y algo
    # más grande para que se note al lado de cada campo del formulario.
    st.markdown(
        """
        <style>
        /* Reemplaza el icono de ayuda por un "?" blanco sutil, SOLO en los
           campos del formulario (selectbox, texto, fecha, archivo). NO toca
           tablas/dataframes ni barras de herramientas, para que en Estadísticas
           no aparezcan "?" de más. Un solo selector por campo evita el "?" doble. */
        div[data-testid="stSelectbox"] [data-testid="stTooltipHoverTarget"] svg,
        div[data-testid="stMultiSelect"] [data-testid="stTooltipHoverTarget"] svg,
        div[data-testid="stTextInput"] [data-testid="stTooltipHoverTarget"] svg,
        div[data-testid="stTextArea"] [data-testid="stTooltipHoverTarget"] svg,
        div[data-testid="stDateInput"] [data-testid="stTooltipHoverTarget"] svg,
        div[data-testid="stFileUploader"] [data-testid="stTooltipHoverTarget"] svg {
            display: none !important;
        }
        div[data-testid="stSelectbox"] [data-testid="stTooltipHoverTarget"]::after,
        div[data-testid="stMultiSelect"] [data-testid="stTooltipHoverTarget"]::after,
        div[data-testid="stTextInput"] [data-testid="stTooltipHoverTarget"]::after,
        div[data-testid="stTextArea"] [data-testid="stTooltipHoverTarget"]::after,
        div[data-testid="stDateInput"] [data-testid="stTooltipHoverTarget"]::after,
        div[data-testid="stFileUploader"] [data-testid="stTooltipHoverTarget"]::after {
            content: "?";
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.14);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.55);
            font-weight: 700;
            font-size: 12px;
            line-height: 1;
            cursor: help;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.header("🧭 Autodiagnóstico de Calidad — Código Nacional de Buenas Prácticas")
    st.caption(
        "Matriz de Autodiagnóstico para la Calidad de la Producción Estadística (ONE). "
        "3 niveles (GEI · GPE · GRE), 15 principios, 67 requisitos y 252 elementos de verificación. "
        "Cada institución guarda su propio autodiagnóstico."
    )
    if nivel_forzado:
        st.info(f"📂 Estás en el nivel **{_NOMBRE_NIVEL.get(nivel_forzado, nivel_forzado)}** "
                f"({nivel_forzado}). En 'Marcar cumplimiento' verás solo los elementos de este nivel.")

    institucion_id = _selector_institucion()
    if institucion_id is None:
        return

    usuario = st.session_state.get("usuario") or {}
    resultado_sync = crud_adx.sincronizar_si_cambio(institucion_id, usuario.get("id"))
    if resultado_sync is not None:
        ok_sync, msg_sync, _ = resultado_sync
        if ok_sync:
            st.success(f"🔄 Datos actualizados automáticamente desde el Excel. {msg_sync}")
        else:
            st.warning(f"⚠️ No se pudo leer el Excel configurado: {msg_sync}")

    st.divider()
    tab_marcar, tab_stats, tab_plan, tab_seg, tab_importar = st.tabs(
        ["✅ Marcar cumplimiento", "📊 Estadísticas", "📋 Plan de acción",
         "📈 Seguimiento", "📤 Cargar CSV/JSON"]
    )
    with tab_marcar:
        _mostrar_marcado(institucion_id, nivel_forzado)
    with tab_stats:
        _mostrar_estadisticas(institucion_id)
    with tab_plan:
        _mostrar_plan_accion(institucion_id)
    with tab_seg:
        _mostrar_seguimiento(institucion_id)
    with tab_importar:
        _mostrar_importar(institucion_id)


# ---------------------------------------------------------------------------
# Pestaña 1 — Marcar cumplimiento (nivel de las 252 verificaciones)
# ---------------------------------------------------------------------------

def _fecha_a_date(valor):
    """ISO string almacenado → datetime.date (o None) para la columna de fecha."""
    if not valor:
        return None
    try:
        return datetime.date.fromisoformat(str(valor)[:10])
    except ValueError:
        return None


def _fecha_a_iso(valor):
    """Valor de la columna de fecha (date/Timestamp/None/NaT) → 'YYYY-MM-DD' o None."""
    if valor is None:
        return None
    try:
        if pd.isna(valor):
            return None
    except (TypeError, ValueError):
        pass
    if hasattr(valor, "isoformat"):
        try:
            return valor.isoformat()[:10]
        except Exception:  # noqa: BLE001
            return None
    s = str(valor).strip()
    return s[:10] or None


def _leer_evidencia_extra_todos(institucion_id: int) -> dict:
    """Lee de una sola vez los enlaces/archivos de todas las verificaciones."""
    _asegurar_tabla_evidencia_extra()
    conn = db_mod.obtener_conexion()
    conn.row_factory = sqlite3.Row
    try:
        filas = conn.execute(
            "SELECT verificacion_id, enlace_actual, enlace_anterior, "
            "archivo_actual_nombre, archivo_anterior_nombre "
            "FROM autodx_evidencia_extra WHERE institucion_id=?",
            (institucion_id,),
        ).fetchall()
        return {f["verificacion_id"]: dict(f) for f in filas}
    finally:
        conn.close()


def _mime_archivo(nombre: str) -> str:
    ext = (nombre.rsplit(".", 1)[-1].lower() if "." in nombre else "")
    return {
        "pdf": "application/pdf", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }.get(ext, "application/octet-stream")


def _tabla_llenados(institucion_id: int, nivel_codigo: str | None = None,
                    principio_numero: int | None = None, requisito_codigo: str | None = None) -> None:
    """Tabla (como la de Plan de acción) con los elementos que ya se han
    llenado/marcado, filtrada igual que los filtros de arriba (Nivel / Principio /
    Requisito). La descarga del archivo va DENTRO de la celda 'Archivo'."""
    import base64
    import html as _html
    import io

    todas = crud_adx.listar_verificaciones(
        institucion_id, nivel_codigo=nivel_codigo, principio_numero=principio_numero,
        requisito_codigo=requisito_codigo)
    extra = _leer_evidencia_extra_todos(institucion_id)

    def _cel_enlace(url):
        if not url:
            return ""
        u = _html.escape(str(url))
        if str(url).lower().startswith("http"):
            txt = u if len(u) <= 34 else u[:34] + "…"
            return f'<a href="{u}" target="_blank" style="color:#8fc0ff">{txt}</a>'
        return u

    def _cel_archivo(nombre, blob):
        if not nombre:
            return ""
        n = _html.escape(str(nombre))
        if blob is None:
            return n
        b64 = base64.b64encode(blob).decode("ascii")
        return (f'<a href="data:{_mime_archivo(nombre)};base64,{b64}" download="{n}" '
                f'style="color:#8fc0ff;font-weight:600">⬇️ {n}</a>')

    headers = ["Código", "Nivel", "Elemento", "¿Cumple?", "Nivel de cumplimiento",
               "Evidencia actual", "Enlace actual", "Archivo actual",
               "Evidencia anterior", "Enlace anterior", "Archivo anterior", "Responsable", "Fecha"]
    idx_html = {6, 7, 9, 10}  # celdas que ya son HTML (enlaces y archivos)

    filas = []       # datos planos para exportar en CSV / Excel
    filas_html = []  # filas de la tabla, con descarga DENTRO de la celda
    for v in todas:
        ex = extra.get(v["verificacion_id"], {})
        lleno = any([
            v["cumple"],
            (v["nivel_cumplimiento"] and v["nivel_cumplimiento"] != "No Iniciado"),
            v["evidencia_actual"], v["evidencia_anterior"], v["comentario"],
            v["accion_mejora"], v["responsable"], v["fecha_cumplimiento"],
            ex.get("enlace_actual"), ex.get("enlace_anterior"),
            ex.get("archivo_actual_nombre"), ex.get("archivo_anterior_nombre"),
        ])
        # Solo se muestran los elementos que YA tienen información (llenos).
        if not lleno:
            continue
        filas.append({
            "Código": v["codigo"], "Nivel": v["nivel_codigo"], "Elemento": v["texto"] or "",
            "¿Cumple?": v["cumple"] or "—", "Nivel de cumplimiento": v["nivel_cumplimiento"] or "—",
            "Evidencia actual": v["evidencia_actual"] or "", "Enlace actual": ex.get("enlace_actual") or "",
            "Archivo actual": ex.get("archivo_actual_nombre") or "",
            "Evidencia anterior": v["evidencia_anterior"] or "", "Enlace anterior": ex.get("enlace_anterior") or "",
            "Archivo anterior": ex.get("archivo_anterior_nombre") or "",
            "Responsable": v["responsable"] or "", "Fecha": v["fecha_cumplimiento"] or "",
        })
        # Blobs solo si el elemento tiene archivo (para no pesar).
        blob_act = blob_ant = None
        if ex.get("archivo_actual_nombre") or ex.get("archivo_anterior_nombre"):
            full = _leer_evidencia_extra(institucion_id, v["verificacion_id"])
            blob_act = full.get("archivo_actual_datos")
            blob_ant = full.get("archivo_anterior_datos")
        celdas = [
            v["codigo"], v["nivel_codigo"], (v["texto"] or "")[:80],
            v["cumple"] or "—", v["nivel_cumplimiento"] or "—",
            v["evidencia_actual"] or "", _cel_enlace(ex.get("enlace_actual")),
            _cel_archivo(ex.get("archivo_actual_nombre"), blob_act),
            v["evidencia_anterior"] or "", _cel_enlace(ex.get("enlace_anterior")),
            _cel_archivo(ex.get("archivo_anterior_nombre"), blob_ant),
            v["responsable"] or "", v["fecha_cumplimiento"] or "",
        ]
        tds = []
        for i, c in enumerate(celdas):
            contenido = c if i in idx_html else _html.escape(str(c))
            tds.append(f"<td>{contenido}</td>")
        filas_html.append("<tr>" + "".join(tds) + "</tr>")

    thead = "<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>"
    n_llenos = len(filas)
    titulo = f"📝 Herramienta de autodiagnóstico ({n_llenos})" if n_llenos else "📝 Herramienta de autodiagnóstico"
    with st.expander(titulo, expanded=False):
        if n_llenos:
            df_ll = pd.DataFrame(filas)
            st.caption(f"{n_llenos} elemento(s) con información registrada (según los filtros de arriba). "
                       "En la columna **Archivo** haz clic en ⬇️ para descargar el archivo desde la misma "
                       "fila; los enlaces se abren con un clic. Arriba tienes CSV y Excel de toda la tabla. "
                       "💡 Si ves un error rojo, apaga el traductor del navegador en esta página.")
            cdl1, cdl2, _sp = st.columns([1, 1, 3])
            cdl1.download_button("⬇️ Descargar en CSV",
                                 data=df_ll.to_csv(index=False).encode("utf-8-sig"),
                                 file_name="lo_que_se_ha_llenado.csv", mime="text/csv",
                                 key="adx_dl_llenado_csv", width="stretch")
            buf = io.BytesIO()
            df_ll.to_excel(buf, index=False, sheet_name="Llenado")
            cdl2.download_button("⬇️ Descargar en Excel (.xlsx)", data=buf.getvalue(),
                                 file_name="lo_que_se_ha_llenado.xlsx",
                                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 key="adx_dl_llenado_xlsx", width="stretch")
            # Tabla con la descarga del archivo DENTRO de la celda "Archivo".
            st.markdown(
                "<style>"
                "#cn-llenados{border-collapse:collapse;width:100%;font-size:.82rem;color:#e8edf5}"
                "#cn-llenados td,#cn-llenados th{border:1px solid rgba(95,175,255,.28);"
                "padding:8px 12px;text-align:left;vertical-align:top;white-space:nowrap;"
                "max-width:300px;overflow:hidden;text-overflow:ellipsis}"
                # Encabezados amigables: en negrita, sobre fondo azul y fijos al
                # hacer scroll. En UNA sola línea (nowrap) para que cada columna
                # tome su ancho natural — ni estiradas/combinadas, ni partidas
                # letra por letra.
                "#cn-llenados thead th{position:sticky;top:0;background:#12305f;color:#cfe0ff;"
                "white-space:nowrap;vertical-align:middle;font-weight:700;padding:8px 12px}"
                "#cn-llenados tbody tr:nth-child(even){background:rgba(18,48,95,.35)}"
                "</style>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div style='overflow:auto;max-height:520px;border:1px solid rgba(95,175,255,.4);"
                "border-radius:10px'><table id='cn-llenados'>"
                f"<thead>{thead}</thead><tbody>{''.join(filas_html)}</tbody></table></div>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("No hay elementos que coincidan con los filtros actuales.")
    st.divider()


def _mostrar_marcado(institucion_id: int, nivel_forzado: str | None = None) -> None:
    tabla_llenados_ph = st.container()  # se muestra ARRIBA, pero se llena tras leer los filtros
    niveles = crud_adx.listar_niveles()
    c1, c2, c3, c4 = st.columns([2, 3, 3, 2])
    with c1:
        if nivel_forzado:
            nombre = next((n["nombre"] for n in niveles if n["codigo"] == nivel_forzado), nivel_forzado)
            st.text_input("Nivel de gestión", value=f"{nivel_forzado} — {nombre}",
                          disabled=True, key="adx_filtro_nivel_fijo")
            nivel_codigo = nivel_forzado
        else:
            opciones_nivel = ["Todos"] + [f"{n['codigo']} — {n['nombre']}" for n in niveles]
            sel_nivel = st.selectbox("Nivel de gestión", opciones_nivel, key="adx_filtro_nivel",
                help="Filtra los elementos por nivel de gestión: GEI (Entorno Institucional), "
                     "GPE (Proceso Estadístico) o GRE (Resultados). Elige 'Todos' para ver el "
                     "resumen general por principio.")
            nivel_codigo = sel_nivel.split(" — ")[0] if sel_nivel != "Todos" else None
    with c2:
        principios = crud_adx.listar_principios(nivel_codigo=nivel_codigo)
        opciones_principio = ["Todos"] + [f"{p['numero']}. {p['nombre']}" for p in principios]
        sel_principio = st.selectbox("Principio", opciones_principio, key="adx_filtro_principio",
            help="Filtra por principio de calidad dentro del nivel seleccionado. "
                 "Cada nivel tiene varios principios.")
        principio_numero = int(sel_principio.split(".", 1)[0]) if sel_principio != "Todos" else None
    with c3:
        requisitos = crud_adx.listar_requisitos(nivel_codigo=nivel_codigo, principio_numero=principio_numero)
        opciones_req = ["Todos"] + [f"{r['codigo']} — {r['requisito_cumplimiento'][:50]}" for r in requisitos]
        sel_req = st.selectbox("Requisito", opciones_req, key="adx_filtro_requisito",
            help="Filtra por requisito específico dentro del principio. "
                 "Cada requisito agrupa varios elementos de verificación.")
        requisito_codigo = sel_req.split(" — ")[0] if sel_req != "Todos" else None
    with c4:
        st.write("")
        st.write("")
        solo_pendientes = st.checkbox("Solo pendientes", key="adx_solo_pendientes")

    # La tabla "Herramienta de autodiagnóstico" (arriba) filtrada igual que estos filtros.
    with tabla_llenados_ph:
        _tabla_llenados(institucion_id, nivel_codigo, principio_numero, requisito_codigo)

    verificaciones = crud_adx.listar_verificaciones(
        institucion_id, nivel_codigo=nivel_codigo, principio_numero=principio_numero,
        requisito_codigo=requisito_codigo,
    )
    if solo_pendientes:
        verificaciones = [v for v in verificaciones if (v["nivel_cumplimiento"] or "No Iniciado") != "Cumplimiento Total"]

    if not verificaciones:
        st.info("No hay elementos que coincidan con los filtros seleccionados.")
        return

    # Sin NINGÚN filtro (Nivel de gestión en "Todos"): se muestra un resumen
    # general. Al elegir un Nivel (o un principio/requisito) se muestran TODOS
    # sus elementos, editables uno por uno.
    if nivel_codigo is None and principio_numero is None and requisito_codigo is None:
        st.info(
            "👉 Elige un **Nivel de gestión** (o un principio/requisito) arriba para ver y "
            "editar todos sus elementos. Abajo, un resumen general por principio:"
        )
        conteo: dict = {}
        for v in verificaciones:
            clave = (v["nivel_codigo"], v["principio_numero"], v["principio_nombre"])
            d = conteo.setdefault(clave, {"total": 0, "pendientes": 0})
            d["total"] += 1
            if (v["nivel_cumplimiento"] or "No Iniciado") != "Cumplimiento Total":
                d["pendientes"] += 1
        df_resumen = pd.DataFrame([
            {"Nivel": k[0], "Principio": f"{k[1]}. {k[2]}", "Elementos": val["total"], "Pendientes": val["pendientes"]}
            for k, val in sorted(conteo.items(), key=lambda x: (x[0][0], x[0][1]))
        ])
        st.dataframe(df_resumen, width="stretch", hide_index=True)
        return

    # Con un Nivel (o principio/requisito) elegido: TODOS sus elementos
    # editables, agrupados por principio y requisito.
    st.caption(f"{len(verificaciones)} elemento(s) de verificación. Abre cada uno para editarlo.")
    requisito_actual = None
    principio_actual = None
    for v in verificaciones:
        if v["principio_numero"] != principio_actual:
            principio_actual = v["principio_numero"]
            st.markdown(f"### {v['nivel_codigo']} · Principio {v['principio_numero']}. {v['principio_nombre']}")
        if v["requisito_codigo"] != requisito_actual:
            requisito_actual = v["requisito_codigo"]
            st.markdown(f"##### Requisito {v['requisito_codigo']}")
            st.caption(v["requisito_cumplimiento"])
        nivel_cump_actual = v["nivel_cumplimiento"] or "No Iniciado"
        color = _COLOR_NIVEL_CUMPLIMIENTO.get(nivel_cump_actual, "#9CA3AF")
        texto = v["texto"] or ""
        etiqueta = f"{v['codigo']} · {nivel_cump_actual} — {texto[:80]}{'…' if len(texto) > 80 else ''}"
        with st.expander(etiqueta):
            st.markdown(f"<span style='color:{color}; font-weight:600;'>● {nivel_cump_actual}</span>",
                        unsafe_allow_html=True)
            if texto:
                st.write(texto)
            _formulario_verificacion(institucion_id, v)


# ---------------------------------------------------------------------------
# Evidencia extra (enlaces + archivos adjuntos) — almacenamiento propio y
# autocontenido, sin tocar crud_autodiagnostico.py. Se guarda en su propia
# tabla, por institución y verificación.
# ---------------------------------------------------------------------------

_EVIDENCIA_EXTRA_LISTA = False


def _asegurar_tabla_evidencia_extra() -> None:
    global _EVIDENCIA_EXTRA_LISTA
    if _EVIDENCIA_EXTRA_LISTA:
        return
    conn = db_mod.obtener_conexion()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS autodx_evidencia_extra (
                institucion_id INTEGER NOT NULL,
                verificacion_id INTEGER NOT NULL,
                enlace_actual TEXT,
                enlace_anterior TEXT,
                archivo_actual_nombre TEXT,
                archivo_actual_datos BLOB,
                archivo_anterior_nombre TEXT,
                archivo_anterior_datos BLOB,
                PRIMARY KEY (institucion_id, verificacion_id)
            )
            """
        )
        conn.commit()
        _EVIDENCIA_EXTRA_LISTA = True
    finally:
        conn.close()


def _leer_evidencia_extra(institucion_id: int, verificacion_id: int) -> dict:
    _asegurar_tabla_evidencia_extra()
    conn = db_mod.obtener_conexion()
    conn.row_factory = sqlite3.Row
    try:
        fila = conn.execute(
            "SELECT * FROM autodx_evidencia_extra WHERE institucion_id=? AND verificacion_id=?",
            (institucion_id, verificacion_id),
        ).fetchone()
        return dict(fila) if fila else {}
    finally:
        conn.close()


def _borrar_evidencia_extra(institucion_id: int, verificacion_id: int) -> None:
    """Elimina enlaces y archivos adjuntos de un elemento (usado por 'Limpiar')."""
    _asegurar_tabla_evidencia_extra()
    conn = db_mod.obtener_conexion()
    try:
        conn.execute(
            "DELETE FROM autodx_evidencia_extra WHERE institucion_id=? AND verificacion_id=?",
            (institucion_id, verificacion_id),
        )
        conn.commit()
    finally:
        conn.close()


def _guardar_evidencia_extra(institucion_id: int, verificacion_id: int,
                             enlace_actual: str, enlace_anterior: str,
                             archivo_actual, archivo_anterior) -> None:
    _asegurar_tabla_evidencia_extra()
    previo = _leer_evidencia_extra(institucion_id, verificacion_id)
    # Si suben un archivo nuevo, se reemplaza; si no, se conserva el anterior.
    if archivo_actual is not None:
        act_nombre, act_datos = archivo_actual.name, archivo_actual.getvalue()
    else:
        act_nombre, act_datos = previo.get("archivo_actual_nombre"), previo.get("archivo_actual_datos")
    if archivo_anterior is not None:
        ant_nombre, ant_datos = archivo_anterior.name, archivo_anterior.getvalue()
    else:
        ant_nombre, ant_datos = previo.get("archivo_anterior_nombre"), previo.get("archivo_anterior_datos")
    conn = db_mod.obtener_conexion()
    try:
        conn.execute(
            """
            INSERT INTO autodx_evidencia_extra
                (institucion_id, verificacion_id, enlace_actual, enlace_anterior,
                 archivo_actual_nombre, archivo_actual_datos,
                 archivo_anterior_nombre, archivo_anterior_datos)
            VALUES (?,?,?,?,?,?,?,?)
            ON CONFLICT(institucion_id, verificacion_id) DO UPDATE SET
                enlace_actual=excluded.enlace_actual,
                enlace_anterior=excluded.enlace_anterior,
                archivo_actual_nombre=excluded.archivo_actual_nombre,
                archivo_actual_datos=excluded.archivo_actual_datos,
                archivo_anterior_nombre=excluded.archivo_anterior_nombre,
                archivo_anterior_datos=excluded.archivo_anterior_datos
            """,
            (institucion_id, verificacion_id, (enlace_actual or None), (enlace_anterior or None),
             act_nombre, act_datos, ant_nombre, ant_datos),
        )
        conn.commit()
    finally:
        conn.close()


# Textos de ayuda (el signo ⓘ / "?" que aparece al lado de cada campo).
# Cada uno explica QUÉ poner y da un EJEMPLO.
_AYUDA = {
    "cumple": (
        "¿Tu institución cumple con este elemento?\n\n"
        "• **SI** = sí se cumple.\n"
        "• **NO** = no se cumple.\n"
        "• **N/A** = no aplica a tu institución.\n\n"
        "Ejemplo: si el elemento pide *'existe un decreto publicado'* y tu institución lo tiene, marca **SI**."
    ),
    "nivel": (
        "Qué tan avanzado está el cumplimiento de este elemento:\n\n"
        "• **No aplica** – no corresponde.\n"
        "• **No Iniciado** – aún no se ha empezado.\n"
        "• **Iniciado (1%–49%)** – ya comenzó.\n"
        "• **Cumplimiento Parcial (50%–99%)** – está a medias.\n"
        "• **Cumplimiento Total (100%)** – totalmente cumplido.\n\n"
        "Ejemplo: si ya lograste el 60% de lo requerido, marca **Cumplimiento Parcial**."
    ),
    "evid_act": (
        "Describe el documento o la prueba MÁS RECIENTE que respalda el cumplimiento de este elemento.\n\n"
        "Ejemplo: *'Decreto 123-2024 publicado en el portal de la ONE el 10/03/2024'.*"
    ),
    "link_act": (
        "Pega el enlace (SharePoint, Drive, sitio web) donde está la evidencia actual.\n\n"
        "Ejemplo: `https://drive.google.com/.../decreto123.pdf`"
    ),
    "file_act": (
        "Sube el archivo de la evidencia actual (PDF, imagen, Word o Excel). Máximo 10 MB.\n\n"
        "Ejemplo: el PDF del decreto o una foto del documento firmado."
    ),
    "evid_ant": (
        "Describe la evidencia de una revisión ANTERIOR, para comparar cómo ha avanzado en el tiempo.\n\n"
        "Ejemplo: *'En 2023 solo existía un borrador sin publicar'.*"
    ),
    "link_ant": (
        "Enlace de la evidencia anterior, si la tienes (SharePoint, Drive, web).\n\n"
        "Ejemplo: `https://drive.google.com/.../borrador2023.pdf`"
    ),
    "file_ant": (
        "Archivo de la evidencia anterior, si lo tienes (PDF, imagen, Word o Excel).\n\n"
        "Ejemplo: el PDF del borrador del año pasado."
    ),
    "coment": (
        "Cualquier aclaración o nota adicional sobre este elemento.\n\n"
        "Ejemplo: *'Pendiente de aprobación por el comité de calidad'.*"
    ),
    "accion": (
        "Qué se va a hacer para cumplir o mejorar este elemento.\n\n"
        "Ejemplo: *'Elaborar y publicar el decreto antes de junio 2025'.*"
    ),
    "resp": (
        "Persona o área responsable de este elemento.\n\n"
        "Ejemplo: *'Dirección de Normativas y Metodologías — Juan Pérez'.*"
    ),
    "fecha": (
        "Fecha en que se cumplió (o se espera cumplir) este elemento.\n\n"
        "Ejemplo: 30/06/2025."
    ),
}


def _formulario_verificacion(institucion_id: int, v: dict) -> None:
    usuario = st.session_state.get("usuario") or {}
    usuario_id = usuario.get("id")
    vid = v["verificacion_id"]
    extra = _leer_evidencia_extra(institucion_id, vid)
    with st.form(f"adx_form_{vid}"):
        c1, c2 = st.columns(2)
        with c1:
            cumple_actual = v["cumple"] or "N/A"
            cumple = st.selectbox("¿Cumple con el elemento?", crud_adx.OPCIONES_CUMPLE,
                                  index=crud_adx.OPCIONES_CUMPLE.index(cumple_actual) if cumple_actual in crud_adx.OPCIONES_CUMPLE else 2,
                                  key=f"adx_cumple_{vid}", help=_AYUDA["cumple"])
        with c2:
            nivel_cumplimiento = st.selectbox("Nivel de cumplimiento", _ORDEN_NIVEL_CUMPLIMIENTO,
                                              index=_ORDEN_NIVEL_CUMPLIMIENTO.index(v["nivel_cumplimiento"] or "No Iniciado"),
                                              key=f"adx_nivel_{vid}", help=_AYUDA["nivel"])

        # --- EVIDENCIA ACTUAL ---
        evidencia_actual = st.text_area("Evidencia actual", value=v["evidencia_actual"] or "",
                                        key=f"adx_evid_act_{vid}", help=_AYUDA["evid_act"])
        enlace_evidencia_actual = st.text_input(
            "Enlace / Link de evidencia actual (SharePoint, Drive, Web)",
            value=extra.get("enlace_actual") or v.get("enlace_evidencia_actual") or "",
            key=f"adx_link_act_{vid}", help=_AYUDA["link_act"])
        archivo_evidencia_actual = st.file_uploader(
            "Adjuntar foto/PDF/archivo de evidencia actual",
            type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx"], key=f"adx_file_act_{vid}",
            help=_AYUDA["file_act"])
        if extra.get("archivo_actual_nombre"):
            st.caption(f"📎 Archivo actual guardado: {extra['archivo_actual_nombre']} "
                       "(sube otro para reemplazarlo)")

        # --- EVIDENCIA ANTERIOR ---
        evidencia_anterior = st.text_area("Evidencia anterior", value=v["evidencia_anterior"] or "",
                                          key=f"adx_evid_ant_{vid}", help=_AYUDA["evid_ant"])
        enlace_evidencia_anterior = st.text_input(
            "Enlace / Link de evidencia anterior (SharePoint, Drive, Web)",
            value=extra.get("enlace_anterior") or v.get("enlace_evidencia_anterior") or "",
            key=f"adx_link_ant_{vid}", help=_AYUDA["link_ant"])
        archivo_evidencia_anterior = st.file_uploader(
            "Adjuntar foto/PDF/archivo de evidencia anterior",
            type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx"], key=f"adx_file_ant_{vid}",
            help=_AYUDA["file_ant"])
        if extra.get("archivo_anterior_nombre"):
            st.caption(f"📎 Archivo anterior guardado: {extra['archivo_anterior_nombre']} "
                       "(sube otro para reemplazarlo)")

        comentario = st.text_area("Comentario", value=v["comentario"] or "",
                                  key=f"adx_coment_{vid}", help=_AYUDA["coment"])
        accion_mejora = st.text_area("Acción de mejora", value=v["accion_mejora"] or "",
                                     key=f"adx_accion_{vid}", help=_AYUDA["accion"])
        c3, c4 = st.columns(2)
        with c3:
            responsable = st.text_input("Responsable", value=v["responsable"] or "",
                                        key=f"adx_resp_{vid}", help=_AYUDA["resp"])
        with c4:
            fecha_previa = None
            if v["fecha_cumplimiento"]:
                try:
                    fecha_previa = datetime.date.fromisoformat(v["fecha_cumplimiento"])
                except ValueError:
                    fecha_previa = None
            fecha_cumplimiento = st.date_input("Fecha de cumplimiento", value=fecha_previa,
                                               key=f"adx_fecha_{vid}", help=_AYUDA["fecha"])
        col_g, col_l = st.columns(2)
        with col_g:
            guardar = st.form_submit_button("💾 Guardar", width="stretch")
        with col_l:
            limpiar = st.form_submit_button("🗑️ Limpiar este elemento", width="stretch")

    # Botones de descarga de archivos ya guardados (fuera del formulario).
    if extra.get("archivo_actual_nombre") and extra.get("archivo_actual_datos") is not None:
        st.download_button(f"⬇️ Descargar evidencia actual ({extra['archivo_actual_nombre']})",
                           data=extra["archivo_actual_datos"], file_name=extra["archivo_actual_nombre"],
                           key=f"adx_dl_act_{vid}")
    if extra.get("archivo_anterior_nombre") and extra.get("archivo_anterior_datos") is not None:
        st.download_button(f"⬇️ Descargar evidencia anterior ({extra['archivo_anterior_nombre']})",
                           data=extra["archivo_anterior_datos"], file_name=extra["archivo_anterior_nombre"],
                           key=f"adx_dl_ant_{vid}")

    if guardar:
        ok, mensaje = crud_adx.guardar_evaluacion_verificacion(
            institucion_id=institucion_id, verificacion_id=vid, cumple=cumple,
            nivel_cumplimiento=nivel_cumplimiento, evidencia_actual=evidencia_actual,
            evidencia_anterior=evidencia_anterior, comentario=comentario, accion_mejora=accion_mejora,
            responsable=responsable,
            fecha_cumplimiento=fecha_cumplimiento.isoformat() if fecha_cumplimiento else None,
            usuario_id=usuario_id,
        )
        try:
            _guardar_evidencia_extra(institucion_id, vid, enlace_evidencia_actual,
                                     enlace_evidencia_anterior, archivo_evidencia_actual,
                                     archivo_evidencia_anterior)
            # Auditoría: registrar si se adjuntó/actualizó un archivo o enlace.
            partes = []
            if archivo_evidencia_actual is not None:
                partes.append(f"archivo actual '{archivo_evidencia_actual.name}'")
            if archivo_evidencia_anterior is not None:
                partes.append(f"archivo anterior '{archivo_evidencia_anterior.name}'")
            if (enlace_evidencia_actual or "").strip() != (extra.get("enlace_actual") or "").strip():
                partes.append("enlace actual")
            if (enlace_evidencia_anterior or "").strip() != (extra.get("enlace_anterior") or "").strip():
                partes.append("enlace anterior")
            if partes:
                from models.logs import registrar_log_standalone
                registrar_log_standalone(
                    usuario_id, "AUTODX_EVIDENCIA",
                    f"Inst {institucion_id} · '{v['codigo']}': adjuntó/actualizó " + ", ".join(partes) + ".")
        except Exception as exc:  # noqa: BLE001
            st.warning(f"Se guardó la evaluación, pero el enlace/archivo de evidencia no: {exc}")
        if ok:
            st.success(mensaje)
            st.rerun()
        else:
            st.error(mensaje)

    if limpiar:
        # Deja el elemento como "no llenado": ¿Cumple? vacío, Nivel 'No Iniciado'
        # y todos los campos en blanco; además borra enlaces y archivos.
        ok, mensaje = crud_adx.guardar_evaluacion_verificacion(
            institucion_id=institucion_id, verificacion_id=vid, cumple=None,
            nivel_cumplimiento="No Iniciado", evidencia_actual="", evidencia_anterior="",
            comentario="", accion_mejora="", responsable="", fecha_cumplimiento=None,
            usuario_id=usuario_id,
        )
        _borrar_evidencia_extra(institucion_id, vid)
        # Limpiar el estado de los widgets de este elemento para que se vean vacíos.
        for _k in (f"adx_cumple_{vid}", f"adx_nivel_{vid}", f"adx_evid_act_{vid}",
                   f"adx_link_act_{vid}", f"adx_file_act_{vid}", f"adx_evid_ant_{vid}",
                   f"adx_link_ant_{vid}", f"adx_file_ant_{vid}", f"adx_coment_{vid}",
                   f"adx_accion_{vid}", f"adx_resp_{vid}", f"adx_fecha_{vid}"):
            st.session_state.pop(_k, None)
        if ok:
            st.success("🗑️ Elemento limpiado (quedó sin llenar).")
            st.rerun()
        else:
            st.error(mensaje)


# ---------------------------------------------------------------------------
# Pestaña 2 — Estadísticas
# ---------------------------------------------------------------------------

def _tabla_resultados_formato_excel(resumen: dict) -> None:
    st.subheader("📄 Resultados — formato de la hoja del Excel")
    st.caption(
        "Conteo por principio de cada categoría y su puntaje, igual que la hoja RESULTADOS. "
        "'Faltantes' = elementos 'No aplica'. 'Total pautas' = elementos que sí aplican. "
        "Los puntajes son el % de elementos del principio en cada categoría."
    )
    filas = []
    puntaje_total_por_nivel: dict = {}
    for p in resumen["por_principio"]:
        total, parcial = p["total"], p["parcial"]
        iniciado, no_ini, no_aplica = p["iniciado"], p["no_iniciado"], p["no_aplica"]
        k = total + parcial + iniciado + no_ini

        def _pct(x):
            return round(x / k * 100, 1) if k else None

        pt_total, pt_parcial = _pct(total), _pct(parcial)
        pt_ini, pt_noini = _pct(iniciado), _pct(no_ini)
        total_pct = round((pt_total or 0) + (pt_parcial or 0) + (pt_ini or 0) + (pt_noini or 0), 1) if k else None
        filas.append({
            "Nivel": _LETRA_NIVEL.get(p["nivel_codigo"], p["nivel_codigo"]),
            "N°": p["principio_numero"], "Principio": p["principio_nombre"],
            "Total": total, "Parcial": parcial, "Iniciado": iniciado,
            "No Iniciado": no_ini, "Faltantes": no_aplica, "Total pautas": k,
            "Puntaje C. total": pt_total, "Puntaje C. Parcial": pt_parcial,
            "Puntaje Iniciado": pt_ini, "Puntaje No iniciado": pt_noini, "Total %": total_pct,
        })
        if k:
            puntaje_total_por_nivel.setdefault(p["nivel_codigo"], []).append(pt_total)
    st.dataframe(pd.DataFrame(filas), width="stretch", hide_index=True)

    filas_nivel = []
    for nivel in resumen["por_nivel"]:
        vals = puntaje_total_por_nivel.get(nivel["nivel_codigo"], [])
        punt = round(sum(vals) / len(vals), 1) if vals else None
        filas_nivel.append({
            "Nivel": _LETRA_NIVEL.get(nivel["nivel_codigo"], nivel["nivel_codigo"]),
            "Gestión": nivel["nivel_nombre"],
            "Puntaje (% en Cumplimiento Total)": f"{punt}%" if punt is not None else "—",
        })
    st.markdown("**Puntaje por nivel** — promedio del % de elementos en 'Cumplimiento Total'")
    st.dataframe(pd.DataFrame(filas_nivel), width="stretch", hide_index=True)


def _informe_completo(institucion_id: int):
    """Devuelve (xlsx_bytes, csv_bytes) con TODO lo llenado: Autodiagnóstico de
    los 3 niveles, Plan de acción y Estadísticas."""
    import io

    # 1) Autodiagnóstico — solo elementos llenados de los 3 niveles.
    todas = crud_adx.listar_verificaciones(institucion_id)
    extra = _leer_evidencia_extra_todos(institucion_id)
    filas_auto = []
    for v in todas:
        ex = extra.get(v["verificacion_id"], {})
        lleno = any([
            v["cumple"], (v["nivel_cumplimiento"] and v["nivel_cumplimiento"] != "No Iniciado"),
            v["evidencia_actual"], v["evidencia_anterior"], v["comentario"], v["accion_mejora"],
            v["responsable"], v["fecha_cumplimiento"], ex.get("enlace_actual"), ex.get("enlace_anterior"),
            ex.get("archivo_actual_nombre"), ex.get("archivo_anterior_nombre"),
        ])
        if not lleno:
            continue
        filas_auto.append({
            "Código": v["codigo"], "Nivel": v["nivel_codigo"],
            "Principio": f"{v['principio_numero']}. {v['principio_nombre']}",
            "Requisito": v["requisito_codigo"], "Elemento": v["texto"] or "",
            "¿Cumple?": v["cumple"] or "", "Nivel de cumplimiento": v["nivel_cumplimiento"] or "",
            "Evidencia actual": v["evidencia_actual"] or "", "Enlace actual": ex.get("enlace_actual") or "",
            "Archivo actual": ex.get("archivo_actual_nombre") or "",
            "Evidencia anterior": v["evidencia_anterior"] or "", "Enlace anterior": ex.get("enlace_anterior") or "",
            "Archivo anterior": ex.get("archivo_anterior_nombre") or "",
            "Comentario": v["comentario"] or "", "Acción de mejora": v["accion_mejora"] or "",
            "Responsable": v["responsable"] or "", "Fecha": v["fecha_cumplimiento"] or "",
        })
    df_auto = pd.DataFrame(filas_auto)

    # 2) Plan de acción.
    plan = crud_adx.listar_plan_accion(institucion_id)
    if plan:
        df_plan = pd.DataFrame(plan)[list(_ETIQUETAS_PLAN.keys())].rename(columns=_ETIQUETAS_PLAN)
    else:
        df_plan = pd.DataFrame(columns=list(_ETIQUETAS_PLAN.values()))

    # 3) Estadísticas (RESULTADOS) por principio + por nivel.
    resumen = crud_adx.calcular_resumen(institucion_id)
    df_stats = pd.DataFrame([{
        "Nivel": p["nivel_codigo"], "N°": p["principio_numero"], "Principio": p["principio_nombre"],
        "No aplica": p["no_aplica"], "No Iniciado": p["no_iniciado"], "Iniciado": p["iniciado"],
        "Cumpl. Parcial": p["parcial"], "Cumpl. Total": p["total"], "Elementos": p["total_elementos"],
        "% Cumplimiento": p["score"],
    } for p in resumen["por_principio"]])
    df_niv = pd.DataFrame([{"Nivel": n["nivel_codigo"], "Gestión": n["nivel_nombre"],
                            "% Cumplimiento": n["score"]} for n in resumen["por_nivel"]])
    df_niv = pd.concat([df_niv, pd.DataFrame([{"Nivel": "GENERAL", "Gestión": "Puntaje general",
                                               "% Cumplimiento": resumen["general"]}])], ignore_index=True)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        (df_auto if not df_auto.empty else pd.DataFrame([{"Aviso": "Sin elementos llenados todavía"}])
         ).to_excel(w, sheet_name="Autodiagnóstico", index=False)
        (df_plan if not df_plan.empty else pd.DataFrame([{"Aviso": "Sin plan de acción"}])
         ).to_excel(w, sheet_name="Plan de acción", index=False)
        df_stats.to_excel(w, sheet_name="Estadísticas", index=False)
        df_niv.to_excel(w, sheet_name="Puntaje por nivel", index=False)
        # Hoja "Diccionario de Datos": documenta las columnas de todas las
        # hojas anteriores (Lineamientos ONE para Diccionario de Datos Pasivo).
        try:
            from data.descripcion_campos import escribir_hoja_descripcion_campos
            escribir_hoja_descripcion_campos(w, {
                "Autodiagnóstico": df_auto if not df_auto.empty else None,
                "Plan de acción": df_plan if not df_plan.empty else None,
                "Estadísticas": df_stats,
                "Puntaje por nivel": df_niv,
            })
        except Exception:  # noqa: BLE001
            # El diccionario es complementario: si algo falla, el informe se
            # entrega igual con sus 4 hojas de datos.
            pass
    return buf.getvalue(), df_auto.to_csv(index=False).encode("utf-8-sig")


def _mostrar_estadisticas(institucion_id: int) -> None:
    resumen = crud_adx.calcular_resumen(institucion_id)
    if not resumen["por_principio"]:
        st.info("⚠️ No hay elementos cargados todavía.")
        return

    st.caption(
        "% de cumplimiento = Cumplimiento Total ÷ (elementos que aplican) × 100, igual que la hoja "
        "RESULTADOS del Excel (solo cuenta lo 100% cumplido; se excluye 'No aplica'). Promediado por "
        "principio y luego por nivel."
    )
    k0, k1, k2, k3 = st.columns(4)
    k0.metric("% General", f"{resumen['general']}%" if resumen["general"] is not None else "—")
    for col, nivel in zip((k1, k2, k3), resumen["por_nivel"]):
        col.metric(f"{nivel['nivel_codigo']} — {nivel['nivel_nombre']}",
                   f"{nivel['score']}%" if nivel["score"] is not None else "—")

    st.markdown("**📥 Descargar resultados**")
    d1, d2, _ = st.columns([1, 1, 2])
    with d1:
        try:
            st.download_button("📊 Excel (.xlsx)", data=crud_adx.exportar_resultados_excel(institucion_id),
                               file_name="Resultados_CNBPEO.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               width="stretch")
        except Exception as exc:  # noqa: BLE001
            st.caption(f"No se pudo generar el Excel: {exc}")
    with d2:
        try:
            st.download_button("📄 PDF", data=crud_adx.exportar_resultados_pdf(institucion_id),
                               file_name="Resultados_CNBPEO.pdf", mime="application/pdf", width="stretch")
        except Exception as exc:  # noqa: BLE001
            st.caption(f"No se pudo generar el PDF: {exc}")

    st.divider()
    st.markdown("### 📦 Informe completo (todo lo llenado)")
    st.caption(
        "Descarga en un solo archivo TODA la información registrada de esta institución: el "
        "Autodiagnóstico llenado de los 3 niveles (GEI/GPE/GRE), el Plan de acción y las Estadísticas. "
        "El Excel trae esas 3 secciones en hojas separadas."
    )
    try:
        xlsx_bytes, csv_bytes = _informe_completo(institucion_id)
        e1, e2, e3 = st.columns(3)
        e1.download_button("📗 Excel completo (.xlsx)", data=xlsx_bytes,
                           file_name="Informe_completo_CNBPEO.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           width="stretch", key="adx_inf_xlsx")
        e2.download_button("📄 CSV (lo llenado)", data=csv_bytes,
                           file_name="Informe_autodiagnostico_CNBPEO.csv", mime="text/csv",
                           width="stretch", key="adx_inf_csv")
        with e3:
            try:
                st.download_button("📕 Estadísticas en PDF",
                                   data=crud_adx.exportar_resultados_pdf(institucion_id),
                                   file_name="Estadisticas_CNBPEO.pdf", mime="application/pdf",
                                   width="stretch", key="adx_inf_pdf")
            except Exception as exc:  # noqa: BLE001
                st.caption(f"PDF no disponible: {exc}")
    except Exception as exc:  # noqa: BLE001
        st.error(f"No se pudo generar el informe completo: {exc}")

    st.divider()
    _tabla_resultados_formato_excel(resumen)

    st.divider()
    st.subheader("% de cumplimiento por principio")
    df_principios = pd.DataFrame(resumen["por_principio"])
    df_principios["etiqueta"] = (
        df_principios["nivel_codigo"] + " · " + df_principios["principio_numero"].astype(str)
        + ". " + df_principios["principio_nombre"]
    )
    df_plot = df_principios.dropna(subset=["score"]).sort_values("score")
    if df_plot.empty:
        st.info("Todos los principios tienen sus elementos marcados como 'No aplica'.")
    else:
        fig = px.bar(df_plot, x="score", y="etiqueta", orientation="h", color="score",
                     color_continuous_scale=_COLOR_SCORE_ESCALA, range_color=[0, 100], text="score",
                     labels={"score": "% cumplimiento", "etiqueta": ""})
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        _grafico_descargable(fig, "autodx_score_por_principio", alto=max(320, 34 * len(df_plot)))

    st.divider()
    st.subheader("Distribución de Nivel de Cumplimiento por nivel de gestión")
    filas_distrib = []
    for p in resumen["por_principio"]:
        for etiqueta, clave in zip(_ORDEN_NIVEL_CUMPLIMIENTO,
                                   ("no_aplica", "no_iniciado", "iniciado", "parcial", "total")):
            filas_distrib.append({"nivel_codigo": p["nivel_codigo"], "categoria": etiqueta, "cantidad": p[clave]})
    df_distrib = pd.DataFrame(filas_distrib).groupby(["nivel_codigo", "categoria"], as_index=False)["cantidad"].sum()
    col_a, col_b = st.columns(2)
    with col_a:
        fig2 = px.bar(df_distrib, x="nivel_codigo", y="cantidad", color="categoria",
                      category_orders={"categoria": _ORDEN_NIVEL_CUMPLIMIENTO},
                      color_discrete_map=_COLOR_NIVEL_CUMPLIMIENTO,
                      labels={"nivel_codigo": "Nivel", "cantidad": "Elementos", "categoria": "Nivel de cumplimiento"})
        _grafico_descargable(fig2, "autodx_distribucion_por_nivel")
    with col_b:
        df_general = df_distrib.groupby("categoria", as_index=False)["cantidad"].sum()
        fig3 = px.pie(df_general, values="cantidad", names="categoria",
                      category_orders={"categoria": _ORDEN_NIVEL_CUMPLIMIENTO}, color="categoria",
                      color_discrete_map=_COLOR_NIVEL_CUMPLIMIENTO, hole=0.4)
        fig3.update_traces(textinfo="percent+label")
        _grafico_descargable(fig3, "autodx_distribucion_general")

    st.divider()
    st.subheader("Detalle por principio")
    tabla = df_principios[[
        "nivel_codigo", "principio_numero", "principio_nombre",
        "no_aplica", "no_iniciado", "iniciado", "parcial", "total", "total_elementos", "score",
    ]].rename(columns={
        "nivel_codigo": "Nivel", "principio_numero": "N°", "principio_nombre": "Principio",
        "no_aplica": "No aplica", "no_iniciado": "No Iniciado", "iniciado": "Iniciado",
        "parcial": "Cumpl. Parcial", "total": "Cumpl. Total", "total_elementos": "Elementos",
        "score": "% Cumplimiento",
    })
    st.dataframe(tabla, width="stretch", hide_index=True)


# ---------------------------------------------------------------------------
# Pestaña 3 — Plan de acción (por institución)
# ---------------------------------------------------------------------------

_ETIQUETAS_PLAN = {
    "requerimiento": "Requerimiento", "accion_mejora": "Acción de mejora",
    "actividades": "Actividades", "insumo": "Insumo", "presupuesto": "Presupuesto",
    "fecha_cumplimiento": "Fecha de cumplimiento", "responsable": "Responsable",
    "indicador_verificable": "Indicador verificable", "riesgo": "Riesgo",
    "acciones_mitigacion": "Acciones de mitigación", "observaciones": "Observaciones",
}


def _campos_plan_form(prefijo: str, valores: dict) -> dict:
    datos = {}
    c1, c2 = st.columns(2)
    with c1:
        datos["requerimiento"] = st.text_area("Requerimiento", value=valores.get("requerimiento") or "", key=f"{prefijo}_req",
            help="Qué se necesita cumplir o mejorar.\n\nEjemplo: 'GEI-1.1.1 — Encuesta para medir la cultura profesional'.")
        datos["actividades"] = st.text_area("Actividades", value=valores.get("actividades") or "", key=f"{prefijo}_act",
            help="Actividades para lograr el requerimiento (una por línea).\n\nEjemplo: 'Definir preguntas / Aplicar encuesta / Analizar resultados'.")
        datos["insumo"] = st.text_input("Insumo", value=valores.get("insumo") or "", key=f"{prefijo}_ins",
            help="Recursos necesarios.\n\nEjemplo: 'Cuestionario, plataforma de recolección'.")
        datos["presupuesto"] = st.text_input("Presupuesto", value=valores.get("presupuesto") or "", key=f"{prefijo}_pre",
            help="Monto estimado, o 'N/A' si no aplica.\n\nEjemplo: 'RD$ 50,000' o 'N/A'.")
        datos["responsable"] = st.text_input("Responsable", value=valores.get("responsable") or "", key=f"{prefijo}_resp",
            help="Persona o área responsable.\n\nEjemplo: 'Dirección de Normativas — Juan Pérez'.")
    with c2:
        datos["accion_mejora"] = st.text_area("Acción de mejora", value=valores.get("accion_mejora") or "", key=f"{prefijo}_acc",
            help="Qué se va a hacer para cumplir el requerimiento.\n\nEjemplo: 'Diseñar y aplicar la encuesta de cultura profesional'.")
        datos["indicador_verificable"] = st.text_area("Indicador verificable", value=valores.get("indicador_verificable") or "", key=f"{prefijo}_ind",
            help="Cómo se comprobará que se cumplió.\n\nEjemplo: 'Informe con los resultados de la encuesta'.")
        datos["riesgo"] = st.text_area("Riesgo", value=valores.get("riesgo") or "", key=f"{prefijo}_rie",
            help="Qué podría impedir el cumplimiento.\n\nEjemplo: 'Baja participación del personal'.")
        datos["acciones_mitigacion"] = st.text_area("Acciones de mitigación", value=valores.get("acciones_mitigacion") or "", key=f"{prefijo}_mit",
            help="Qué se hará para reducir el riesgo.\n\nEjemplo: 'Recordatorios por correo y apoyo de las jefaturas'.")
    # Fecha con CALENDARIO (antes era texto libre donde se podía escribir
    # cualquier cosa). Se intenta interpretar el valor guardado para
    # preseleccionarlo; si el valor viejo no es una fecha válida, arranca vacío.
    _fecha_prev = None
    _val_fecha = (valores.get("fecha_cumplimiento") or "").strip()
    if _val_fecha:
        for _fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%Y/%m/%d"):
            try:
                _fecha_prev = datetime.datetime.strptime(_val_fecha, _fmt).date()
                break
            except ValueError:
                continue
    _fecha_sel = st.date_input("Fecha de cumplimiento", value=_fecha_prev,
                               key=f"{prefijo}_fec", format="DD/MM/YYYY",
                               help="Fecha en que se espera cumplir el requerimiento. Elígela en el calendario.")
    datos["fecha_cumplimiento"] = _fecha_sel.strftime("%d/%m/%Y") if _fecha_sel else ""
    datos["observaciones"] = st.text_area("Observaciones", value=valores.get("observaciones") or "", key=f"{prefijo}_obs",
        help="Notas o aclaraciones adicionales del plan.\n\nEjemplo: 'Pendiente de aprobación por el comité'.")
    return datos


def _mostrar_plan_accion(institucion_id: int) -> None:
    usuario = st.session_state.get("usuario") or {}
    usuario_id = usuario.get("id")
    puede_editar = usuario.get("rol") in ("editor", "supervisor", "administrador")

    st.subheader("📋 Plan de Acción de Implementación")
    st.caption(
        "Acciones de mejora derivadas del autodiagnóstico de esta institución. Equivale a la hoja "
        "'Plan de acción' del Excel."
    )
    filas = crud_adx.listar_plan_accion(institucion_id)
    if filas:
        import html as _html
        # Tabla que muestra TODO el contenido de cada celda (varias líneas),
        # sin cortar — cada requerimiento con todas sus actividades/responsables.
        thead = "<tr>" + "".join(f"<th>{_html.escape(c)}</th>" for c in _ETIQUETAS_PLAN.values()) + "</tr>"
        filas_html = []
        for fila in filas:
            tds = []
            for k in _ETIQUETAS_PLAN.keys():
                v = fila.get(k)
                celda = _html.escape(str(v)).replace("\n", "<br>") if v not in (None, "") else ""
                tds.append(f"<td>{celda}</td>")
            filas_html.append("<tr>" + "".join(tds) + "</tr>")
        st.markdown(
            "<style>"
            "#cn-plan{border-collapse:collapse;width:100%;font-size:.8rem;color:#e8edf5}"
            "#cn-plan td,#cn-plan th{border:1px solid rgba(95,175,255,.28);padding:6px 9px;"
            "text-align:left;vertical-align:top;white-space:pre-wrap;word-break:break-word;min-width:130px}"
            # Encabezados del Plan en UNA sola línea (negrita), aunque el
            # contenido de las celdas de abajo sí conserve sus saltos de línea.
            "#cn-plan thead th{position:sticky;top:0;background:#12305f;color:#cfe0ff;"
            "white-space:nowrap;vertical-align:middle;font-weight:700;padding:8px 12px}"
            "#cn-plan tbody tr:nth-child(even){background:rgba(18,48,95,.35)}"
            "</style>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='overflow:auto;max-height:600px;border:1px solid rgba(95,175,255,.4);"
            "border-radius:10px'><table id='cn-plan'>"
            f"<thead>{thead}</thead><tbody>{''.join(filas_html)}</tbody></table></div>",
            unsafe_allow_html=True,
        )
        # Descargar la tabla del plan (Excel y CSV).
        import io as _io
        df_plan_dl = pd.DataFrame(filas)[list(_ETIQUETAS_PLAN.keys())].rename(columns=_ETIQUETAS_PLAN)
        pb1, pb2, _pbsp = st.columns([1, 1, 3])
        _buf = _io.BytesIO()
        with pd.ExcelWriter(_buf, engine="openpyxl") as _w:
            df_plan_dl.to_excel(_w, sheet_name="Plan de acción", index=False)
        pb1.download_button("📗 Descargar plan (Excel)", data=_buf.getvalue(),
                            file_name="Plan_de_accion_CNBPEO.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            width="stretch", key="adx_plan_dl_xlsx")
        pb2.download_button("📄 Descargar plan (CSV)",
                            data=df_plan_dl.to_csv(index=False).encode("utf-8-sig"),
                            file_name="Plan_de_accion_CNBPEO.csv", mime="text/csv",
                            width="stretch", key="adx_plan_dl_csv")
    else:
        st.info("Todavía no hay filas en el plan de acción de esta institución.")

    if not puede_editar:
        return

    with st.expander("➕ Agregar una fila al plan", expanded=not filas):
        with st.form("adx_plan_nueva"):
            datos = _campos_plan_form("adx_plan_new", {})
            if st.form_submit_button("➕ Agregar"):
                if not (datos["requerimiento"] or datos["accion_mejora"] or datos["actividades"]):
                    st.warning("Escribe al menos el requerimiento, la acción de mejora o las actividades.")
                else:
                    ok, msg = crud_adx.guardar_fila_plan(institucion_id, datos, None, usuario_id)
                    (st.success if ok else st.error)(msg)
                    if ok:
                        st.rerun()

    if filas:
        st.divider()
        st.markdown("**Editar o eliminar filas existentes**")
        for fila in filas:
            titulo = (fila.get("requerimiento") or fila.get("accion_mejora") or f"Fila {fila['id']}")[:70]
            with st.expander(f"✏️ {titulo}"):
                with st.form(f"adx_plan_edit_{fila['id']}"):
                    datos = _campos_plan_form(f"adx_plan_e{fila['id']}", fila)
                    ce1, ce2 = st.columns(2)
                    guardar = ce1.form_submit_button("💾 Guardar cambios")
                    eliminar = ce2.form_submit_button("🗑️ Eliminar fila")
                if guardar:
                    ok, msg = crud_adx.guardar_fila_plan(institucion_id, datos, fila["id"], usuario_id)
                    (st.success if ok else st.error)(msg)
                    if ok:
                        st.rerun()
                if eliminar:
                    ok, msg = crud_adx.eliminar_fila_plan(institucion_id, fila["id"], usuario_id)
                    (st.success if ok else st.error)(msg)
                    if ok:
                        st.rerun()


# ---------------------------------------------------------------------------
# Pestaña 4 — Seguimiento (por institución)
# ---------------------------------------------------------------------------

_ORDINALES_SEG = ["1er", "2do", "3er", "4to", "5to", "6to", "7mo", "8vo", "9no", "10mo",
                  "11º", "12º", "13º", "14º", "15º"]


def _etiquetas_unicas_seguimiento(seguimientos: list[dict]) -> dict[int, str]:
    """Devuelve {id_seguimiento: etiqueta única} para usar como columnas sin
    colisiones aunque dos cortes tengan el mismo nombre (esto era lo que
    reventaba la tabla comparativa con 'Duplicate column names')."""
    conteo_nombre: dict[str, int] = {}
    for s in seguimientos:
        conteo_nombre[s["nombre"]] = conteo_nombre.get(s["nombre"], 0) + 1
    usadas: set[str] = set()
    etiq: dict[int, str] = {}
    for s in seguimientos:
        base = s["nombre"]
        # Si el nombre se repite, se le agrega la fecha para distinguirlos.
        lbl = base if conteo_nombre[base] == 1 else f"{base} · {str(s.get('fecha_snapshot') or '')[:10]}"
        # Garantía final de unicidad (por si nombre+fecha también coinciden).
        if lbl in usadas:
            lbl = f"{lbl} (#{s['id']})"
        usadas.add(lbl)
        etiq[s["id"]] = lbl
    return etiq


def _mostrar_seguimiento(institucion_id: int) -> None:
    import io

    usuario = st.session_state.get("usuario") or {}
    usuario_id = usuario.get("id")
    puede_gestionar = usuario.get("rol") in ("supervisor", "administrador")

    st.subheader("📈 Seguimiento — evolución del cumplimiento en el tiempo")
    st.caption(
        "Registra un 'corte' del cumplimiento actual de esta institución con un nombre "
        "(ej. '1er Resultado', '2do Resultado') para comparar cómo evoluciona en el tiempo."
    )

    seguimientos = crud_adx.listar_seguimientos(institucion_id)
    n_existentes = len(seguimientos)
    # Nombre sugerido automático: el siguiente número. Al registrar un corte,
    # la app hace rerun, este número avanza (1er → 2do → 3er…) y el campo se
    # reinicia solo con el nuevo valor sugerido.
    sugerido = (f"{_ORDINALES_SEG[n_existentes]} Resultado"
                if n_existentes < len(_ORDINALES_SEG) else f"Resultado {n_existentes + 1}")

    if puede_gestionar:
        with st.form("adx_seg_nuevo", clear_on_submit=True):
            c1, c2 = st.columns([1, 2])
            nombre = c1.text_input("Nombre del seguimiento", value=sugerido,
                                   key=f"adx_seg_nombre_{n_existentes}")
            descripcion = c2.text_input("Descripción (opcional)", key=f"adx_seg_desc_{n_existentes}")
            if st.form_submit_button("💾 Registrar corte actual", type="primary"):
                ok, msg = crud_adx.guardar_seguimiento(institucion_id, nombre, descripcion, usuario_id)
                (st.success if ok else st.error)(msg)
                if ok:
                    st.rerun()
    else:
        st.info("Solo supervisores y administradores pueden registrar o eliminar cortes.")

    if not seguimientos:
        st.info("Todavía no hay cortes registrados para esta institución. Registra el primero arriba.")
        return

    # Etiqueta única por corte (evita el error de columnas duplicadas).
    etiq = _etiquetas_unicas_seguimiento(seguimientos)

    st.divider()
    # ── Filtro: elegir qué cortes comparar ──────────────────────────────
    opciones = [etiq[s["id"]] for s in seguimientos]
    sel = st.multiselect("🔎 Filtrar cortes a comparar", opciones, default=opciones,
                         key="adx_seg_filtro")
    ids_sel = {sid for sid, lbl in etiq.items() if lbl in sel}
    segs_sel = [s for s in seguimientos if s["id"] in ids_sel]
    if not segs_sel:
        st.info("Selecciona al menos un corte en el filtro de arriba.")
        return

    # ── Gráfico: % General por corte ────────────────────────────────────
    st.markdown("**% General por corte**")
    df_gen = pd.DataFrame([{"Corte": etiq[s["id"]], "% General": s["general"] or 0,
                            "Fecha": s["fecha_snapshot"]} for s in segs_sel])
    fig = px.line(df_gen, x="Corte", y="% General", markers=True, range_y=[0, 100], text="% General")
    fig.update_traces(textposition="top center")
    _grafico_descargable(fig, "autodx_seguimiento_general")

    # ── Tabla comparativa por principio ─────────────────────────────────
    detalle = [d for d in crud_adx.obtener_detalle_seguimientos(institucion_id)
               if d["seguimiento_id"] in ids_sel]
    pivote = None
    if detalle:
        df_det = pd.DataFrame(detalle)
        df_det["Corte"] = df_det["seguimiento_id"].map(etiq)
        df_det["Principio"] = (df_det["nivel_codigo"] + " · "
                               + df_det["principio_numero"].astype(str) + ". "
                               + df_det["principio_nombre"])
        pivote = df_det.pivot_table(index="Principio", columns="Corte", values="score", aggfunc="first")
        orden_cols = [etiq[s["id"]] for s in segs_sel if etiq[s["id"]] in pivote.columns]
        pivote = pivote[orden_cols]
        st.markdown("**% de cumplimiento por principio, comparado entre cortes**")
        st.dataframe(pivote, width="stretch")

    # ── Botón: generar / descargar el seguimiento en Excel ──────────────
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_gen.to_excel(w, sheet_name="% General", index=False)
        if pivote is not None:
            pivote.reset_index().to_excel(w, sheet_name="Por principio", index=False)
    st.download_button("📥 Generar seguimiento (Excel)", data=buf.getvalue(),
                       file_name="Seguimiento_CNBPEO.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       key="adx_seg_generar", width="stretch")

    if puede_gestionar:
        st.divider()
        st.markdown("**Eliminar un corte**")
        for s in seguimientos:
            c1, c2 = st.columns([4, 1])
            c1.write(f"**{etiq[s['id']]}** — {s['fecha_snapshot']} · General: {s['general']}%")
            if c2.button("🗑️ Eliminar", key=f"adx_seg_del_{s['id']}"):
                ok, msg = crud_adx.eliminar_seguimiento(institucion_id, s["id"], usuario_id)
                (st.success if ok else st.error)(msg)
                if ok:
                    st.rerun()


# ---------------------------------------------------------------------------
# Pestaña 5 — Excel automático (por institución)
# ---------------------------------------------------------------------------

_COLUMNAS_IMPORT = ["codigo", "texto", "cumple", "nivel_cumplimiento", "evidencia_actual",
                    "evidencia_anterior", "comentario", "accion_mejora", "responsable", "fecha_cumplimiento"]

_ALIAS_IMPORT = {
    "codigo": "codigo", "code": "codigo", "cod": "codigo",
    "cumple": "cumple", "cumple_con_el_elemento": "cumple",
    "nivel_de_cumplimiento": "nivel_cumplimiento", "nivel_cumplimiento": "nivel_cumplimiento", "nivel": "nivel_cumplimiento",
    "evidencia_actual": "evidencia_actual", "evidencia": "evidencia_actual",
    "evidencia_anterior": "evidencia_anterior",
    "comentario": "comentario", "comentarios": "comentario",
    "accion_de_mejora": "accion_mejora", "accion_mejora": "accion_mejora",
    "responsable": "responsable",
    "fecha_de_cumplimiento": "fecha_cumplimiento", "fecha_cumplimiento": "fecha_cumplimiento", "fecha": "fecha_cumplimiento",
}
_MAP_CUMPLE = {"si": "SI", "sí": "SI", "s": "SI", "no": "NO", "n": "NO",
               "n/a": "N/A", "na": "N/A", "no_aplica": "N/A", "no aplica": "N/A"}
_MAP_NIVEL = {"no aplica": "No aplica", "no_aplica": "No aplica", "no iniciado": "No Iniciado",
              "no_iniciado": "No Iniciado", "iniciado": "Iniciado",
              "cumplimiento parcial": "Cumplimiento Parcial", "parcial": "Cumplimiento Parcial",
              "cumplimiento total": "Cumplimiento Total", "total": "Cumplimiento Total"}


def _norm_clave_import(s) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode("ascii").lower().strip()
    for ch in " ¿?¡!.-/":
        s = s.replace(ch, "_")
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def _borrar_evaluaciones_institucion(institucion_id: int) -> None:
    """Borra todas las evaluaciones de una institución (para 'sobrescribir')."""
    conn = db_mod.obtener_conexion()
    try:
        conn.execute("DELETE FROM autodx_evaluaciones_inst WHERE institucion_id=?", (institucion_id,))
        conn.commit()
    finally:
        conn.close()
    try:
        crud_adx._invalidar_cache_evaluaciones()  # noqa: SLF001
    except Exception:  # noqa: BLE001
        pass


def _mostrar_importar(institucion_id: int) -> None:
    import io
    import json

    usuario = st.session_state.get("usuario") or {}
    es_admin = usuario.get("rol") in ("administrador", "supervisor")

    st.subheader("📤 Cargar datos por archivo (CSV, JSON o Excel)")
    st.caption(
        "Sube un archivo **CSV**, **JSON** o **Excel (.xlsx)** con la información ya llenada y se carga de "
        "una vez en la institución seleccionada arriba: se actualizan las variables (¿Cumple?, Nivel de "
        "cumplimiento, evidencias, comentario, acción, responsable y fecha) y los cuadros/estadísticas se "
        "recalculan solos. El archivo debe tener una columna **codigo** (ej. GEI-1.1.1). Las evidencias "
        "con archivo o enlace las subes tú a mano después."
    )

    actuales = crud_adx.listar_verificaciones(institucion_id)

    if not es_admin:
        st.info("Solo un supervisor o administrador puede cargar datos por archivo.")
        return

    archivo = st.file_uploader("Sube tu archivo CSV, JSON o Excel (.xlsx)",
                               type=["csv", "json", "xlsx"], key="adx_csvjson")
    if archivo is None:
        return

    contenido = archivo.getvalue()
    nombre = archivo.name.lower()

    sobrescribir = st.checkbox(
        "🔁 Sobrescribir: borrar lo que ya tiene esta institución antes de cargar "
        "(deja solo lo que traiga el archivo)", key="adx_sobrescribir")

    # ── Excel = Herramienta oficial (Matriz con hojas GEI / GPE / GRE) ──
    # Se lee con el importador de la Matriz: carga las variables de los 3
    # niveles y también el Plan de acción que traiga el archivo.
    if nombre.endswith(".xlsx"):
        try:
            okp, msgp, resp = crud_adx.previsualizar_importacion(contenido)
        except Exception:  # noqa: BLE001
            okp, msgp, resp = False, "", {}
        if okp and resp.get("con_datos"):
            st.success(f"📘 Herramienta (Matriz GEI/GPE/GRE) reconocida. {msgp}")
            no_rec_x = resp.get("no_reconocidos") or []
            if no_rec_x:
                st.warning(f"{len(no_rec_x)} código(s) del archivo no coinciden con las 252 "
                           "verificaciones y se ignorarán.")
            df_prev_x = pd.DataFrame([{
                "Código": el["codigo"], "¿Cumple?": el.get("cumple") or "—",
                "Nivel de cumplimiento": el.get("nivel") or "(sin cambio)",
            } for el in resp["con_datos"]])
            with st.expander(f"Ver las {len(resp['con_datos'])} verificaciones que se cargarán", expanded=True):
                st.dataframe(df_prev_x, width="stretch", hide_index=True)
            st.caption("Se cargan las variables de los 3 niveles (GEI/GPE/GRE) y el Plan de acción que "
                       "traiga el archivo. Las evidencias con archivo o enlace las subes tú a mano después.")
            if st.button("📥 Cargar Herramienta y actualizar todo", type="primary", key="adx_cargar_matriz"):
                if sobrescribir:
                    _borrar_evaluaciones_institucion(institucion_id)
                ok_i, msg_i, _ = crud_adx.importar_desde_excel(
                    institucion_id, contenido, archivo.name, usuario.get("id"))
                if ok_i:
                    st.success(f"✅ {msg_i} Las estadísticas y los cuadros ya se actualizaron.")
                    st.rerun()
                else:
                    st.error(msg_i)
            return
        # Si el .xlsx no es la Matriz oficial, se intenta como tabla simple abajo.

    registros = []
    try:
        if nombre.endswith(".json"):
            data = json.loads(contenido.decode("utf-8-sig", errors="replace"))
            if isinstance(data, dict):
                if "datos" in data or "data" in data:
                    registros = data.get("datos") or data.get("data") or []
                else:
                    registros = [{"codigo": k, **(vv if isinstance(vv, dict) else {})} for k, vv in data.items()]
            elif isinstance(data, list):
                registros = data
        elif nombre.endswith(".xlsx"):
            hojas = pd.read_excel(io.BytesIO(contenido), sheet_name=None)
            frames = [d for d in hojas.values() if not d.empty]
            if frames:
                registros = pd.concat(frames, ignore_index=True).to_dict("records")
        else:
            try:
                df = pd.read_csv(io.BytesIO(contenido))
            except Exception:  # noqa: BLE001
                df = pd.read_csv(io.BytesIO(contenido), encoding="latin-1", sep=None, engine="python")
            registros = df.to_dict("records")
    except Exception as exc:  # noqa: BLE001
        st.error(f"No se pudo leer el archivo: {exc}")
        return

    if not registros:
        st.warning("El archivo no trae registros.")
        return

    def _txt(x):
        if x is None:
            return None
        s = str(x).strip()
        return None if s.lower() in ("", "nan", "none") else s

    actuales_por_cod = {v["codigo"]: v for v in actuales}
    preparados, no_rec = [], []
    for r in registros:
        campos = {}
        for k, val in (r.items() if isinstance(r, dict) else []):
            nk = _norm_clave_import(k)
            if nk in _ALIAS_IMPORT:
                campos[_ALIAS_IMPORT[nk]] = val
        cod = str(campos.get("codigo") or "").strip()
        if not cod:
            continue
        v = actuales_por_cod.get(cod)
        if not v:
            no_rec.append(cod)
            continue
        cumple_raw = _txt(campos.get("cumple"))
        nivel_raw = _txt(campos.get("nivel_cumplimiento"))
        if sobrescribir:
            cumple = _MAP_CUMPLE.get(cumple_raw.lower()) if cumple_raw else None
            nivel = _MAP_NIVEL.get(nivel_raw.lower()) if nivel_raw else "No Iniciado"
            preparados.append({
                "codigo": cod, "vid": v["verificacion_id"], "cumple": cumple, "nivel": nivel,
                "evidencia_actual": _txt(campos.get("evidencia_actual")) or "",
                "evidencia_anterior": _txt(campos.get("evidencia_anterior")) or "",
                "comentario": _txt(campos.get("comentario")) or "",
                "accion_mejora": _txt(campos.get("accion_mejora")) or "",
                "responsable": _txt(campos.get("responsable")) or "",
                "fecha": _txt(campos.get("fecha_cumplimiento")),
            })
        else:
            cumple = _MAP_CUMPLE.get(cumple_raw.lower()) if cumple_raw else (v["cumple"] or None)
            nivel = _MAP_NIVEL.get(nivel_raw.lower()) if nivel_raw else (v["nivel_cumplimiento"] or "No Iniciado")
            preparados.append({
                "codigo": cod, "vid": v["verificacion_id"], "cumple": cumple, "nivel": nivel,
                "evidencia_actual": _txt(campos.get("evidencia_actual")) or (v["evidencia_actual"] or ""),
                "evidencia_anterior": _txt(campos.get("evidencia_anterior")) or (v["evidencia_anterior"] or ""),
                "comentario": _txt(campos.get("comentario")) or (v["comentario"] or ""),
                "accion_mejora": _txt(campos.get("accion_mejora")) or (v["accion_mejora"] or ""),
                "responsable": _txt(campos.get("responsable")) or (v["responsable"] or ""),
                "fecha": _txt(campos.get("fecha_cumplimiento")) or (v["fecha_cumplimiento"] or None),
            })

    if no_rec:
        st.warning(f"{len(no_rec)} código(s) no coinciden con las 252 verificaciones y se ignorarán: "
                   + ", ".join(no_rec[:15]) + ("…" if len(no_rec) > 15 else ""))
    if not preparados:
        st.error("No se reconoció ningún elemento válido. Revisa que exista la columna **codigo** "
                 "con códigos como GEI-1.1.1.")
        return

    st.success(f"✅ {len(preparados)} elemento(s) listos para cargar en esta institución.")
    df_prev = pd.DataFrame([{
        "Código": p["codigo"], "¿Cumple?": p["cumple"] or "—", "Nivel de cumplimiento": p["nivel"],
        "Evidencia": "Sí" if (p["evidencia_actual"] or p["evidencia_anterior"]) else "No",
        "Responsable": p["responsable"],
    } for p in preparados])
    with st.expander(f"Ver los {len(preparados)} elementos que se van a cargar", expanded=True):
        st.dataframe(df_prev, width="stretch", hide_index=True)

    if st.button("📥 Cargar y actualizar todo", type="primary", key="adx_cargar_csvjson"):
        if sobrescribir:
            _borrar_evaluaciones_institucion(institucion_id)
        n_ok, errores = 0, []
        for p in preparados:
            ok, msg = crud_adx.guardar_evaluacion_verificacion(
                institucion_id=institucion_id, verificacion_id=p["vid"], cumple=p["cumple"],
                nivel_cumplimiento=p["nivel"], evidencia_actual=p["evidencia_actual"],
                evidencia_anterior=p["evidencia_anterior"], comentario=p["comentario"],
                accion_mejora=p["accion_mejora"], responsable=p["responsable"],
                fecha_cumplimiento=p["fecha"], usuario_id=usuario.get("id"),
            )
            if ok:
                n_ok += 1
            else:
                errores.append(f"{p['codigo']}: {msg}")
        if errores:
            st.error("Algunos no se cargaron:\n\n- " + "\n- ".join(errores[:10]))
        st.success(f"✅ {n_ok} elemento(s) cargados. Las estadísticas y los cuadros ya se actualizaron.")
        st.rerun()
