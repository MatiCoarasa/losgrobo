class CustomClient:
    def __init__(self, numero_telefono, session_id, tipo_tramite=None, numero_poliza=None, nombre=None, dni=None):
        self._numero_telefono = numero_telefono
        self._session_id = session_id
        self._tipo_tramite = tipo_tramite
        self._numero_poliza = numero_poliza
        self._nombre = nombre
        self._dni = dni

    @property
    def numero_telefono(self):
        return self._numero_telefono

    @property
    def session_id(self):
        return self._session_id

    @property
    def tipo_tramite(self):
        return self._tipo_tramite

    @tipo_tramite.setter
    def tipo_tramite(self, tramite):
        self._tipo_tramite = tramite

    @property
    def numero_poliza(self):
        return self._numero_poliza

    @numero_poliza.setter
    def numero_poliza(self, poliza):
        self._numero_poliza = poliza

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, dni):
        self._dni = dni
