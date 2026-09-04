"""
views/instrucciones.py
======================
Instrucciones del Autodiagnóstico — contenido de la hoja INSTRUCCIONES de la
Matriz de Autodiagnóstico para la Calidad de la Producción Estadística (ONE,
versión 004). Pantalla informativa de solo lectura.
"""

import streamlit as st


def mostrar_instrucciones() -> None:
    st.header("📖 Instrucciones del Autodiagnóstico")
    st.caption("Matriz de Autodiagnóstico para la Calidad de la Producción Estadística — "
               "Dirección de Normativas y Metodologías · Versión 004 · Revisión 2024-05-23")

    st.subheader("Propósito")
    st.write(
        "La presente matriz tiene como propósito facilitar una herramienta que sirva como soporte "
        "para dar seguimiento al cumplimiento de los Principios Fundamentales de las Estadísticas "
        "Oficiales, apoyada en la adaptación del cuestionario para el autodiagnóstico de la CEPAL."
    )

    st.subheader("Metodología")
    st.write(
        "La metodología básica para diagnosticar el estado de los elementos de los Principios "
        "Fundamentales de Calidad para las Estadísticas Oficiales consiste en la utilización del "
        "cuestionario de auto-evaluación elaborado por la CEPAL, adoptado con mejoras que responden "
        "a las necesidades de la Oficina Nacional de Estadística de la República Dominicana. La "
        "matriz está dirigida a establecer si en la práctica se toman en consideración las "
        "metodologías, procedimientos, leyes, políticas y demás normas definidas para dar "
        "cumplimiento a los Principios de Calidad de las Estadísticas Oficiales."
    )

    st.subheader("Estructura de la matriz")
    st.markdown(
        """
La herramienta cuenta con los siguientes campos a completar:

1. **Principio:** el principio de calidad, que busca normalizar los procesos.
2. **Requisito de cumplimiento:** el aspecto del principio que se debe cumplir.
3. **Código de elemento:** la codificación asignada a cada elemento (ej. GEI-1.1.1).
4. **Elemento que deben asegurarse:** el requerimiento concreto a verificar.
5. **¿Cumple con el elemento? (Estado de cumplimiento):** **SI** si se cumple, **NO** si no se cumple, **N/A** si no aplica.
6. **Nivel de cumplimiento:** *No aplica*, *No Iniciado*, *Iniciado* (se han iniciado los trabajos), *Cumplimiento Parcial* (50%–99%) o *Cumplimiento Total* (100%).
7. **Evidencia actual:** el documento o evidencia más reciente del cumplimiento (inicial, parcial o total).
8. **Evidencia anterior:** evidencia de un autodiagnóstico previo (no aplica para el primer autodiagnóstico).
9. **Comentario:** necesidades, debilidades, fortalezas y otros aspectos a considerar.
10. **Acción de mejora:** la mejora que se puede aplicar.
11. **Responsable:** quién realiza la acción.
12. **Fecha de cumplimiento:** la fecha en que se da cumplimiento al elemento o entregable.
        """
    )

    st.subheader("Escala de cumplimiento (Indicador de Implementación)")
    st.table({
        "Nivel": ["No aplica", "No Iniciado", "Iniciado", "Cumplimiento Parcial", "Cumplimiento Total"],
        "Rango": ["El elemento no es pertinente", "0%", "1% – 49%", "50% – 99%", "100%"],
    })
    st.info(
        "Solo podrán tener estatus **Cumplimiento Total** aquellos requerimientos que cumplan con: "
        "**a)** evidencia entregada, y **b)** valoración al 100%."
    )

    st.subheader("Pasos a seguir")
    st.markdown(
        """
1. **1er paso.** Para iniciar el llenado, ve al nivel de gestión con el que pretendes iniciar (GEI, GPE o GRE) y especifica si cumples con el elemento (SI / NO / N/A) y su nivel de cumplimiento.
2. **2do paso.** Si es la primera vez que se implementa, coloca la evidencia actual y deja la evidencia anterior en blanco.
3. **3er paso.** En la casilla de comentarios, especifica necesidades, debilidades, fortalezas y otros aspectos a considerar.
4. **4to paso.** Si se encuentra la necesidad de una acción de mejora, especifícala en la casilla de acción de mejora.
5. **5to paso.** Identifica el/la responsable de la acción de mejora y la fecha de cumplimiento.
        """
    )

    st.subheader("Plan de acción · Resultados · Seguimiento")
    st.markdown(
        """
- **Plan de acción:** para los elementos calificados con **NO** se describen las acciones de mejora o fortalecimiento (actividades, insumos, presupuesto, fecha prevista, responsable).
- **Resultados:** resumen del conteo de cada categoría por principio y el puntaje de cumplimiento por principio y por nivel.
- **Seguimiento:** presenta los niveles de avance en el tiempo (en valor porcentual y en gráfica), para dar seguimiento a la implementación comparando cada medición con la anterior.
        """
    )

    st.caption(
        "Fuentes consultadas: Cuestionario de autoevaluación de la CEPAL · Principios Fundamentales "
        "de las Estadísticas Oficiales (ONU) · Código Regional de Buenas Prácticas para las "
        "Estadísticas en América Latina y el Caribe (CEPAL)."
    )
