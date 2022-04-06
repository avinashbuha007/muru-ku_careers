import requests
from lxml import html
from config import db_table_name, connection, cursor, create_database, create_table


def get_job_data(session):
    url = 'https://www.ezyhaul.com/career/'
    response = session.get(url)
    print(response.status_code, url)

    if response.status_code == 200:
        all_post = []
        site_link = "https://career.thelorry.com/"
        response = requests.get(site_link)
        resp = html.fromstring(response.text)

        job_link = resp.xpath('//a[@class="awsm-job-listing-item awsm-grid-item"]/@href')
        for job in job_link:
            all_post.append(job)

        i = 1
        while i < 5:

            url = "https://career.thelorry.com/wp-admin/admin-ajax.php"

            payload = f"action=loadmore&paged={i}&listings_per_page=6"
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
                'Origin': 'https://career.thelorry.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://career.thelorry.com/',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.'
            }

            post_response = requests.post(url, headers=headers, data=payload)
            post_type = html.fromstring(post_response.content)
            available = post_type.xpath('//*[@class="awsm-load-more-main awsm-no-more-jobs-container"]//text()')
            if available:
                break
            job_post = post_type.xpath('//a[@class="awsm-job-listing-item awsm-grid-item"]/@href')
            for job in job_post:
                all_post.append(job)
            i += 1

        for job in all_post:
            job_response = requests.get(job)
            job_resp = html.fromstring(job_response.text)

            job_title = "".join(job_resp.xpath('//*[@class="entry-title"]/text()')).replace("\u200b", "").strip()

            try:
                key = job_resp.xpath('//div[@class="awsm-job-entry-content entry-content"]/p/strong')
                value = job_resp.xpath('//div[@class="awsm-job-entry-content entry-content"]/p/following-sibling::ul')
                Description = []
                for i in range(0, len(key)):
                    key1 = " ".join(key[i].xpath('./text()'))
                    value1 = " , ".join(value[i].xpath('./li/text()')).replace(' ', ' ').replace("\u200b", "").strip()

                    desc = f"{key1} = {value1} "
                    Description.append(desc)

                if not Description:
                    key = job_resp.xpath('//div[@class="awsm-job-entry-content entry-content"]//h4')
                    for i in key:
                        key1 = " ".join(i.xpath('./text()'))
                        value1 = " ".join(i.xpath(f'./following-sibling::ul[1]/li/text()')).replace(' ', ' ').replace("\u200b", "").strip()

                        desc = f"{key1} = {value1} "
                        Description.append(desc)

            except Exception as e:
                key = job_resp.xpath('//div[@class="awsm-job-entry-content entry-content"]/p/strong')
                value = job_resp.xpath('//div[@class="awsm-job-entry-content entry-content"]/p/following-sibling::ul')
                Description = []
                for i in range(0, len(key)-1):
                    key1 = " ".join(key[i+1].xpath('./text()'))
                    value1 = " , ".join(value[i].xpath('./li/text()')).replace(' ', ' ').replace("\u200b", "").strip()

                    desc = f"{key1} = {value1} "
                    Description.append(desc)

            Description = ''.join(Description)

            location = ", ".join(
                job_resp.xpath('//*[contains(text(),"Job Location: ")]/parent::span/following-sibling::span/text()'))

            if job_title:
                    data_dict = {
                        'website_name': 'thelorry',
                        'website_url': 'https://thelorry.com/my/',
                        'career_url': 'https://career.thelorry.com/',
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
