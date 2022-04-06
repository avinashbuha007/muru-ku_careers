import requests
from lxml import html
import json
import datetime
import csv


headers = {'Accept':'application/json, text/plain, */*',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}


def get_website_url(session, main_site_url):
    response = session.get(main_site_url, headers=headers)
    print(response.status_code,main_site_url)
    if response.status_code == 200:
        dom = html.fromstring(response.text)
        try:
            json_data = json.loads(response.text)
        except:
            json_data = None

        if json_data:
            for website_url in json_data:
                website_url = website_url['web']

                with open('muru-ku_website_lists.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([website_url])



if __name__ == "__main__":
    with open('muru-ku_website_lists.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["website_url"])

    session = requests.Session()
    main_site_url = "https://startupapi.1337.ventures/startups"
    try:
        get_website_url(session, main_site_url)
    except Exception as e:
        print(e)