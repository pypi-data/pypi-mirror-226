import os

from aibloks.errors import AiBloksException
from aibloks.library import Library
from aibloks.requestor import Requestor

class Libraries():

    def __init__(self, requestor):
        self.requestor = requestor
    
    def get_libraries(self):
        response = self.requestor.make_request(method="GET", route="api/v1/libraries").json()
        if 'libraries' not in response:
            raise AiBloksException("An unknown error occured retrieving user libraries")
        libraries = []
        for library_json in response["libraries"]:
            libraries.append(Library(self.requestor,library_json["name"]))
        return libraries

    def get_library(self, library_name):
        self.requestor.make_request(method="GET", route=f"api/v1/libraries/{library_name}").json()
        return Library(self.requestor, library_name)
    
    def create_library(self,library_name):
        self.requestor.make_request(method="POST", route='api/v1/libraries/', json={ 'name': library_name }).json()
        return Library(self.requestor, library_name)
     
    def delete_library(self, library):
        return self.requestor.make_request(method="DELETE", route=f"api/v1/libraries/{library.name}").json()


