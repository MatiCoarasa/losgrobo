import sqlite3

def update_client_in_database(value, field, session_id):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {table_name} SET {field} = {value} WHERE session_id = '{session_id}'")
        connection.commit()


def initialize_database():
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        if DEV_MODE:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"CREATE TABLE {table_name} (name TEXT, dni INT, phone_number TEXT, tipo_tramite TEXT, numero_poliza INT, session_id TEXT, numero_solicitud INT, cargado_reporte INT, PRIMARY KEY (session_id))")
            connection.commit()


def get_user_by_session_id(session_id):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT name, dni, phone_number, tipo_tramite, numero_poliza FROM {table_name} WHERE session_id = '{session_id}'")
        result = cursor.fetchone()
        if result:
            return CustomClient(nombre=result[0], dni=result[1], numero_telefono=result[2], tipo_tramite=result[3], numero_poliza=result[4], session_id=session_id)
        else:
            return None


def user_exists_by_session_id(session_id):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT phone_number FROM {table_name} WHERE session_id = '{session_id}'")
        return cursor.fetchone() is not None

def get_unloaded_clients_from_db():
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT name, dni, phone_number, tipo_tramite, numero_poliza, session_id FROM {table_name} WHERE cargado_reporte = 0 AND dni IS NOT NULL')
        clients = []
        for row in cursor.fetchall():
            client_db = CustomClient(nombre=row[0], dni=row[1], numero_telefono=row[2], tipo_tramite=row[3], numero_poliza=row[4], session_id=row[5])
            clients.append(client_db)
        return clients


def update_loaded_client_report(session_id):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {table_name} SET cargado_reporte = 1 WHERE session_id = '{session_id}'")
        connection.commit()


def initialize_user_in_database(phone_number, session_id):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {table_name} (phone_number, session_id, cargado_reporte) VALUES ('{phone_number}', '{session_id}', 0)")
        connection.commit()
        