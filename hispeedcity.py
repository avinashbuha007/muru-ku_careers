import requests
from lxml import html
import sys
from config import db_table_name,connection, cursor, create_database, create_table

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}


def get_description(dom):
    description = ""
    try:
        for tr in dom.xpath('//table[@class="table"]/tr'):
            desc = tr.xpath('./td/div/ul/li/text()')
            description = "\n".join(list(filter(None,desc)))
    except:
        description = None
    return description


def get_job_data(session, job_url):
    response = session.get(job_url, headers=headers)
    print(response.status_code, job_url)

    if response.status_code == 200:
        dom = html.fromstring(response.text)

        try:
            for tr in dom.xpath('//table[@class="table"]/tr'):
                job_title = ""
                try:
                    for job_title in tr.xpath('./td[1]/text()'):
                        job_title = job_title.replace('\r','').replace('\n','').replace('\t','').strip()
                except:
                    job_title = None

                location = ""
                try:
                    for location in tr.xpath('./td[3]/text()'):
                        location = location.replace('\r','').replace('\n','').replace('\t','').strip()
                except:
                    location = None

                description = ""
                try:
                    desc_button = tr.xpath('./td[7]/button/text()')

                    if desc_button:
                        description = get_description(dom)
                except:
                    description = ""
                if job_title:
                    data_dict = {
                        'website_name': 'hispeedcity',
                        'website_url': 'http://www.hispeedcity.com/',
                        'career_url' : 'http://www.hispeedcity.com/8.html',
                        'job_title': job_title,
                        'location': location,
                        'description': description
                    }

                    field_list = []
                    value_list = []
                    for field in data_dict:
                        field_list.append(str(field))
                        value_list.append(str(data_dict[field]).replace("'", "’"))
                    fields = ','.join(field_list)

                    values = "','".join(value_list)
                    insert_db = f"insert into {db_table_name} " + "( " + fields + " ) values ( '" + values + "' )"
                    cursor.execute(insert_db)

                    connection.commit()
                    print(data_dict)
        except Exception as e:
            print("data not found")


def get_career_data(session):
    career_url = "http://www.hispeedcity.com/8.html"
    response = session.get(career_url, headers=headers)
    print(response.status_code, career_url)

    if response.status_code == 200:
        dom = html.fromstring(response.text)

        try:
            for url in dom.xpath('//div[@class="jrwm_bodyer_a_miaoshu"]//ul/a'):
                job_url_list = url.xpath('./@href')
                if job_url_list:
                    job_url = "http://www.hispeedcity.com/" + job_url_list[0]
                    get_job_data(session, job_url)
        except:
            print("job url not forund")


if __name__ == "__main__":
    create_database()
    create_table()
    session = requests.Session()
    try:
        get_career_data(session)
    except Exception as e:
        print(e)
    connection.close()
