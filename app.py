"""
app.py
======
Punto de entrada de la aplicación CNBPE — Oficina Nacional de Estadística (ONE).

Ejecutar con:
    streamlit run app.py
"""

import logging
import time

import streamlit as st

# ── Logging institucional ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Bootstrap de base de datos (migraciones idempotentes) ───────────────────
# Llamada EXPLÍCITA (Hallazgo #4 del informe de revisión de código de agosto
# 2026): antes, `import data.database` disparaba el bootstrap completo como
# efecto secundario del import. Ahora inicializar_base_datos() se invoca acá,
# una sola vez por proceso, antes de cualquier st.* — el punto de entrada
# real de la aplicación.
from data.database import inicializar_base_datos
from config import DB_PATH

inicializar_base_datos()

# ── Seguridad: permisos del archivo de BD al arrancar ───────────────────────
from security.hardening import asegurar_permisos_db
asegurar_permisos_db(DB_PATH)

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="CNBPEO - ONE 📊",
    page_icon="📊",
    layout="wide",
)

# ── Estilos institucionales ──────────────────────────────────────────────────
# Los colores usan las variables de tema que Streamlit expone en runtime
# (--text-color, --background-color, --secondary-background-color) en vez de
# hex fijos. Streamlit ya trae un selector de tema claro/oscuro nativo (menú
# ☰ → Settings → Theme); con colores hardcodeados, el título y el footer
# institucionales quedaban casi ilegibles al activar el modo oscuro (texto
# azul oscuro sobre fondo oscuro). El azul institucional (#002F6C) se
# conserva como acento en modo claro vía color-mix, sin perder legibilidad
# en oscuro.
st.markdown("""
    <style>
    /* ═══ FONDO AZUL CNBPEO EN TODA LA APP (forzado por CSS, no depende del config.toml) ═══ */
    .stApp, div[data-testid="stAppViewContainer"], section[data-testid="stMain"] {
        background: #0a1830 !important;
    }
    /* Sidebar azul con degradado (igual que la portada) */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg,#0e2a5e 0%,#0a1c40 100%) !important;
    }
    /* Barra superior transparente */
    div[data-testid="stHeader"], header[data-testid="stHeader"] {
        background: transparent !important;
    }
    /* Texto general claro */
    .stApp, section[data-testid="stSidebar"], p, span, label, li, td, th, h1, h2, h3, h4, h5, h6 {
        color: #e8edf5;
    }
    /* Radios del menú: punto seleccionado AZUL (no rojo) */
    section[data-testid="stSidebar"] div[role="radiogroup"] label div:first-child {
        border-color: #5aa9ff !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] div:first-child,
    div[role="radiogroup"] input:checked + div {
        background-color: #2f7ee0 !important;
        border-color: #2f7ee0 !important;
    }
    /* Botones primarios y de formulario en AZUL (no rojo) */
    button[kind="primary"], button[kind="primaryFormSubmit"],
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(180deg,#2f7ee0,#1d5fc0) !important;
        border: none !important; color: #fff !important;
    }
    /* Botones secundarios: tono azul de tarjeta */
    button[kind="secondary"], button[data-testid="baseButton-secondary"] {
        background: #0e2148 !important;
        border: 1px solid rgba(95,175,255,.6) !important; color: #e8edf5 !important;
    }
    /* Checkbox marcado en azul */
    div[data-testid="stCheckbox"] input:checked ~ div,
    label[data-baseweb="checkbox"] span[data-checked="true"] {
        background-color: #2f7ee0 !important; border-color: #2f7ee0 !important;
    }
    /* Slider / progreso en azul */
    div[data-testid="stProgress"] div[role="progressbar"] > div,
    div[data-baseweb="slider"] div[role="slider"] { background-color: #2f7ee0 !important; }

    .main-title {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #b9c9e6 !important;
        opacity: 0.9;
        text-align: center;
        margin-bottom: 25px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        text-align: center;
        padding: 8px;
        font-size: 12px;
        border-top: 1px solid rgba(128, 128, 128, 0.3);
    }

    /* ── Tono azul CNBPEO en las cajas de trabajo (mismos tonos de la portada) ── */
    /* Contenedores con borde (st.container(border=True), tarjetas de métrica…) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #0e2148 !important;
        border: 1px solid rgba(95,175,255,.6) !important;
        border-radius: 14px !important;
    }
    /* Inputs: selectbox, text_input, number_input, date, file uploader */
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: #0e2148 !important;
        color: #e8edf5 !important;
    }
    /* BORDE FINO Y ELEGANTE en TODOS los campos (estilo de la referencia):
       delgado, azul suave, sin sombra pesada. */
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div {
        border: 1px solid rgba(120,162,224,.55) !important;
        border-radius: 8px !important;
        background-color: #0e2148 !important;
        box-shadow: none !important;
    }
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input {
        border: 1px solid rgba(120,162,224,.55) !important;
        border-radius: 8px !important;
        background-color: #0e2148 !important;
        color: #e8edf5 !important;
        box-shadow: none !important;
    }
    /* Desplegables (selectbox: ¿Cumple?, Nivel...) y campo de Fecha.
       A estas cajas BaseWeb les ignora el 'border', así que el borde fino se
       dibuja con una sombra interna de 1px (inset) — así SÍ se ve siempre. */
    div[data-testid="stSelectbox"] div[data-baseweb="select"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"],
    div[data-testid="stDateInput"] div[data-baseweb="input"],
    div[data-testid="stDateInput"] div[data-baseweb="base-input"],
    div[data-testid="stDateInput"] > div > div {
        border: 1px solid rgba(120,162,224,.55) !important;
        border-radius: 8px !important;
        background-color: #0e2148 !important;
        box-shadow: inset 0 0 0 1px rgba(120,162,224,.7) !important;
    }
    /* Al hacer clic/escribir, el borde se aclara (azul más nítido). */
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"] > div:focus-within,
    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stDateInput"] input:focus {
        border: 1px solid #5aa9ff !important;
        box-shadow: 0 0 0 2px rgba(90,169,255,.25) !important;
    }
    /* Botón "Subida" del cargador de archivos: borde fino punteado. */
    section[data-testid="stFileUploaderDropzone"],
    div[data-testid="stFileUploader"] section {
        border: 1px dashed rgba(120,162,224,.6) !important;
        border-radius: 10px !important;
        background-color: #0e2148 !important;
    }
    /* Menú desplegable del selectbox */
    ul[data-testid="stSelectboxVirtualDropdown"],
    div[data-baseweb="popover"] ul {
        background-color: #0e2148 !important;
    }
    /* Métrica (st.metric) — la tarjeta del % general */
    div[data-testid="stMetric"] {
        background: #0e2148 !important;
        border: 1px solid rgba(95,175,255,.6) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
    }
    /* Tablas y dataframes */
    div[data-testid="stTable"] table,
    div[data-testid="stDataFrame"] {
        background-color: #0e2148 !important;
    }
    div[data-testid="stTable"] thead tr th,
    div[data-testid="stDataFrame"] [role="columnheader"] {
        background-color: #12305f !important;
        color: #cfe0ff !important;
    }
    div[data-testid="stTable"] tbody tr td,
    div[data-testid="stDataFrame"] [role="gridcell"] {
        background-color: #0e2148 !important;
        color: #e8edf5 !important;
    }
    /* Expanders (Material de apoyo: categorías desplegables) */
    div[data-testid="stExpander"] details {
        background: #0e2148 !important;
        border: 1px solid rgba(95,175,255,.6) !important;
        border-radius: 12px !important;
    }
    div[data-testid="stExpander"] summary {
        background: #12305f !important;
        border-radius: 12px !important;
    }
    /* Pestañas seleccionadas (Marcar cumplimiento, Estadísticas…) */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #5aa9ff !important;
    }
    div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] {
        background-color: #2f7ee0 !important;
    }
    /* Cajas de info/aviso con tono azul */
    div[data-testid="stAlertContainer"] {
        background: rgba(47,126,224,.10) !important;
        border: 1px solid rgba(95,175,255,.6) !important;
    }
    /* Popover (⚙️ Administración) */
    div[data-testid="stPopoverBody"] {
        background: #0e2148 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── Estado de sesión ─────────────────────────────────────────────────────────
# Se inicializa aquí (antes del header) porque _mostrando_landing() ya
# necesita leer landing_dismissed para decidir si el header se muestra.
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None
if "show_help" not in st.session_state:
    st.session_state.show_help = False
if "landing_dismissed" not in st.session_state:
    st.session_state.landing_dismissed = False
if "opcion_publica_preseleccionada" not in st.session_state:
    st.session_state.opcion_publica_preseleccionada = None
if "opcion_autenticada_preseleccionada" not in st.session_state:
    # Permite que una vista (p. ej. Aprobar Indicadores → "Revisar en
    # Actualizar Indicador") navegue programáticamente a otra opción del
    # menú de sesión autenticada, en vez de solo poder decirle al usuario
    # "ve a tal pantalla" — mismo patrón que opcion_publica_preseleccionada.
    st.session_state.opcion_autenticada_preseleccionada = None


# ── Persistencia de sesión al REFRESCAR (F5) ─────────────────────────────────
# Streamlit borra st.session_state en cada refresco del navegador, lo que
# botaba al usuario al menú de inicio. Para que se quede EXACTAMENTE donde
# estaba, al iniciar sesión guardamos un token en la URL (?s=...) y el
# usuario + la opción de menú en un almacén a nivel de proceso; al refrescar,
# restauramos la sesión desde ese token. La ÚNICA forma de salir es "Cerrar
# sesión", que borra el token. El almacén se vacía si se reinicia el servidor
# (streamlit), lo cual obliga —correctamente— a volver a iniciar sesión.
@st.cache_resource
def _almacen_sesiones_persistentes():
    """Dict compartido {token: {"usuario": ..., "opcion": ...}} que sobrevive
    los reruns y refrescos mientras el servidor siga corriendo."""
    return {}


def _restaurar_sesion_si_refresco() -> None:
    """Si la sesión de Streamlit se perdió por un refresco pero la URL trae un
    token válido, restaura el usuario y la última opción de menú."""
    if st.session_state.get("usuario") is not None:
        return
    token = st.query_params.get("s")
    if not token:
        return
    registro = _almacen_sesiones_persistentes().get(token)
    if not registro:
        return
    st.session_state["usuario"] = registro["usuario"]
    st.session_state["_token_sesion"] = token
    if registro.get("opcion"):
        st.session_state["menu_autenticado_radio"] = registro["opcion"]
    # Reinicia el temporizador de inactividad para que el refresco no cuente
    # como sesión expirada.
    try:
        from security.auth import registrar_actividad as _reg_act
        _reg_act()
    except Exception:
        pass


_restaurar_sesion_si_refresco()


def _mostrando_landing() -> bool:
    """True si en este render se va a mostrar la landing institucional
    (views/landing.py). Esa pantalla ya trae su propio título/subtítulo
    centralizados dentro del cuadro azul — el header genérico de aquí se
    omite en ese caso puntual para no duplicarlo, tal como se ve en el
    resto de la app (Consultas, Dashboard, login, etc.)."""
    return (
        st.session_state["usuario"] is None
        and "usuario_pendiente_2fa" not in st.session_state
        and "usuario_pendiente_setup_2fa" not in st.session_state
        and not st.session_state.landing_dismissed
    )


if not _mostrando_landing():
    st.markdown('<h1 class="main-title">Oficina Nacional de Estadística (ONE)</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle">Código Nacional de Buenas Prácticas para las Estadísticas Oficiales (CNBPEO)</h3>', unsafe_allow_html=True)

# ── Seguridad y utilidades de sesión ─────────────────────────────────────────
# NOTA DE RENDIMIENTO: las vistas (views.*) NO se importan aquí arriba a
# propósito. Cada vista arrastra dependencias pesadas (pandas, plotly,
# fpdf2, openpyxl), y como Python solo importa un módulo una vez por
# proceso, hacerlo a nivel de módulo de app.py forzaba ese costo (~1-1.5s)
# ANTES de poder pintar la pantalla de login — de ahí la sensación de
# lentitud/cuelgue al arrancar. En su lugar, cada vista se importa de forma
# perezosa (lazy import) solo cuando el usuario ya autenticado la selecciona
# en el menú, vía _importar_vista() más abajo.
from security.auth import (
    BloqueadoError,
    confirmar_activacion_totp,
    generar_y_guardar_codigos_respaldo,
    iniciar_enrolamiento_totp,
    logout,
    validar_credenciales,
    verificar_codigo_respaldo,
    verificar_segundo_factor,
)
from security.hardening import (
    intentos_restantes,
    registrar_actividad,
    verificar_timeout_sesion,
    minutos_restantes_sesion,
)
from utils.ui_mensajes import marcar_mensaje, mostrar_mensaje_pendiente
import importlib

# ── Roles y opciones de menú ─────────────────────────────────────────────────
# Punto 9: el acceso de solo lectura ya no es un rol de login — es el acceso
# público por defecto SIN sesión (pensado para el enlace público en la
# página de la ONE). Cualquiera que entre sin sesión ve exactamente estas
# opciones automáticamente, sin necesidad de una cuenta.
# Menú enfocado en el Código Nacional de Buenas Prácticas (CNBPEO): el menú de
# la izquierda muestra solo lo del autodiagnóstico. "Administrar Usuarios" y
# "Ver Auditoría" ya no van en el radio; se acceden desde el botón
# "⚙️ Administración" (tipo tres puntos) que se muestra arriba solo al admin.
# Los ítems A/B/C abren el Autodiagnóstico ya filtrado en su nivel (GEI/GPE/GRE).
_MENU_CODIGO: list[str] = [
    "Instrucciones",
    "Autodiagnóstico",
    "A. Gestión del entorno institucional",
    "B. Gestión del Proceso Estadístico",
    "C. Gestión de resultados estadísticos",
    "Material de apoyo",
]

_OPCIONES_POR_ROL: dict[str, list[str]] = {
    "editor": list(_MENU_CODIGO),
    "supervisor": list(_MENU_CODIGO),
    "administrador": list(_MENU_CODIGO),
}

# Opciones de administración accesibles desde el botón "⚙️ Administración"
# (solo administrador), fuera del menú de la izquierda.
_OPCIONES_ADMINISTRACION: list[str] = ["Administrar Usuarios", "Ver Auditoría"]

# Mapa opción de menú -> (módulo, nombre de función). La importación real
# del módulo se hace en _importar_vista(), solo cuando se necesita.
_ROUTER: dict[str, tuple[str, str]] = {
    # Administración (solo admin, desde el botón "⚙️ Administración").
    "Ver Auditoría": ("views.ver_auditoria", "mostrar_ver_auditoria"),
    "Administrar Usuarios": ("views.admin_usuarios", "mostrar_administrar_usuarios"),
    # Autodiagnóstico CNBPE (menú principal).
    "Autodiagnóstico": ("views.autodiagnostico", "mostrar_autodiagnostico"),
    "Instrucciones": ("views.instrucciones", "mostrar_instrucciones"),
    "Material de apoyo": ("views.material_apoyo", "mostrar_material_apoyo"),
    "A. Gestión del entorno institucional": ("views.autodiagnostico", "mostrar_autodiagnostico_gei"),
    "B. Gestión del Proceso Estadístico": ("views.autodiagnostico", "mostrar_autodiagnostico_gpe"),
    "C. Gestión de resultados estadísticos": ("views.autodiagnostico", "mostrar_autodiagnostico_gre"),
}


def _importar_vista(opcion: str):
    """Importa perezosamente el módulo de la vista seleccionada y devuelve
    su función de entrada. Devuelve None si la opción no está registrada."""
    destino = _ROUTER.get(opcion)
    if destino is None:
        return None
    modulo_path, nombre_funcion = destino
    modulo = importlib.import_module(modulo_path)
    return getattr(modulo, nombre_funcion)


def _ejecutar_vista(vista, opcion: str) -> None:
    """Ejecuta la vista seleccionada blindada contra errores no controlados.

    Cualquier excepción que se escape de una vista (bug de código, dato
    inesperado, etc.) se captura acá antes de que Streamlit la muestre en
    pantalla con su traceback técnico — eso expone detalles internos y
    rompe la experiencia de un usuario que no tiene por qué entenderlos.

    En vez de eso: se registra el error completo (traceback incluido) vía
    ``logger.exception`` — queda en los logs del servidor (journalctl del
    servicio systemd en producción, ver DESPLIEGUE_PRODUCCION.md) con un
    identificador de incidente corto, y al usuario se le muestra un mensaje
    genérico con ese mismo identificador para que pueda reportarlo sin
    exponer la causa técnica real.
    """
    try:
        vista()
    except Exception:
        incidente = f"ERR-{int(time.time())}"
        usuario_actual = st.session_state.get("usuario") or {}
        logger.exception(
            "Error no controlado en vista '%s' (incidente %s, usuario '%s').",
            opcion, incidente, usuario_actual.get("username", "público"),
        )
        st.error(
            "⚠️ Ocurrió un error inesperado al procesar esta sección. "
            "El equipo técnico ya tiene el detalle registrado.\n\n"
            f"Si el problema persiste, reporta este código: **{incidente}**"
        )

def _mostrar_boton_ayuda() -> None:
    """Botón + panel de documentación descargable, en la esquina superior
    derecha del área principal — como estuvo en versiones anteriores a
    d33a82b, revertido a pedido explícito de Randy tras ver el resultado
    en el sidebar (no era lo que quería, prefiere la esquina de siempre).

    Nota heredada de cuando se movió al sidebar (commit d33a82b): ahí
    competía por posición con la barra de herramientas nativa de
    Streamlit (☰ / "Deploy", fija en la esquina superior derecha) y podía
    quedar parcialmente tapada por ella. Se deja un `st.write("")` como
    espaciador antes de la fila del botón para separarlo verticalmente de
    esa barra — no hay forma de confirmarlo sin un navegador real en este
    entorno de desarrollo, así que conviene que Randy confirme visualmente
    que no vuelve a taparse tras desplegar.
    """
    st.write("")
    col_h1, col_h2 = st.columns([7, 2])
    with col_h2:
        if st.button("🧭 Ayudas y Guías", width='stretch'):
            st.session_state.show_help = not st.session_state.show_help

    if st.session_state.show_help:
        st.markdown("### 📖 Documentación del Sistema CNBPEO")
        # Los manuales/guías del CNBPEO todavía no están cargados. Antes esta
        # sección descargaba los PDFs viejos del sistema SIDOE, que ya no
        # aplican — se quitaron para no entregar documentos equivocados.
        #
        # CUANDO TENGAS los documentos oficiales de ESTA herramienta:
        #   1) Crea la carpeta 'docs' dentro de C:\CNBPEO_actualizacion (si no existe).
        #   2) Copia ahí tus PDFs, por ejemplo: manual_uso.pdf, guia_rapida.pdf...
        #   3) Agrégalos a la lista _DOCS_CNBPEO de abajo (nombre visible, archivo).
        # Solo aparecerán para descargar los archivos que EXISTAN en 'docs';
        # mientras la lista esté vacía o los archivos no existan, no se descarga
        # nada y se muestra el aviso de "próximamente".
        _DOCS_CNBPEO: list[tuple[str, str]] = [
            # ("📘 Manual de Uso", "docs/manual_uso.pdf"),
            # ("📗 Guía rápida", "docs/guia_rapida.pdf"),
        ]
        _mostrados = 0
        for _nombre, _archivo in _DOCS_CNBPEO:
            try:
                with open(_archivo, "rb") as _f:
                    st.download_button(_nombre, _f, _archivo, mime="application/pdf",
                                       key=f"dl_doc_{_archivo}")
                    _mostrados += 1
            except FileNotFoundError:
                pass
        if _mostrados == 0:
            st.info(
                "📚 Los manuales y guías de esta herramienta estarán disponibles "
                "aquí **próximamente**. Todavía no se han cargado los documentos "
                "oficiales del CNBPEO — cuando estén listos, aparecerán en esta "
                "sección para descargar."
            )


def _mostrar_logo_sidebar() -> None:
    import os as _os
    _logo = "tracking/cnbpeo_logo.png" if _os.path.exists("tracking/cnbpeo_logo.png") else "tracking/logo_one.png"
    st.sidebar.image(_logo, width=185)


def _mostrar_footer() -> None:
    st.markdown("""
        <div class="footer">
            Desarrollado por Randy A. Medina — Oficina Nacional de Estadística (ONE) 🇩🇴 —
            Código Nacional de Buenas Prácticas para las Estadísticas Oficiales (CNBPEO)
        </div>
    """, unsafe_allow_html=True)


def _procesar_intento_login(key_prefix: str = "") -> None:
    """Renderiza el formulario de login y procesa el intento si se envía.

    Si el usuario tiene 2FA (TOTP) activado, el login NO se completa aquí:
    se guarda en ``usuario_pendiente_2fa`` (no en ``usuario``, que es lo que
    el resto de la app trata como "sesión iniciada") y se muestra un
    segundo formulario (``_procesar_segundo_factor``) para el código. Solo
    tras un código válido se establece ``usuario`` y arranca la sesión real.
    """
    with st.form(f"login_form{key_prefix}"):
        username = st.text_input("Usuario", placeholder="Ingrese su usuario", key=f"_login_user{key_prefix}")
        password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña",
                                 key=f"_login_pass{key_prefix}")
        st.checkbox("Recordarme", value=True, key=f"_recordarme_login{key_prefix}")
        submit = st.form_submit_button("🔒 Iniciar sesión", width="stretch", type="primary")

    if not submit:
        return

    username_strip = username.strip()
    if not username_strip or not password:
        st.error("Por favor ingrese usuario y contraseña.")
        return

    try:
        usuario_login = validar_credenciales(username_strip, password)
        if usuario_login:
            if usuario_login.get("totp_habilitado"):
                st.session_state["usuario_pendiente_2fa"] = usuario_login
                st.rerun()
            elif usuario_login.get("requiere_2fa"):
                # El administrador exigió 2FA para este usuario (ver
                # views/admin_usuarios.py) pero todavía no lo configuró —
                # se fuerza el enrolamiento antes de establecer la sesión,
                # en vez de dejarlo entrar sin 2FA como el resto de los
                # logins sin totp_habilitado.
                st.session_state["usuario_pendiente_setup_2fa"] = usuario_login
                st.rerun()
            else:
                st.session_state["usuario"] = usuario_login
                registrar_actividad()  # iniciar timer de inactividad
                logger.info("Sesión iniciada para usuario '%s'.", usuario_login["username"])
                st.rerun()
        else:
            restantes = intentos_restantes(username_strip)
            if restantes > 0:
                st.error(
                    f"❌ Credenciales inválidas o usuario inactivo. "
                    f"Intentos restantes: {restantes}."
                )
            else:
                st.error("❌ Credenciales inválidas.")
    except BloqueadoError as exc:
        st.error(f"🔒 {exc}")


def _procesar_segundo_factor() -> None:
    """Segundo paso del login cuando el usuario tiene 2FA activado: pide el
    código de 6 dígitos de la app autenticadora, o alternativamente un
    código de respaldo de un solo uso si el usuario no tiene acceso a su
    dispositivo, antes de establecer la sesión real."""
    usuario_pendiente = st.session_state["usuario_pendiente_2fa"]
    st.info(f"🔐 Hola, {usuario_pendiente['username']}. Ingresa el código de tu app autenticadora.")

    usar_respaldo = st.checkbox(
        "No tengo acceso a mi app autenticadora — usar un código de respaldo"
    )

    with st.form("segundo_factor_form"):
        if usar_respaldo:
            codigo = st.text_input(
                "Código de respaldo", max_chars=9, help="Formato AAAA-AAAA"
            )
        else:
            codigo = st.text_input("Código de 6 dígitos", max_chars=6)
        col_confirmar, col_cancelar = st.columns(2)
        with col_confirmar:
            confirmar = st.form_submit_button("Confirmar")
        with col_cancelar:
            cancelar = st.form_submit_button("Cancelar")

    if cancelar:
        del st.session_state["usuario_pendiente_2fa"]
        st.rerun()

    if not confirmar:
        return

    if usar_respaldo:
        valido = verificar_codigo_respaldo(usuario_pendiente["id"], codigo)
    else:
        valido = verificar_segundo_factor(usuario_pendiente["id"], codigo)

    if valido:
        st.session_state["usuario"] = usuario_pendiente
        del st.session_state["usuario_pendiente_2fa"]
        registrar_actividad()  # iniciar timer de inactividad
        if usar_respaldo:
            from models.logs import registrar_log_standalone
            from security.auth import contar_codigos_respaldo_restantes

            restantes = contar_codigos_respaldo_restantes(usuario_pendiente["id"])
            registrar_log_standalone(
                usuario_pendiente["id"],
                "TOTP_CODIGO_RESPALDO_USADO",
                f"Usuario '{usuario_pendiente['username']}' (id={usuario_pendiente['id']}), "
                f"restantes={restantes}",
            )
            logger.warning(
                "Sesión iniciada con código de respaldo para usuario '%s' (%d restantes).",
                usuario_pendiente["username"], restantes,
            )
            st.session_state["totp_aviso_respaldo_usado"] = restantes
        else:
            logger.info("Sesión iniciada (con 2FA) para usuario '%s'.", usuario_pendiente["username"])
        st.rerun()
    else:
        st.error("❌ Código inválido. Intenta de nuevo.")


def _procesar_configuracion_2fa_obligatoria() -> None:
    """Fuerza el enrolamiento TOTP durante el login cuando el administrador
    marcó ``requiere_2fa`` para este usuario y todavía no lo tiene
    configurado (ver ``views/admin_usuarios.py`` — sección 'Exigir 2FA').

    Mismo flujo de enrolamiento que el autoservicio de 2FA en
    ``views/admin_usuarios.py`` (QR + confirmación + códigos de respaldo
    mostrados una sola vez), pero ejecutado ANTES de establecer la sesión
    real: el usuario no puede acceder a ninguna vista hasta completarlo.
    """
    usuario_pendiente = st.session_state["usuario_pendiente_setup_2fa"]
    st.warning(
        f"🔐 Hola, {usuario_pendiente['username']}. Tu administrador exige "
        "que actives la verificación en dos pasos (2FA) antes de continuar. "
        "No podrás acceder al sistema hasta completar este paso."
    )

    # ── Paso final: mostrar códigos de respaldo una sola vez y terminar login ──
    if st.session_state.get("setup2fa_codigos_respaldo"):
        st.success("✅ 2FA activado correctamente.")
        st.warning(
            "⚠️ Guarda estos códigos de respaldo en un lugar seguro — es la "
            "única vez que se muestran. Te permiten entrar si pierdes acceso "
            "a tu app autenticadora."
        )
        st.code("\n".join(st.session_state["setup2fa_codigos_respaldo"]), language=None)
        if st.button("Continuar al sistema"):
            st.session_state["usuario"] = usuario_pendiente
            del st.session_state["usuario_pendiente_setup_2fa"]
            del st.session_state["setup2fa_codigos_respaldo"]
            registrar_actividad()  # iniciar timer de inactividad
            logger.info(
                "Sesión iniciada tras configurar 2FA obligatorio para usuario '%s'.",
                usuario_pendiente["username"],
            )
            st.rerun()
        return

    # ── Paso 1: iniciar enrolamiento (generar secreto/QR) ────────────────────
    if not st.session_state.get("setup2fa_uri"):
        if st.button("🔐 Comenzar configuración de 2FA"):
            secreto, uri = iniciar_enrolamiento_totp(usuario_pendiente["id"])
            st.session_state["setup2fa_secreto"] = secreto
            st.session_state["setup2fa_uri"] = uri
            st.rerun()
        if st.button("Cancelar e ingresar más tarde"):
            del st.session_state["usuario_pendiente_setup_2fa"]
            st.rerun()
        return

    # ── Paso 2: escanear QR y confirmar el primer código ─────────────────────
    import io

    import qrcode

    uri = st.session_state["setup2fa_uri"]
    secreto = st.session_state["setup2fa_secreto"]
    img = qrcode.make(uri)
    buf_qr = io.BytesIO()
    img.save(buf_qr, format="PNG")
    st.image(buf_qr.getvalue(), caption="Escanea con tu app autenticadora", width=220)
    with st.expander("¿No puedes escanear el código?"):
        st.code(secreto, language=None)
        st.caption("Ingresa este secreto manualmente en tu app autenticadora.")

    with st.form("confirmar_2fa_obligatorio_form"):
        codigo_confirmacion = st.text_input("Código de 6 dígitos", max_chars=6)
        col_conf, col_canc = st.columns(2)
        with col_conf:
            confirmar = st.form_submit_button("✅ Confirmar y activar")
        with col_canc:
            cancelar = st.form_submit_button("Cancelar")

    if cancelar:
        # No desactiva nada en BD (el usuario podrá reintentar al volver a
        # loguearse), solo limpia el estado local del asistente.
        del st.session_state["setup2fa_uri"]
        del st.session_state["setup2fa_secreto"]
        del st.session_state["usuario_pendiente_setup_2fa"]
        st.rerun()

    if confirmar:
        from models.logs import registrar_log_standalone

        try:
            confirmar_activacion_totp(usuario_pendiente["id"], codigo_confirmacion)
            registrar_log_standalone(
                usuario_pendiente["id"], "ACTIVAR_2FA_OBLIGATORIO",
                f"Usuario '{usuario_pendiente['username']}' (id={usuario_pendiente['id']})",
            )
            del st.session_state["setup2fa_uri"]
            del st.session_state["setup2fa_secreto"]

            # Códigos de respaldo: se generan de una vez al activar, igual
            # que en el autoservicio de admin_usuarios.py.
            codigos_respaldo = generar_y_guardar_codigos_respaldo(usuario_pendiente["id"])
            st.session_state["setup2fa_codigos_respaldo"] = codigos_respaldo
            registrar_log_standalone(
                usuario_pendiente["id"], "TOTP_CODIGOS_REGENERADOS",
                f"Usuario '{usuario_pendiente['username']}' (id={usuario_pendiente['id']})",
            )
            st.rerun()
        except (ValueError, LookupError) as exc:
            st.error(f"❌ {exc}")


usuario = st.session_state["usuario"]

# Si acabamos de iniciar sesión (por cualquier vía) y todavía no hay token
# persistente, lo creamos y lo ponemos en la URL para sobrevivir refrescos.
if usuario is not None and not st.session_state.get("_token_sesion"):
    import secrets as _secrets
    _tok_nuevo = _secrets.token_urlsafe(16)
    st.session_state["_token_sesion"] = _tok_nuevo
    _almacen_sesiones_persistentes()[_tok_nuevo] = {
        "usuario": usuario,
        "opcion": st.session_state.get("menu_autenticado_radio"),
    }
    st.query_params["s"] = _tok_nuevo

# ═══════════════════════════════════════════════════════════════════════════
# 2FA PENDIENTE — el usuario pasó usuario/contraseña pero falta el código TOTP
# ═══════════════════════════════════════════════════════════════════════════
# Se corta el flujo aquí (antes del modo público) para no exponer ninguna
# vista, ni siquiera de solo lectura, mientras el login está a medias.
if usuario is None and "usuario_pendiente_2fa" in st.session_state:
    _mostrar_logo_sidebar()
    st.header("🔐 Verificación en dos pasos")
    _procesar_segundo_factor()
    _mostrar_footer()
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# 2FA OBLIGATORIO PENDIENTE DE CONFIGURAR — el admin lo exigió (ver
# views/admin_usuarios.py) y este usuario todavía no lo tiene activado
# ═══════════════════════════════════════════════════════════════════════════
if usuario is None and "usuario_pendiente_setup_2fa" in st.session_state:
    _mostrar_logo_sidebar()
    st.header("🔐 Configuración obligatoria de 2FA")
    _procesar_configuracion_2fa_obligatoria()
    _mostrar_footer()
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# MODO PÚBLICO (punto 9) — sin sesión iniciada
# ═══════════════════════════════════════════════════════════════════════════
# El acceso de solo lectura no requiere login: cualquiera que entre al
# sistema sin haber iniciado sesión ve directamente Consulta / Ficha /
# Dashboard de solo lectura — pensado para el enlace público en la página
# de la ONE. Crear,
# editar, eliminar indicadores, Auditoría, Administrar Usuarios y Auxiliares
# siguen exigiendo login como Editor o Administrador.
if usuario is None:
    st.sidebar.image("tracking/cnbpeo_logo.png", width=185)
    st.sidebar.markdown(
        '<p style="color:#cdd8ee;font-weight:700;font-size:.72rem;letter-spacing:1.2px;'
        'margin:-6px 0 8px 4px">OFICINA NACIONAL DE ESTADÍSTICA</p>',
        unsafe_allow_html=True,
    )
    mostrar_mensaje_pendiente()
    # Panel de login siempre visible en el lado izquierdo (estilo portada
    # oficial): encabezado, formulario, y tarjetas de ayuda / acceso seguro.
    st.sidebar.markdown(
        """
        <style>
        section[data-testid="stSidebar"] div[data-testid="stTextInput"] input,
        section[data-testid="stSidebar"] div[data-baseweb="input"]{
            background:#0b1a3a !important;border-radius:10px !important;
            border:1px solid rgba(120,160,230,.30) !important;}
        /* Botones "Iniciar sesión" en azul (login del sidebar y CTA de la portada) */
        section[data-testid="stSidebar"] button[kind="primary"],
        section[data-testid="stSidebar"] button[kind="primaryFormSubmit"],
        div[data-testid="stMainBlockContainer"] button[kind="primary"]{
            background:linear-gradient(180deg,#2f7ee0,#1d5fc0) !important;
            border:none !important;color:#ffffff !important;}
        section[data-testid="stSidebar"] input[type="checkbox"]{accent-color:#2f7ee0}
        .cn-login-head{font-weight:700;font-size:1.08rem;color:#e8edf5;margin:2px 0 6px}
        .cn-side-card{background:rgba(30,55,100,.30);border:1px solid rgba(120,160,230,.22);
            border-radius:12px;padding:12px 14px;margin-top:14px}
        .cn-side-card .t{font-weight:700;color:#e8edf5;font-size:.94rem}
        .cn-side-card .s{color:#9fb0cf;font-size:.8rem;margin-top:3px;line-height:1.4}
        </style>
        <div class="cn-login-head" id="ir-login" style="scroll-margin-top:16px">🔒 Iniciar sesión</div>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        _procesar_intento_login()
    st.sidebar.markdown(
        '<div class="cn-side-card"><div class="t">❓ ¿Necesitas ayuda?</div>'
        '<div class="s">Contacta al administrador del sistema.</div></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<div class="cn-side-card"><div class="t">🛡️ Acceso seguro</div>'
        '<div class="s">Tus datos están protegidos con los más altos estándares de seguridad.</div></div>',
        unsafe_allow_html=True,
    )

    # Portada institucional (única pantalla del modo público). El login está
    # siempre visible arriba; ya no hay accesos al módulo viejo de indicadores.
    from views.landing import mostrar_landing

    mostrar_landing()
    _mostrar_footer()
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# SESIÓN AUTENTICADA
# ═══════════════════════════════════════════════════════════════════════════

# ── Timeout de sesión por inactividad ────────────────────────────────────────
if verificar_timeout_sesion():
    usuario_expirado = st.session_state.get("usuario", {}).get("username", "desconocido")
    logger.info("Sesión expirada por inactividad para usuario '%s'.", usuario_expirado)
    _tok_exp = st.session_state.get("_token_sesion")
    if _tok_exp:
        _almacen_sesiones_persistentes().pop(_tok_exp, None)
    st.query_params.clear()
    logout(st.session_state)
    marcar_mensaje(
        "warning",
        "⏱️ Tu sesión ha expirado por inactividad. Por favor vuelve a iniciar sesión.",
    )
    st.rerun()

# ── Registrar actividad en cada renderizado ───────────────────────────────────
registrar_actividad()

_mostrar_boton_ayuda()

# ── Menú lateral ─────────────────────────────────────────────────────────────
_mostrar_logo_sidebar()
st.sidebar.write(f"👤 **{usuario['username']}** ({usuario['rol']})")

# Aviso único (se limpia solo) si esta sesión se inició con un código de
# respaldo: recuerda al usuario cuántos le quedan antes de que lo olvide.
if "totp_aviso_respaldo_usado" in st.session_state:
    restantes = st.session_state.pop("totp_aviso_respaldo_usado")
    if restantes == 0:
        st.sidebar.error(
            "🔑 Usaste tu último código de respaldo. Genera un lote nuevo "
            "desde Administrar Usuarios → 2FA lo antes posible."
        )
    else:
        st.sidebar.warning(
            f"🔑 Entraste con un código de respaldo. Te quedan **{restantes}**. "
            "Considera reactivar tu 2FA con tu dispositivo o generar códigos nuevos."
        )

# Mostrar tiempo restante de sesión en el sidebar
mins = minutos_restantes_sesion()
if mins <= 10:
    st.sidebar.warning(f"⏳ Sesión expira en {mins} min")
else:
    st.sidebar.caption(f"⏳ Sesión activa ({mins} min restantes)")

if st.sidebar.button("Cerrar Sesión"):
    logger.info("Sesión cerrada manualmente por usuario '%s'.", usuario["username"])
    _tok_cerrar = st.session_state.get("_token_sesion")
    if _tok_cerrar:
        _almacen_sesiones_persistentes().pop(_tok_cerrar, None)
    st.query_params.clear()
    logout(st.session_state)
    st.rerun()

# ── Opciones según rol ────────────────────────────────────────────────────────
opciones = _OPCIONES_POR_ROL.get(usuario.get("rol"))
if opciones is None:
    st.error(
        f"🚫 El rol '{usuario.get('rol')}' no está reconocido por el sistema. "
        "Roles válidos: editor, supervisor, administrador. "
        "Contacte a un administrador."
    )
    st.stop()

# El radio necesita un `key` explícito para poder forzar una navegación
# programática (p. ej. "Aprobar Indicadores" -> "Editar antes de aprobar",
# ver views/aprobar_indicadores.py::_ir_a_actualizar_indicador). Sin `key`,
# Streamlit igual le asigna uno interno automático basado en label+options,
# y como ese radio ya se había renderizado antes en la sesión (el
# supervisor ya estaba parado en "Aprobar Indicadores"), reutiliza el valor
# ya guardado en session_state y el argumento `index=` de abajo se ignora
# por completo — la navegación "funcionaba" en el sentido de que
# opcion_autenticada_preseleccionada quedaba bien calculado, pero el radio
# nunca se movía de la opción en la que ya estaba, así que el supervisor
# se quedaba viendo "Aprobar Indicadores" en vez de caer en "Actualizar
# Indicador". Con un `key` propio, se puede sobrescribir ese valor a mano
# en session_state antes de instanciar el widget para forzar el salto, y
# se consume una sola vez (igual que _indicador_a_editar_id) para no
# pisar una navegación manual posterior del usuario.
_KEY_MENU_AUTENTICADO = "menu_autenticado_radio"
preseleccion = st.session_state.opcion_autenticada_preseleccionada
if preseleccion in opciones:
    st.session_state[_KEY_MENU_AUTENTICADO] = preseleccion
    st.session_state.opcion_autenticada_preseleccionada = None
elif _KEY_MENU_AUTENTICADO not in st.session_state:
    st.session_state[_KEY_MENU_AUTENTICADO] = opciones[0]
elif st.session_state[_KEY_MENU_AUTENTICADO] not in opciones:
    # El rol cambió entre renders (p. ej. otro usuario inició sesión) y la
    # opción memorizada ya no existe en el menú de este rol.
    st.session_state[_KEY_MENU_AUTENTICADO] = opciones[0]
opcion = st.sidebar.radio(
    "Selecciona una opción:", opciones, key=_KEY_MENU_AUTENTICADO
)

# Recordar la página actual en el almacén persistente, para que al refrescar
# (F5) el usuario vuelva a caer en esta misma opción y no en el inicio.
_tok_actual = st.session_state.get("_token_sesion")
if _tok_actual:
    _reg_actual = _almacen_sesiones_persistentes().get(_tok_actual)
    if _reg_actual is not None:
        _reg_actual["opcion"] = opcion

# ── Menú "⚙️ Administración" (tipo tres puntos), solo administrador ───────────
# Streamlit no permite añadir opciones al menú nativo de arriba a la derecha,
# así que se ofrece un botón propio que abre un pop-over con las funciones de
# administración (Administrar Usuarios / Ver Auditoría), fuera del menú de la
# izquierda que quedó enfocado en el Código.
if usuario.get("rol") == "administrador" and hasattr(st, "popover"):
    _c_izq, _c_admin = st.columns([4, 1])
    with _c_admin:
        with st.popover("⚙️ Administración", width='stretch'):
            if st.button("👥 Administrar Usuarios", key="pop_admin_users", width='stretch'):
                st.session_state["_vista_admin_override"] = "Administrar Usuarios"
                st.rerun()
            if st.button("🕵️ Ver Auditoría", key="pop_ver_audit", width='stretch'):
                st.session_state["_vista_admin_override"] = "Ver Auditoría"
                st.rerun()

# Si el usuario cambió de opción en el menú de la izquierda, se sale del modo
# administración para volver al Código.
if st.session_state.get("_ultima_opcion_menu") != opcion:
    st.session_state["_vista_admin_override"] = None
st.session_state["_ultima_opcion_menu"] = opcion

# ── Enrutador ─────────────────────────────────────────────────────────────────
override = st.session_state.get("_vista_admin_override")
if (override in _OPCIONES_ADMINISTRACION and usuario.get("rol") == "administrador"):
    if st.button("← Volver al menú del Código"):
        st.session_state["_vista_admin_override"] = None
        st.rerun()
    vista_admin = _importar_vista(override)
    if vista_admin:
        _ejecutar_vista(vista_admin, override)
    else:
        st.error(f"Opción no reconocida: {override}")
else:
    vista = _importar_vista(opcion)
    if vista:
        _ejecutar_vista(vista, opcion)
    else:
        st.error(f"Opción no reconocida: {opcion}")

# ── Footer institucional ──────────────────────────────────────────────────────
_mostrar_footer()
