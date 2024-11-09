import requests

url = "http://127.0.0.1:8000/api/upload/"
file_path = "C:/Users/BAPS/Downloads/datasheet.xlsx"
# file_path = "C:/Users/BAPS/Downloads/datasheet.csv"
# file_path = "C:/Users/BAPS/Downloads/datasheet.ics"

# open file and stoer object in varible
with open(file_path, 'rb') as file:
    # postdata
    files = {'file': file}
    
    response = requests.post(url, files=files)    
    print(response.status_code)
    print(response.json())
