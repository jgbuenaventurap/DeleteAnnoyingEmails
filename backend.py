from Google import Create_Service
import json

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

correo="contacto@gorigogo.com"
blacklist=[]

pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,q=correo).execute()
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
if len(blacklist)<1000:
   revblacklist=revchunk(blacklist)
   for revlist in revblacklist:
      SERVICE.users().messages().batchDelete(userId="me",body={'ids':revlist}).execute()
else:
   revblacklist=list(reversed(blacklist))
   SERVICE.users().messages().batchDelete(userId="me",body={'ids':blacklist}).execute()
blacklist.clear()
