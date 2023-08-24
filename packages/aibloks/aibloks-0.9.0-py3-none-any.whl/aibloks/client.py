import json
import requests
from urllib.parse import urljoin

from aibloks.libraries import Libraries
from aibloks.requestor import Requestor
from aibloks.instantai import InstantAi

class AiBloksClient:

    def __init__(self, username, api_key, endpoint_url="https://app.aibloks.com"):
        self.requestor = Requestor(username, api_key, endpoint_url)
        self.libraries = Libraries(self.requestor)
        self.instantai = InstantAi(self.requestor)
    
    # Library Methods
    def get_libraries(self):
        return self.libraries.get_libraries()
    
    def get_library(self, library_name):
        return self.libraries.get_library(library_name)
    
    def create_library(self, library_name):
        return self.libraries.create_library(library_name)
    
    def delete_library(self, library_name):
        return self.libraries.delete_library(library_name)
    
    # Ai Retrieval Methods
    

    # InstantAi Methods
    def get_instantai_models(self, library):
        return self.instantai.get_models(library)
    
    def get_instantai_templates(self, library):
        return self.instantai.get_templates(library)
    
    def get_instantai_reports(self, library):
        return self.instantai.get_reports(library_name)
    
    def get_instantai_report(self, ai_trx_id):
        return self.instantai.get_report(ai_trx_id)
    
    def create_instantai_report(self, library, template_name, gen_model_name, doc_list=[]):
        return self.instantai.create_report(library, template_name, gen_model_name, doc_list)


    def download_instantai_report(self, library, ai_trx_id, download_folder):
        return self.instantai.download_instantai_report(library, ai_trx_id, download_folder)
    
    