import uuid
import difflib
import os
from datetime import datetime
from utils import read_list_from_file

rtas_posibles = read_list_from_file("respuestas.txt")
csv_name = os.getenv("CSV_NAME", "pedidos.csv")

class Usuario:

    def __init__(self, telefono):
        self._telefono = telefono
        self._id_session = uuid.uuid4()
        self._mensajes = []
        self._transaccion = {}

    def add_mensaje(self, texto):
        self._mensajes.append(texto)

    @property
    def telefono(self):
        return self._telefono

    @property
    def mensajes(self):
        return self._mensajes

    @property
    def session_id(self):
        return self._id_session

    def __str__(self):
        return f'Telefono: {self._telefono} - ID: {self._id_session}\nTransaccion: {self._transaccion}'

    @property
    def transaccion(self):
        return self._transaccion

    def set_transaccion_attribute(self, atributo, valor):
        self._transaccion[atributo] = valor


def write_in_csv(usuario):
    if isinstance(usuario, Usuario):
        hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        telefono = usuario.telefono

        transaccion = usuario.transaccion
        string_transaccion = format_transaccion_to_csv(transaccion)

        pedido = f'{hora_actual},{telefono},{string_transaccion}'
        with open(csv_name, 'a') as pedidos_file:
            pedidos_file.write('\n')
            pedidos_file.write(pedido)


def format_transaccion_to_csv(transaccion):
    string_csv = ','.join(transaccion.values())
    return string_csv
    
def obtener_usuario(sesiones, numero_usuario):
    if numero_usuario in sesiones:
        return sesiones[numero_usuario]
    else:
        usuario = Usuario(numero_usuario)
        sesiones[numero_usuario] = usuario
        return usuario


def almacenar_rta(rta, df_response, user):

    if isinstance(user, Usuario):
        try:
            id_intent = int(df_response.intent.display_name[0])
        except ValueError:
            return
        if 1 <= id_intent <= 7:
            try:
                rta = difflib.get_close_matches(rta, rtas_posibles, n=1)[0]
            except IndexError:
                pass
            if id_intent == 1:
                user.set_transaccion_attribute("Tipo negocio", rta)
            elif id_intent == 2:
                user.set_transaccion_attribute("Destino comercial", rta)
            elif id_intent == 3:
                user.set_transaccion_attribute("Precio", rta)
            elif id_intent == 4:
                user.set_transaccion_attribute("Cereal", rta)
            elif id_intent == 5:
                user.set_transaccion_attribute("Cosecha", rta)
            elif id_intent == 6:
                user.set_transaccion_attribute("Tipo entrega", rta)
            elif id_intent == 7:
                user.set_transaccion_attribute("Pago", rta)
