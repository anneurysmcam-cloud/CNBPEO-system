"""
data/autodiagnostico_catalogo.py
=================================
Catálogo estático (fuente de verdad) de la Matriz de Autodiagnóstico para
la Calidad de la Producción Estadística, extraído del Código Nacional de
Buenas Prácticas para las Estadísticas Oficiales (ONE, versión 004,
revisión 2024-05-23 — ver hoja INSTRUCCIONES del Excel de referencia).

Jerarquía: Nivel (3: GEI/GPE/GRE) > Principio (15) > Elemento (67 —
corresponde a lo que el Excel original llama "Requisito de cumplimiento";
ver la nota en data/database.py::migrar_autodiagnostico_tablas() sobre por
qué se simplificó a este nivel y no al de "Código de elemento" (252 filas)
del Excel, donde el original marca cumplimiento).

Estos datos solo se usan una vez, en
data.database.sembrar_autodiagnostico() (idempotente vía el UNIQUE de
autodx_elementos.codigo) — no se importan en caliente en cada request.
"""

# (codigo, letra, nombre, descripcion, orden)
NIVELES: list[tuple] = [
    ("GEI", "A", """Gestión del entorno institucional""", """A. Gestión del entorno institucional: El entorno institucional para la Oficina Nacional de Estadísticas (ONE) y los miembros del Sistema Estadístico Nacional (SEN) es un elemento indispensable para reforzar la credibilidad y eficiencia de las estadísticas oficiales. Al mismo tiempo, el SEN debe tener un ente rector que ejerza la función de coordinar y regular la investigación, la producción y la difusión de estadísticas de calidad mediante políticas, normas y estándares.""", 1),
    ("GPE", "B", """Gestión del proceso estadístico""", """B. Gestión del Proceso Estadístico: La aplicación de metodologías, estándares nacionales e internacionales acompañado de las buenas prácticas estadística aseguran una producción de calidad.""", 2),
    ("GRE", "C", """Gestión de resultados estadísticos""", """C. Gestión de resultados estadísticos: las estadísticas oficiales deben satisfacer las necesidades de los usuarios y cumplir con las normas de calidad establecidas para los productos estadísticos.""", 3),
]

# (numero_global_1_a_15, nivel_codigo, nombre, orden)
PRINCIPIOS: list[tuple] = [
    (1, "GEI", """Asegurar la imparcialidad y la objetividad""", 1),
    (2, "GEI", """Asegurar la independencia profesional.""", 2),
    (3, "GEI", """Asegurar la trasparencia, confidencialidad estadística y seguridad de los datos""", 3),
    (4, "GEI", """Asegurar la calidad""", 4),
    (5, "GEI", """Asegurar la suficiencia de los recursos""", 5),
    (6, "GPE", """Procedimientos estadísticos apropiados""", 6),
    (7, "GPE", """Asegurar la solidez metodológica""", 7),
    (8, "GPE", """Asegurar una buena relación de costo - eficiencia""", 8),
    (9, "GPE", """Manejo de la carga del encuestado""", 9),
    (10, "GRE", """Asegurar la relevancia""", 10),
    (11, "GRE", """Asegurar la precisión y la confiabilidad""", 11),
    (12, "GRE", """Asegurar la oportunidad y la puntualidad""", 12),
    (13, "GRE", """Asegurar la accesibilidad y la claridad""", 13),
    (14, "GRE", """Asegurar la coherencia y la comparabilidad""", 14),
    (15, "GRE", """Gestión de los metadatos""", 15),
]

# (codigo, nivel_codigo, principio_numero, numero, requisito_cumplimiento, detalle, orden)
# "detalle" es el desglose original en sub-puntos verificables (columna
# "Elemento que deben de asegurarse" del Excel, una viñeta por cada
# "Código de elemento" GEI-N.N.N que caía bajo este requisito) — se muestra
# como referencia de apoyo al marcar el cumplimiento, pero no se puntúa por
# separado.
ELEMENTOS: list[tuple] = [
    ("GEI-1.1", "GEI", 1, "1.1", """Se debe contemplar mediante decreto u otra  disposición formal, disponible al público, que estipule que las Instituciones del SEN deben desarrollar, producir y difundir estadísticas siguiendo estándares profesionales y tratar a todas las personas usuarias por igual.""", """- La cultura y tradición profesional aseguran la imparcialidad y la objetividad de las estadísticas producidas por las agencias estadísticas, independientemente de la existencia o ausencia de leyes o disposiciones formales.
- Se reconoce la objetividad e imparcialidad de las estadísticas oficiales (y no es puesta en duda) por observadores neutrales y el público en general (por ejemplo, se encuentra medida con indicadores de imagen institucional).""", 1),
    ("GEI-1.2", "GEI", 1, "1.2", """Las Unidades Organizacionales de Estadísticas (UOE)  agencias de estadística deben implementar una declaración o código de conducta o ética que rija las prácticas estadísticas, y se debe dar la realización de seguimiento a su cumplimiento.""", """- Existen protocolos éticos o un código de conducta para garantizar la imparcialidad y la objetividad.""", 2),
    ("GEI-1.3", "GEI", 1, "1.3", """Las fuentes de datos, conceptos, clasificaciones y  metodologías se deben elegir de forma objetiva y considerando las mejores prácticas internacionales.""", """- Las fuentes, los conceptos, los métodos, los procesos para el desarrollo, la producción y la difusión de los datos se eligen sobre la base de consideraciones, principios y buenas prácticas estadísticas nacionales e internacionales.""", 3),
    ("GEI-1.4", "GEI", 1, "1.4", """El SEN a través de su Unidad Administrativa debe de cumplir con mecanismos para anunciar con anticipación las fechas y el horario o bien, existir un calendario de publicaciones estadísticas, que incluye la fecha y hora (cuando corresponde) de las publicaciones estadísticas y que este sea puesto a disposición del público con antelación. En caso de que las fechas de publicación establecidas en el calendario de difusión no cumplan, las divergencias deben ser notificadas públicamente con anticipación, junto con las nuevas fechas de difusión y las causas del retraso.""", """- Existe un calendario público de publicación que contiene toda la información sobre las publicaciones planeadas por la ONE en el período de los próximos 12 meses.
- Existe un calendario público de publicación que contiene toda la información sobre las publicaciones planeadas por el SEN en el período de los próximos 12 meses.
- Las estadísticas se publican en la fecha y hora (cuando corresponde) determinadas en el calendario de publicación
- Los cambios en el calendario de publicación se anuncian con antelación y se explican los motivos de los cambios.
- El intercambio de resultados estadísticos antes de la publicación oficial (una "presentación previa privilegiada") se mantiene al mínimo y se encuentra debidamente justificado y estrictamente controlado y documentado, y corresponde solo a fines informativos.""", 4),
    ("GEI-1.5", "GEI", 1, "1.5", """En los casos en que se detecten errores, se deben corregir  a la mayor brevedad y se informará a las personas usuarias sobre cómo estos afectaron las estadísticas publicadas.""", """- Existe una política normada y documentada sobre cómo corregir los datos publicados cuando se detectan errores.
- La política de tratamiento de errores está disponible al público.
- La corrección de errores para la operación estadística involucrada es documentada y de conocimiento público""", 5),
    ("GEI-2.1", "GEI", 2, "2.1", """El Director/a General de la Oficina Nacional de Estadísticas debe ser nombrado basado en criterios profesionales y de manera transparente.""", """- Las reglas que se aplican para nombrar y asignar el cargo de director(a) de la Oficina Nacional de Estadísticas, se basan en competencias profesional, son transparentes y están libres de consideraciones políticas.""", 6),
    ("GEI-2.2", "GEI", 2, "2.2", """Se ha declarado explícitamente mediante Ley u otra disposición formal, que las Instituciones integrantes del SEN, incluyendo la ONE están obligadas a diseñar, producir y difundir estadísticas sin interferencia de otros.""", """- Las leyes y regulaciones bajo las cuales operan las unidades estadísticas dentro de los ministerios, departamentos y otras agencias en los diferentes niveles del gobierno, garantizan la independencia profesional de la ONE y de otros productores de estadísticas oficiales.
- En el caso de no contar con una ley ni una disposición formal en la cual se declare que es necesaria la independencia profesional de las agencias estadísticas, de todas maneras, existen una cultura y tradición profesional, así como precedentes históricos o convenciones, en donde se reconoce esta independencia como esencial para la credibilidad de los resultados de los organismos de estadística.""", 7),
    ("GEI-2.3", "GEI", 2, "2.3", """El Director/a de la Oficina Nacional de Estadísticas contempla una posición jerárquica suficiente como para garantizar el diálogo y el liderazgo frente a las autoridades políticas y organismos gubernamentales.""", """- El jefe de la Oficina Nacional de estadísticas tiene una posición jerárquica suficientemente alta para garantizar el diálogo y el liderazgo frente a las autoridades políticas y los organismos gubernamentales.""", 8),
    ("GEI-2.4", "GEI", 2, "2.4", """La ONE, como ente rector del SEN, dirige las decisiones sobre métodos, estándares de, calidad y procedimientos estadísticos a ser usados en la producción de estadísticas, quedando al margen de las decisiones gubernamentales.""", """- El jefe de la ONE y los jefes de las unidades estadísticas del gobierno que producen estadísticas oficiales, toman decisiones de manera independiente sobre el desarrollo, la producción y la difusión de estadísticas oficiales, teniendo en cuenta las consideraciones profesionales, los métodos, los estándares y los procedimientos estadísticos.
- La presentación de informes y rendición de cuentas de la ONE a los órganos gubernamentales superiores, a los ministerios o departamentos y a otras agencias, no afecta su independencia profesional.""", 9),
    ("GEI-3.1", "GEI", 3, "3.1", """Se encuentran disponibles al público los términos y condiciones para producir y difundir estadísticas oficiales.""", """- La información sobre el origen y las fuentes de los datos, los conceptos y los métodos utilizados para el desarrollo, la producción y la difusión de las estadísticas oficiales, se ponen a disposición del público.
- La información sobre estándares estadísticos está disponible al público.
- Se notifica con anticipación al público, sobre los cambios importantes en la metodología, las fuentes de los datos o las técnicas estadísticas utilizadas.
- La política de difusión se comparte con todo el público.
- Se divulgan públicamente los privilegios de acceso previo a los resultados estadísticos.""", 10),
    ("GEI-3.2", "GEI", 3, "3.2", """La confidencialidad estadística se encuentrar garantizada por la ley.""", """- Existe una ley o alguna otra disposición normativa vigente que asegure el manejo adecuado por parte de la ONE, con respecto a la confidencialidad estadística y a la seguridad de la información recibida por parte de los proveedores de datos y de los encuestados.
- Existe una ley o alguna otra disposición normativa vigente que asegure el manejo adecuado por parte de los miembros del SEN, con respecto a la confidencialidad estadística y a la seguridad de la información recibida por parte de los proveedores de datos y de los encuestados.""", 11),
    ("GEI-3.3", "GEI", 3, "3.3", """Existen normas, estándares, directrices, prácticas o procedimientos adecuados para garantizar la confidencialidad estadística.""", """- Se proporcionan directrices e instrucciones, a todo el personal de la ONE, sobre la protección de la confidencialidad estadística de la información a lo largo del proceso estadístico.
- Se llevan a cabo programas de capacitación periódicos y continuos para todo el personal sobre el concepto de confidencialidad en las estadísticas y las buenas prácticas, para asegurar la privacidad de la información que se maneja.
- La estructura organizativa y los acuerdo para el desarrollo y para la implementación de prácticas que garantizan la confidencialidad estadística, son adecuados para hacer frente a las necesidades estadísticas.
- El personal firma, desde el momento de su nombramiento, acuerdos de compromiso para mantener la confidencialidad de la información que se mantienen incluso después de que el personal deja de trabajar en la agencia estadística.""", 12),
    ("GEI-3.4", "GEI", 3, "3.4", """Se contemplan sanciones para cualquier violación intencional de confidencialidad estadística.""", """- Existen disposiciones legales o de otra índole que permiten aplicar 
sanciones administrativas, penales y disciplinarias por incumplir la confidencialidad estadística.
- La información sobre las disposiciones y sanciones al incumplimiento de la confidencialidad estadística se comparte con todo el personal de las agencias estadísticas y se ponen a disposición de todo el público.""", 13),
    ("GEI-3.5", "GEI", 3, "3.5", """La seguridad e integridad de los datos y su transmisión se encuentran asegurados por políticas y prácticas apropiadas.""", """- Existe una política de seguridad de las tecnologías de la información (TI) y es conocida por todo el personal.
- Se implementan medidas y procesos de seguridad física adecuados para asegurar la seguridad de los datos y de las bases de información, siguiendo la política de seguridad de TI y en concordancia con las mejores prácticas y los estándares internacionales.
- Se realizan periódicamente auditorías de seguridad del sistema de seguridad de los datos.
- Todos los accesos a los repositorios de datos y los canales de transmisión de los datos son monitoreados.
- Se evalúa el riesgo de incumplimiento a la seguridad de la información, para la transferencia de los datos y se aplican los procedimientos adecuados para eliminar o minimizar este riesgo.""", 14),
    ("GEI-4.1", "GEI", 4, "4.1", """Existe en la ONE y en el SEN una política de calidad que siga los lineamientos de los principios fundamentales de las estadísticas oficiales.""", """- La política de calidad estadística y el compromiso de la ONE con esta es conocida y comprendida públicamente.
- La ONE promueve el interés mutuo por la calidad con todo su personal e incluye información sobre las discrepancias de los atributos que afectan el programa de trabajo estadístico.
- La ONE, ponen a disposición de las personas usuarias externas sus normas de calidad o una versión resumida de ellas.""", 15),
    ("GEI-4.2", "GEI", 4, "4.2", """La ONE promueve la evaluación y mejora continua de los procesos y productos estadísticos.""", """- Las metodologías y los procesos se documentan de manera regular.
- Se realizan intercambios de buenas prácticas entre las diferentes agencias de estadísticas.
- Existen procedimientos para asegurar que la documentación requerida sobre la calidad sea actualizada periódicamente.
- Existe un plan de aseguramiento de la calidad o un mecanismo similar para describir los estándares de trabajo, las obligaciones formales (como las leyes y las reglas internas) y las acciones de control de calidad para prevenir, monitorear y evaluar los posibles errores y controlar el proceso de producción estadística.
- Se utilizan planes de trabajo, cronogramas, formularios o plantillas estándar para facilitar la actualización de la documentación de los procedimientos y acciones de aseguramiento de la calidad, de manera consistente.
- Las agencias de estadística utilizan un marco nacional de aseguramiento de la calidad (NQAF) como base para las evaluaciones de calidad periódicas (autoevaluaciones u otras evaluaciones).
- Las agencias de estadística utilizan un NQAF que se basa en alguno de los marcos globales o regionalmente aceptados.
- Los sistemas o marcos generales de calidad, como la Gestión de Calidad Total (TQM) y los de la Organización Internacional de Normalización (ISO) 9000, se utilizan junto con el NQAF.
- Se siguen las iniciativas de calidad de los organismos estadísticos internacionales y regionales, como el Sistema Estadístico Europeo (SEE), según corresponda.""", 16),
    ("GEI-4.3", "GEI", 4, "4.3", """Existe algún organismo dentro de la ONE que sea responsable de la gestión de la calidad de la información producida.""", """- Se le asigna la responsabilidad de la gestión de calidad a un gerente de calidad, comité de calidad, unidad o grupo de expertos o asesores.""", 17),
    ("GEI-4.4", "GEI", 4, "4.4", """El organismo responsable de la calidad de la producción estadística de la ONE, cuenta con el apoyo y coordinación necesaria para cumplir con la gestión de la calidad estadística.""", """- Se establece un grupo de trabajo sobre la calidad de los datos en toda la agencia estadística y se reúne periódicamente.
- Los asuntos sobre la calidad son discutidos por la gerencia y con la agencia estadística, de manera periódica (por ejemplo, en una reunión anual de revisión de la calidad)""", 18),
    ("GEI-4.5", "GEI", 4, "4.5", """Las pautas para implementar la gestión de la calidad se definen y colocan a disposición del público.""", """- Se definen, producen y emiten lineamientos para la implementación de la gestión de la calidad que: Describen los principios y el marco de calidad que se sigue; Describen todo el proceso estadístico e identifican la documentación relevante para cada etapa de la producción estadística; Describen los métodos para realizar seguimiento a la calidad en cada etapa del proceso de producción estadística; Identifican los indicadores (medidas de calidad) para evaluar la calidad de las principales etapas de producción, incluidos los indicadores para las fuentes de los datos.
- Se ponen a disposición de todo el público, los lineamientos, los manuales metodológicos y los manuales sobre las buenas prácticas para el aseguramiento de la calidad.
- Existen mecanismos para asegurar la calidad de la recopilación de los datos (incluido el uso de registros administrativos y los provenientes de otras fuentes) y la calidad en la edición de estos datos.""", 19),
    ("GEI-4.6", "GEI", 4, "4.6", """La ONE define, establece e implementar los indicadores necesarios que permitan medir la calidad de los productos estadisticos.""", """- Se preparan, publican y actualizan periódicamente, informes de calidad para que sean de utilidad para ofrecer una perspectiva al productor y a las personas usuarias, según corresponda.
- Se definen, calculan y monitorean indicadores que permiten el seguimiento y el logro de mejoras en la calidad. Algunos ejemplos de indicadores de calidad incluyen: Referencias en los medios, visitas a las páginas web, resultados de las encuestas de satisfacción a las personas usuarias (miden relevancia); Desviaciones estándar y otras medidas de precisión, tasas de respuesta (precisión); Número y tamaño de las revisiones (confiabilidad); Período de tiempo entre la finalización de un período de referencia y la difusión de las estadísticas (oportunidad); Tasa de resultados estadísticos publicados en la fecha anunciada (puntualidad); Sobrecarga a los encuestados.""", 20),
    ("GEI-4.7", "GEI", 4, "4.7", """La ONE da seguimiento de manera regular y sistemática a la satisfacción de las personas usuarias con los productos y procesos estadísticos sometiéndolos a revisiones periódicas de calidad, en función al balance de los principios de calidad, normas y experiencias internaciones, entre otros.""", """- Se realizan revisiones periódicas a la calidad de los productos y procesos principales, para evaluar el cumplimiento de las directrices internas y de los estándares internacionales.
- Se crean equipos de revisión, en los que pueden participar expertos internos y externos.
- Los revisores internos del organismo de estadística están capacitados en métodos y herramientas de auditoría.
- Las acciones de mejora derivadas del resultado de las revisiones de calidad se definen y programan para su implementación.
- La alta gerencia está informada de los resultados de las revisiones para realizar seguimiento a las acciones de mejora.
- Se realizan evaluaciones comparativas, de los procesos estadísticos principales, con otras agencias estadísticas para identificar buenas prácticas.
- Existen procedimientos para monitorear y gestionar la calidad de las diferentes etapas de la producción estadística, de acuerdo con el Modelo Genérico del Proceso Estadístico (GSBPM).
- Se examinan sistemáticamente las confrontaciones entre los principios de calidad (por ejemplo, el balance entre la precisión, la puntualidad y los costos).
- Se realizan revisiones de calidad por parte de expertos externos (también por parte de organizaciones internacionales). Por ejemplo, revisiones de los dominios estadísticos clave (informes del Fondo Monetario Internacional sobre la observancia de los Estándares y Códigos (ROSC)) u otras revisiones como revisiones por pares, auditorías externas y revisiones periódicas.""", 21),
    ("GEI-5.1", "GEI", 5, "5.1", """La ONE cuenta con los recursos financieros, humanos, materiales y tecnológicos suficientes para la implementación del trabajo estadístico y desarrolla los programas estadísticos de corto, mediano y largo plazo.""", """- Existe una estrategia de movilización de recursos, como una Estrategia Nacional para el Desarrollo de Estadísticas (ENDE).
- El plan de trabajo anual es viable dados los recursos disponibles.
- Se miden los costos (humanos y financieros) de cada etapa de la producción estadística.""", 22),
    ("GEI-5.2", "GEI", 5, "5.2", """Los principios de planificación y gestión están dirigidos al uso óptimo de los recursos disponibles.""", """- Se emplean tecnología de la información adecuadas para incrementar la eficiencia.
- Se busca la estandarización, la integración y la automatización de la producción y de la difusión de estadísticas para incrementar la eficiencia y reducir los costos.""", 23),
    ("GPE-6.1", "GPE", 6, "6.1", """Los procesos estadísticos deben ser probados antes de su implementación.""", """- La estrategia para las pruebas piloto se incluye en la fase de diseño del modelo de proceso estadístico.
- Los procedimientos para la recolección de los datos y las herramientas e instrumentos de recopilación, como los cuestionarios electrónicos, se prueban y ajustan (si es necesario y posible) antes de la operación de campo, para mejorar la captura, minimizando la carga al informante.
- Los cuestionarios de las encuestas se prueban utilizando métodos apropiados (por ejemplo, prueba piloto, grupos focales, etc).
- Los sistemas de recopilación de datos administrativos y de otro tipo se prueban antes de su utilización.
- Los procedimientos para el tratamiento y procesamiento de los datos se prueban y ajustan, de ser necesario y posible, antes de su aplicación, con base en experiencias anteriores de la operación estadística y resultados de la prueba piloto, entre otras.
- La evaluación de la prueba piloto es tenida en cuenta para las mejoras e implementación del proceso de produción de la operación estadística.
- En el caso de integrar datos de una o más fuentes, se prueba la calidad de los procedimientos de integración.""", 24),
    ("GPE-6.2", "GPE", 6, "6.2", """La Oficina de Estadísticas debe dar seguimiento de manera oportuna y sistemática a los procesos estadísticos para cada programa de información generado. Cada etapa del proceso estadístico se debe establecer bajo bases científicas y documentadas. Las mismas se deben monitorear en el marco de la mejora continua para la calidad de la operación estadística.""", """- La ONE y las UOE tienen procedimientos y lineamientos consistentes, coherentes, claros, accesibles y transparentes para todas las etapas de la producción de estadísticas.
- La documentación de los procesos de producción sigue el modelo GSBPM.
- Existe una política clara para archivar los datos y las estadísticas y esta se cumple.
- Los procedimientos estadísticos emplean técnicas estadísticas reconocidas internacionalmente.
- Se revisan y validan todas las fuentes de datos, para identificar posibles problemas, errores y discrepancias, como valores atípicos, datos faltantes y errores de codificación.
- Se analizan los efectos de la edición e imputación de datos, y sus efectos son parte de la información pública de la operación estadística, como parte de la evaluación de calidad de la recopilación de los datos.
- Todas las bases de datos estadísticas están diseñadas y organizadas de tal manera que permiten y facilitan el cruce de la información, utilizando identificadores únicos para cada unidad estadística, según corresponda, y a su vez se garantiza la seguridad y la privacidad de los datos.""", 25),
    ("GPE-6.3", "GPE", 6, "6.3", """Deben existir procedimientos para utilizar eficazmente los datos de los registros administrativos y de otro tipo de fuentes con fines estadísticos.""", """- La ONE y las UOE cuentan con herramientas y lineamientos, conocidos por las personas usuarias, y los utilizan para evaluar la calidad de los datos provenientes de registros administrativos y de otras fuentes de datos.
- Se desarrollan e implementan procesos y aplicaciones de software adecuados para la recopilación, procesamiento y análisis de los datos de registros administrativos y de otras fuentes de datos, que se utilizarán con fines estadísticos.
- Los propietarios y titulares de los registros administrativos y de otras fuentes de datos informan  a la ONE y las UOE  de cualquier cambio realizado en el proceso de producción de sus datos.
- La ONE y las UOE disponen de metadatos relacionados con los registros administrativos y de las otras fuentes de datos, incluidos los conceptos, definiciones, clasificaciones, cobertura poblacional para el objetivo y otros aspectos metodológicos.
- Existe documentación que describe el cumplimiento de la calidad por parte de los registros administrativos y de otras fuentes de datos, en términos de definiciones, conceptos, cobertura, etc.""", 26),
    ("GPE-6.4", "GPE", 6, "6.4", """Para las revisiones de las operaciones estadísticas, según su tipo se deben seguir procedimientos estándares y transparentes.""", """- Existe una política, directrices y/o principios para las revisiones, estos son de conocimiento público y se cumplen.
- Las revisiones de las estadísticas publicadas van acompañadas de metadatos que proporcionan las explicaciones necesarias.""", 27),
    ("GPE-6.5", "GPE", 6, "6.5", """Los metadatos y la documentación de los métodos y de los diferentes procesos estadísticos se deben gestionar en todos los procesos y se deben compartir de manera apropiada.""", """- Existen y se siguen las políticas y estándares para mantener y actualizar los metadatos.
- El proceso de producción estadística y de sus metadatos relacionados se realiza de manera paralela.
- Los metadatos se capturan a lo largo del proceso estadístico siguiendo los lineamientos del proceso estadistico y se almacenan en un sistema de gestion de metadatos.""", 28),
    ("GPE-7.1", "GPE", 7, "7.1", """Los procesos metodológicos deben establecerse para cada etapa de la operación estadística a desarrollar por la ONE, deben ser consistentes con los estándares internacionales y los principios fundamentales de las estadísticas oficiales.""", """- Las metodologías son revisadas y  evaluadas en función de las fuentes de datos disponibles y las actualizaciones en procesos estadísticos nacionales, regionales y/o internacionales disponibles.
- Los diseños muéstrales se basan en metodologías sólidas y datos poblacionales lo más actualizados posibles.
- Los procedimientos de edición estadística y los métodos de imputación utilizados, se basan en una metodología sólida conocida para las personas usuarias.""", 29),
    ("GPE-7.2", "GPE", 7, "7.2", """Los procesos metodológicos deben establecerse por la ONE, deben documentarse de forma detallada y deben hacerse de conocimiento público, los mismos deben ser revisados periódicamente y actualizados según sea necesario.""", """- La ONE cuenta con una estructura organizativa que asegure el desarrollo y aplicación de métodos estadísticos sólidos en las distintas etapas del proceso estadístico y para las distintas operaciones estadísticas
- Las metodologías son públicas y contienen todos los detalles del proceso estadístico asegurando procesos comparables, consistentes, coherentes y replicables.
- Se planifican, implementan y publican procedimientos de seguimiento adecuados para el caso de la no respuesta.
- La ONE, de contar con la potestad, revisa las metodologías utilizadas por organismos independientes para la recolección de los datos y la producción de estadísticas.""", 30),
    ("GPE-7.3", "GPE", 7, "7.3", """La ONE debe desarrollar un programa de capacitación anual para su personal y la contratación de personal técnico debe contemplar las cualidades acordes a la función que vayan a ejercer, además se deben llevar a cabo programas de especialización técnica acorde al área de desarrollo.""", """- El personal de la ONE se contrata en función de sus antecedentes académicos, cualificaciones y experiencia adecuada.
- Se encuentran especificados, todos los requisitos de cualificaciones requeridos para todos los cargos.
- Existen programas de capacitación, formación y desarrollo para garantizar que el personal adquiere y actualiza continuamente sus conocimientos metodológicos.
- Las habilidades del personal se actualizan periódicamente, de manera que el personal tiene las capacidades para utilizar nuevas fuentes de datos y nuevas herramientas y tiene la posibilidad de cambiar de posición laboral.
- Se recomienda y promueve la asistencia del personal a cursos de capacitación relevantes y a conferencias nacionales o internacionales.""", 31),
    ("GPE-7.4", "GPE", 7, "7.4", """La ONE debe seleccionar sus fuentes de datos teniendo en cuenta especialmente la oportunidad, el costo/eficiencia y la fiabilidad.""", """- Si existe la oportunidad, se evalúa con frecuencia el uso de distintas fuentes alternativas de datos, incluidas encuestas, los censos, los registros administrativos, el big data y otras fuentes de datos.
- Se evalúa la calidad de los registros administrativos u otras fuentes de datos para su uso estadístico. Idealmente, cuando se usan datos de registros administrativos, se debe asegurar que: El universo poblacional de los registros es consistente con los requerimientos para la producción de las estadísticas; Las clasificaciones usadas son las apropiadas; Los conceptos base de los registros son los apropiados; Los registros están completos y actualizados; La cobertura geográfica es completa y las unidades de medición están definidas e identificadas adecuadamente.
- Existe la definicion de los lineamientos metodológicos a seguir en la utilización de otras fuentes de datos no estructurados (como el Big data), en particular relacionados con la población estadística y la veracidad y volatilidad de dichos datos.""", 32),
    ("GPE-7.5", "GPE", 7, "7.5", """La ONE debe trabajar de manera conjunta con la comunidad científica para mejorar los métodos estadísticos y para promover la innovación en el desarrollo, producción y difusión de estadísticas oficiales.""", """- Se establece cooperación con la comunidad científica, por ejemplo, a través de conferencias, talleres, grupos de trabajo y cursos de capacitación, para discutir desarrollos metodológicos y tecnológicos relevantes (por ejemplo, con respecto a la explotación de nuevas fuentes de datos).
- Existen acuerdos con instituciones académicas para la cooperación e intercambio de personal calificado.
- El personal de la ONE realiza actividades de cooperación en temas metodológicos con sus pares a nivel internacional.
- Se incentiva la participación frecuente en presentaciones y conferencias nacionales e internacionales relevantes para el intercambio de conocimientos y experiencias.""", 33),
    ("GPE-8.1", "GPE", 8, "8.1", """Los costos de producción de cada operación estadística se deben medir y analizan individualmente, y deben de existir mecanismos para evaluar la razón costo-eficiencia de los procesos estadísticos.""", """- Existe un sistema para registrar los costos y el tiempo utilizado para obtener los productos estadísticos, y de ser posible, se estima el tiempo empleado en las etapas principales del proceso.
- Los costos de producir las estadísticas están bien documentados en cada fase del proceso estadístico y se revisan periódicamente para evaluar la eficiencia de su producción.
- Se llevan a cabo análisis de costo-beneficio para determinar la combinación de cumplimiento más adecuada en términos de calidad de los datos.
- La necesidad de recolección de cada variable estadística se encuentra justificada en base a los objetivos y usos de la operación estadística.
- Existe un proceso de revisión continua que considera si un producto estadístico en particular todavía está operando de la manera más costo- eficiente para cumplir con los objetivos y usos establecidos para el mismo.
- Los instrumentos de recolección de los datos están diseñados de manera que minimizan la carga del informante, los costos y tiempos de procesamiento, maximizando la calidad de la captura de la información necesaria.""", 34),
    ("GPE-8.2", "GPE", 8, "8.2", """La ONE debe contar con procedimientos para evaluar la pertinencia de las demandas estadísticas emergentes, entre los que se considera el análisis costo.""", """- Las demandas de nuevas estadísticas son evaluadas con respecto a la relevancia de los objetivos de la operación estadística, la disponibilidad de información y los costos asociados; además, se discuten con la administración, con base en los aportes de los persona usuarias y la cooperación con otros grupos de interés.""", 35),
    ("GPE-8.3", "GPE", 8, "8.3", """Deben existir procedimientos para evaluar la necesidad de dar continuidad a todas las estadísticas y procedimientos para determinar si se puede suspender alguna de ellas para liberar recursos.""", """- Se realizan discusiones de manera frecuente, por parte de la gerencia sobre la utilidad de todas las estadísticas; las discusiones incluyen los aportes de los persona usuarias, tales como los resultados de las encuestas de satisfacción de las persona usuarias.
- El uso de diferentes productos estadísticos, incluidas las bases de datos estadísticas, se monitorea y evalúa para evaluar su relevancia.
- Las persona usuarias y los grupos de interés son informados y consultados sobre la posible no continuidad de algunos productos estadísticos.""", 36),
    ("GPE-8.4", "GPE", 8, "8.4", """Se deben aplicar tecnologías de información y comunicación modernas para mejorar el desempeño de los procesos estadísticos.""", """- Existe una estrategia adecuada de TI, que se revisa y actualiza periódicamente para mejorar la eficacia y la eficiencia de los procesos estadísticos.
- La arquitectura e infraestructura de TI y el hardware, se revisan y actualizan periódicamente, y se identifican las posibilidades de innovación y modernización.
- Las operaciones administrativas de rutina y los procesos estadísticos repetitivos (por ejemplo: recolección de datos, codificación, edición de datos, validación de datos, intercambio de datos) se automatizan siempre que sea posible y se revisan periódicamente.""", 37),
    ("GPE-8.5", "GPE", 8, "8.5", """Se deben realizar esfuerzos proactivos para mejorar el potencial estadístico de los registros administrativos y de otras fuentes de datos.""", """- De ser solicitada, la ONE y las UOE brindan información requerida por organismo legislativo para asegurar la obtención y el acceso constante a las fuentes de datos de los registros administrativos y de los demás tipos de datos con fines estadísticos.
- Se propicia y se cuenta con los elementos legales y técnicos para la generación de acuerdos apropiados con los propietarios de los datos de registros administrativos y de otras bases de datos (por ejemplo, acuerdos de prestación de servicios o mediante legislación nacional), para acceder a los datos, permitir el flujo de datos y metadatos y otros aspectos relevantes.
- Se lleva a cabo una evaluación de las posibles fuentes de datos de registros administrativos antes de comenzar cualquier encuesta nueva.
- Los métodos de integración y vinculación de los datos se llevan a cabo de manera proactiva, sujeto a consideraciones de seguridad y privacidad de estos.
- Los informes de calidad de los registros administrativos y los provenientes de otras fuentes para la producción de estadísticas oficiales son establecidos por la agencia estadística responsable en cooperación con los propietarios o titulares de los datos.""", 38),
    ("GPE-8.6", "GPE", 8, "8.6", """La ONE debe desarrollar estrategias que promuevan la implementación de sistemas de producción integrados y estandarizados.""", """- La ONE y las UOE han desarrollado estrategias para pasar a un sistema de producción estadística más integrado y estandarizado dentro de su organización.
- La ONE y las UOE promueven, comparten e implementan soluciones estandarizadas para aumentar la eficacia y la eficiencia.
- La arquitectura empresarial estadística de la agencia de estadísticas se basa en estándares y lineamientos internacionales como el GSBPM, el GAMSO, la Arquitectura estadística de producción común (CSPA) y el SDMX.""", 39),
    ("GPE-9.1", "GPE", 9, "9.1", """La información solicitada en una encuesta estadística debe solo limitarse a lo necesario para el cumplimiento de los objetivos de la misma""", """- Se considera explícitamente la disponibilidad e idoneidad de los datos existentes (datos de encuestas existentes, datos de registros administrativos y de otras fuentes de datos) antes de sugerir la puesta en marcha de una nueva encuesta.
- La recolección de cualquier elemento de datos, que sea igual o similar a los recopilados en otra encuesta, se limita a lo que se considera necesario para fines de verificación y posibles cruces de información.
- Cuando es posible, las encuestas o partes de la información que se recopilará en las encuestas se extraen o derivan de los registros administrativos disponibles.
- Existen indicadores que permitan medir la carga de los encuestados y estos son considerados en los informes de calidad""", 40),
    ("GPE-9.2", "GPE", 9, "9.2", """En la ONE deben existir mecanismos de difusión para sensibilizar a los informantes/encuestados sobre el valor y el uso de la información estadística y la relevancia de la información capturada por la operación estadística para promover la respuesta veraz y oportuna.""", """- Se ponen a disposición de los informantes, paquetes de información que proporcionan elementos importantes y necesarios sobre la encuesta y que explican el valor de las estadísticas oficiales.
- Los informantes reciben los resultados finales o el resultado del censo o la encuesta en la que participaron.
- Se diseñan estrategias con grupos comunitarios, escuelas, gremios empresariales y otros grupos de interés para crear conciencia sobre el valor de las estadísticas oficiales.
- Se desarrollan productos web que brindan la información estadística necesaria a las persona usuarias de información (empresas y a los individuos), y estos productos se promueven a través de estrategias con comunidades y encuestados.
- Se establece una presencia en las redes sociales para promover la participación en encuestas y censos.
- Existen prácticas estándar para recibir comentarios de las/os informantes y para responder a sus solicitudes y quejas de manera frecuente.""", 41),
    ("GPE-9.3", "GPE", 9, "9.3", """Se deben utilizar métodos sólidos, incluidas las soluciones de tecnología de la información (TI), en las encuestas para minimizar o distribuir la carga de los informantes.""", """- Se utilizan técnicas de muestreo apropiadas para minimizar los tamaños de muestra y a la vez lograr el nivel objetivo de precisión.
- Las encuestas por muestreo se coordinan para distribuir la carga de los informantes.
- Se ofrecen múltiples formas para la recopilación de la información a los informantes , incluidas encuestas electrónicas.
- La recopilación de datos se realiza en el momento más adecuado conforme al flujo de información planeado.""", 42),
    ("GPE-9.4", "GPE", 9, "9.4", """La ONE debe promover el intercambio de datos, el uso de registros administrativos y otras fuentes, entre sus áreas productoras de información para minimizar la carga del encuestado.""", """- Existe y se comparte con las persona usuarias de la información, la documentación de los datos ya disponibles dentro del SEN, incluidos los datos históricos archivados.
- Existen herramientas técnicas para compartir e intercambiar datos dentro del sistema estadístico nacional (por ejemplo, acuerdos formales, servicios web, bases de datos comunes).
- Los archivos de datos (repositorios) se comparten entre las agencias de estadísticas para la producción de estadísticas oficiales y en cumplimiento de las políticas de confidencialidad.
- Existe información sobre la calidad de los datos (por ejemplo, sobre cobertura y posibilidades de cruces).
- Se promueve en todo el SEN el uso de registros administrativos y de otro tipo de fuentes de información, como alternativas a los datos captados por las encuestas para la producción de estadísticas oficiales.""", 43),
    ("GRE-10.1", "GRE", 10, "10.1", """Existen procedimientos para identificar a las personas usuarias, sus necesidades y mecanismos de consulta sobre el contenido del programa de trabajo estadístico.""", """- Existe una legislación o alguna otra disposición formal que incluye la obligación de realizar consultas con las principales personas usuarias de las estadísticas.
- Existen procesos de consulta estructurados y periódicos (por ejemplo, consejos y comités asesores o grupos de trabajo) con los grupos de interés y con las personas usuarias clave para revisar el contenido del programa estadístico y la utilidad de las estadísticas existentes e identificar los requisitos para la producción de nuevas estadísticas.
- Los comentarios del servicio de atención al usuario, centro o línea directa se analizan para comprender e identificar las necesidades de las personas usuarias.
- Se recopilan y analizan los indicadores sobre el uso de las estadísticas (por ejemplo, análisis web, número y tipos de descargas, suscriptores de informes), para mejorar los productos estadísticos.""", 44),
    ("GRE-10.2", "GRE", 10, "10.2", """Se tiene en cuenta las necesidades y los requisitos de las personas usuarias, y se realizan los análisis necesarios para determinar la priorización, que quedan reflejados en el programa de trabajo estadistico cuando corresponde.""", """- Se satisfacen las necesidades prioritarias de las personas usuarias y estas se ven reflejadas en el programa de trabajo de la oficina de estadística.
- Existen procedimientos para priorizar las diversas necesidades de las personas usuarias en el programa de trabajo y en los objetivos estratégicos.
- Se analiza la información sobre el uso de las estadísticas para apoyar el establecimiento de prioridades.
- Se realiza una evaluación periódica del programa de trabajo estadístico para identificar las nuevas necesidades y aquellas que han bajado de prioridad.
- Existen procesos para monitorear y consultar con las partes interesadas la relevancia y la utilidad práctica de las estadísticas existentes (con respecto al alcance, nivel de detalle, costo, etc.) de acuerdo con las necesidades emergentes de las personas usuarias.""", 45),
    ("GRE-10.3", "GRE", 10, "10.3", """Las estadísticas basadas en nuevas fuentes de datos y fuentes de datos existentes se desarrollan en respuesta a las necesidades emergentes de información del sistema de planificación nacional y de la sociedad.""", """- Se establece una unidad de innovación para considerar y experimentar con nuevas fuentes de datos para satisfacer las necesidades emergentes de información.
- Se establece cooperación con la comunidad científica y con los propietarios o titulares de las nuevas fuentes de datos para experimentar y ser pioneros en el uso de estas fuentes de datos.
- La ONE discute internamente y de manera frecuente las posibilidades de explotar nuevas fuentes de datos.""", 46),
    ("GRE-10.4", "GRE", 10, "10.4", """Se mide periódicamente la satisfacción de las personas usuarias y se realiza un seguimiento sistemático.""", """- Se llevan a cabo encuestas y análisis de satisfacción de las personas usuarias o estudios similares de manera periódica y se evalúan y analizan los resultados.
- Se identifican e implementan acciones de mejora derivadas de las encuestas o estudios de satisfacción de las personas usuarias.
- Las encuestas de satisfacción del usuario incluyen preguntas a las personas usuarias respecto a la disponibilidad de metadatos.
- Existen medidas para evaluar la satisfacción de las personas usuarias principales con productos específicos (por ejemplo, encuestas e indicadores específicos de satisfacción del usuario, incluida la puntualidad y otras características a nivel de producto).""", 47),
    ("GRE-11.1", "GRE", 11, "11.1", """Se evalúan y validan de manera periódica las fuentes de datos, los datos integrados, los resultados intermedios y los resultados estadísticos finales.""", """- Se desarrollan y gestionan sistemas basados en estándares, para evaluar y validar las bases de datos origen, los datos integrados, los resultados intermedios y los resultados estadísticos finales.
- Los datos se verifican sistemáticamente y se comparan con los datos utilizados mediante otras fuentes de información y a través del tiempo.
- Los resultados estadísticos se comparan con otras fuentes de información existentes para asegurar su validez.""", 48),
    ("GRE-11.2", "GRE", 11, "11.2", """Se debe medir, evaluar y documentar los errores de muestreo. Los errores que no son de muestreo de ser posible, se deben describir y estimados.""", """- Existen procedimientos y lineamientos para medir y gestionar los errores estadísticos (por ejemplo, minimización de errores o equilibrios)
- Se identifican y describen las posibles fuentes de errores de muestreo.
- Se miden y evalúan los errores de muestreo.
- Se identifican, describen y evalúan los errores de no muestreo (errores en las fuentes de datos, errores de respuesta, errores de cobertura, errores relacionados con mediciones, procesamiento y análisis, etc.)
- Se analizan los errores estadísticos de muestreo y no muestreo, para identificar acciones de mejora.
- La información sobre los errores de muestreo y no muestreo se pone a disposición de las personas usuarias como parte de los metadatos.""", 49),
    ("GRE-11.3", "GRE", 11, "11.3", """Se debe llevar a cabo estudios y análisis de las revisiones y se utilizan para mejorar las fuentes de datos, los procesos estadísticos y los resultados. (Referirse al glosario de término en lo que respecta a la definición de "revisión")""", """- Se identifican claramente los datos y estadísticas preliminares de aquellos que ya están revisados.
- Se ponen a disposición de las personas usuarias, información sobre el momento, las razones y la naturaleza de las revisiones.
- La política de revisión sigue procedimientos estándar y transparentes en el contexto de cada encuesta.
- La información sobre la magnitud y los motivos de las revisiones, de los indicadores clave, se utiliza para mejorar los procesos estadísticos.
- Se provee información sobre la magnitud y los motivos de las revisiones, de los indicadores clave, y se dispone públicamente.""", 50),
    ("GRE-12.1", "GRE", 12, "12.1", """Las Unidades Organizacionales de Estadísticas deben cumplir con estándares internacionales sobre la oportunidad de las estadísticas u otros objetivos relacionados con este principio.""", """- La oportunidad en la publicación de las estadísticas de la ONE cumple con los estándares de difusión de los organismos internacionales como el Fondo Monetario Internacional (FMI) u otros que determinan la relevancia de la puntualidad (por ejemplo, los requisitos de la Agenda 2030 para los ODS).
- Se hace seguimiento a las divergencias respecto a los objetivos internacionales de puntualidad y, si no se cumplen, se toman medidas para garantizar su cumplimiento.
- En el momento de establecer los objetivos, se tienen en cuenta las divergencias generales entre la puntualidad y las otras dimensiones de la calidad (por ejemplo, precisión, costo y carga del encuestado).""", 51),
    ("GRE-12.2", "GRE", 12, "12.2", """La relación con los proveedores de datos debe ser gestionada con respecto a las necesidades de oportunidad y puntualidad.""", """- Existen acuerdos con los proveedores de los datos, sobre las fechas de entrega acordadas y el formato a utilizarse.
- Existen procedimientos para asegurar el flujo efectivo y oportuno de datos de los proveedores hacia la ONE.
- Existen procedimientos de seguimiento para garantizar la recepción oportuna de los datos.""", 52),
    ("GRE-12.3", "GRE", 12, "12.3", """Se deben publicar resultados preliminares de las estadísticas cuando su precisión y confiabilidad sean aceptables de acuerdo con los criterios de calidad, metodologías naciones e internacionales.""", """- Se considera y evalúa la posibilidad y la necesidad de publicar datos estadísticos preliminares, al mismo tiempo que se considera la precisión y confiabilidad de la información.
- Las personas usuarias reciben información apropiada sobre la calidad de las estadísticas preliminares.
- Los resultados preliminares se revisan de acuerdo con la política de revisión establecida.
- Los resultados finales se distinguen claramente de los resultados preliminares.""", 53),
    ("GRE-12.4", "GRE", 12, "12.4", """Se debe medir y supervisar la puntualidad, de acuerdo con las fechas de lanzamiento planificadas, como las establecidas en un calendario de publicaciones.""", """- La puntualidad, o la relación de cumplimiento de la puntualidad (es decir, la tasa de estadísticas publicadas a tiempo), se mide de acuerdo con lo que se establece en el calendario de publicación. El establecimiento del calendario de publicación debe ocurrir al menos 3 meses antes de la publicación de las estadísticas relevantes.
- La información sobre la puntualidad de las estadísticas publicadas se discute con la dirección y se pone a disposición de las personas usuarias.""", 54),
    ("GRE-13.1", "GRE", 13, "13.1", """Las estadísticas y sus metadatos deben presentarse de manera que se facilite la interpretación adecuada y las comparaciones significativas.""", """- Las estadísticas se presentan de manera clara y comprensible. (Referirse al glosario de términos en lo que respecta a la definición de "claridad" e "interpretabilidad")
- Las guías que describen el contenido apropiado, los formatos y los estilos de presentación preferidos (diseño y claridad de los textos, tablas y gráficos) de los resultados de una ONE y UOE, están disponibles y se usan en las publicaciones de las estadísticas y de las bases de datos.
- Los datos estadísticos publicados están abiertos para uso libre, siempre que se haga referencia a la agencia responsable de su elaboración.
- Se ponen a disposición del público los documentos metodológicos actualizados (sobre los conceptos, el alcance, las clasificaciones, las bases y fuentes de datos, los métodos de recolección y las técnicas estadísticas), así como las medidas de calidad y el programa de trabajo de la ONE y las UOE.
- Los textos explicativos que acompañan a los datos se revisan para mayor claridad y legibilidad. (Notas técnicas o metodológicas, anexos técnicos, etc.)
- Se incluyen comparaciones de los datos en las publicaciones cuando es adecuado.
- Los datos preliminares y los datos revisados(definitivos) ​​se identifican y explican en las estadísticas publicadas.
- Se publican los metadatos más relevantes, junto con los resultados estadísticos, para comprender y utilizar las estadísticas.
- Existe una política para archivar las estadísticas ya publicadas.""", 55),
    ("GRE-13.2", "GRE", 13, "13.2", """Debe existir una política u estrategia pública de difusión de datos.""", """- En la medida de lo posible, se debe suministrar apoyo técnico para el análisis de datos a solicitud de las personas usuarias y según los acuerdos, hacerlos públicos.
- Se informa al público que, cuando sea posible, se pueden proporcionar a solicitud resultados personalizados, estadísticas que no se difunden de manera rutinaria y series de tiempo más largas, y se les indica a los usuarios cómo realizar estas solicitudes. Los resultados estadísticos 
de estas consultas se hacen públicos siempre que sea posible y se acompañan de notas que informan sobre su correcto uso e interpretación.
- Los catálogos de publicaciones y otros servicios se ponen a disposición de las personas usuarias.
- Se pone a disposición de las personas usuarias de la 
información el costo relacionado para brindar servicios estadísticos complementarios.
- Se ha desarrollado y acordado una estrategia con las personas usuarias estratégicas para la publicación de los datos y microdatos anonimizados.""", 56),
    ("GRE-13.3", "GRE", 13, "13.3", """Se utiliza tecnología de información y comunicación moderna para facilitar el acceso de manera práctica a las estadísticas.""", """- Las estadísticas se difunden por varios canales, adecuados para todas las personas usuarias, siendo el sitio web de la ONE y las instituciones que conforman el SEN el canal principal.
- Las personas usuarias pueden extraer grupos de datos, a partir de bases de datos estadísticas publicadas en la web, en los formatos más apropiados y comunes (xlsx, cvc, html, etc.).
- Los datos estadísticos se pueden descargar mediante una interfaz de programación de aplicaciones (API), de manera rápida, con cruces sencillos desde un aplicativo en línea, que se puedan consultar en diferentes dispositivos.
- Las estadísticas se difunden de manera que facilitan la divulgación por parte de los medios de comunicación.
- Se establecen acuerdos con personas usuarias clave para la transmisión eficiente y periódica de las estadísticas y los datos.
- Existe la forma de acceder (componente tecnológico) a datos anonimizados  o mecanismos para acceder a  microdatos.
- Se ha considerado explícitamente las divergencias entre la accesibilidad y la confidencialidad estadística (es decir, el nivel de detalle en las tablas).""", 57),
    ("GRE-13.4", "GRE", 13, "13.4", """Se debe permitir el acceso a los microdatos con fines de investigación, sujeto a reglas y protocolos específicos sobre confidencialidad estadística, los cuales deben estar publicados en el sitio web de la Unidad Organizacional de Estadísticas.""", """- La ONE y las UOE controlan o supervisan el acceso de los investigadores a los microdatos al proporcionarlos en un entorno seguro..
- Se consulta a los investigadores sobre la efectividad de los acuerdos de acceso a los microdatos.
- La infraestructura para el acceso remoto a los microdatos está disponible, con el control adecuado.""", 58),
    ("GRE-13.5", "GRE", 13, "13.5", """La ONE debe contar con una estrategia y mecanismos específicos para hacer del conocimiento público los diferentes canales disponibles para acceder a la información estadística.""", """- La ONE y los otros productores del SEN tienen una estrategia para 
administrar las relaciones con los medios y mantener un contacto frecuente con los medios de comunicación.
- La ONE y las UOE organizan jornadas de capacitación y divulgación para los periodistas, de manera periódica.
- La ONE y las UOE organizan capacitación para los estudiantes sobre cómo usar las estadísticas.
- Se incentiva a productores y a las personas usuarias a publicar artículos sobre temas estadísticos y sobre cómo se deben usar las estadísticas de manera adecuada.""", 59),
    ("GRE-13.6", "GRE", 13, "13.6", """La ONE cuenta con un área específica de relacionamiento que brinda soporte a las personas usuarias de manera oportuna.""", """- Los servicios de soporte a las personas usuarias están disponibles para proporcionarles asistencia rápida que permita ayudarles a acceder e interpretar los datos.
- Los servicios de asistencia al usuario cuentan con el personal adecuado para atender una amplia gama de personas usuarias.""", 60),
    ("GRE-13.7", "GRE", 13, "13.7", """La evaluación de calidad de los productos estadísticos debe ser de información pública para las personas usuarias.""", """- Se definen los informes de calidad estandar armonizados para las operaciones estadísticas de la ONE.
- Las estadísticas publicadas van acompañadas de informes de calidad estándar, que incluyen información sobre la periodicidad de las estadísticas, las fuentes de los datos, los métodos de producción y su calidad (precisión y fiabilidad, puntualidad y oportunidad, coherencia y comparabilidad, accesibilidad y claridad).
- Los resultados de las evaluaciones de calidad o revisiones se hacen públicos.""", 61),
    ("GRE-14.1", "GRE", 14, "14.1", """Se deben utilizar estándares internacionales, regionales y nacionales con respecto a definiciones, unidades, variables y clasificaciones.""", """- La ONE promueve la adopción de estándares nacionales, regionales o internacionales.
- Existen directrices, un repositorio común de conceptos estadísticos, definiciones de unidades y variables y clasificaciones y otros mecanismos.
- Se realiza seguimiento al cumplimiento de las normas internacionales, regionales o nacionales para la producción estadísticas. Cualquier desviación de estos estándares se hace explícita y se incluye en los metadatos, junto con las razones de tales desviaciones.""", 62),
    ("GRE-14.2", "GRE", 14, "14.2", """Deben existir procedimientos o directrices para garantizar y controlar la coherencia y consistencia interna, intra-sectorial e intersectorial.""", """- Las estadísticas derivadas de diferentes fuentes o con diferentes periodicidades (por ejemplo, mensual, trimestral y anual), se comparan, se explican y se revisan las concordancias de las diferencias, según corresponda.
- Se promueve la cooperación y el intercambio de conocimientos entre programas y temáticas estadísticas individuales.
- Los procedimientos y directrices específicos del proceso estadístico están disponibles para asegurar que los resultados sean coherentes internamente.
- Antes de lanzar nuevas estadísticas o programas estadísticos, se analiza la relación conceptual y metodológica con las estadísticas existentes.
- Los resultados estadísticos se comparan con otras fuentes estadísticas o registros administrativos que proporcionan la misma información o similar sobre el mismo tema, y las divergencias se identifican y explican a las personas usuarias.
- Se desarrollan procedimientos o lineamientos internos para garantizar y monitorear la coherencia y consistencia interna.
- Se elaboran procedimientos y directrices para garantizar que se puedan combinar los resultados de diferentes fuentes. El cumplimiento se evalúa periódicamente.""", 63),
    ("GRE-14.3", "GRE", 14, "14.3", """Se debe mantener una comparabilidad de las estadísticas durante un período de tiempo razonable y su comparabilidad entre áreas geográficas.""", """- Los cambios en los métodos de compilación de los datos están claramente identificados, descritos y medidos para facilitar la interpretación de los resultados.
- La metadata en general incluye una sección sobre la evaluación de la consistencia interna y la comparabilidad a lo largo del tiempo y si es pertinente con otras estadísticas relacionadas con el tema.
- Se explican las rupturas de la serie de tiempo y se ponen a disposición del público los métodos para garantizar el empalme de las series durante el período de tiempo.
- Se evalúan los efectos de los cambios en las metodologías en las estimaciones finales y se proporciona información apropiada a las personas usuarias.
- Los cambios significativos en la sociedad y los fenómenos a medir se reflejan en los cambios apropiados en los conceptos, clasificaciones, definiciones y poblaciones objetivo.
- Se explican las diferencias dentro de áreas geográficas o a nivel de país debido a diferentes conceptos o metodologías.""", 64),
    ("GRE-15.1", "GRE", 15, "15.1", """Se debe encontrar definido y documentado correctamente el sistema de gestión de metadatos de la ONE y las UOE.""", """- Se cuenta con una estrategia, lineamientos y procedimientos para la gestión y difusión de los metadatos.
- La gestión de los metadatos se reconoce como responsabilidad de todo el personal involucrado en la operación estadística.""", 65),
    ("GRE-15.2", "GRE", 15, "15.2", """Los metadatos se deben documentar, archivar y difundir de acuerdo con las normas internacionalmente aceptadas.""", """- Se utilizan estándares internacionales, regionales, nacionales o internos para la documentación, la gestión y el archivo de los metadatos.
- Existen procedimientos para asegurar que los metadatos se documentan de acuerdo con los estandares internacionales  y se actualizan periódicamente.
- Los metadatos están disponibles al mismo tiempo que los datos y las estadísticas a las que pertenecen.
- Existe una forma sistemática de archivar los metadatos que también asegura que estén disponibles para su reutilización en el futuro.
- Se pone a disposición del público un glosario de conceptos estadísticos.""", 66),
    ("GRE-15.3", "GRE", 15, "15.3", """Existen programas de capacitación y desarrollo del personal relacionados con la gestión de metadatos y con los sistemas de información y documentación.""", """- Los responsables de los procesos estadísticos están capacitados para documentar adecuadamente los datos y describir los procesos relevantes.""", 67),
]

# (codigo_verificacion, elemento_codigo_padre, texto_elemento, orden)
# Los 252 "Código de elemento" del Excel (columna "Elemento que deben de
# asegurarse"), cada uno bajo su Requisito de cumplimiento (los 67 de
# ELEMENTOS). ESTE es el nivel donde se marca el cumplimiento, igual que el
# Excel original.
VERIFICACIONES: list[tuple] = [
    ('GEI-1.1.1', 'GEI-1.1', """La cultura y tradición profesional aseguran la imparcialidad y la objetividad de las estadísticas producidas por las agencias estadísticas, independientemente de la existencia o ausencia de leyes o disposiciones formales.""", 1),
    ('GEI-1.1.2', 'GEI-1.1', """Se reconoce la objetividad e imparcialidad de las estadísticas oficiales (y no es puesta en duda) por observadores neutrales y el público en general (por ejemplo, se encuentra medida con indicadores de imagen institucional).""", 2),
    ('GEI-1.2.1', 'GEI-1.2', """Existen protocolos éticos o un código de conducta para garantizar la imparcialidad y la objetividad.""", 3),
    ('GEI-1.3.1', 'GEI-1.3', """Las fuentes, los conceptos, los métodos, los procesos para el desarrollo, la producción y la difusión de los datos se eligen sobre la base de consideraciones, principios y buenas prácticas estadísticas nacionales e internacionales.""", 4),
    ('GEI-1.4.1', 'GEI-1.4', """Existe un calendario público de publicación que contiene toda la información sobre las publicaciones planeadas por la ONE en el período de los próximos 12 meses.""", 5),
    ('GEI-1.4.2', 'GEI-1.4', """Existe un calendario público de publicación que contiene toda la información sobre las publicaciones planeadas por el SEN en el período de los próximos 12 meses.""", 6),
    ('GEI-1.4.3', 'GEI-1.4', """Las estadísticas se publican en la fecha y hora (cuando corresponde) determinadas en el calendario de publicación""", 7),
    ('GEI-1.4.4', 'GEI-1.4', """Los cambios en el calendario de publicación se anuncian con antelación y se explican los motivos de los cambios.""", 8),
    ('GEI-1.4.5', 'GEI-1.4', """El intercambio de resultados estadísticos antes de la publicación oficial (una "presentación previa privilegiada") se mantiene al mínimo y se encuentra debidamente justificado y estrictamente controlado y documentado, y corresponde solo a fines informativos.""", 9),
    ('GEI-1.5.1', 'GEI-1.5', """Existe una política normada y documentada sobre cómo corregir los datos publicados cuando se detectan errores.""", 10),
    ('GEI-1.5.2', 'GEI-1.5', """La política de tratamiento de errores está disponible al público.""", 11),
    ('GEI-1.5.3', 'GEI-1.5', """La corrección de errores para la operación estadística involucrada es documentada y de conocimiento público""", 12),
    ('GEI-2.1.1', 'GEI-2.1', """Las reglas que se aplican para nombrar y asignar el cargo de director(a) de la Oficina Nacional de Estadísticas, se basan en competencias profesional, son transparentes y están libres de consideraciones políticas.""", 13),
    ('GEI-2.2.1', 'GEI-2.2', """Las leyes y regulaciones bajo las cuales operan las unidades estadísticas dentro de los ministerios, departamentos y otras agencias en los diferentes niveles del gobierno, garantizan la independencia profesional de la ONE y de otros productores de estadísticas oficiales.""", 14),
    ('GEI-2.2.2', 'GEI-2.2', """En el caso de no contar con una ley ni una disposición formal en la cual se declare que es necesaria la independencia profesional de las agencias estadísticas, de todas maneras, existen una cultura y tradición profesional, así como precedentes históricos o convenciones, en donde se reconoce esta independencia como esencial para la credibilidad de los resultados de los organismos de estadística.""", 15),
    ('GEI-2.3.1', 'GEI-2.3', """El jefe de la Oficina Nacional de estadísticas tiene una posición jerárquica suficientemente alta para garantizar el diálogo y el liderazgo frente a las autoridades políticas y los organismos gubernamentales.""", 16),
    ('GEI-2.4.1', 'GEI-2.4', """El jefe de la ONE y los jefes de las unidades estadísticas del gobierno que producen estadísticas oficiales, toman decisiones de manera independiente sobre el desarrollo, la producción y la difusión de estadísticas oficiales, teniendo en cuenta las consideraciones profesionales, los métodos, los estándares y los procedimientos estadísticos.""", 17),
    ('GEI-2.4.2', 'GEI-2.4', """La presentación de informes y rendición de cuentas de la ONE a los órganos gubernamentales superiores, a los ministerios o departamentos y a otras agencias, no afecta su independencia profesional.""", 18),
    ('GEI-3.1.1', 'GEI-3.1', """La información sobre el origen y las fuentes de los datos, los conceptos y los métodos utilizados para el desarrollo, la producción y la difusión de las estadísticas oficiales, se ponen a disposición del público.""", 19),
    ('GEI-3.1.2', 'GEI-3.1', """La información sobre estándares estadísticos está disponible al público.""", 20),
    ('GEI-3.1.3', 'GEI-3.1', """Se notifica con anticipación al público, sobre los cambios importantes en la metodología, las fuentes de los datos o las técnicas estadísticas utilizadas.""", 21),
    ('GEI-3.1.4', 'GEI-3.1', """La política de difusión se comparte con todo el público.""", 22),
    ('GEI-3.1.5', 'GEI-3.1', """Se divulgan públicamente los privilegios de acceso previo a los resultados estadísticos.""", 23),
    ('GEI-3.2.1', 'GEI-3.2', """Existe una ley o alguna otra disposición normativa vigente que asegure el manejo adecuado por parte de la ONE, con respecto a la confidencialidad estadística y a la seguridad de la información recibida por parte de los proveedores de datos y de los encuestados.""", 24),
    ('GEI-3.2.2', 'GEI-3.2', """Existe una ley o alguna otra disposición normativa vigente que asegure el manejo adecuado por parte de los miembros del SEN, con respecto a la confidencialidad estadística y a la seguridad de la información recibida por parte de los proveedores de datos y de los encuestados.""", 25),
    ('GEI-3.3.1', 'GEI-3.3', """Se proporcionan directrices e instrucciones, a todo el personal de la ONE, sobre la protección de la confidencialidad estadística de la información a lo largo del proceso estadístico.""", 26),
    ('GEI-3.3.2', 'GEI-3.3', """Se llevan a cabo programas de capacitación periódicos y continuos para todo el personal sobre el concepto de confidencialidad en las estadísticas y las buenas prácticas, para asegurar la privacidad de la información que se maneja.""", 27),
    ('GEI-3.3.3', 'GEI-3.3', """La estructura organizativa y los acuerdo para el desarrollo y para la implementación de prácticas que garantizan la confidencialidad estadística, son adecuados para hacer frente a las necesidades estadísticas.""", 28),
    ('GEI-3.3.4', 'GEI-3.3', """El personal firma, desde el momento de su nombramiento, acuerdos de compromiso para mantener la confidencialidad de la información que se mantienen incluso después de que el personal deja de trabajar en la agencia estadística.""", 29),
    ('GEI-3.4.1', 'GEI-3.4', """Existen disposiciones legales o de otra índole que permiten aplicar 
sanciones administrativas, penales y disciplinarias por incumplir la confidencialidad estadística.""", 30),
    ('GEI-3.4.2', 'GEI-3.4', """La información sobre las disposiciones y sanciones al incumplimiento de la confidencialidad estadística se comparte con todo el personal de las agencias estadísticas y se ponen a disposición de todo el público.""", 31),
    ('GEI-3.5.1', 'GEI-3.5', """Existe una política de seguridad de las tecnologías de la información (TI) y es conocida por todo el personal.""", 32),
    ('GEI-3.5.2', 'GEI-3.5', """Se implementan medidas y procesos de seguridad física adecuados para asegurar la seguridad de los datos y de las bases de información, siguiendo la política de seguridad de TI y en concordancia con las mejores prácticas y los estándares internacionales.""", 33),
    ('GEI-3.5.3', 'GEI-3.5', """Se realizan periódicamente auditorías de seguridad del sistema de seguridad de los datos.""", 34),
    ('GEI-3.5.4', 'GEI-3.5', """Todos los accesos a los repositorios de datos y los canales de transmisión de los datos son monitoreados.""", 35),
    ('GEI-3.5.5', 'GEI-3.5', """Se evalúa el riesgo de incumplimiento a la seguridad de la información, para la transferencia de los datos y se aplican los procedimientos adecuados para eliminar o minimizar este riesgo.""", 36),
    ('GEI-4.1.1', 'GEI-4.1', """La política de calidad estadística y el compromiso de la ONE con esta es conocida y comprendida públicamente.""", 37),
    ('GEI-4.1.2', 'GEI-4.1', """La ONE promueve el interés mutuo por la calidad con todo su personal e incluye información sobre las discrepancias de los atributos que afectan el programa de trabajo estadístico.""", 38),
    ('GEI-4.1.3', 'GEI-4.1', """La ONE, ponen a disposición de las personas usuarias externas sus normas de calidad o una versión resumida de ellas.""", 39),
    ('GEI-4.2.1', 'GEI-4.2', """Las metodologías y los procesos se documentan de manera regular.""", 40),
    ('GEI-4.2.2', 'GEI-4.2', """Se realizan intercambios de buenas prácticas entre las diferentes agencias de estadísticas.""", 41),
    ('GEI-4.2.3', 'GEI-4.2', """Existen procedimientos para asegurar que la documentación requerida sobre la calidad sea actualizada periódicamente.""", 42),
    ('GEI-4.2.4', 'GEI-4.2', """Existe un plan de aseguramiento de la calidad o un mecanismo similar para describir los estándares de trabajo, las obligaciones formales (como las leyes y las reglas internas) y las acciones de control de calidad para prevenir, monitorear y evaluar los posibles errores y controlar el proceso de producción estadística.""", 43),
    ('GEI-4.2.5', 'GEI-4.2', """Se utilizan planes de trabajo, cronogramas, formularios o plantillas estándar para facilitar la actualización de la documentación de los procedimientos y acciones de aseguramiento de la calidad, de manera consistente.""", 44),
    ('GEI-4.2.6', 'GEI-4.2', """Las agencias de estadística utilizan un marco nacional de aseguramiento de la calidad (NQAF) como base para las evaluaciones de calidad periódicas (autoevaluaciones u otras evaluaciones).""", 45),
    ('GEI-4.2.7', 'GEI-4.2', """Las agencias de estadística utilizan un NQAF que se basa en alguno de los marcos globales o regionalmente aceptados.""", 46),
    ('GEI-4.2.8', 'GEI-4.2', """Los sistemas o marcos generales de calidad, como la Gestión de Calidad Total (TQM) y los de la Organización Internacional de Normalización (ISO) 9000, se utilizan junto con el NQAF.""", 47),
    ('GEI-4.2.9', 'GEI-4.2', """Se siguen las iniciativas de calidad de los organismos estadísticos internacionales y regionales, como el Sistema Estadístico Europeo (SEE), según corresponda.""", 48),
    ('GEI-4.3.1', 'GEI-4.3', """Se le asigna la responsabilidad de la gestión de calidad a un gerente de calidad, comité de calidad, unidad o grupo de expertos o asesores.""", 49),
    ('GEI-4.4.1', 'GEI-4.4', """Se establece un grupo de trabajo sobre la calidad de los datos en toda la agencia estadística y se reúne periódicamente.""", 50),
    ('GEI-4.4.2', 'GEI-4.4', """Los asuntos sobre la calidad son discutidos por la gerencia y con la agencia estadística, de manera periódica (por ejemplo, en una reunión anual de revisión de la calidad)""", 51),
    ('GEI-4.5.1', 'GEI-4.5', """Se definen, producen y emiten lineamientos para la implementación de la gestión de la calidad que: Describen los principios y el marco de calidad que se sigue; Describen todo el proceso estadístico e identifican la documentación relevante para cada etapa de la producción estadística; Describen los métodos para realizar seguimiento a la calidad en cada etapa del proceso de producción estadística; Identifican los indicadores (medidas de calidad) para evaluar la calidad de las principales etapas de producción, incluidos los indicadores para las fuentes de los datos.""", 52),
    ('GEI-4.5.2', 'GEI-4.5', """Se ponen a disposición de todo el público, los lineamientos, los manuales metodológicos y los manuales sobre las buenas prácticas para el aseguramiento de la calidad.""", 53),
    ('GEI-4.5.3', 'GEI-4.5', """Existen mecanismos para asegurar la calidad de la recopilación de los datos (incluido el uso de registros administrativos y los provenientes de otras fuentes) y la calidad en la edición de estos datos.""", 54),
    ('GEI-4.6.1', 'GEI-4.6', """Se preparan, publican y actualizan periódicamente, informes de calidad para que sean de utilidad para ofrecer una perspectiva al productor y a las personas usuarias, según corresponda.""", 55),
    ('GEI-4.6.2', 'GEI-4.6', """Se definen, calculan y monitorean indicadores que permiten el seguimiento y el logro de mejoras en la calidad. Algunos ejemplos de indicadores de calidad incluyen: Referencias en los medios, visitas a las páginas web, resultados de las encuestas de satisfacción a las personas usuarias (miden relevancia); Desviaciones estándar y otras medidas de precisión, tasas de respuesta (precisión); Número y tamaño de las revisiones (confiabilidad); Período de tiempo entre la finalización de un período de referencia y la difusión de las estadísticas (oportunidad); Tasa de resultados estadísticos publicados en la fecha anunciada (puntualidad); Sobrecarga a los encuestados.""", 56),
    ('GEI-4.7.1', 'GEI-4.7', """Se realizan revisiones periódicas a la calidad de los productos y procesos principales, para evaluar el cumplimiento de las directrices internas y de los estándares internacionales.""", 57),
    ('GEI-4.7.2', 'GEI-4.7', """Se crean equipos de revisión, en los que pueden participar expertos internos y externos.""", 58),
    ('GEI-4.7.3', 'GEI-4.7', """Los revisores internos del organismo de estadística están capacitados en métodos y herramientas de auditoría.""", 59),
    ('GEI-4.7.4', 'GEI-4.7', """Las acciones de mejora derivadas del resultado de las revisiones de calidad se definen y programan para su implementación.""", 60),
    ('GEI-4.7.5', 'GEI-4.7', """La alta gerencia está informada de los resultados de las revisiones para realizar seguimiento a las acciones de mejora.""", 61),
    ('GEI-4.7.6', 'GEI-4.7', """Se realizan evaluaciones comparativas, de los procesos estadísticos principales, con otras agencias estadísticas para identificar buenas prácticas.""", 62),
    ('GEI-4.7.7', 'GEI-4.7', """Existen procedimientos para monitorear y gestionar la calidad de las diferentes etapas de la producción estadística, de acuerdo con el Modelo Genérico del Proceso Estadístico (GSBPM).""", 63),
    ('GEI-4.7.8', 'GEI-4.7', """Se examinan sistemáticamente las confrontaciones entre los principios de calidad (por ejemplo, el balance entre la precisión, la puntualidad y los costos).""", 64),
    ('GEI-4.7.9', 'GEI-4.7', """Se realizan revisiones de calidad por parte de expertos externos (también por parte de organizaciones internacionales). Por ejemplo, revisiones de los dominios estadísticos clave (informes del Fondo Monetario Internacional sobre la observancia de los Estándares y Códigos (ROSC)) u otras revisiones como revisiones por pares, auditorías externas y revisiones periódicas.""", 65),
    ('GEI-5.1.1', 'GEI-5.1', """Existe una estrategia de movilización de recursos, como una Estrategia Nacional para el Desarrollo de Estadísticas (ENDE).""", 66),
    ('GEI-5.1.2', 'GEI-5.1', """El plan de trabajo anual es viable dados los recursos disponibles.""", 67),
    ('GEI-5.1.3', 'GEI-5.1', """Se miden los costos (humanos y financieros) de cada etapa de la producción estadística.""", 68),
    ('GEI-5.2.1', 'GEI-5.2', """Se emplean tecnología de la información adecuadas para incrementar la eficiencia.""", 69),
    ('GEI-5.2.2', 'GEI-5.2', """Se busca la estandarización, la integración y la automatización de la producción y de la difusión de estadísticas para incrementar la eficiencia y reducir los costos.""", 70),
    ('GPE-6.1.1', 'GPE-6.1', """La estrategia para las pruebas piloto se incluye en la fase de diseño del modelo de proceso estadístico.""", 71),
    ('GPE-6.1.2', 'GPE-6.1', """Los procedimientos para la recolección de los datos y las herramientas e instrumentos de recopilación, como los cuestionarios electrónicos, se prueban y ajustan (si es necesario y posible) antes de la operación de campo, para mejorar la captura, minimizando la carga al informante.""", 72),
    ('GPE-6.1.3', 'GPE-6.1', """Los cuestionarios de las encuestas se prueban utilizando métodos apropiados (por ejemplo, prueba piloto, grupos focales, etc).""", 73),
    ('GPE-6.1.4', 'GPE-6.1', """Los sistemas de recopilación de datos administrativos y de otro tipo se prueban antes de su utilización.""", 74),
    ('GPE-6.1.5', 'GPE-6.1', """Los procedimientos para el tratamiento y procesamiento de los datos se prueban y ajustan, de ser necesario y posible, antes de su aplicación, con base en experiencias anteriores de la operación estadística y resultados de la prueba piloto, entre otras.""", 75),
    ('GPE-6.1.6', 'GPE-6.1', """La evaluación de la prueba piloto es tenida en cuenta para las mejoras e implementación del proceso de produción de la operación estadística.""", 76),
    ('GPE-6.1.7', 'GPE-6.1', """En el caso de integrar datos de una o más fuentes, se prueba la calidad de los procedimientos de integración.""", 77),
    ('GPE-6.2.1', 'GPE-6.2', """La ONE y las UOE tienen procedimientos y lineamientos consistentes, coherentes, claros, accesibles y transparentes para todas las etapas de la producción de estadísticas.""", 78),
    ('GPE-6.2.2', 'GPE-6.2', """La documentación de los procesos de producción sigue el modelo GSBPM.""", 79),
    ('GPE-6.2.3', 'GPE-6.2', """Existe una política clara para archivar los datos y las estadísticas y esta se cumple.""", 80),
    ('GPE-6.2.4', 'GPE-6.2', """Los procedimientos estadísticos emplean técnicas estadísticas reconocidas internacionalmente.""", 81),
    ('GPE-6.2.5', 'GPE-6.2', """Se revisan y validan todas las fuentes de datos, para identificar posibles problemas, errores y discrepancias, como valores atípicos, datos faltantes y errores de codificación.""", 82),
    ('GPE-6.2.6', 'GPE-6.2', """Se analizan los efectos de la edición e imputación de datos, y sus efectos son parte de la información pública de la operación estadística, como parte de la evaluación de calidad de la recopilación de los datos.""", 83),
    ('GPE-6.2.7', 'GPE-6.2', """Todas las bases de datos estadísticas están diseñadas y organizadas de tal manera que permiten y facilitan el cruce de la información, utilizando identificadores únicos para cada unidad estadística, según corresponda, y a su vez se garantiza la seguridad y la privacidad de los datos.""", 84),
    ('GPE-6.3.1', 'GPE-6.3', """La ONE y las UOE cuentan con herramientas y lineamientos, conocidos por las personas usuarias, y los utilizan para evaluar la calidad de los datos provenientes de registros administrativos y de otras fuentes de datos.""", 85),
    ('GPE-6.3.2', 'GPE-6.3', """Se desarrollan e implementan procesos y aplicaciones de software adecuados para la recopilación, procesamiento y análisis de los datos de registros administrativos y de otras fuentes de datos, que se utilizarán con fines estadísticos.""", 86),
    ('GPE-6.3.3', 'GPE-6.3', """Los propietarios y titulares de los registros administrativos y de otras fuentes de datos informan  a la ONE y las UOE  de cualquier cambio realizado en el proceso de producción de sus datos.""", 87),
    ('GPE-6.3.4', 'GPE-6.3', """La ONE y las UOE disponen de metadatos relacionados con los registros administrativos y de las otras fuentes de datos, incluidos los conceptos, definiciones, clasificaciones, cobertura poblacional para el objetivo y otros aspectos metodológicos.""", 88),
    ('GPE-6.3.5', 'GPE-6.3', """Existe documentación que describe el cumplimiento de la calidad por parte de los registros administrativos y de otras fuentes de datos, en términos de definiciones, conceptos, cobertura, etc.""", 89),
    ('GPE-6.4.1', 'GPE-6.4', """Existe una política, directrices y/o principios para las revisiones, estos son de conocimiento público y se cumplen.""", 90),
    ('GPE-6.4.2', 'GPE-6.4', """Las revisiones de las estadísticas publicadas van acompañadas de metadatos que proporcionan las explicaciones necesarias.""", 91),
    ('GPE-6.5.1', 'GPE-6.5', """Existen y se siguen las políticas y estándares para mantener y actualizar los metadatos.""", 92),
    ('GPE-6.5.2', 'GPE-6.5', """El proceso de producción estadística y de sus metadatos relacionados se realiza de manera paralela.""", 93),
    ('GPE-6.5.3', 'GPE-6.5', """Los metadatos se capturan a lo largo del proceso estadístico siguiendo los lineamientos del proceso estadistico y se almacenan en un sistema de gestion de metadatos.""", 94),
    ('GPE-7.1.1', 'GPE-7.1', """Las metodologías son revisadas y  evaluadas en función de las fuentes de datos disponibles y las actualizaciones en procesos estadísticos nacionales, regionales y/o internacionales disponibles.""", 95),
    ('GPE-7.1.2', 'GPE-7.1', """Los diseños muéstrales se basan en metodologías sólidas y datos poblacionales lo más actualizados posibles.""", 96),
    ('GPE-7.1.3', 'GPE-7.1', """Los procedimientos de edición estadística y los métodos de imputación utilizados, se basan en una metodología sólida conocida para las personas usuarias.""", 97),
    ('GPE-7.2.1', 'GPE-7.2', """La ONE cuenta con una estructura organizativa que asegure el desarrollo y aplicación de métodos estadísticos sólidos en las distintas etapas del proceso estadístico y para las distintas operaciones estadísticas""", 98),
    ('GPE-7.2.2', 'GPE-7.2', """Las metodologías son públicas y contienen todos los detalles del proceso estadístico asegurando procesos comparables, consistentes, coherentes y replicables.""", 99),
    ('GPE-7.2.3', 'GPE-7.2', """Se planifican, implementan y publican procedimientos de seguimiento adecuados para el caso de la no respuesta.""", 100),
    ('GPE-7.2.4', 'GPE-7.2', """La ONE, de contar con la potestad, revisa las metodologías utilizadas por organismos independientes para la recolección de los datos y la producción de estadísticas.""", 101),
    ('GPE-7.3.1', 'GPE-7.3', """El personal de la ONE se contrata en función de sus antecedentes académicos, cualificaciones y experiencia adecuada.""", 102),
    ('GPE-7.3.2', 'GPE-7.3', """Se encuentran especificados, todos los requisitos de cualificaciones requeridos para todos los cargos.""", 103),
    ('GPE-7.3.3', 'GPE-7.3', """Existen programas de capacitación, formación y desarrollo para garantizar que el personal adquiere y actualiza continuamente sus conocimientos metodológicos.""", 104),
    ('GPE-7.3.4', 'GPE-7.3', """Las habilidades del personal se actualizan periódicamente, de manera que el personal tiene las capacidades para utilizar nuevas fuentes de datos y nuevas herramientas y tiene la posibilidad de cambiar de posición laboral.""", 105),
    ('GPE-7.3.5', 'GPE-7.3', """Se recomienda y promueve la asistencia del personal a cursos de capacitación relevantes y a conferencias nacionales o internacionales.""", 106),
    ('GPE-7.4.1', 'GPE-7.4', """Si existe la oportunidad, se evalúa con frecuencia el uso de distintas fuentes alternativas de datos, incluidas encuestas, los censos, los registros administrativos, el big data y otras fuentes de datos.""", 107),
    ('GPE-7.4.2', 'GPE-7.4', """Se evalúa la calidad de los registros administrativos u otras fuentes de datos para su uso estadístico. Idealmente, cuando se usan datos de registros administrativos, se debe asegurar que: El universo poblacional de los registros es consistente con los requerimientos para la producción de las estadísticas; Las clasificaciones usadas son las apropiadas; Los conceptos base de los registros son los apropiados; Los registros están completos y actualizados; La cobertura geográfica es completa y las unidades de medición están definidas e identificadas adecuadamente.""", 108),
    ('GPE-7.4.3', 'GPE-7.4', """Existe la definicion de los lineamientos metodológicos a seguir en la utilización de otras fuentes de datos no estructurados (como el Big data), en particular relacionados con la población estadística y la veracidad y volatilidad de dichos datos.""", 109),
    ('GPE-7.5.1', 'GPE-7.5', """Se establece cooperación con la comunidad científica, por ejemplo, a través de conferencias, talleres, grupos de trabajo y cursos de capacitación, para discutir desarrollos metodológicos y tecnológicos relevantes (por ejemplo, con respecto a la explotación de nuevas fuentes de datos).""", 110),
    ('GPE-7.5.2', 'GPE-7.5', """Existen acuerdos con instituciones académicas para la cooperación e intercambio de personal calificado.""", 111),
    ('GPE-7.5.3', 'GPE-7.5', """El personal de la ONE realiza actividades de cooperación en temas metodológicos con sus pares a nivel internacional.""", 112),
    ('GPE-7.5.4', 'GPE-7.5', """Se incentiva la participación frecuente en presentaciones y conferencias nacionales e internacionales relevantes para el intercambio de conocimientos y experiencias.""", 113),
    ('GPE-8.1.1', 'GPE-8.1', """Existe un sistema para registrar los costos y el tiempo utilizado para obtener los productos estadísticos, y de ser posible, se estima el tiempo empleado en las etapas principales del proceso.""", 114),
    ('GPE-8.1.2', 'GPE-8.1', """Los costos de producir las estadísticas están bien documentados en cada fase del proceso estadístico y se revisan periódicamente para evaluar la eficiencia de su producción.""", 115),
    ('GPE-8.1.3', 'GPE-8.1', """Se llevan a cabo análisis de costo-beneficio para determinar la combinación de cumplimiento más adecuada en términos de calidad de los datos.""", 116),
    ('GPE-8.1.4', 'GPE-8.1', """La necesidad de recolección de cada variable estadística se encuentra justificada en base a los objetivos y usos de la operación estadística.""", 117),
    ('GPE-8.1.5', 'GPE-8.1', """Existe un proceso de revisión continua que considera si un producto estadístico en particular todavía está operando de la manera más costo- eficiente para cumplir con los objetivos y usos establecidos para el mismo.""", 118),
    ('GPE-8.1.6', 'GPE-8.1', """Los instrumentos de recolección de los datos están diseñados de manera que minimizan la carga del informante, los costos y tiempos de procesamiento, maximizando la calidad de la captura de la información necesaria.""", 119),
    ('GPE-8.2.1', 'GPE-8.2', """Las demandas de nuevas estadísticas son evaluadas con respecto a la relevancia de los objetivos de la operación estadística, la disponibilidad de información y los costos asociados; además, se discuten con la administración, con base en los aportes de los persona usuarias y la cooperación con otros grupos de interés.""", 120),
    ('GPE-8.3.1', 'GPE-8.3', """Se realizan discusiones de manera frecuente, por parte de la gerencia sobre la utilidad de todas las estadísticas; las discusiones incluyen los aportes de los persona usuarias, tales como los resultados de las encuestas de satisfacción de las persona usuarias.""", 121),
    ('GPE-8.3.2', 'GPE-8.3', """El uso de diferentes productos estadísticos, incluidas las bases de datos estadísticas, se monitorea y evalúa para evaluar su relevancia.""", 122),
    ('GPE-8.3.3', 'GPE-8.3', """Las persona usuarias y los grupos de interés son informados y consultados sobre la posible no continuidad de algunos productos estadísticos.""", 123),
    ('GPE-8.4.1', 'GPE-8.4', """Existe una estrategia adecuada de TI, que se revisa y actualiza periódicamente para mejorar la eficacia y la eficiencia de los procesos estadísticos.""", 124),
    ('GPE-8.4.2', 'GPE-8.4', """La arquitectura e infraestructura de TI y el hardware, se revisan y actualizan periódicamente, y se identifican las posibilidades de innovación y modernización.""", 125),
    ('GPE-8.4.3', 'GPE-8.4', """Las operaciones administrativas de rutina y los procesos estadísticos repetitivos (por ejemplo: recolección de datos, codificación, edición de datos, validación de datos, intercambio de datos) se automatizan siempre que sea posible y se revisan periódicamente.""", 126),
    ('GPE-8.5.1', 'GPE-8.5', """De ser solicitada, la ONE y las UOE brindan información requerida por organismo legislativo para asegurar la obtención y el acceso constante a las fuentes de datos de los registros administrativos y de los demás tipos de datos con fines estadísticos.""", 127),
    ('GPE-8.5.2', 'GPE-8.5', """Se propicia y se cuenta con los elementos legales y técnicos para la generación de acuerdos apropiados con los propietarios de los datos de registros administrativos y de otras bases de datos (por ejemplo, acuerdos de prestación de servicios o mediante legislación nacional), para acceder a los datos, permitir el flujo de datos y metadatos y otros aspectos relevantes.""", 128),
    ('GPE-8.5.3', 'GPE-8.5', """Se lleva a cabo una evaluación de las posibles fuentes de datos de registros administrativos antes de comenzar cualquier encuesta nueva.""", 129),
    ('GPE-8.5.4', 'GPE-8.5', """Los métodos de integración y vinculación de los datos se llevan a cabo de manera proactiva, sujeto a consideraciones de seguridad y privacidad de estos.""", 130),
    ('GPE-8.5.5', 'GPE-8.5', """Los informes de calidad de los registros administrativos y los provenientes de otras fuentes para la producción de estadísticas oficiales son establecidos por la agencia estadística responsable en cooperación con los propietarios o titulares de los datos.""", 131),
    ('GPE-8.6.1', 'GPE-8.6', """La ONE y las UOE han desarrollado estrategias para pasar a un sistema de producción estadística más integrado y estandarizado dentro de su organización.""", 132),
    ('GPE-8.6.2', 'GPE-8.6', """La ONE y las UOE promueven, comparten e implementan soluciones estandarizadas para aumentar la eficacia y la eficiencia.""", 133),
    ('GPE-8.6.3', 'GPE-8.6', """La arquitectura empresarial estadística de la agencia de estadísticas se basa en estándares y lineamientos internacionales como el GSBPM, el GAMSO, la Arquitectura estadística de producción común (CSPA) y el SDMX.""", 134),
    ('GPE-9.1.1', 'GPE-9.1', """Se considera explícitamente la disponibilidad e idoneidad de los datos existentes (datos de encuestas existentes, datos de registros administrativos y de otras fuentes de datos) antes de sugerir la puesta en marcha de una nueva encuesta.""", 135),
    ('GPE-9.1.2', 'GPE-9.1', """La recolección de cualquier elemento de datos, que sea igual o similar a los recopilados en otra encuesta, se limita a lo que se considera necesario para fines de verificación y posibles cruces de información.""", 136),
    ('GPE-9.1.3', 'GPE-9.1', """Cuando es posible, las encuestas o partes de la información que se recopilará en las encuestas se extraen o derivan de los registros administrativos disponibles.""", 137),
    ('GPE-9.1.4', 'GPE-9.1', """Existen indicadores que permitan medir la carga de los encuestados y estos son considerados en los informes de calidad""", 138),
    ('GPE-9.2.1', 'GPE-9.2', """Se ponen a disposición de los informantes, paquetes de información que proporcionan elementos importantes y necesarios sobre la encuesta y que explican el valor de las estadísticas oficiales.""", 139),
    ('GPE-9.2.2', 'GPE-9.2', """Los informantes reciben los resultados finales o el resultado del censo o la encuesta en la que participaron.""", 140),
    ('GPE-9.2.3', 'GPE-9.2', """Se diseñan estrategias con grupos comunitarios, escuelas, gremios empresariales y otros grupos de interés para crear conciencia sobre el valor de las estadísticas oficiales.""", 141),
    ('GPE-9.2.4', 'GPE-9.2', """Se desarrollan productos web que brindan la información estadística necesaria a las persona usuarias de información (empresas y a los individuos), y estos productos se promueven a través de estrategias con comunidades y encuestados.""", 142),
    ('GPE-9.2.5', 'GPE-9.2', """Se establece una presencia en las redes sociales para promover la participación en encuestas y censos.""", 143),
    ('GPE-9.2.6', 'GPE-9.2', """Existen prácticas estándar para recibir comentarios de las/os informantes y para responder a sus solicitudes y quejas de manera frecuente.""", 144),
    ('GPE-9.3.1', 'GPE-9.3', """Se utilizan técnicas de muestreo apropiadas para minimizar los tamaños de muestra y a la vez lograr el nivel objetivo de precisión.""", 145),
    ('GPE-9.3.2', 'GPE-9.3', """Las encuestas por muestreo se coordinan para distribuir la carga de los informantes.""", 146),
    ('GPE-9.3.3', 'GPE-9.3', """Se ofrecen múltiples formas para la recopilación de la información a los informantes , incluidas encuestas electrónicas.""", 147),
    ('GPE-9.3.4', 'GPE-9.3', """La recopilación de datos se realiza en el momento más adecuado conforme al flujo de información planeado.""", 148),
    ('GPE-9.4.1', 'GPE-9.4', """Existe y se comparte con las persona usuarias de la información, la documentación de los datos ya disponibles dentro del SEN, incluidos los datos históricos archivados.""", 149),
    ('GPE-9.4.2', 'GPE-9.4', """Existen herramientas técnicas para compartir e intercambiar datos dentro del sistema estadístico nacional (por ejemplo, acuerdos formales, servicios web, bases de datos comunes).""", 150),
    ('GPE-9.4.3', 'GPE-9.4', """Los archivos de datos (repositorios) se comparten entre las agencias de estadísticas para la producción de estadísticas oficiales y en cumplimiento de las políticas de confidencialidad.""", 151),
    ('GPE-9.4.4', 'GPE-9.4', """Existe información sobre la calidad de los datos (por ejemplo, sobre cobertura y posibilidades de cruces).""", 152),
    ('GPE-9.4.5', 'GPE-9.4', """Se promueve en todo el SEN el uso de registros administrativos y de otro tipo de fuentes de información, como alternativas a los datos captados por las encuestas para la producción de estadísticas oficiales.""", 153),
    ('GRE-10.1.1', 'GRE-10.1', """Existe una legislación o alguna otra disposición formal que incluye la obligación de realizar consultas con las principales personas usuarias de las estadísticas.""", 154),
    ('GRE-10.1.2', 'GRE-10.1', """Existen procesos de consulta estructurados y periódicos (por ejemplo, consejos y comités asesores o grupos de trabajo) con los grupos de interés y con las personas usuarias clave para revisar el contenido del programa estadístico y la utilidad de las estadísticas existentes e identificar los requisitos para la producción de nuevas estadísticas.""", 155),
    ('GRE-10.1.3', 'GRE-10.1', """Los comentarios del servicio de atención al usuario, centro o línea directa se analizan para comprender e identificar las necesidades de las personas usuarias.""", 156),
    ('GRE-10.1.4', 'GRE-10.1', """Se recopilan y analizan los indicadores sobre el uso de las estadísticas (por ejemplo, análisis web, número y tipos de descargas, suscriptores de informes), para mejorar los productos estadísticos.""", 157),
    ('GRE-10.2.1', 'GRE-10.2', """Se satisfacen las necesidades prioritarias de las personas usuarias y estas se ven reflejadas en el programa de trabajo de la oficina de estadística.""", 158),
    ('GRE-10.2.2', 'GRE-10.2', """Existen procedimientos para priorizar las diversas necesidades de las personas usuarias en el programa de trabajo y en los objetivos estratégicos.""", 159),
    ('GRE-10.2.3', 'GRE-10.2', """Se analiza la información sobre el uso de las estadísticas para apoyar el establecimiento de prioridades.""", 160),
    ('GRE-10.2.4', 'GRE-10.2', """Se realiza una evaluación periódica del programa de trabajo estadístico para identificar las nuevas necesidades y aquellas que han bajado de prioridad.""", 161),
    ('GRE-10.2.5', 'GRE-10.2', """Existen procesos para monitorear y consultar con las partes interesadas la relevancia y la utilidad práctica de las estadísticas existentes (con respecto al alcance, nivel de detalle, costo, etc.) de acuerdo con las necesidades emergentes de las personas usuarias.""", 162),
    ('GRE-10.3.1', 'GRE-10.3', """Se establece una unidad de innovación para considerar y experimentar con nuevas fuentes de datos para satisfacer las necesidades emergentes de información.""", 163),
    ('GRE-10.3.2', 'GRE-10.3', """Se establece cooperación con la comunidad científica y con los propietarios o titulares de las nuevas fuentes de datos para experimentar y ser pioneros en el uso de estas fuentes de datos.""", 164),
    ('GRE-10.3.3', 'GRE-10.3', """La ONE discute internamente y de manera frecuente las posibilidades de explotar nuevas fuentes de datos.""", 165),
    ('GRE-10.4.1', 'GRE-10.4', """Se llevan a cabo encuestas y análisis de satisfacción de las personas usuarias o estudios similares de manera periódica y se evalúan y analizan los resultados.""", 166),
    ('GRE-10.4.2', 'GRE-10.4', """Se identifican e implementan acciones de mejora derivadas de las encuestas o estudios de satisfacción de las personas usuarias.""", 167),
    ('GRE-10.4.3', 'GRE-10.4', """Las encuestas de satisfacción del usuario incluyen preguntas a las personas usuarias respecto a la disponibilidad de metadatos.""", 168),
    ('GRE-10.4.4', 'GRE-10.4', """Existen medidas para evaluar la satisfacción de las personas usuarias principales con productos específicos (por ejemplo, encuestas e indicadores específicos de satisfacción del usuario, incluida la puntualidad y otras características a nivel de producto).""", 169),
    ('GRE-11.1.1', 'GRE-11.1', """Se desarrollan y gestionan sistemas basados en estándares, para evaluar y validar las bases de datos origen, los datos integrados, los resultados intermedios y los resultados estadísticos finales.""", 170),
    ('GRE-11.1.2', 'GRE-11.1', """Los datos se verifican sistemáticamente y se comparan con los datos utilizados mediante otras fuentes de información y a través del tiempo.""", 171),
    ('GRE-11.1.3', 'GRE-11.1', """Los resultados estadísticos se comparan con otras fuentes de información existentes para asegurar su validez.""", 172),
    ('GRE-11.2.1', 'GRE-11.2', """Existen procedimientos y lineamientos para medir y gestionar los errores estadísticos (por ejemplo, minimización de errores o equilibrios)""", 173),
    ('GRE-11.2.2', 'GRE-11.2', """Se identifican y describen las posibles fuentes de errores de muestreo.""", 174),
    ('GRE-11.2.3', 'GRE-11.2', """Se miden y evalúan los errores de muestreo.""", 175),
    ('GRE-11.2.4', 'GRE-11.2', """Se identifican, describen y evalúan los errores de no muestreo (errores en las fuentes de datos, errores de respuesta, errores de cobertura, errores relacionados con mediciones, procesamiento y análisis, etc.)""", 176),
    ('GRE-11.2.5', 'GRE-11.2', """Se analizan los errores estadísticos de muestreo y no muestreo, para identificar acciones de mejora.""", 177),
    ('GRE-11.2.6', 'GRE-11.2', """La información sobre los errores de muestreo y no muestreo se pone a disposición de las personas usuarias como parte de los metadatos.""", 178),
    ('GRE-11.3.1', 'GRE-11.3', """Se identifican claramente los datos y estadísticas preliminares de aquellos que ya están revisados.""", 179),
    ('GRE-11.3.2', 'GRE-11.3', """Se ponen a disposición de las personas usuarias, información sobre el momento, las razones y la naturaleza de las revisiones.""", 180),
    ('GRE-11.3.3', 'GRE-11.3', """La política de revisión sigue procedimientos estándar y transparentes en el contexto de cada encuesta.""", 181),
    ('GRE-11.3.4', 'GRE-11.3', """La información sobre la magnitud y los motivos de las revisiones, de los indicadores clave, se utiliza para mejorar los procesos estadísticos.""", 182),
    ('GRE-11.3.5', 'GRE-11.3', """Se provee información sobre la magnitud y los motivos de las revisiones, de los indicadores clave, y se dispone públicamente.""", 183),
    ('GRE-12.1.1', 'GRE-12.1', """La oportunidad en la publicación de las estadísticas de la ONE cumple con los estándares de difusión de los organismos internacionales como el Fondo Monetario Internacional (FMI) u otros que determinan la relevancia de la puntualidad (por ejemplo, los requisitos de la Agenda 2030 para los ODS).""", 184),
    ('GRE-12.1.2', 'GRE-12.1', """Se hace seguimiento a las divergencias respecto a los objetivos internacionales de puntualidad y, si no se cumplen, se toman medidas para garantizar su cumplimiento.""", 185),
    ('GRE-12.1.3', 'GRE-12.1', """En el momento de establecer los objetivos, se tienen en cuenta las divergencias generales entre la puntualidad y las otras dimensiones de la calidad (por ejemplo, precisión, costo y carga del encuestado).""", 186),
    ('GRE-12.2.1', 'GRE-12.2', """Existen acuerdos con los proveedores de los datos, sobre las fechas de entrega acordadas y el formato a utilizarse.""", 187),
    ('GRE-12.2.2', 'GRE-12.2', """Existen procedimientos para asegurar el flujo efectivo y oportuno de datos de los proveedores hacia la ONE.""", 188),
    ('GRE-12.2.3', 'GRE-12.2', """Existen procedimientos de seguimiento para garantizar la recepción oportuna de los datos.""", 189),
    ('GRE-12.3.1', 'GRE-12.3', """Se considera y evalúa la posibilidad y la necesidad de publicar datos estadísticos preliminares, al mismo tiempo que se considera la precisión y confiabilidad de la información.""", 190),
    ('GRE-12.3.2', 'GRE-12.3', """Las personas usuarias reciben información apropiada sobre la calidad de las estadísticas preliminares.""", 191),
    ('GRE-12.3.3', 'GRE-12.3', """Los resultados preliminares se revisan de acuerdo con la política de revisión establecida.""", 192),
    ('GRE-12.3.4', 'GRE-12.3', """Los resultados finales se distinguen claramente de los resultados preliminares.""", 193),
    ('GRE-12.4.1', 'GRE-12.4', """La puntualidad, o la relación de cumplimiento de la puntualidad (es decir, la tasa de estadísticas publicadas a tiempo), se mide de acuerdo con lo que se establece en el calendario de publicación. El establecimiento del calendario de publicación debe ocurrir al menos 3 meses antes de la publicación de las estadísticas relevantes.""", 194),
    ('GRE-12.4.2', 'GRE-12.4', """La información sobre la puntualidad de las estadísticas publicadas se discute con la dirección y se pone a disposición de las personas usuarias.""", 195),
    ('GRE-13.1.1', 'GRE-13.1', """Las estadísticas se presentan de manera clara y comprensible. (Referirse al glosario de términos en lo que respecta a la definición de "claridad" e "interpretabilidad")""", 196),
    ('GRE-13.1.2', 'GRE-13.1', """Las guías que describen el contenido apropiado, los formatos y los estilos de presentación preferidos (diseño y claridad de los textos, tablas y gráficos) de los resultados de una ONE y UOE, están disponibles y se usan en las publicaciones de las estadísticas y de las bases de datos.""", 197),
    ('GRE-13.1.3', 'GRE-13.1', """Los datos estadísticos publicados están abiertos para uso libre, siempre que se haga referencia a la agencia responsable de su elaboración.""", 198),
    ('GRE-13.1.4', 'GRE-13.1', """Se ponen a disposición del público los documentos metodológicos actualizados (sobre los conceptos, el alcance, las clasificaciones, las bases y fuentes de datos, los métodos de recolección y las técnicas estadísticas), así como las medidas de calidad y el programa de trabajo de la ONE y las UOE.""", 199),
    ('GRE-13.1.5', 'GRE-13.1', """Los textos explicativos que acompañan a los datos se revisan para mayor claridad y legibilidad. (Notas técnicas o metodológicas, anexos técnicos, etc.)""", 200),
    ('GRE-13.1.6', 'GRE-13.1', """Se incluyen comparaciones de los datos en las publicaciones cuando es adecuado.""", 201),
    ('GRE-13.1.7', 'GRE-13.1', """Los datos preliminares y los datos revisados(definitivos) ​​se identifican y explican en las estadísticas publicadas.""", 202),
    ('GRE-13.1.8', 'GRE-13.1', """Se publican los metadatos más relevantes, junto con los resultados estadísticos, para comprender y utilizar las estadísticas.""", 203),
    ('GRE-13.1.9', 'GRE-13.1', """Existe una política para archivar las estadísticas ya publicadas.""", 204),
    ('GRE-13.2.1', 'GRE-13.2', """En la medida de lo posible, se debe suministrar apoyo técnico para el análisis de datos a solicitud de las personas usuarias y según los acuerdos, hacerlos públicos.""", 205),
    ('GRE-13.2.2', 'GRE-13.2', """Se informa al público que, cuando sea posible, se pueden proporcionar a solicitud resultados personalizados, estadísticas que no se difunden de manera rutinaria y series de tiempo más largas, y se les indica a los usuarios cómo realizar estas solicitudes. Los resultados estadísticos 
de estas consultas se hacen públicos siempre que sea posible y se acompañan de notas que informan sobre su correcto uso e interpretación.""", 206),
    ('GRE-13.2.3', 'GRE-13.2', """Los catálogos de publicaciones y otros servicios se ponen a disposición de las personas usuarias.""", 207),
    ('GRE-13.2.4', 'GRE-13.2', """Se pone a disposición de las personas usuarias de la 
información el costo relacionado para brindar servicios estadísticos complementarios.""", 208),
    ('GRE-13.2.5', 'GRE-13.2', """Se ha desarrollado y acordado una estrategia con las personas usuarias estratégicas para la publicación de los datos y microdatos anonimizados.""", 209),
    ('GRE-13.3.1', 'GRE-13.3', """Las estadísticas se difunden por varios canales, adecuados para todas las personas usuarias, siendo el sitio web de la ONE y las instituciones que conforman el SEN el canal principal.""", 210),
    ('GRE-13.3.2', 'GRE-13.3', """Las personas usuarias pueden extraer grupos de datos, a partir de bases de datos estadísticas publicadas en la web, en los formatos más apropiados y comunes (xlsx, cvc, html, etc.).""", 211),
    ('GRE-13.3.3', 'GRE-13.3', """Los datos estadísticos se pueden descargar mediante una interfaz de programación de aplicaciones (API), de manera rápida, con cruces sencillos desde un aplicativo en línea, que se puedan consultar en diferentes dispositivos.""", 212),
    ('GRE-13.3.4', 'GRE-13.3', """Las estadísticas se difunden de manera que facilitan la divulgación por parte de los medios de comunicación.""", 213),
    ('GRE-13.3.5', 'GRE-13.3', """Se establecen acuerdos con personas usuarias clave para la transmisión eficiente y periódica de las estadísticas y los datos.""", 214),
    ('GRE-13.3.6', 'GRE-13.3', """Existe la forma de acceder (componente tecnológico) a datos anonimizados  o mecanismos para acceder a  microdatos.""", 215),
    ('GRE-13.3.7', 'GRE-13.3', """Se ha considerado explícitamente las divergencias entre la accesibilidad y la confidencialidad estadística (es decir, el nivel de detalle en las tablas).""", 216),
    ('GRE-13.4.1', 'GRE-13.4', """La ONE y las UOE controlan o supervisan el acceso de los investigadores a los microdatos al proporcionarlos en un entorno seguro..""", 217),
    ('GRE-13.4.2', 'GRE-13.4', """Se consulta a los investigadores sobre la efectividad de los acuerdos de acceso a los microdatos.""", 218),
    ('GRE-13.4.3', 'GRE-13.4', """La infraestructura para el acceso remoto a los microdatos está disponible, con el control adecuado.""", 219),
    ('GRE-13.5.1', 'GRE-13.5', """La ONE y los otros productores del SEN tienen una estrategia para 
administrar las relaciones con los medios y mantener un contacto frecuente con los medios de comunicación.""", 220),
    ('GRE-13.5.2', 'GRE-13.5', """La ONE y las UOE organizan jornadas de capacitación y divulgación para los periodistas, de manera periódica.""", 221),
    ('GRE-13.5.3', 'GRE-13.5', """La ONE y las UOE organizan capacitación para los estudiantes sobre cómo usar las estadísticas.""", 222),
    ('GRE-13.5.4', 'GRE-13.5', """Se incentiva a productores y a las personas usuarias a publicar artículos sobre temas estadísticos y sobre cómo se deben usar las estadísticas de manera adecuada.""", 223),
    ('GRE-13.6.1', 'GRE-13.6', """Los servicios de soporte a las personas usuarias están disponibles para proporcionarles asistencia rápida que permita ayudarles a acceder e interpretar los datos.""", 224),
    ('GRE-13.6.2', 'GRE-13.6', """Los servicios de asistencia al usuario cuentan con el personal adecuado para atender una amplia gama de personas usuarias.""", 225),
    ('GRE-13.7.1', 'GRE-13.7', """Se definen los informes de calidad estandar armonizados para las operaciones estadísticas de la ONE.""", 226),
    ('GRE-13.7.2', 'GRE-13.7', """Las estadísticas publicadas van acompañadas de informes de calidad estándar, que incluyen información sobre la periodicidad de las estadísticas, las fuentes de los datos, los métodos de producción y su calidad (precisión y fiabilidad, puntualidad y oportunidad, coherencia y comparabilidad, accesibilidad y claridad).""", 227),
    ('GRE-13.7.3', 'GRE-13.7', """Los resultados de las evaluaciones de calidad o revisiones se hacen públicos.""", 228),
    ('GRE-14.1.1', 'GRE-14.1', """La ONE promueve la adopción de estándares nacionales, regionales o internacionales.""", 229),
    ('GRE-14.1.2', 'GRE-14.1', """Existen directrices, un repositorio común de conceptos estadísticos, definiciones de unidades y variables y clasificaciones y otros mecanismos.""", 230),
    ('GRE-14.1.3', 'GRE-14.1', """Se realiza seguimiento al cumplimiento de las normas internacionales, regionales o nacionales para la producción estadísticas. Cualquier desviación de estos estándares se hace explícita y se incluye en los metadatos, junto con las razones de tales desviaciones.""", 231),
    ('GRE-14.2.1', 'GRE-14.2', """Las estadísticas derivadas de diferentes fuentes o con diferentes periodicidades (por ejemplo, mensual, trimestral y anual), se comparan, se explican y se revisan las concordancias de las diferencias, según corresponda.""", 232),
    ('GRE-14.2.2', 'GRE-14.2', """Se promueve la cooperación y el intercambio de conocimientos entre programas y temáticas estadísticas individuales.""", 233),
    ('GRE-14.2.3', 'GRE-14.2', """Los procedimientos y directrices específicos del proceso estadístico están disponibles para asegurar que los resultados sean coherentes internamente.""", 234),
    ('GRE-14.2.4', 'GRE-14.2', """Antes de lanzar nuevas estadísticas o programas estadísticos, se analiza la relación conceptual y metodológica con las estadísticas existentes.""", 235),
    ('GRE-14.2.5', 'GRE-14.2', """Los resultados estadísticos se comparan con otras fuentes estadísticas o registros administrativos que proporcionan la misma información o similar sobre el mismo tema, y las divergencias se identifican y explican a las personas usuarias.""", 236),
    ('GRE-14.2.6', 'GRE-14.2', """Se desarrollan procedimientos o lineamientos internos para garantizar y monitorear la coherencia y consistencia interna.""", 237),
    ('GRE-14.2.7', 'GRE-14.2', """Se elaboran procedimientos y directrices para garantizar que se puedan combinar los resultados de diferentes fuentes. El cumplimiento se evalúa periódicamente.""", 238),
    ('GRE-14.3.1', 'GRE-14.3', """Los cambios en los métodos de compilación de los datos están claramente identificados, descritos y medidos para facilitar la interpretación de los resultados.""", 239),
    ('GRE-14.3.2', 'GRE-14.3', """La metadata en general incluye una sección sobre la evaluación de la consistencia interna y la comparabilidad a lo largo del tiempo y si es pertinente con otras estadísticas relacionadas con el tema.""", 240),
    ('GRE-14.3.3', 'GRE-14.3', """Se explican las rupturas de la serie de tiempo y se ponen a disposición del público los métodos para garantizar el empalme de las series durante el período de tiempo.""", 241),
    ('GRE-14.3.4', 'GRE-14.3', """Se evalúan los efectos de los cambios en las metodologías en las estimaciones finales y se proporciona información apropiada a las personas usuarias.""", 242),
    ('GRE-14.3.5', 'GRE-14.3', """Los cambios significativos en la sociedad y los fenómenos a medir se reflejan en los cambios apropiados en los conceptos, clasificaciones, definiciones y poblaciones objetivo.""", 243),
    ('GRE-14.3.6', 'GRE-14.3', """Se explican las diferencias dentro de áreas geográficas o a nivel de país debido a diferentes conceptos o metodologías.""", 244),
    ('GRE-15.1.1', 'GRE-15.1', """Se cuenta con una estrategia, lineamientos y procedimientos para la gestión y difusión de los metadatos.""", 245),
    ('GRE-15.1.2', 'GRE-15.1', """La gestión de los metadatos se reconoce como responsabilidad de todo el personal involucrado en la operación estadística.""", 246),
    ('GRE-15.2.1', 'GRE-15.2', """Se utilizan estándares internacionales, regionales, nacionales o internos para la documentación, la gestión y el archivo de los metadatos.""", 247),
    ('GRE-15.2.2', 'GRE-15.2', """Existen procedimientos para asegurar que los metadatos se documentan de acuerdo con los estandares internacionales  y se actualizan periódicamente.""", 248),
    ('GRE-15.2.3', 'GRE-15.2', """Los metadatos están disponibles al mismo tiempo que los datos y las estadísticas a las que pertenecen.""", 249),
    ('GRE-15.2.4', 'GRE-15.2', """Existe una forma sistemática de archivar los metadatos que también asegura que estén disponibles para su reutilización en el futuro.""", 250),
    ('GRE-15.2.5', 'GRE-15.2', """Se pone a disposición del público un glosario de conceptos estadísticos.""", 251),
    ('GRE-15.3.1', 'GRE-15.3', """Los responsables de los procesos estadísticos están capacitados para documentar adecuadamente los datos y describir los procesos relevantes.""", 252),
]

# (nombre, orden) — Principales instituciones públicas del Sistema Estadístico
# Nacional (SEN) de la República Dominicana. Lista base; los usuarios pueden
# agregar otras desde la app (opción "escribir nueva").
INSTITUCIONES: list[tuple] = [
    ("Oficina Nacional de Estadística (ONE)", 1),
    ("Banco Central de la República Dominicana", 2),
    ("Ministerio de Economía, Planificación y Desarrollo (MEPyD)", 3),
    ("Ministerio de Hacienda", 4),
    ("Ministerio de Salud Pública (MSP)", 5),
    ("Ministerio de Educación (MINERD)", 6),
    ("Ministerio de Educación Superior, Ciencia y Tecnología (MESCyT)", 7),
    ("Ministerio de Agricultura", 8),
    ("Ministerio de Trabajo", 9),
    ("Ministerio de Industria, Comercio y Mipymes (MICM)", 10),
    ("Ministerio de Medio Ambiente y Recursos Naturales", 11),
    ("Ministerio de Turismo (MITUR)", 12),
    ("Ministerio de Obras Públicas y Comunicaciones (MOPC)", 13),
    ("Ministerio de Interior y Policía", 14),
    ("Ministerio de Relaciones Exteriores (MIREX)", 15),
    ("Ministerio de la Mujer", 16),
    ("Ministerio de Cultura", 17),
    ("Ministerio de Deportes y Recreación", 18),
    ("Ministerio de la Juventud", 19),
    ("Ministerio de Energía y Minas", 20),
    ("Ministerio de la Presidencia", 21),
    ("Ministerio Administrativo de la Presidencia", 22),
    ("Dirección General de Impuestos Internos (DGII)", 23),
    ("Dirección General de Aduanas (DGA)", 24),
    ("Tesorería de la Seguridad Social (TSS)", 25),
    ("Superintendencia de Bancos (SB)", 26),
    ("Superintendencia de Seguros", 27),
    ("Superintendencia del Mercado de Valores (SIMV)", 28),
    ("Junta Central Electoral (JCE)", 29),
    ("Instituto Dominicano de Seguros Sociales (IDSS)", 30),
    ("Consejo Nacional de la Seguridad Social (CNSS)", 31),
    ("Instituto Nacional de Bienestar Estudiantil (INABIE)", 32),
    ("Consejo Nacional para la Niñez y la Adolescencia (CONANI)", 33),
    ("Instituto Nacional de Formación Técnico Profesional (INFOTEP)", 34),
    ("Instituto Agrario Dominicano (IAD)", 35),
    ("Instituto Nacional de Recursos Hidráulicos (INDRHI)", 36),
    ("Corporación Dominicana de Empresas Eléctricas Estatales (CDEEE)", 37),
    ("Instituto Nacional de Tránsito y Transporte Terrestre (INTRANT)", 38),
    ("Oficina Nacional de Propiedad Industrial (ONAPI)", 39),
    ("Otra institución", 99),
]
