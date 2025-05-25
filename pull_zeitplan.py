import datetime
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import json

# api-endpoint
URL = "https://secure.unicatt.it/didatticaweb2/ps/lezioni/"

# defining a params dict for the parameters to be sent to the API
BODY = {
    "codiceSede":"RM",
    "annoAccademico":"2024",
    "codiceFacolta":"75012",
    "codiceCorsoDiLaurea":"0H0C",
    "annoDiCorso":"1"
}

retry_strategy = Retry(
    total=4,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor = 2
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

# sending get request and saving the response as response object
r = http.post(url = URL, json=BODY, timeout=10.0)

# extracting data in json format
data = r.json()
reformatted_data: dict = {
    "main_course_data": data["corsoDiLaurea"],
    "last_executed": str(datetime.datetime.now()),
    "lessons_list": {}
}
lesson_dict: dict = data["lezioniCalendario"]
for date, course_list in lesson_dict.items():
    new_courses_list = []
    for course_data in course_list:
        new_courses_list.append({
            "name" : course_data["descrizioneInsegnamento"],
            "aula" : course_data["descrizioneAula"],
            "start" : course_data["oraInizio"],
            "end" : course_data["oraFine"],
            "note" : course_data["note"],
        })
    reformatted_data["lessons_list"][date] = new_courses_list
pretty_data = json.dumps(reformatted_data, indent=4, sort_keys=True)
print(pretty_data)
with open("lesson_data.json", "w") as file:
    file.write(pretty_data)
