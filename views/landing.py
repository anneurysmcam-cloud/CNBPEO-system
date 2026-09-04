"""
views/landing.py
=================
Portada institucional pública del CNBPE (Código Nacional de Buenas Prácticas
para las Estadísticas Oficiales). Se muestra a quien entra sin sesión: presenta
la herramienta e invita a iniciar sesión (el formulario de login vive en el
panel izquierdo — ver app.py). No hay accesos al módulo viejo de indicadores.

Diseño: hero con la portada oficial del Código como imagen, tarjetas
informativas, fichas de cifras (3·15·67·252), escala de cumplimiento con
colores y una barra de "Iniciar sesión".
"""

import base64
from pathlib import Path

import streamlit as st

_ASSETS = Path(__file__).resolve().parent.parent / "tracking"
_HERO_BG_PATH = _ASSETS / "CNBPEO_like.jpg"

_NIVELES_CNBPEO = [
    ("GEI", "Gestión del Entorno Institucional · 5 principios"),
    ("GPE", "Gestión del Proceso Estadístico · 4 principios"),
    ("GRE", "Gestión de los Resultados Estadísticos · 6 principios"),
]


@st.cache_data(show_spinner=False)
def _img_base64(ruta: str) -> str:
    """Codifica una imagen a base64 una sola vez por proceso (None-safe)."""
    p = Path(ruta)
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode("ascii")


def _estilos() -> str:
    return """
    <style>
    /* Fondo azul institucional en toda la portada pública (main + sidebar) */
    .stApp, div[data-testid="stAppViewContainer"]{ background:#0a1830 !important; }
    section[data-testid="stSidebar"] > div{ background:linear-gradient(180deg,#0e2a5e 0%,#0a1c40 100%) !important; }
    div[data-testid="stHeader"], header[data-testid="stHeader"]{ background:transparent !important; }

    div[data-testid="stMainBlockContainer"],
    div[data-testid="stAppViewContainer"] .block-container{
        padding-top:1.0rem; max-width:1180px; margin-left:auto !important; margin-right:auto !important;}
    div[data-testid="stAlertContainer"], div[data-testid="stAlert"]{ margin-top:2.4rem; }

    .cn-hero{position:relative;overflow:hidden;border-radius:20px;min-height:300px;
        padding:32px 30px;
        background:
          linear-gradient(90deg,#0a2150 0%,#0a2150 30%,rgba(10,33,80,.45) 50%,rgba(10,33,80,0) 72%,rgba(10,33,80,0) 100%),
          url("data:image/jpeg;base64,__HERO_BG__") right center / auto 145% no-repeat,
          #0a2150;
        border:1px solid rgba(80,140,230,.3);box-shadow:0 18px 44px rgba(2,10,30,.5)}
    .cn-left{position:relative;z-index:2;max-width:600px}
    .cn-eyebrow{color:#8fc0ff !important;font-weight:700;letter-spacing:2.4px;text-transform:uppercase;font-size:.76rem;margin:0 0 6px}
    .cn-title{color:#ffffff !important;font-weight:800;font-size:3.6rem;line-height:1;letter-spacing:1px;margin:0 0 12px}
    .cn-subtitle{color:#ffffff !important;font-weight:700;font-size:1.55rem;line-height:1.15;margin:0;max-width:520px}
    .cn-subtitle b{color:#5aa9ff !important}
    .cn-rule{width:64px;height:4px;background:#3b93f7;border-radius:3px;margin:13px 0 15px}
    .cn-tagline{color:rgba(255,255,255,.85) !important;font-size:.95rem;line-height:1.6;max-width:500px;margin:0}
    .cn-cover{flex:none;width:210px;position:relative;z-index:2}
    .cn-cover img{width:100%;border-radius:12px;display:block;box-shadow:0 14px 34px rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.12)}
    @media(max-width:900px){.cn-cover{display:none}.cn-title{font-size:2.8rem}.cn-subtitle{font-size:1.3rem}}

    .cn-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:16px}
    .cn-card{background:#0e2148;border:1px solid rgba(80,140,230,.16);border-radius:16px;padding:18px;min-height:220px}
    .cn-icb{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.35rem;margin-bottom:11px}
    .cn-icb.blue{background:rgba(59,147,247,.16)} .cn-icb.green{background:rgba(31,157,107,.16)} .cn-icb.violet{background:rgba(139,110,246,.16)}
    .cn-card h3{margin:0 0 11px;font-size:1.08rem;color:#e8edf5}
    .cn-card ul{margin:0;padding:0}
    .cn-card li{opacity:.85;font-size:.9rem;line-height:1.5;margin-bottom:8px;list-style:none;position:relative;padding-left:22px;color:#e8edf5}
    .cn-card li::before{content:"✓";position:absolute;left:0;color:#37c98d;font-weight:800}
    .cn-card p{opacity:.85;font-size:.9rem;line-height:1.55;margin:0;color:#e8edf5}
    .cn-chip{display:flex;gap:11px;align-items:center;background:rgba(59,147,247,.08);border-radius:10px;padding:8px 11px;margin-bottom:8px}
    .cn-chip .code{font-weight:800;color:#5aa9ff;min-width:40px}
    .cn-chip .name{opacity:.85;font-size:.84rem;color:#e8edf5}
    .cn-foot{color:#9aa4b2;font-size:.8rem;margin-top:11px}

    .cn-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:16px}
    .cn-stat{background:#0e2148;border:1px solid rgba(80,140,230,.16);border-radius:14px;padding:14px 16px;display:flex;align-items:center;gap:12px}
    .cn-si{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex:none}
    .cn-num{font-weight:800;font-size:1.8rem;line-height:1;color:#fff}
    .cn-lbl{color:#9aa4b2;font-size:.79rem;margin-top:3px}

    .cn-stitle{font-weight:700;font-size:1rem;margin:20px 2px 11px;color:#e8edf5}
    .cn-scale{display:flex;gap:9px;flex-wrap:wrap}
    .cn-pill{display:flex;align-items:center;gap:8px;background:#0e2148;border:1px solid rgba(80,140,230,.16);border-radius:999px;padding:7px 13px;font-size:.84rem;color:#e8edf5}
    .cn-dot{width:11px;height:11px;border-radius:50%}

    .cn-banner{display:flex;align-items:center;gap:16px;margin-top:18px;background:linear-gradient(90deg,#0f2a5e,#12336f);
        border:1px solid rgba(80,140,230,.3);border-radius:16px;padding:16px 20px}
    .cn-bi{width:44px;height:44px;border-radius:50%;background:rgba(59,147,247,.2);display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex:none}
    .cn-bt{flex:1;min-width:0}
    .cn-bt b{font-size:1.0rem;color:#fff} .cn-bt p{margin:2px 0 0;color:rgba(255,255,255,.75);font-size:.87rem}
    .cn-cta{flex:none;background:linear-gradient(180deg,#2f7ee0,#1d5fc0);color:#fff;font-weight:700;
        font-size:1rem;padding:13px 30px;border-radius:12px;white-space:nowrap;box-shadow:0 8px 20px rgba(29,95,192,.42)}
    </style>
    """


def _html() -> str:
    return """
    <div class="cn-hero">
      <div class="cn-left">
        <p class="cn-eyebrow">Oficina Nacional de Estadística</p>
        <h1 class="cn-title">CNBPE</h1>
        <div class="cn-subtitle">Código Nacional de <b>Buenas Prácticas</b> para las Estadísticas Oficiales</div>
        <div class="cn-rule"></div>
        <p class="cn-tagline">Herramienta institucional de la Oficina Nacional de Estadística para evaluar,
          por institución, el cumplimiento del Código — alineado con los Principios Fundamentales de la ONU
          y el Código Regional de CEPAL.</p>
      </div>
    </div>

    <div class="cn-cards">
      <div class="cn-card">
        <div class="cn-icb blue">🧭</div><h3>¿Qué puedes hacer aquí?</h3>
        <ul>
          <li>Autodiagnóstico por institución del SEN</li>
          <li>Marcar los 252 elementos (SI/NO/N/A + nivel)</li>
          <li>Estadísticas (RESULTADOS) y export a Excel/PDF</li>
          <li>Plan de acción y seguimiento en el tiempo</li>
        </ul>
      </div>
      <div class="cn-card">
        <div class="cn-icb green">🖥️</div><h3>El sistema</h3>
        <p>Lleva a un entorno digital la Matriz de Autodiagnóstico para la Calidad de la Producción
          Estadística: verifica, elemento por elemento, si la práctica institucional cumple con el Código
          y registra la evidencia. Además importa y lee el Excel automáticamente.</p>
      </div>
      <div class="cn-card">
        <div class="cn-icb violet">✅</div><h3>Niveles del Código</h3>
        <div class="cn-chip"><span class="code">GEI</span><span class="name">Gestión del Entorno Institucional · 5 principios</span></div>
        <div class="cn-chip"><span class="code">GPE</span><span class="name">Gestión del Proceso Estadístico · 4 principios</span></div>
        <div class="cn-chip"><span class="code">GRE</span><span class="name">Gestión de Resultados Estadísticos · 6 principios</span></div>
        <div class="cn-foot">3 niveles · 15 principios · 67 requisitos · 252 elementos</div>
      </div>
    </div>

    <div class="cn-stats">
      <div class="cn-stat"><div class="cn-si" style="background:rgba(59,147,247,.16)">🏛️</div><div><div class="cn-num">3</div><div class="cn-lbl">niveles de gestión</div></div></div>
      <div class="cn-stat"><div class="cn-si" style="background:rgba(31,157,107,.16)">⭐</div><div><div class="cn-num">15</div><div class="cn-lbl">principios de calidad</div></div></div>
      <div class="cn-stat"><div class="cn-si" style="background:rgba(139,110,246,.16)">📋</div><div><div class="cn-num">67</div><div class="cn-lbl">requisitos</div></div></div>
      <div class="cn-stat"><div class="cn-si" style="background:rgba(240,173,78,.18)">🛡️</div><div><div class="cn-num">252</div><div class="cn-lbl">elementos de verificación</div></div></div>
    </div>

    """


_BANNER_HTML = (
    '<div class="cn-banner"><div class="cn-bi">🚀</div>'
    '<div class="cn-bt"><b>Para usar la herramienta, inicia sesión con tu usuario institucional.</b>'
    '<p>Accede para evaluar, dar seguimiento y mejorar la calidad estadística institucional.</p></div>'
    '<a href="#ir-login" class="cn-cta" style="text-decoration:none;display:inline-block">'
    '🔒&nbsp; Iniciar sesión</a></div>'
)


def mostrar_landing() -> None:
    """Renderiza la portada pública. El login vive en el panel izquierdo
    (siempre visible); la barra final es la llamada a la acción."""
    st.markdown(_estilos().replace("__HERO_BG__", _img_base64(str(_HERO_BG_PATH))),
                unsafe_allow_html=True)
    st.markdown(_html(), unsafe_allow_html=True)
    st.markdown(_BANNER_HTML, unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:#9aa4b2;font-size:.82rem;margin-top:18px'>"
        "© Oficina Nacional de Estadística (ONE) · Código Nacional de Buenas Prácticas para las "
        "Estadísticas Oficiales (CNBPEO)</p>",
        unsafe_allow_html=True,
    )
