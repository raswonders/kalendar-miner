import sys
import json
import pickle
import requests as req
from bs4 import BeautifulSoup

site = 'http://kalendar.aktuality.sk/meniny/'

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Spt',
          'Oct', 'Nov', 'Dec']


def main():
    # soup = load_test_page()
    # print(soup)
    soup = parse_page(site)
    root_elem = soup.find(id='content-inner')
    table_list = root_elem.find_all('table')
    # dictionary contains list of names for each month
    cal_dict = {}
    i = 0
    # <table> represents a month and <tr> a day
    # first <tr> always add empty name in the zero index
    for table_elem in table_list:
        names_month = []
        for tr_elem in table_elem.find_all('tr'):
            names_day = []
            name_data = tr_elem.find('td', class_='value')
            if name_data is not None:
                for a_elem in name_data.find_all('a'):
                    names_day.append(a_elem.string)
            names_month.append(', '.join(names_day))
        # 1st Jan (i == 0) and May (i == 4) has no name
        if i == 0 or i == 4:
            names_month.insert(1, '')
        # 2nd Nov (i == 10) has no name
        elif i == 10:
            names_month.insert(2, '')
        # 25th Dec (i == 11) has no name
        elif i == 11:
            names_month.insert(25, '')
        cal_dict[months[i]] = names_month
        i += 1

    test_cal_dict(cal_dict)
    save_json_as_js(cal_dict, "calendar.js")


def parse_page(url, payload=None):
    try:
        response = req.get(url, payload)
        response.encoding = "utf-8"
    except req.exceptions.ConnectionError:
        print("ERROR: couldn't connect")
        sys.exit(1)
    else:
        if response.status_code >= 400:
            print("ERROR: status code %s!" % response.status_code)
            sys.exit(1)
        else:
            return BeautifulSoup(response.text, 'lxml')


def save_test_page(url, filename='test_page'):
    sys.setrecursionlimit(20000)
    soup = parse_page(url)
    with open(filename, 'wb') as file:
        pickle.dump(soup, file)


def load_test_page(filename='test_page'):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def save_json_as_js(data, filename):
    with open(filename, 'w') as file:
        file.write('calendar_str = ')
        file.write(repr(json.dumps(data)))


def test_cal_dict(calendar_dict):
    test_year(calendar_dict)
    test_month(calendar_dict, 'Jan', 31, '', 'Emil')
    test_month(calendar_dict, 'Feb', 28, 'Tatiana', 'Zlatica')
    test_month(calendar_dict, 'Mar', 31, 'Albín', 'Benjamín')
    test_month(calendar_dict, 'Apr', 30, 'Hugo', 'Anastázia')
    test_month(calendar_dict, 'May', 31, '', 'Petrana, Petronela')
    test_month(calendar_dict, 'Jun', 30, 'Žaneta', 'Melánia')
    test_month(calendar_dict, 'Jul', 31, 'Diana', 'Ignác')
    test_month(calendar_dict, 'Aug', 31, 'Božidara', 'Nora')
    test_month(calendar_dict, 'Spt', 30, 'Drahoslava', 'Jarolím')
    test_month(calendar_dict, 'Oct', 31, 'Arnold', 'Aurélia')
    test_month(calendar_dict, 'Nov', 30, 'Denis, Denisa', 'Ondrej, Andrej')
    test_month(calendar_dict, 'Dec', 31, 'Edmund', 'Silvester')


def test_year(calendar_dict):
    # Calendar has 12 months
    assert len(calendar_dict) == 12, "Should be 12"


def test_month(calendar_dict, month_name, month_len, first_name, last_name):
    month_len_comp = month_len + 1
    assert len(calendar_dict[month_name]) == month_len_comp, "Should be %s" % str(month_len_comp)
    assert calendar_dict[month_name][1] == first_name, "Should be %s" % first_name
    assert calendar_dict[month_name][month_len] == last_name, "Should be %s" % last_name


if __name__ in ["__main__", "builtins", "pydevconsole"]:
    main()
