from flask import Flask, render_template, request
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
contrasena = os.getenv('EMAIL_PASSWORD')  # Ahora la contraseña viene de una variable de entorno


app = Flask(__name__)

def guardar_en_csv(turno):
    archivo = 'turnos.csv'
    encabezados = ['Nombre', 'Contacto', 'Profesional', 'Día', 'Horario', 'Tratamiento', 'Pago']
    try:
        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=encabezados)
            if f.tell() == 0:
                escritor.writeheader()
            escritor.writerow(turno)
    except Exception as e:
        print(f"Error al guardar en CSV: {e}")

def enviar_correo(turno):
    print("📧 Intentando enviar correo...")  # Debugging

    remitente = 'pjuanpi370@gmail.com'
    contrasena = 'tfqyeesyzwwtttap'
    destinatario = turno['Contacto']
    asunto = 'Confirmación de Turno - Estética Cecilia'
    cuerpo = f"""
    Estimado/a {turno['Nombre']},

    Su turno ha sido agendado con éxito. A continuación, los detalles:

    Profesional: {turno['Profesional']}
    Día: {turno['Día']}
    Horario: {turno['Horario']}
    Tratamiento: {turno['Tratamiento']}
    Forma de pago: {turno['Pago']}

    Gracias por elegirnos.

    Atentamente,
    Estética Cecilia
    """

    try:
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.ehlo()  # Agregado para evitar problemas de resolución
        servidor.starttls()
        servidor.ehlo()  # Agregado nuevamente por seguridad
        servidor.login(remitente, contrasena)
        servidor.send_message(mensaje)
        servidor.quit()

        print("✅ Correo enviado correctamente")  
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")  


@app.route('/')
def formulario():
    print("🌍 Página de inicio cargada correctamente")  # Para verificar que Flask está corriendo
    return render_template('formulario.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    nombre = request.form.get('nombre')
    contacto = request.form.get('contacto')
    profesional = request.form.get('profesional')
    dia = request.form.get('dia')
    horario = request.form.get('horario')
    tratamiento = request.form.get('tratamiento')
    pago = request.form.get('pago')
    
    if not all([nombre, contacto, profesional, dia, horario, tratamiento, pago]):
        return "Error: Todos los campos son obligatorios", 400
    
    turno = {
        'Nombre': nombre,
        'Contacto': contacto,
        'Profesional': profesional,
        'Día': dia,
        'Horario': horario,
        'Tratamiento': tratamiento,
        'Pago': pago
    }
    
    guardar_en_csv(turno)
    enviar_correo(turno)
    return "Turno agendado correctamente"  # Esto debe ser un HTML en producción

if __name__ == '__main__':
    app.run(debug=True)
