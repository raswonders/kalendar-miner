import sys
import pickle
import requests as req
from bs4 import BeautifulSoup

site = 'http://kalendar.aktuality.sk/meniny/'


def main():
    save_test_page(site)
    # soup = parse_page(site)
    # print(soup)


def test():
    soup = load_test_page()
    print(soup)


def parse_page(url, payload=None):
    try:
        response = req.get(url, payload)
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


if __name__ in ["__main__", "builtins", "pydevconsole"]:
    # main()
    test()
