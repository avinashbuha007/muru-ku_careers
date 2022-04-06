import requests
from lxml import html
from config import ConfigDatabase


crsr = ConfigDatabase.DictCrsr
sourceTable = ConfigDatabase.table_name

try:
    conn = ConfigDatabase.conn
    conn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {ConfigDatabase.databse_name}")
    crsr = conn.cursor()
    CT = f"""CREATE TABLE IF NOT EXISTS `{ConfigDatabase.table_name}` (`ID` int(11) NOT NULL AUTO_INCREMENT,
                                                                `website_name` TEXT,
                                                                `website_url` TEXT,
                                                                `career_url` TEXT,
                                                                `job_title` TEXT,
                                                                `location` TEXT,
                                                                `description` longtext,
                                                                PRIMARY KEY (`ID`))"""
    crsr.execute(CT)
    conn.commit()

except Exception as e:
    print(e)

def get_job_data(session, job_url):
    response = session.get(job_url)
    print(response.status_code, job_url)

    if response.status_code == 200:
        dom = html.fromstring(response.text)

        try:
            try:
                job_title = dom.xpath('//div[@class="career-job-name"]//div[@class="animated fadeInLeftShort"]/b/text()')[0]
            except:
                job_title = None

            try:
               loc = ''.join(dom.xpath('//div[@class="career-job-name"]//div[@class="animated fadeInLeftShort"]/p/text()'))
               location = loc.split(',')[0]
            except:
                location = None

            try:
                desc = ''.join(dom.xpath('//*[@class="desc"]//text()')).strip().replace('\r','').strip()
                description = "".join(list(filter(None, desc)))

            except:
                description = ""
            if job_title:
                data_dict = {
                    'website_name': 'fincrew',
                    'website_url': 'https://www.fincrew.my/',
                    'career_url': 'https://www.fincrew.my/en/career.html',
                    'job_title': job_title,
                    'location': location,
                    'description': description
                }

                connection = ConfigDatabase.conn
                cursor = ConfigDatabase.DictCrsr

                field_list = []
                value_list = []
                for field in data_dict:
                    field_list.append(str(field))
                    value_list.append(str(data_dict[field]).replace("'", "’"))
                fields = ','.join(field_list)

                values = "','".join(value_list)
                insert_db = f"insert into {ConfigDatabase.table_name} " + "( " + fields + " ) values ( '" + values + "' )"
                cursor.execute(insert_db)

                connection.commit()
                print(data_dict)

        except Exception as e:
            print(e)
            print("data not found")

def get_career_data(session):
    career_url = "https://www.fincrew.my/en/career.html"
    response = session.get(career_url)
    print(response.status_code, career_url)

    if response.status_code == 200:
        dom = html.fromstring(response.text)

        try:
            a = dom.xpath('//li[@class="animated fadeInLeft"]')
            for i in a:
                job_url = i.xpath('./div[@class="career-apply"]/a/@href')[0]
                get_job_data(session, job_url)
        except:
            print("job url not forund")

if __name__ == "__main__":
    session = requests.Session()
    try:
        get_career_data(session)
    except Exception as e:
        print(e)
    ConfigDatabase.conn.close()

