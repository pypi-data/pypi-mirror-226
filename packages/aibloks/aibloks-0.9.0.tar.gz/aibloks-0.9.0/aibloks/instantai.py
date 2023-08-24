import json
import os

from aibloks.errors import AiBloksException
from aibloks.requestor import Requestor

class InstantAi:

    def __init__(self, requestor):
        self.requestor = requestor

    def get_templates(self, library):
        json_payload = {
            "library_name": library.name
        }
        response = self.requestor.make_request(method="GET", route=f"api/v1/instantai/templates", json=json_payload).text
        responseObj = self.requestor.json_to_obj(response)
        if not responseObj.templates:
            return []
        return responseObj.templates
    
    def get_models(self, library):
        json_payload = {
            "library_name": library.name
        }
        response = self.requestor.make_request(method="GET", route=f"api/v1/instantai/models", json=json_payload).text
        responseObj = self.requestor.json_to_obj(response)
        if not responseObj.models:
            return []
        return responseObj.models

    def get_reports(self, library):
        json_payload = {
            "library_name": library.name
        }
        response = self.requestor.make_request(method="GET", route=f"api/v1/instantai/reports", json=json_payload).text
        responseObj = self.requestor.json_to_obj(response)
        if not responseObj.reports:
            return []
        return responseObj.reports
    
    def create_report(self, library, template, gen_model, doc_list=[]):
        json_payload = {
            "library": library.name,
            "templateName": template.name,
            "genModelName": gen_model.model_name,
            "docList": doc_list
        }
        response = self.requestor.make_request(method="POST", route=f"api/v1/instantai/reports", json=json_payload).json()
        if 'ai_trx_id' not in response:
            raise AiBloksException("Error: Failed to create report")
        return response['ai_trx_id']
    
    def get_report(self, ai_trx_id): 
        response = self.requestor.make_request(method="GET", route=f"api/v1/instantai/reports/{ai_trx_id}").text
        responseObj = self.requestor.json_to_obj(response)
        if not responseObj.report:
            return {}
        return responseObj.report

    def download_instantai_report(self, library, ai_trx_id, download_folder):
        json_payload = {
            "library_name": library.name,
            "ai_trx_id": int(ai_trx_id)
        }
        response = self.requestor.make_request(method="GET", route=f"api/v1/instantai/reports/{ai_trx_id}/files", json=json_payload)

        # Get the filename from the Content-Disposition header
        content_disposition = response.headers['Content-Disposition']
        file_name = "aibloks_report.zip"
        for part in content_disposition.split(';'):
            if 'filename=' in part:
                file_name = part.split('=')[1].strip()
                break
        
        # Download the file
        downloaded_file = os.path.join(download_folder, file_name)
        open(downloaded_file, 'wb').write(response.content)
        return downloaded_file
       