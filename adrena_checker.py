import requests
from lxml import html
from dataclasses import dataclass
# ignore warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

### SECRET VARS ###
CHAT_ID = os.environ.get('CHAT_ID')
TOKEN = os.environ.get('TOKEN')

def website_query(site):
    '''
    Gets request, returns status code
    '''
    response = requests.get(site, verify=False)
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

def create_element_dict(element):
    '''
    creates dictionary from element tags
    '''
    element_dict = {}
    for child in element.getchildren():
        element_dict[child.tag] = child.text
    return element_dict

@dataclass
class Product:
    DISCOUNT: bool
    DISCOUNT_PERCT: str
    PRICE: str

def get_product_info(element_dict):
    '''
    maps element tags to DISCOUNT, DISCOUNT_PERCT, PRICE
    '''
    
    product = Product(DISCOUNT=False, DISCOUNT_PERCT=None, PRICE=None)
    
    if 'strike' in element_dict.keys():
        product.DISCOUNT = True
    if 'h4' in element_dict.keys():
        product.DISCOUNT_PERCT = element_dict['h4']
    if 'h2' in element_dict.keys():
        product.PRICE = element_dict['h2']
    
    return product

# creating a boolean switch
def bool_switch(product):
    '''
    returns True if product is available
    '''

    Status = product.PRICE

    if Status == "On back order":
        return False
    else:
        return True


def tele_messenger(bool_switch, product):
    '''
    sends message to telegram
    '''
    
    if bool_switch == True:
        API_Token = TOKEN
        chat = CHAT_ID

        Price = product.PRICE
        Discount = product.DISCOUNT
        Discount_Perct = product.DISCOUNT_PERCT

        message = 'Poison Adrena 164L BFS-2\nPrice: {}\nDiscount: {}\nDiscount Percentage: {}'.format(
            Price, Discount, Discount_Perct)

        url = f'https://api.telegram.org/bot{API_Token}/sendMessage?chat_id={chat}&text={message}'

        response = requests.get(url)

        return print(response.status_code)

    else:
        return print("Product is not available")

def main():
    '''
    Main function
    '''
    
    xpath_query = xpath_query = "//div[@class='text-right']"
    site = 'https://www.plat.co.jp/shop/catalog/product_info/language/en/products_id/74581/cPath/4027_85_8147/reel/shimano-2024-metanium-dc-71xg-left-handle-free-shipping.html' 
    
    response = website_query(site)
    element = get_element(response, xpath_query)
    element_dict = create_element_dict(element)
    product = get_product_info(element_dict)
    
    status = bool_switch(product)
    
    tele_messenger(status, product)


if __name__ == "__main__":
    main()
