#Tax Calculator
    Simple RESTful API to calculate income tax based tax bands provided.

#Installation
    pip3 install -r requirements.txt

#Usage
    python3 manage.py runserver 0.0.0.0:8001

#Endpoints
    /swagger/ - Displays API endpoint info.

    /calculator/ - used to calculate tax owed.
       post:
            {
            "salary": 52000.00, - Decimal field (required)
            "show_tax_bands": true  - boolean (optional)
            }

#Tax Band Inputs:
    changing the file content with in the github repo and setting a flag called refresh_data to True will update the tax bands
