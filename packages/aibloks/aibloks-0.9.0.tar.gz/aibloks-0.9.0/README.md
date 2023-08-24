# Ai Bloks Python API Library

[![PyPI version](https://img.shields.io/pypi/v/anthropic.svg)](https://pypi.org/project/anthropic/)

The Ai Bloks Python library provides access to the [Ai Bloks REST API](https://app.aibloks.com/api/docs/) from any Python 3.10+ application. 

## Installation

```sh
pip install aibloks
```

## Usage

```python
from aibloks import AiBloksClient, AiBloksException, Library

username         = os.environ.get("USERNAME")
api_key          = os.environ.get("API_KEY")
endpoint_url     = os.environ.get("ENDPOINT_URL")
s3_access_key    = os.environ.get("S3_ACCESS_KEY")
s3_access_secret = os.environ.get("S3_ACCESS_SECRET")

try:
    # Create an instance of the AiBloksClient
    aib_client = AiBloksClient(username, api_key, endpoint_url)
 
    # Create a new library
    my_library = aib_client.create_library("my_library")

    # Import files from an AWS S3 Bucket into the library
    my_library.import_documents(service="aws_s3", 
                                bucket_name="aibloks-sample-docs", 
                                access_key=s3_access_key, 
                                access_secret=s3_access_secret )

except AiBloksException as e:
    print(e)
```

## Handling errors

When the library is unable to connect to the API (e.g., due to network connection problems or a timeout), a exception of type AiBloksException is raised. 

## Requirements

Python 3.10 or higher.