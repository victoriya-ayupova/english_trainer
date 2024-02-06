import requests
from pprint import pprint

url = "https://microsoft-translator-text.p.rapidapi.com/translate"

querystring = {"to[0]": "ru", "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}

# payload1 = [{"Text": "The largest cities, which have territory larger than the capital, are Hamilton, Auckland and Christchurch."}]
# payload = [{'Text':'The word <mstrans:dictionary translation=\"wordomatic\">wordomatic</mstrans:dictionary> is a dictionary entry.'}]
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "3b8bd67427mshed8694733d40180p1b4a89jsnf1e84dff777c",
    "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
}


def translate(sent: str) -> str:
    payload = [{'Text': f'{sent}'}]
    response = requests.post(url, json=payload, headers=headers, params=querystring)
    return response.json()[0]['translations'][0]['text']

