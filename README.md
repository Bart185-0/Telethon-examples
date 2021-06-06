# Telethon-examples

Prerequisiti
--------------------------------------------------

- Debian 10 64-bit o derivati

- Python 3.7.3

- Gestore di pacchetti pip3  - > sudo apt install python3-pip

- Telethon library -> pip3 install -U telethon  (testato su v1.19.2 e v1.21.1)

- Cryptg -> pip3 install -U --user telethon cryptg

- sqlite3 per asyncio aiosqlite -> pip install aiosqlite

----------------------------------------------------------------------------------------------------
cryptg   -> https://github.com/cher-nov/cryptg

telethon -> https://github.com/LonamiWebs/Telethon


IMPORTANTE
--------------------------------------------------
Compilare i campi all'interno dello script di esempio. I campi sono personali e quindi non forniti qui.

channel = "https://t.me/"  -> link del canale  

phone    = ""              -> vostro numero di telefono

api_id   = ""              -> api_id vedi sotto-> 

api_hash = ""              -> api_hash vedi sotto

upday    = "2021-06-06"    -> indica la data di upload del file. Scegliete un giorno disponibile secondo il formato "YYYY-MM-DD"

percorso = "/home/"        -> un percorso dove scaricare i file e con diritti di scrittura


----------------------------------------------------------------------------------------------------
Ottenere i valori di api_id e api_hash da telegram
----------------------------------------------------------------------------------------------------
Raggiungere la pagina https://my.telegram.org/auth

Digitare il proprio numero di telefono compreso di prefisso internazionale oppure un numero virtuale

Ricevi un msg su telegram client: prendi nota del codice ricevuto esempio 'dzrf8n7jag'

Incollalo nel campo confirm code

Cliccare su API development tools

Completare i campi richiesti

Prendere nota dei valori di "App api_id:" e "App api_hash"

----------------------------------------------------------------------------------------------------

