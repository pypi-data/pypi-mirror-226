import os

from aibloks.errors import AiBloksException
from aibloks.requestor import Requestor

class Library:

    def __init__(self, requestor, name):
        self.requestor = requestor
        self.name = name

    def __str__(self):
        return f"{self.name} {self.get_status()}"
     
    def get_status(self):
        return self.requestor.make_request(method="GET", route=f"api/v1/libraries/{self.name}/status").json()
    
    def get_documents(self):
        response = self.requestor.make_request(method="GET", route=f"api/v1/libraries/{self.name}/documents/").text
        responseObj = self.requestor.json_to_obj(response)
        if not responseObj.documents:
            return []
        return responseObj.documents
    
    def upload_document(self, document_path): 
        files = {'file':(os.path.basename(document_path), open(document_path, 'rb'))}
        return self.requestor.make_request(method="POST", route=f"api/v1/libraries/{self.name}/documents/upload", files=files).json()
   
    def initialize(self):
        print ("TBD")
        
    def import_documents(self, service, bucket_name, access_key, access_secret, folder=""):
        if service == "aws_s3":
            json_payload = {
                "awsConfig": {
                    "bucketName": bucket_name,
                    "accessKey": access_key,
                    "accessSecret": access_secret,
                    "folder": folder
                }
            }
            return self.requestor.make_request(method="POST", route=f"api/v1/libraries/{self.name}/documents/import", json=json_payload).json()
        raise AiBloksException(f"Unsupported service type for library import: '{service}'")