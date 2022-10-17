from Google import Create_Service
import json
import datetime 
from datetime import timedelta
from timeit import default_timer as timer

CLIENT_FILE="client.json"
API_NAME="gmail"
API_VERSION="v1"
SCOPES=["https://mail.google.com/"]

SERVICE=Create_Service(CLIENT_FILE,API_NAME,API_VERSION,SCOPES)

def desmenuzar(google_mails):
   ids_emails=[]
   google_id_emails = [item.get("id") for item in google_mails]
   for ids in google_id_emails : 
      ids_emails.append(ids) 
   return ids_emails 

def revchunk(a):
  a_list = list(reversed(a))
  chunked_list = list()
  chunk_size = 1000
  for i in range(0, len(a_list), chunk_size):
      chunked_list.append(a_list[i:i+chunk_size])
  return chunked_list

correo="noreply-co@customers.decathlon.com"
blacklist=[]
dates=[]
actual_date = datetime.date.today()
pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,q=correo).execute()
Tiempo1 = timer()

for msg in pagetoken_dict['messages']:
    m_id = msg['id'] 
    message = SERVICE.users().messages().get(userId='me', id=m_id).execute()
    payload = message['payload'] 
    header = payload['headers']

    for item in header:
        if item['name'] == 'Date':
           date = item['value']
           dates.append(date)

#aqui las convierte en una lista para que se puedan leer
for i in range(len(dates)):
  a = dates[i].split(" ")
  unwanted = [0, 5] 
  for ele in sorted(unwanted, reverse = True):
      del a[ele]
  month_name = a[1]
  #esto es para volver el mes de letras en número
  datetime_object = datetime.datetime.strptime(month_name, "%b")
  a[1] = str(datetime_object.month)
  stri = a[2]+"-"+a[1]+"-"+a[0]+" "+a[3]
  dates[i] = stri
#aquí define la fecha actual
actual_date = datetime.datetime.today()
for date in dates:
  #aquí convierte las cosas en el formato de la libreria Datetime 
  date_given = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
  print(date_given)
  #aquí las compara: si al sumar tres días a la fecha de envío da menor a la fecha actual, pues da True y se borra
  print(f"Es {date_given+timedelta(days = 3) < actual_date} que el correo se envió hace 3 días o más")

print(dates)

if len(pagetoken_dict)==1:
   print(f"No hay mensajes para borrar de la direccion {correo}")
else:
   pagetoken = pagetoken_dict.get('nextPageToken')
   tokens = pagetoken
   blacklist=blacklist+(desmenuzar(pagetoken_dict.get('messages')))

   while tokens!="":
         pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,pageToken=tokens,q=correo).execute()
         pagetoken=pagetoken_dict.get('nextPageToken')
         blacklist=blacklist+(desmenuzar(pagetoken_dict.get('messages')))
         tokens=pagetoken
         if len(pagetoken_dict)==2:
            blacklist=blacklist+(desmenuzar(pagetoken_dict.get('messages')))
            tokens=""
   if len(blacklist)>1000:
      revblacklist=revchunk(blacklist)
      for revlist in revblacklist:
         SERVICE.users().messages().batchDelete(userId="me",body={'ids':revlist}).execute()
      print(f"Borrado exitoso de {len(blacklist)} correos")
   else:
      revblacklist=list(reversed(blacklist))
      SERVICE.users().messages().batchDelete(userId="me",body={'ids':blacklist}).execute()
      print(f"Borrado exitoso de {len(blacklist)} correos de {correo}")
  
Tiempo2 = timer()
TTotal = Tiempo2 - Tiempo1
a=[{correo:len(blacklist),"Tiempo de ejecucion":Tiempo2-Tiempo1}]

if len(pagetoken_dict) !=1:
   try:
      jsonFile = json.load(open('blacklist.json'))
   except FileNotFoundError:
      jsonFile = {}
      archivo = open('blacklist.json', 'a+')
   except json.decoder.JSONDecodeError:
      jsonFile = {}

   jsonFile.setdefault("correo" + str(len(jsonFile) + 1),
    {
        correo: len(blacklist),
        "TiempoEjecucion": Tiempo2 - Tiempo1
    }
)
   archivo = open('blacklist.json', 'w')
   json.dump(jsonFile, archivo, indent=4)
   archivo.close()

print("Tiempo de Procesamiento =",TTotal,"seg.") 
print(a)
blacklist.clear()