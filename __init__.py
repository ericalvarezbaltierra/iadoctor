from flask import Flask, render_template, redirect, url_for,  jsonify, request
#import openai
#import logging
from logging.handlers import RotatingFileHandler
from heyoo import WhatsApp
from clases import librerias
#from datetime import datetime

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
#handler.setLevel(logging.INFO)


app = Flask(__name__)

app.logger.addHandler(handler)

@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    f2 = open("log.txt", "a")
    f2.write("entro al programa \n")
    f2.close()
    #Este sería el procedimiento principal. Este es el que WhatsApp manda llamar cuando recibe un mensaje
    #de aqui iniciamos todo el proceso con el chat
    l = librerias
   
 
    #SI HAY DATOS RECIBIDOS VIA GET 
    # este es el caso para validad en Face book si es valida la página
    #mem = ""
    #if request.method == "GET":
    #    #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
    #    if request.args.get('hub.verify_token') == "HolaNovato":
    #        #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
    #        men = " entro al if del get"
    #        return request.args.get('hub.challenge')
    #    else:
    #        #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
#   #       men =  " entro al else get"
#   #       return "Error de autentificacion nueva."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    f2 = open("log.txt", "a")
    f2.write("salio de valiacion\n")

    f2.close()
    mensaje = "hola python, programa"
    data=request.get_json()
    
    f2 = open("log.txt", "a")
    f2.write("despues del request \n")

    f2.close()
    #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    telefono = data['entry'][0]['changes'][0]['value']['messages'][0]['from'] 
  
    f2 = open("log.txt", "a")
    f2.write("despues de telefono " + telefono+ " \n")
    f2.close()
    #mensaje="Telefono:"+data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje="|Mensaje:"+data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
   
    f2 = open("log.txt", "a")
    f2.write("despues de mensaje  " + mensaje+ " \n")
    f2.close()
   
    # hay que revisar si el mensaje ya había sido recibido para que no se procese otra vez.
    # hay que almacenar el mensaje en una base de datos y revisar si no había llegado.

    
    #estos son los mensajes por default
    diagnostico = "Ninguno"
    Mensaje = """¡Bienvenido al asistente médico! Este sistema está diseñado para apoyar a los profesionales de la salud en el proceso de diagnóstico de enfermedades. Aquí te presentamos algunas pistas para utilizar este asistente de manera efectiva: \n
Para acceder a una consulta médica, proporciona los datos completos del paciente, incluyendo nombre, datos generales y detalles sobre los síntomas presentados. Es importante también mencionar los antecedentes médicos, tanto personales como hereditarios, para obtener una evaluación más precisa.\n
Si deseas revisar el historial médico de un paciente en particular, simplemente indica 'Quiero el historial médico' seguido del nombre completo de la persona. Esto permitirá acceder a su historial clínico y obtener información relevante sobre tratamientos anteriores, condiciones médicas previas y otros datos importantes para el análisis actual.\n
Recuerda que este asistente está diseñado para facilitar el trabajo de los médicos, proporcionando información útil y agilizando el proceso de diagnóstico. ¡Estamos aquí para ayudarte en la atención de tus pacientes!"""
  
    f2 = open("log.txt", "a")
    f2.write("que tiene mensaje "+ mensaje+ "\n")
    f2.close()
    # si el mesaje tien algún dato se inicia el procedimiento de chatgtp
    if mensaje is not None:
        f2 = open("log.txt", "a")
        f2.write("entro if del mensaje")
        f2.close()
        funcion, argumentos= l.ordena_sintomas (mensaje) #ordeno el mensaje y si quiso una consulta recibirá argumentos.
        f2 = open("log.txt", "a")
        f2.write("termino ordena")
        f2.close()
        
        
        if funcion == "none":
            f2 = open("log.txt", "a")
            f2.write("Entra en Mensaje solamente, por que no  hubo funcion \n")
            f2.close()
            l.enviar(telefono,Mensaje)
        else:
            f2 = open("log.txt", "a")
            f2.write("Entra en diagnostico por que si hubo funcion \n")
            f2.close()
            diagnostico = l.Pedimos_dignostico(argumentos)
            l.enviar(telefono,diagnostico)
       # l.Almacenar_consulta(argumentos,diagnostico)
        
       
    #RETORNAMOS EL STATUS EN UN JSON

    return diagnostico
    #return jsonify({"status": "success"}, 200)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hola Mundo'

@app.route('/redirect')
def redirect_to_google():
    return redirect("https://www.google.com")

if __name__ == '__main__':
    app.run(debug=True)


mensaje = """Paciente: Juan Pérez
Edad: 45 años
Género: Masculino
Datos Clínicos y Síntomas:
Juan Pérez ha experimentado los siguientes síntomas en los últimos días:

Fiebre: Juan ha tenido fiebre alta (38.5°C) durante tres días consecutivos.
Tos: Ha desarrollado una tos persistente, que inicialmente era seca pero ahora está produciendo flema amarillo-verde.
Dificultad para respirar: Juan ha experimentado dificultad para respirar, especialmente al realizar actividades físicas moderadas.
Fatiga: Se siente constantemente cansado y con poca energía.
Dolor en el pecho: Ha experimentado dolor en el pecho al toser o respirar profundamente.
Sudoración excesiva: Ha sudado profusamente, especialmente por las noches.
Confusión: Ha mostrado signos de confusión ocasional.
"""