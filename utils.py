import datetime

def obtener_saludo():
    hora_actual = datetime.datetime.now()
    if int(hora_actual.hour) < 12:
        return "Buen día"
    elif int(hora_actual.hour) < 19:
        return "Buenas tardes"
    else:
        return "Buenas noches"


def get_current_time():
    return datetime.datetime.now().strftime('%d/%m %H:%M')


def read_list_from_file(file_path):
    file = open(file_path, "r")
    content = file.read()
    list = content.split(',')

    return list