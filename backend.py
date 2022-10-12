from Google import Create_Service
import json
import datetime 

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

"""def jsonBlacklist():
   a_file = open("blacklist.json", "r")
   json_object = json.load(a_file)
   a_file.close()
   json_object={correo:len(blacklist)}
   a_file = open("blacklist.json", "a")
   json.dump(json_object, a_file)
   a_file.close()"""

correo="newsletter@bbcearth.bbc.com"
blacklist=[]
dates=[]
actual_date = datetime.date.today()
print(actual_date)
pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,q=correo).execute()

for msg in pagetoken_dict['messages']:
    m_id = msg['id'] # get id of individual message
    message = SERVICE.users().messages().get(userId='me', id=m_id).execute()
    payload = message['payload'] 
    header = payload['headers']

    for item in header:
        if item['name'] == 'Date':
           date = item['value']
           dates.append(date)



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
         #jsonBlacklist()
         SERVICE.users().messages().batchDelete(userId="me",body={'ids':revlist}).execute()
      print(f"Borrado exitoso de {len(blacklist)} correos")
   else:
      revblacklist=list(reversed(blacklist))
      #jsonBlacklist()
      SERVICE.users().messages().batchDelete(userId="me",body={'ids':blacklist}).execute()
      print(f"Borrado exitoso de {len(blacklist)} correos de {correo}")
   blacklist.clear()



   
          
