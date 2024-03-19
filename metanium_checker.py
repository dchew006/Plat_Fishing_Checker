import os
import requests
from lxml import html
from dataclasses import dataclass
# ignore warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"

### SECRET VARS ###
CHAT_ID = os.environ.get('CHAT_ID')
TOKEN = os.environ.get('TOKEN')

def website_query(site):
    '''
    Gets request, returns status code
    '''
    response = requests.get(site, verify=False, headers={
                            'User-Agent': user_agent})
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return ValueError

    return response


def get_element(response, xpath_query):
    '''
    Get elements
    '''
    tree = html.fromstring(response.content)
    element = tree.xpath(xpath_query)

    # Conditional Check > ValueError on None
    if element:
        pass
    else:
        return ValueError

    return element[0]

def bool_switch(product):
    '''
    returns True if product is available
    '''
    
    if product == ValueError:
        return True
    else:
        return False


def tele_messenger(bool_switch, site):
    '''
    sends message to telegram
    '''

    if bool_switch == True:
        API_Token = TOKEN
        chat = CHAT_ID

        message = 'Metanium DC 71XG is available.\nSite: ' + site

        url = f'https://api.telegram.org/bot{API_Token}/sendMessage?chat_id={chat}&text={message}'

        response = requests.get(url)

        return print(response.status_code)

    else:
        return print("Product is not available")


def main():
    '''
    Main function
    '''

    xpath_query = xpath_query = "//span[@data-role='no_stock']"
    site = 'https://www.digitaka.com/item/5/4/2/4969363046659'

    response = website_query(site)
    product = get_element(response, xpath_query)
    status = bool_switch(product)

    print(status)
    tele_messenger(status, site)


if __name__ == "__main__":
    main()