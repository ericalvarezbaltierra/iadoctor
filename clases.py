import openai
#import mysql
#import pymysql
import pymongo
#import os
import json
from heyoo import WhatsApp

class librerias:
    #db = pymysql.connector.connect(host="localhost",
    #                             user="root",
    #                             password="",
    #                             database="consulta")

    def sintomas ():
         #pedimos los sintomas por medio de leguale del usuario desordenado
         return "sintoma"
    
    def ordena_sintomas (mensaje):
        f2 = open("log.txt", "a")
        f2.write("Entro en ordena sintomas \n")
        f2.close()
        #aca pedimos al ia que nos ordene los que pedimos en campos
        #hacemos nuestra primera peticion de 3
        openai.api_key = "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"  # Reemplaza con tu clave de API de OpenAI
        conversacion_actual = mensaje
        modelo = "gpt-3.5-turbo-1106" # este es mas barato  "gpt-3.5-turbo-0613" # este es el que ya tenia para las funciones

        #**********************************
        # mejora tratando de aplicar una especie de menú, donde pidan varias opciones
        # Se brinda un menu cuando el usuario no halla determinado que quiere una consulta.
        # cuando aplique las palabras clave el chat determina que funcion esta siendo llama
        respuesta_openai = openai.ChatCompletion.create(
        model=modelo,
        messages=[
            {"role": "system", "content": "Estás actuando como auxiliar de un médico. Ordenaras los elementos en los propiedades establecidas en la función"},
            {"role": "user", "content": conversacion_actual},
             ],
                functions=[
                    {
                    "name": "diagnostico_clinico",
                    "description": "evaluación de la salud para  conocer, diagnosticar y tratar problemas médicos, identificar los elementos de una consulta medica",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "Nombre": {
                                "type": "string",
                                "description": "Nombre completo del paciente ",
                            },
                            "Genero": {
                                "type": "string",
                                "description": "Si es hombre o mujer o de otro genero",
                            },
                            "edad": {
                                "type": "string",
                                "description": "La edad del paciente",
                            },
                            "Peso": {
                                "type": "string",
                                "description": "Peso corporal del paciente",
                            },
                             "Molestias": {
                                "type": "string",
                                "description": "Dolores y molestias",
                            },
                            "conciente": {
                                "type": "string",
                                "description": "el paciente esta conciente o inconciente",
                            },
                            "aspecto": {
                                "type": "string",
                                "description": "si especifican problemas fisicos en el cuerpo del paciente",
                            },
                            "presion sanguinea": {
                                "type": "string",
                                "description": "presión sistólica y la presión diastólica ",
                            },
                            "temperatura": {
                                "type": "string",
                                "description": "Temperatura del paciente ",
                            },
                             "Historial": {
                                "type": "string",
                                "description": "Antecedentes de consultas medicas pasadas",
                            },
                             "Enfermedades": {
                                "type": "string",
                                "description": "todas las Enfermedades que actualmente tiene el paciente cronicas o temporales",
                            },
                             "Genetica": {
                                "type": "string",
                                "description": "Enfermedades que tiene el paciente que son de origen genetico",
                            },
                             "medicamentos": {
                                "type": "string",
                                "description": "Todos los medicamentos que esta tomando actualmente",
                            },
                             "doctores": {
                                "type": "string",
                                "description": "los doctores que ya ha consultado con anterioridad",
                            },
                            "animo": {
                                "type": "string",
                                "description": "que estado de animo cuenta el paciente, como se siente en su estado animico",
                            },
                            "sintomas": {
                                "type": "string",
                                "description": "todos las manifestaciones físicas o mentales que indican que hay un problema de salud",
                            }
                        },
                        "required": [],
                    },
                },
                {
                    "name": "open_chrome",
                    "description": "Abrir el explorador Chrome en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir"
                            }
                        }
                    }
                }
            ],
            function_call="auto",
        )
        mensaje_respuesta = respuesta_openai['choices'][0]['message']['content']
        #print (mensaje_respuesta)
        message = respuesta_openai["choices"][0]["message"]
        
        #Nuestro amigo GPT quiere llamar a alguna funcion?
        if message.get("function_call"):
            #Sip    
            function_name = message["function_call"]["name"] #Que funcion?
            # separar los valores por atributo.
            args = message.to_dict()['function_call']['arguments'] #Con que datos?
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
        else:
            function_name = "none" # si no quiere una consulta medica hay que mandar un mensaje sobre que este eso es consulta médica
            args = ""
        #regresamos el nombre de la funcion y los argumentos.
        f2 = open("log.txt", "a")
        f2.write("salio de funcion y esta es la funcion que fue encontrada\n")
        f2.write(function_name + " \n")
        f2.close()
        return function_name,args
    
    
    def historial(): # aca tengo duda si es necesario buscar en el historial.
        # pedimos los historiales del paciente, Buscamos únicamente los elementos
        # de las consultas pasadas que dicen que esta abierta.
        return "valor"

    def Pedimos_dignostico(argumentos):
        # se junta los datos de los sintomas ordenados de la consulta, junto con el historial obteido.
        # hacemos la segunda consulta pediendo que se realice la consulta medica
        # dado la posible enfermedad, los medicamentos a tomar y las dosis. 
        # trataremos de ordenar los resultados obtenidos, como es 
        # El diagnostico, tratamiento y medicamento en formato JSON.
         # Indica el API Key
        f2 = open("log.txt", "a")
        f2.write("Entramos en diagnostico\n")
        # f2.write(argumentos + " \n")
        f2.close()
        mensaje  =  " Realiza un diagnostico clinico para auxiliar al médico, ordena el resultado presentando en primer lugar el diagnostico, en segundo lugar los posibles medicamentos a tomar y tercer lugar las recomendaciones para la recuperación del paciente.\n"
        mensaje = mensaje + " Para los medicamentos di la dosis a tomar y la frecuencia. \n"
        mensaje = mensaje + " No es necesario mencionar el resumen ni conclusiones, no necesario decir es resultado de un para auxiliar al médico, \n  "
        mensaje = mensaje +" no es necesario mencionar las advertencias sobre ir a consulta con un doctor, ni advertir sobre la compra de medicamentos sin preescripción médica. "
        mensaje = mensaje + " Los datos del paciente son los siguientes: \n"
        for clave, valor in argumentos.items():
            mensaje = mensaje + " " + clave + " " + valor
  

        openai.api_key = "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"
        # Uso de ChapGPT en Python
        model_engine = "gpt-3.5-turbo-1106"
        prompt = mensaje
        f2 = open("log.txt", "a")
        f2.write("la informacion con la que cuenta chat para trabajar \n")
        f2.write(mensaje)
        f2.close()
        respuesta_openai = openai.ChatCompletion.create(
        model=model_engine, temperature=0.1,
        messages=[
            {"role": "system", "content": "Estás actuando como auxiliar de un médico. Solo es para entrenamieto médico"},
             {"role": "assistant", "content": "Sacar dignosticos medico precisos basados en los datos proporcionados"},
            {"role": "user", "content": prompt}
             ]
        )
        #completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=2024, n=1, stop=None, temperature=0.1)
        mensaje_respuesta = respuesta_openai['choices'][0]['message']['content']
        f2 = open("log.txt", "a")
        f2.write("salimos de diagnostico y el resultado del diagnostico fue: \n")
        f2.write(mensaje_respuesta + " \n")
        f2.close()
        return mensaje_respuesta 
    
    def almacenar_consulta(argumentos,diagnostico):
        #***************************************
        #tengo que almacenar los datos en una tabla de la base de datos
        # se almacena los sintomas que ya ordenados por el chat y se agrega el diagnostico la enfermedad
        # que resulto, así como los medicamentos y  

        return "se almaceno"
    
    def Ordenar_resultados():
        # Mandamos la tercera llamada y le decimos que ordene y muestre en forma 
        # natural el resultado de la consula
        # es en esta ventana, lo que el médico manda cerrar las consultas pasadas o aun habra 
        # seguimiento
        return ""
    def recomendaciones ():
        
        return ""
    
    def historial ():
        #numero de consultas
        return ""
    
    def enviar(telefonoEnvia,textoMensaje):
        f2 = open("log.txt", "a")
        f2.write("entramos en envia\n")
        telefonoEnvia = telefonoEnvia [:2]+telefonoEnvia [3:]
        f2.write(telefonoEnvia + " telefono \n")
        f2.write(textoMensaje + " telefono \n")
        f2.close()
        #TOKEN DE ACCESO DE FACEBOOK
        token='EAAJLGYX94nIBOZCGq22vtLHICHFXwAVTZA30O1A8kwXFdG9lOj5HaGEmPavDgXOLcVwwRXnDTkDQUvYgA0SyASzL81BePn1KrikKffoW0vGmMfn8ZBAOiA5yzNJRZA41jo5azGQllKp6769x2c9TGMCW36ko7u3IQlMdZCBaIIlA77BiClJCIGwZBy3Eu2yhxZAoalDSGwP4ZB5k7YuG'
        #IDENTIFICADOR DE NÚMERO DE TELÉFONO
        idNumeroTeléfono='129737616895368'
        #TELEFONO QUE RECIBE (EL DE NOSOTROS QUE DIMOS DE ALTA)
        #telefonoEnvia='528461101854'
        #MENSAJE A ENVIAR
        #textoMensaje="Es este el mensaje |"
        #URL DE LA IMAGEN A ENVIAR
        #urlImagen='https://i.imgur.com/a95COMf.jpeg'
        #INICIALIZAMOS ENVIO DE MENSAJES
        mensajeWa=WhatsApp(token,idNumeroTeléfono)
        #ENVIAMOS UN MENSAJE DE TEXTO
        mensajeWa.send_message(textoMensaje,telefonoEnvia)
        #ENVIAMOS UNA IMAGEN
        #mensajeWa.send_image(image=urlImagen,recipient_id=telefonoEnvia,)
        f2 = open("log.txt", "a")
        f2.write("salimos  envia\n")
     
        f2.close()
        return "mensaje enviado"
    
    
