from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,and_
import csv
from datetime import *
import calendar
from service.tablas import *
 #Create database connection object


hoy = datetime.now()
first_day_of_month = datetime(hoy.year, hoy.month, 1)
first_friday = first_day_of_month + timedelta(days=((4-calendar.monthrange(hoy.year,hoy.month)[0])+7)%7)
# 4 is friday of week
third_friday = first_friday + timedelta(days=14)

def graficos():
    alertas=db.session.query(Informe.tipo_alerta,func.count(Informe.tipo_alerta)).group_by(Informe.tipo_alerta)
    estados=db.session.query(Informe.tipo_alerta,Informe.estado,func.count(Informe.tipo_alerta)).group_by(Informe.tipo_alerta,Informe.estado)
    return render_template('morris.html',alertas=alertas,estados=estados)
def subirArchivos():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
        return render_template('morris.html')
    else:
        return render_template('form_component.html')
def datos():
    informes=Informe.query.order_by(Informe.denominacion).all()
    return render_template('responsive_table.html',informes=informes)
def tablas():
    pendientes=db.session.query(Informe.nro_remitente,Informe.denominacion,Informe.fecha,Informe.diasTranscurridos,Informe.monto,Informe.estado).filter(Informe.estado =='A la Espera de Información').order_by(Informe.diasTranscurridos)
    pendientes_120=db.session.query(Informe.nro_remitente,Informe.denominacion,Informe.fecha,Informe.diasTranscurridos,Informe.monto,Informe.estado).filter(and_(Informe.diasTranscurridos <=150, Informe.diasTranscurridos >=120 ,Informe.estado =='A la Espera de Información')).order_by(Informe.diasTranscurridos)
    favorables=db.session.query(Informe.nro_remitente,Informe.denominacion,Informe.fecha,Informe.diasTranscurridos,Informe.monto,Informe.estado).filter(and_(Informe.diasTranscurridos> 150 ,Informe.estado.in_(['Resuelto Favorable','Resuelto Desfavorable'])))
    return render_template('tablas.html',pendientes=pendientes,pendientes_120=pendientes_120,favorables=favorables)
def cargarDatos():
	with open(sys.argv[1], 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		i=0
		for row in spamreader:
		# Insert new employee
			if i!=0:
				#fila=[row[0],row[1],datetime.strptime(row[4], "%d/%m/%Y").date(),0,row[6],row[7],row[9],row[14],hoy,hoy
				if len(row[2]) ==0:
					persona=row[0]
				else:
					persona=row[2]
				Informe(nro_remitente=row[0], denominacion=row[1], fecha=datetime.strptime(row[4], "%d/%m/%Y").date(), diasTranscurridos=(third_friday-datetime.strptime(row[4], "%d/%m/%Y")).days, tipo_alerta=row[6], estado=row[7],tipo_comprobante=row[9] , monto=row[12], fecha_creacion=hoy.date(), fecha_actualizacion=hoy.date(),nro_transaccion=row[21],persona_id=persona)
				db.session.commit()
			else:
				i=1