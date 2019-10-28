from getpass import getpass
from yandex_music.client import Client
from yandex_music.exceptions import BadRequest

filename = 'credentials.json'
login = input("Yandex e-mail adress: ")
password = getpass()

try:
    client = Client.from_credentials(login, password)
except BadRequest:
    print("Login or password is not valid")
else:
    cred = '{"token":"' + client.token + '"}'
    with open(filename, "w") as file:
        file.write(cred)
    print(f"Your token successfully saved into '{filename}'")
