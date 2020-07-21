import os
import dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
os.environ["GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"] = "roots.pem"
project_id = "bot-grobocopatel-ogpttq"
language_code = "es-ES"
session_client = dialogflow.SessionsClient()

def get_df_response(text, session_id):
    session = session_client.session_path(project_id, session_id)    
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response_dialogflow = session_client.detect_intent(session=session, query_input=query_input)

    return response_dialogflow.query_result


def es_respuesta_final(query_result):
    return query_result.diagnostic_info.fields["end_conversation"].bool_value

def operacion_confirmada(query_result):
    operacion_confirmada = False
    try:
        operacion_confirmada = query_result.intent.display_name[0] == '9'
    except ValueError:
        pass

    return operacion_confirmada
