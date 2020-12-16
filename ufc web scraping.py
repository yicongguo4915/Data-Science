import json, requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

url = 'http://ufcstats.com/statistics/fighters'

def extract_data(c):
    curr_url = url + "?char={}&page=all".format(c)
    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'

        r = s.get(curr_url)
        soup = BeautifulSoup(r.content, 'html5lib')
        blocks = soup.select('.b-statistics__table-row')
        output = []
        for block in blocks[2:]:
            # print(block)
            link = block.select_one('a')['href']
            fighter_data = get_fighter(link)
            output.append(fighter_data)

        return output


def get_fighter(fighter_url):
    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'

        r   = s.get(fighter_url)
        soup = BeautifulSoup(r.content, 'html5lib')

        name   = soup.select_one('.b-content__title-highlight').text.strip()
        record = soup.select_one('.b-content__title-record').text.strip().split()[-1]
        nick   = soup.select_one('.b-content__Nickname').text.strip()

        fighter = dict(Name=name, Record=record, Nickname=nick)

        for i in soup.select('li .b-list__box-item-title'):
            stat, value = i.text.strip()[:-1], i.next.next.strip()
            if stat:
                fighter[stat] = value

        return fighter

def extract_fighter_data():
    data = []
    for i in range(26):
        curr_char = chr(ord('a') + i)
        curr_data = extract_data(curr_char)
        data = data + curr_data

    # print(type(data[0]))
    dfItem = pd.read_json(json.dumps(data))
    dfItem.to_csv('ufc scrapping data.csv')

    return dfItem
    # print(dfItem)

if __name__ == "__main__":
    data_frame = extract_fighter_data()
    # print(data_frame)