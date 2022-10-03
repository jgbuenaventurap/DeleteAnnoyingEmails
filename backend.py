from Google import Create_Service

CLIENT_FILE="client.json"
API_NAME="gmail"
API_VERSION="v1"
SCOPES=["https://mail.google.com/"]

SERVICE=Create_Service(CLIENT_FILE,API_NAME,API_VERSION,SCOPES)
SERVICE.users().getProfile(userId="me").execute()
SERVICE.users().messages().list(userId="me",q="otraformadeestudiar@palermo.edu").execute()
SERVICE.users().messages().delete(userId="me",id="18376d3f581c8c06").execute()