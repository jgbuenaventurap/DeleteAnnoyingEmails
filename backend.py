from Google import Create_Service

CLIENT_FILE="client.json"
API_NAME="gmail"
API_VERSION="v1"
SCOPES=["https://mail.google.com/"]

SERVICE=Create_Service(CLIENT_FILE,API_NAME,API_VERSION,SCOPES)

google_dict=SERVICE.users().messages().list(userId="me",q="updates@academia-mail.com").execute()
google_mails=(google_dict.get('messages'))
google_id_emails = [item.get("id") for item in google_mails]
print(len(google_id_emails))
for ids in google_id_emails:

   SERVICE.users().messages().delete(userId="me",id=ids).execute() 
   print(f"id correo {ids} ")


