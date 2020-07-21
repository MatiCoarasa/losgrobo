import datetime
import os
import random
from time import sleep

import dialogflow
import requests
from usuario import Usuario, obtener_usuario, almacenar_rta, write_in_csv
from os.path import dirname, join
from dotenv import load_dotenv
from flask import Flask
from flask import request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from mail import send_informe
import sqlite3
import sys
import threading
import uuid
import dotenv
import flask
import twilio
import dflow

from client import CustomClient

# Cargo variables de ambiente desde .env
ambiente_ejecucion = os.getenv("AMBIENTE", "dev")
if ambiente_ejecucion == "dev":
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    dotenv.load_dotenv(dotenv_path)

# Credentials - Twilio
numero_twilio = os.getenv('TWILIO_NUMERO')
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
client = Client(account_sid, auth_token)

# Variables para la conversación
live_sessions_id = {}
session_client = dialogflow.SessionsClient()

app = Flask(__name__)

@app.route("/", methods=["POST"])
def manejar_mensaje():

    numero_usuario = request.form["From"].split(":")[1] # Llega en formato 'whatsapp:+54911...'
    usuario = obtener_usuario(live_sessions_id, numero_usuario)
    mensaje_usuario = str(request.form["Body"])
    print(f'Mensaje usuario: {mensaje_usuario}')
    usuario.add_mensaje(mensaje_usuario)

    if mensaje_usuario.lower().strip() == 'enviar informe':
        send_informe()
        return format_response('Informe enviado')

    respuesta_df = dflow.get_df_response(mensaje_usuario, usuario.session_id) # Retorna query_result, no el texto de rta


    if dflow.es_respuesta_final(respuesta_df):
        if dflow.operacion_confirmada(respuesta_df):
            write_in_csv(usuario)
        del live_sessions_id[numero_usuario]

    texto_respuesta = respuesta_df.fulfillment_text

    if not texto_respuesta:
        texto_respuesta = "Error en la respuesta. Inténtelo de nuevo."
        print(f'Respuesta BOT: {texto_respuesta}')
        return format_response(texto_respuesta)

    almacenar_rta(mensaje_usuario, respuesta_df, usuario)
    print(usuario)
    print(f'Respuesta BOT: {texto_respuesta}')
    return format_response(respuesta_df.fulfillment_text)


def format_response(mensaje):
    rta_fallo_twilio = MessagingResponse()
    rta_fallo_twilio.message(mensaje)
    return str(rta_fallo_twilio)


def send_twilio_message(mensaje, numero):
    message = client.messages.create(from_=numero_twilio, body=mensaje, to="whatsapp:" + numero)


if __name__ == "__main__":

    port = int(os.getenv('PORT', 5000))
    print(f'Levantando servidor en puerto {port}')

    # Se inicializa el servidor con Flask que escuchará las respuestas de los clientes.
    app.run(port=port, debug=True, use_reloader=False)
