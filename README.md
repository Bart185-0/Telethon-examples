# Telethon-examples

INSTALL
-------------------------
Debian 10 64-bit
Installazione pulita su vps remota o in locale con vmware o direttamente su macchina fisica.

Verifica python3
----------------------------------------------------------------------------------------------------
y21@debian:~$ python3 -V
Python 3.7.3

Installare il gestore di pacchetti Pip se non presente
----------------------------------------------------------------------------------------------------
y21@debian:~$ sudo apt install python3-pip

Verifica installazione di Pip
----------------------------------------------------------------------------------------------------
y21@debian:~$ pip3 --version

pip 18.1 from /usr/lib/python3/dist-packages/pip (python 3.7)

Installare la libreria Telethon
----------------------------------------------------------------------------------------------------
y21@debian:~$ pip3 install -U telethon

Verifica installazione Telethon
----------------------------------------------------------------------------------------------------
y21@debian:~$ python3 -c "import telethon; print(telethon.__version__)"
1.21.1

Installare cryptg
----------------------------------------------------------------------------------------------------
y21@debian:~$ pip3 install -U --user telethon cryptg

Verifica installazione Cryptg
----------------------------------------------------------------------------------------------------
y21@debian:~$ pip3 show cryptg

Name: cryptg

Version: 0.2.post4

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

cryptg   -> https://github.com/cher-nov/cryptg
telethon -> https://github.com/LonamiWebs/Telethon

