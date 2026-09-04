import sqlite3, os
db='data/cnbpe.db' if os.path.exists('data/cnbpe.db') else 'cnbpe.db'
conn=sqlite3.connect(db)
c=conn.cursor()
c.execute('DELETE FROM adx_seguimiento_detalle WHERE seguimiento_id IN (SELECT id FROM adx_seguimientos WHERE nombre IN (''cbc'', ''s'', ''1er'', ''1r''))')
c.execute('DELETE FROM adx_seguimientos WHERE nombre IN (''cbc'', ''s'', ''1er'', ''1r'')')
conn.commit()
conn.close()
print('Base de datos limpiada con exito')
