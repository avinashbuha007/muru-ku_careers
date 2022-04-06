import requests
from lxml import html
from config import db_table_name, connection, cursor, create_database, create_table


def get_job_data(session):
    url = 'https://gokudos.io/careers/'
    payload = {}
    headers = {
        'authority': 'gokudos.io',
        # 'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        # 'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        # 'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'sec-fetch-site': 'none',
        # 'sec-fetch-mode': 'navigate',
        # 'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cookie': 'wschkid=f359cd8b89938fe9635931d2086831c8c29a9aeb.1649316490.1; PHPSESSID=4hrirq09gbttjbrgmkcnutv87g; _gcl_au=1.1.810440712.1649230121; _gid=GA1.2.218951750.1649230121; _fbp=fb.1.1649230123781.1128241675; messagesUtk=73df9772f5024584be72871d75d170a6; _hjSessionUser_2849176=eyJpZCI6Ijc2ODYxNzg1LWNmZDQtNTNjMC04M2I3LTM5MDZhNTM0OTA2ZiIsImNyZWF0ZWQiOjE2NDkyMzAxMjYxNjksImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionRejected=1; _ga_DGB26T33ST=GS1.1.1649241652.4.0.1649241652.0; _ga=GA1.2.69397561.1649230121; _hjIncludedInSessionSample=1; _hjSession_2849176=eyJpZCI6IjNiZTc3YzA5LWQyZmMtNDc5ZS05YjY5LWNmY2Y0YTUyYThjZCIsImNyZWF0ZWQiOjE2NDkyNDE2NTQ2MjYsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=1'
    }

    response = session.get(url, headers=headers, data=payload)

    print(response.status_code, url)

    if response.status_code == 200:
        dom = html.fromstring(response.text)
        post_link = dom.xpath('//h2[@class="entry-title"]/a/@href')
        for post in post_link:
            # response = requests.get(post)
            response = requests.request("GET", post, headers=headers, data=payload)
            post_resp = html.fromstring(response.text)

            job_title = "".join(post_resp.xpath('//h1[@class="entry-title"]/text()'))

            key = post_resp.xpath('//div[@class="entry-content single-content"]/p')
            Description = []
            for k in key:
                key1 = "".join(k.xpath('.//text()'))
                try:
                    # value1 = "".join(k.xpath('.//following-sibling::ul[1]//text()'))
                    value1 = " , ".join(k.xpath('.//strong/parent::p/following-sibling::ul[1]//text()'))
                except:
                    value1 = ""

                if value1:
                    Description.append(f'{key1} = {value1}')
                else:
                    Description.append(key1)

            Description = ' '.join(Description)

            if job_title:
                data_dict = {
                    'website_name': 'gokudos',
                    'website_url': 'https://gokudos.io/',
                    'career_url': 'https://gokudos.io/careers/',
                    'job_title': job_title,
                    'description': Description
                }
            print(data_dict)

            field_list = []
            value_list = []
            for field in data_dict:
                field_list.append(str(field))
                value_list.append(str(data_dict[field]).replace("'", "’"))
            fields = ','.join(field_list)
            values = "','".join(value_list)

            insert_db = f"insert into {db_table_name} " + "( " + fields + " ) values ( '" + values + "' )"
            try:
                cursor.execute(insert_db)
                print('Data inserted')
            except Exception as e:
                print(e)
            connection.commit()


if __name__ == "__main__":
    create_database()
    create_table()
    session = requests.Session()
    try:
        get_job_data(session)
    except Exception as e:
        print(e)
