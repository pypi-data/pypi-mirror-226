<h1 align='center'>=======  ClasseVivaAPI - Python  =======</h1>

<br></br>

## Informazioni

[`ClasseVivaAPI`]() è una libreria <b>[`Python`](https://www.python.org/)</b> che permette di utlizzare l'API di <b>[`Classeviva`](https://web.spaggiari.eu/)</b> - <b>[`GruppoSpaggiariParma`](https://web.spaggiari.eu/www/app/default/index.php)</b> per ottenere informazioni come <b>Voti</b>, <b>Note</b> e <b>Documenti</b>, relative ad un account ClasseViva.

<br></br>

## Installa ClasseVivaAPI da [`PyPI`]()

```bash
pip install CVV-API
```
<br></br>

## Utilizzo

<b>Richiedi i VOTI di un utente (richiesta senza parametri):</b>
```py
from ClasseVivaAPI import Utente, RequestURLs

utente = Utente(uid="USERNAME", pwd="PASSWORD")  # Crea un Utente utilizzando USERNAME e PASSWORD del tuo account ClasseViva
utente.login()  # Effetua l'accesso all'account, verificando che i dati inseriti siano corretti

voti = utente.request(RequestURLs.voti)  # Richiesta all'API (utente.request()) di ottenere i VOTI (ReqeusteURLs.voti) dell'utente dal quale si effettua la richiesta
print(voti.json())  # Stampa il risultato della richiesto nella console, in formato JSON
```
#

<b>Richiedi l'AGENDA di un utente (richiesta con parametri):</b>
```py
from ClasseVivaAPI import Utente, RequestURLs

utente = Utente(uid="USERNAME", pwd="PASSWORD")  # Crea un Utente utilizzando USERNAME e PASSWORD del tuo account ClasseViva
utente.login()  # Effetua l'accesso all'account, verificando che i dati inseriti siano corretti

voti = utente.request(RequestURLs.agenda, (20230301, 20230302))  # Richiesta all'API (utente.request()) di ottenere l'AGENDA (RequestURLs.agenda) dell'utente dal quale si effettua la richiesta, inserendo la data di inizio e di fine in formato AAAAMMGG (Esempio: '20230301' = 1 Marzo 2023)
print(voti.json())  # Stampa il risultato della richiesto nella console, in formato JSON
```

<br></br>
<br></br>

`` Utente ``
-------------------

<b>Rappresenta un utente di ClasseViva (di tipo studente)</b>

<br></br>
**Classe**
```py
class Utente()
```

<br></br>
**Costruttore**
```py
def __init__(
  self,
  uip: str,
  pwd: str
) -> None:
```

&emsp;&emsp; Parametri:

&emsp;&emsp; - ``uid``:  Username dell'utente

&emsp;&emsp; - ``pwd``:  Password dell'utente


<br></br>
**Attributi:**
  - ``self.uid``:  Username dell'utente
  - ``self.pwd``:  Password dell'utente
  - ``self.ident``:  Identificato dell'utente
  - ``self.token``:  Token della sessione
  - ``self.is_logged_in``:  Indica se l'utente ha effettuato l'accesso o meno

<br></br>
**Metodi:**
  - ``self.login()``:  Effettua l'accesso alla sessione di ClasseViva
```py
  login(self) -> Response
```
    
  - ``self.request()``: Invia una richiesta all'API di ClasseViva
```py
  request(self, request_url: tuple, parmas=None) -> Response
```
<br></br>
<br></br>

`` RequestURLs ``
-------------------
<b>Rappresenta la lista di URL disponibili per le richieste all'API di ClasseViva</b>

<br></br>
**Classe**
```py
class RequestURLs()
```

<br></br>
**Attributi:**
- ``self.base_url``: URL di base per le richieste all'API di ClasseViva
- ``self.students_url``: URL di base per le richieste relative agli studenti
<br></br>
- ``self.assenze``: URL per ottenere le informazioni sulle assenze
- ``self.agenda``: URL per ottenere le informazioni sull'agenda
- ``self.didattica``: URL per ottenere le informazioni sulla didattica
- ``self.libri``: URL per ottenere le informazioni sui libri scolastici
- ``self.calendario``: URL per ottenere le informazioni sul calendario
- ``self.card``: URL per ottenere le informazioni sulla card dello studente
- ``self.voti``: URL per ottenere le informazioni sui voti
- ``self.lezioni_oggi``: URL per ottenere le informazioni sulle lezioni del giorno
- ``self.lezioni_giorno``: URL per ottenere le informazioni sulle lezioni di un giorno specifico
- ``self.note``: URL per ottenere le informazioni sulle note
- ``self.periods``: URL per ottenere le informazioni sui periodi
- ``self.materie``: URL per ottenere le informazioni sulle materie
- ``self.login`` URL per effettuare il login
- ``self.noticeboard``: URL per ottenere le informazioni sulla bacheca
- ``self.documenti``: URL per ottenere le informazioni sui documenti

<br></br>
<br></br>

## Contributi e Supporto
Se hai idee per migliorare questa libreria o hai riscontrato problemi, puoi contribuire aprendo issue o pull request su GitHub. Sarò felice di ricevere feedback e aiutarti nelle tue implementazioni.

<br></br>

## Licenza
Questa libreria è rilasciata con la licenza [`MIT License`](https://opensource.org/license/mit/).

Buon utilizzo della libreria ClasseVivaAPI!