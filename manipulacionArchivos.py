import json


def OpenfileCorreos():   
    emailS =  [];

    with open("correos.json", "r") as file:
        emailS = json.load(file);

    return emailS;


def upDateFileCorreos(correos):
    with open("correos.json","w") as archivo:
        json.dump(correos, archivo,indent=4);
     

# for a in emailS['correos']:
#     if a['correo'] == 'noticias@promociones.cinemark.com.co':
#         print([a]);
