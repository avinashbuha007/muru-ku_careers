import requests
from lxml import html
from config import db_table_name, connection, cursor, create_database, create_table


def get_job_data(session):
    url = 'https://careers.kaodim.com/posts'
    response = session.get(url)
    print(response.status_code, url)

    if response.status_code == 200:
        dom = html.fromstring(response.text)

        for tr in dom.xpath('//*[@class="job-table mt-60"]//tbody//tr'):
            job_title = ""
            try:
                for job_title in tr.xpath('.//td[1]//a//text()'):
                    job_title = job_title.replace('\r', '').replace('\n', '').replace('\t', '').strip()
            except:
                job_title = None

            location = ""
            try:
                for location in tr.xpath('.//td[3]//text()'):
                    location = location.replace('\r', '').replace('\n', '').replace('\t', '').strip()
            except:
                location = None

            description = ""
            try:
                description_links = tr.xpath('.//td[1]//a//@href')[0]
                whole_link = 'https://careers.kaodim.com' + description_links
                post_url = requests.get(whole_link)
                response = html.fromstring(post_url.text)
                description = ' '.join(
                    response.xpath('//*[@class="content-markdown col-md-10 mx-auto"]//text()')).replace('\n',
                                                                                                        ' ').strip()
            except:
                description = ""

            if job_title:
                data_dict = {
                    'website_name': 'kaodim',
                    'website_url': 'https://www.kaodim.com/',
                    'career_url': 'https://careers.kaodim.com/posts',
                    'job_title': job_title,
                    'location': location,
                    'description': description
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

            connection.commit()


if __name__ == "__main__":
    create_database()
    create_table()
    session = requests.Session()
    try:
        get_job_data(session)
    except Exception as e:
        print(e)
