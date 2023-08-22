import requests
import json
import re


# ==== Classe Principale (Utente) ===== #
class Utente:
    # === Inizializza Utente === #
    def __init__(self, uid: str, pwd: str):
        self.uid = uid
        self.pwd = pwd
        self.ident = ''
        self.token = ''

        self.is_logged_in = False

    # === Effettua il Login === #
    def login(self):
        response = requests.post(RequestURLs.login[0], headers=header, data=f'{{"ident":null,"pass":"{self.pwd}","uid":"{self.uid}"}}')

        if response.status_code == 200:
            data = json.loads(response.text)

            self.ident = re.search(r'\d+', data['ident']).group()
            self.token = data['token']
            self.is_logged_in = True

            print('Login effettuato con successo.')
        else:
            print('Errore durante il Login.')

        return response

    # === Effettua una Richiesta 'GET' === #
    def request(self, reqeust_url: tuple, params=None):
        args = (self.ident,) + (params,)

        if self.is_logged_in:
            headers = self.get_headers()

            if reqeust_url[1] == 'get':
                response = requests.get(reqeust_url[0].format(*args), headers=headers)
            else:
                response = requests.post(reqeust_url[0].format(*args), headers=headers)

            if response.status_code == 200:
                print(f'Richiesta avvenuta con successo:')
                print(f'{response.text}')
                return response
            else:
                print(f'Errore durante la richiesta: {response.text}')
                return None
        else:
            print(f"Errore durante la richiesta: L'utente non ha effetuato il login.")
            return None

    def get_headers(self):
        headers = header.copy()
        headers['Z-Auth-Token'] = self.token

        return headers


# ===== Reqeust URLs ===== #
class RequestURLs:
    base_url: str = 'https://web.spaggiari.eu/rest/v1'
    students_url: str = f'{base_url}/students/{{}}'  # Student Ident

    assenze: tuple = (f'{students_url}/absences/details', 'get')
    agenda: tuple = (f'{students_url}/agenda/all/{{}}/{{}}', 'get')  # Data Inizio (YYYYMMDD) / Data Fine (YYYYMMDD)
    didattica: tuple = (f'{students_url}/didactics', 'get')
    libri: tuple = (f'{students_url}/schoolbooks', 'get')
    calendario: tuple = (f'{students_url}/calendar/all', 'get')
    card: tuple = (f'{students_url}/card', 'get')
    voti: tuple = (f'{students_url}/grades', 'get')
    lezioni_oggi: tuple = (f'{students_url}/lessons/today', 'get')
    lezioni_giorno: tuple = (f'{students_url}/lessons/{{}}', 'get')  # Lezioni Giorno (YYYYMMDD)
    note: tuple = (f'{students_url}/notes/all', 'get')
    periods: tuple = (f'{students_url}/perioids', 'get')
    materie: tuple = (f'{students_url}/subjects', 'get')

    login: tuple = (f'{base_url}/auth/login', 'post')
    noticeboard: tuple = (f'{students_url}/noticeboard', 'post')
    documenti: tuple = (f'{students_url}/documents', 'post')


# ===== Default Header ===== #
header: dict[str, str] = {
    "User-Agent": "CVVS/std/4.1.7 Android/10",
    "Content-Type": "application/json",
    "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K"
}