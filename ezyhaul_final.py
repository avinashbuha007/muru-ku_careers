import requests
from lxml import html
from config import db_table_name, connection, cursor, create_database, create_table


def get_job_data(session):
    url = 'https://www.ezyhaul.com/career/'
    response = session.get(url)
    print(response.status_code, url)

    if response.status_code == 200:
        dom = html.fromstring(response.text)
        key = dom.xpath('//div[@class="et_pb_toggle_content clearfix"]//p')

        for k in key:

            job_title = "".join(k.xpath('.//strong/text()')).replace("\xa0", "").strip()
            if not job_title:
                job_title = "".join(k.xpath('.//b//text()')).replace("\xa0", "").strip()
            if not job_title:
                job_title = "".join(k.xpath('.//b/span/text()'))
            if ":" in job_title:
                job_title = job_title.split(":")[0].strip()

            if not job_title:
                continue

            location = " ".join(k.xpath('.//preceding::h5//text()'))
            if location:
                location = location.split(' ')[-1]

            Description = "".join(k.xpath('.//following-sibling::ul/li//text()')).replace("\xa0", "").strip()

            if job_title:
                data_dict = {
                    'website_name': 'ezyhaul',
                    'website_url': 'https://www.ezyhaul.com/',
                    'career_url': 'https://www.ezyhaul.com/career/',
                    'job_title': job_title,
                    'location': location,
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
    connection.close()
