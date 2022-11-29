import json


def OpenfileCorreos():
    emailS = []
    objeUpdate = {}
    with open("correos.json", "r") as file:
        emailS = json.load(file)
        listCorreos = emailS["correos"]
        objeUpdate = {listCorreos}
    return objeUpdate


def upDateFileCorreos(correos):
    with open("correos.json", "w") as archivo:
        json.dump(correos, archivo, indent=4)


def agreeMail(mail: str, days: int):
    obje = {"correo": mail, "dias": days}
    emailS = []
    objeUpdate = {}
    with open("correos.json", "r") as file:
        emailS = json.load(file)
        listCorreos = emailS["correos"]
        if obje in listCorreos:
            if obje["correo"] == mail:
               index = listCorreos.index(obje)
               listCorreos[index] = listCorreos.appen(obje)
        else:
            listCorreos.append(obje)
        objeUpdate = {"correos": listCorreos}
    with open("correos.json", "w") as file_update:
        json.dump(objeUpdate, file_update, indent=4)

    return objeUpdate
