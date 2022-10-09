from Google import Create_Service

CLIENT_FILE="client.json"
API_NAME="gmail"
API_VERSION="v1"
SCOPES=["https://mail.google.com/"]

SERVICE=Create_Service(CLIENT_FILE,API_NAME,API_VERSION,SCOPES)
correo="no-reply@twitch.tv"
flag=False
pagetoken_list=[]
ids_emails=[]
tokens=""
count=0
while flag==False:
   pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,q=correo).execute()
   pagetoken=pagetoken_dict.get('nextPageToken')
   pagetoken_list.append(pagetoken)
   tokens=pagetoken
   while tokens!="":
      print(flag)
      pagetoken_dict=SERVICE.users().messages().list(userId="me",maxResults=500,pageToken=tokens,q=correo).execute()
      pagetoken=pagetoken_dict.get('nextPageToken')
      print(pagetoken)
      print(len(pagetoken_dict))
      print(tokens)
      pagetoken_list.append(pagetoken)
      tokens=pagetoken
      if len(pagetoken_dict)==2:
         tokens=""
         flag=True

print(pagetoken_list)

for token_sheet in pagetoken_list :
   google_dict=SERVICE.users().messages().list(userId="me",maxResults=500,pageToken=token_sheet,q=correo).execute()
   google_mails=(google_dict.get('messages'))
   google_id_emails = [item.get("id") for item in google_mails]
   for ids in google_id_emails : 
            ids_emails.append(ids)  

print(ids_emails)
for ids in ids_emails:

   SERVICE.users().messages().delete(userId="me",id=ids).execute() 
   count+=1
   print(f"id correo {count} ")

#SERVICE.users().messages().batchDelete(userId="me").body({"ids":ids_emails})

pagetoken_list.clear()
google_id_emails.clear()
ids_emails.clear()
