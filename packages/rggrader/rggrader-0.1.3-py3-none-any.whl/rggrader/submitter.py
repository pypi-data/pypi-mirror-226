import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def submit(id_student, name, assignment_name, result, question_name='', code=''):
    data = {
        "id": id_student,
        "name": name,
        "assignment_name": assignment_name,
        "question_name": question_name,
        "code": code,
        "result": result
    }

    r = requests.post('https://rea-submitter.fly.dev/submission/submit/bquery', json=data)
    if r.status_code == 200:
        return 'Assignment successfully submitted'
    else:
        return 'Failed to submit assignment'

def upload_image(filename, filepath):
    creds = Credentials.from_service_account_file('service_account.json', 
                                                  scopes=['https://www.googleapis.com/auth/drive'])

    service = build('drive', 'v3', credentials=creds)

    # Search for the file to see if it exists
    response = service.files().list(q="name = '{}'".format(filename),
                                    spaces='drive',
                                    fields='files(id, parents)').execute()
    
    if not response['files']:  # If the file did not exist, create it
        file_metadata = {
            'name': filename, 
            'mimeType': 'image/jpeg', 
            'parents': ['1NovWd7FF2_jXF4YXIZAuNyV5zkMO2CJ1']
        }
        media = MediaFileUpload(filepath,
                                mimetype='image/jpeg',
                                resumable=True)

        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
        print('File created. File ID: %s' % file.get('id'))
    else:  # If the file existed, delete it and create a new one with same metadata
        for file in response['files']:
            old_file_id = file['id']
            old_file_parents = ",".join(file.get('parents', []))
            
            # Create new file
            file_metadata = {
                'name': filename, 
                'mimeType': 'image/jpeg', 
                'parents': ['1NovWd7FF2_jXF4YXIZAuNyV5zkMO2CJ1']
            }
            media = MediaFileUpload(filepath,
                                    mimetype='image/jpeg',
                                    resumable=True)
            new_file = service.files().create(body=file_metadata,
                                              media_body=media,
                                              fields='id').execute()
            
            # Move the new file to the old parent directory
            service.files().update(fileId=new_file['id'],
                                   addParents=old_file_parents).execute()
            
            # Delete the old file
            service.files().delete(fileId=old_file_id).execute()

            print('File updated. Old File ID: %s, New File ID: %s' % (old_file_id, new_file['id']))