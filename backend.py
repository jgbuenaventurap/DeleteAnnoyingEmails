# print('inicio la ejecucion
import datetime
import json
from datetime import timedelta
from timeit import default_timer as timer

from Google import Create_Service

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

with open('correos.json') as json_correos:
   dict_json = json.load(json_correos)
   for info in dict_json["correos"]:
      correo = info["correo"]
      date_json = info["dias"]
      blacklist=[]
      dates=[]
      actual_date = datetime.date.today()
      pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,q=correo).execute()
      Tiempo1 = timer()
      if date_json != 0:
         #blacklist=desmenuzar(pagetoken_dict.get('messages'))
         if len(pagetoken_dict) == 1:
            print(f"No hay mensajes para borrar de la direccion {correo}")
         else:
            for msg in pagetoken_dict['messages']:
               m_id = msg['id'] 
               blacklist.append(m_id)
               size1 = len(blacklist)
               message = SERVICE.users().messages().get(userId='me', id=m_id).execute()
               payload = message['payload'] 
               header = payload['headers']

               for item in header:
                  if item['name'] == 'Date':
                     date = item['value']
                     dates.append(date)
            
            for i in range(len(dates)): #3
               datelist = dates[i].split(" ") #4
               unwanted = [0, 5] 
               for ele in sorted(unwanted, reverse = True):
                  del datelist[ele]
               month_name = datelist[1]
               datetime_object = datetime.datetime.strptime(month_name, "%b")
               datelist[1] = str(datetime_object.month)
               stri = datelist[2]+"-"+datelist[1]+"-"+datelist[0]+" "+datelist[3]
               dates[i] = stri
            actual_date = datetime.datetime.today() #3

            for date in dates: #3
               date_given = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")#4
               if date_given+timedelta(days = date_json) < actual_date:
                  blacklist.pop(dates.index(date)) 
               size2 = len(blacklist)
            if size1 == size2:
               print(f"No hay mensajes para borrar de la direccion {correo}")
            else:
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
            
      else:
         #pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,q=correo).execute()
         if len(pagetoken_dict) == 1:
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

