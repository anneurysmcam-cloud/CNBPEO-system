"""
views/material_apoyo.py
=======================
Material de apoyo del Autodiagnóstico, organizado como la biblioteca de
documentos de la ONE: categorías desplegables, cada una con sus documentos
(subidos por el admin y guardados en la BD) y opción de subir nuevos. Incluye
enlaces de referencia del Código Nacional de Buenas Prácticas (CNBPEO).
"""

import streamlit as st

from models import crud_autodiagnostico as crud_adx

# Categorías, en el mismo orden que el portal de la ONE. La primera es la del
# Código y su Herramienta de Autodiagnóstico (Excel).
_CATEGORIAS = [
    "Código Nacional de Buenas Prácticas y sus Herramientas de Aplicación",
    "Lineamientos a Implementar para la Mejora de la Producción Estadística",
    "Guías",
    "Manuales Metodológicos para las Operaciones Estadísticas",
    "Otros documentos",
]

_ENLACES_REFERENCIA = [
    ("Calidad de la producción estadística — Oficina Nacional de Estadística (ONE)",
     "Página oficial de la ONE sobre la calidad de la producción estadística.",
     "https://www.one.gob.do/datos-y-estadisticas/temas/cuestiones-estrategicas-y-de-gestion-de-las-estadisticas-oficiales/calidad-de-la-produccion-estadistica/"),
    ("Principios Fundamentales de las Estadísticas Oficiales (ONU)",
     "Marco internacional que rige la producción de estadísticas oficiales.",
     "https://unstats.un.org/unsd/dnss/gp/fundprinciples.aspx"),
    ("Código Regional de Buenas Prácticas en Estadísticas (CEPAL)",
     "Base regional sobre la que se adapta el Código Nacional.",
     "https://www.cepal.org/es/publicaciones/codigo-regional-buenas-practicas-estadisticas-america-latina-caribe"),
]


def _icono(nombre_archivo: str, mime: str | None) -> str:
    ext = (nombre_archivo.rsplit(".", 1)[-1].lower() if "." in nombre_archivo else "")
    if ext == "pdf":
        return "📕"
    if ext in ("xls", "xlsx", "csv"):
        return "📗"
    if ext in ("doc", "docx"):
        return "📘"
    if ext in ("ppt", "pptx"):
        return "📙"
    if ext in ("png", "jpg", "jpeg", "gif"):
        return "🖼️"
    return "📄"


def _tamano(bytes_: int | None) -> str:
    if not bytes_:
        return "—"
    if bytes_ >= 1024 * 1024:
        return f"{bytes_ / (1024*1024):.1f} MB"
    return f"{bytes_ / 1024:.0f} KB"


def _render_documento(doc: dict, es_admin: bool, usuario_id) -> None:
    c1, c2, c3 = st.columns([6, 1.4, 0.8])
    with c1:
        contenido = crud_adx.obtener_material(doc["id"])
        st.markdown(f"{_icono(doc['nombre_archivo'], doc.get('mime'))}  **{doc['titulo']}**")
        st.caption(f"Subido: {doc.get('fecha_subida') or '—'} · {_tamano(doc.get('tamano'))} · {doc['nombre_archivo']}")
    with c2:
        if contenido:
            st.download_button("⬇️ Descargar", data=contenido["contenido"],
                               file_name=doc["nombre_archivo"],
                               mime=doc.get("mime") or "application/octet-stream",
                               key=f"mat_dl_{doc['id']}", width="stretch")
    with c3:
        if es_admin and st.button("🗑️", key=f"mat_del_{doc['id']}", help="Eliminar"):
            ok, msg = crud_adx.eliminar_material(doc["id"], usuario_id)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


def _render_subida(categoria: str, es_primera: bool, usuario_id) -> None:
    etiqueta = "⬆️ Subir la Herramienta de Excel u otro documento a esta categoría" if es_primera \
        else "⬆️ Subir un documento a esta categoría"
    with st.form(f"mat_form_{categoria}", clear_on_submit=True):
        st.markdown(f"**{etiqueta}**")
        titulo = st.text_input("Título del documento", key=f"mat_tit_{categoria}",
                               placeholder="Ej. Herramienta de Autodiagnóstico (Excel)" if es_primera else "Ej. Guía…")
        archivo = st.file_uploader(
            "Archivo (Excel, PDF, Word, imagen…)",
            type=["xlsx", "xls", "pdf", "doc", "docx", "ppt", "pptx", "png", "jpg", "jpeg", "txt", "csv"],
            key=f"mat_file_{categoria}",
        )
        if st.form_submit_button("⬆️ Subir"):
            if archivo is None:
                st.warning("Elige un archivo para subir.")
            else:
                ok, msg = crud_adx.guardar_material(
                    titulo or archivo.name, archivo.name, archivo.type,
                    archivo.getvalue(), usuario_id, categoria=categoria,
                )
                (st.success if ok else st.error)(msg)
                if ok:
                    st.rerun()


def mostrar_material_apoyo() -> None:
    usuario = st.session_state.get("usuario") or {}
    usuario_id = usuario.get("id")
    es_admin = usuario.get("rol") in ("administrador", "supervisor")

    st.header("📚 Material de apoyo — Documentos")
    st.caption("Biblioteca de documentos del Código Nacional de Buenas Prácticas para las "
               "Estadísticas Oficiales, organizada por categorías.")

    documentos = crud_adx.listar_material()
    por_categoria: dict[str, list] = {c: [] for c in _CATEGORIAS}
    for doc in documentos:
        cat = doc.get("categoria")
        if cat not in por_categoria:
            cat = "Otros documentos"
        por_categoria[cat].append(doc)

    for i, categoria in enumerate(_CATEGORIAS):
        docs_cat = por_categoria[categoria]
        # No mostrar "Otros documentos" si está vacía y no es admin.
        if categoria == "Otros documentos" and not docs_cat and not es_admin:
            continue
        expandida = (i == 0) or bool(docs_cat)
        with st.expander(f"📁  {categoria}   ·   {len(docs_cat)} documento(s)", expanded=expandida):
            if docs_cat:
                for doc in docs_cat:
                    _render_documento(doc, es_admin, usuario_id)
                    st.divider()
            else:
                st.caption("Sin documentos en esta categoría todavía.")
            if es_admin:
                _render_subida(categoria, es_primera=(i == 0), usuario_id=usuario_id)

    st.divider()
    st.subheader("🔗 Enlaces de referencia")
    for titulo, descripcion, url in _ENLACES_REFERENCIA:
        st.markdown(f"**[{titulo}]({url})**")
        st.caption(descripcion)
