import requests
from bs4 import BeautifulSoup
import smtplib
import time

FROM_EMAIL =''
FROM_EMAIL_PW = ''
TO_EMAIL = ''
# You can find your HTTP header at: https://www.whatismybrowser.com/detect/what-is-my-user-agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

product_info = [
     {
         "product_name" : "Amazon Echo",
         "url" : "https://www.amazon.ca/dp/B07KD6RCKS/ref=ods_gw_ha_h1_ha_chs_traffic_tpr_122919?pf_rd_p=426d2306-e69f-49d6-982a-325af468b173&pf_rd_r=W7SCC5TMMYZ960BDFAAV",
         "desired_price" : 80
     },
     {
         "product_name" : "Bose QC Headphones",
         "url" : "https://www.amazon.ca/QuietComfort-Wireless-Headphones-Cancelling-Control/dp/B07NXDPLJ9/ref=gbps_img_s-4_fb90_1d95f6f9?smid=A3DWYIK6Y9EEQB&pf_rd_p=137d9502-30de-4e08-ba6c-cae999ecfb90&pf_rd_s=slot-4&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A3DWYIK6Y9EEQB&pf_rd_r=J8S87ZEZJFS50TWY4K73",
         "desired_price" : 400
     },
     {
         "product_name" : "Fleece Blanket",
         "url" : "https://www.amazon.ca/Bedsure-Fleece-Blanket-Lightweight-Microfiber/dp/B07VDDB3S4/ref=gbps_img_s-4_fb90_1a17418c?smid=A3LDROY0BE4ISH&pf_rd_p=137d9502-30de-4e08-ba6c-cae999ecfb90&pf_rd_s=slot-4&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A3DWYIK6Y9EEQB&pf_rd_r=TR7WBY6BFJA5EJW9XZJW",
         "desired_price" : 29.99
     },
     {
         "product_name" : "Stylus Pen",
         "url" : "https://www.amazon.ca/Magnetic-Charging-Touchscreen-Compatible-Smartphone/dp/B07N2HLZ93/ref=gbps_img_s-4_fb90_99ebff35?smid=A3J6JB769KBNLG&pf_rd_p=137d9502-30de-4e08-ba6c-cae999ecfb90&pf_rd_s=slot-4&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A3DWYIK6Y9EEQB&pf_rd_r=9QS1YXG31D90A2W04KRS",
         "desired_price" : 35
     }
]


def get_product_price(url):

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'lxml')
    
    sales_price = None
    raw_price = soup.find(id='priceblock_dealprice')
    
    # Check if there is currently a deal running
    if raw_price is not None:
        sales_price = soup.find(id='priceblock_dealprice').get_text()
    
    if sales_price is not None:
        sales_price = float(sales_price.split()[1])
    
    return sales_price

def send_email(products):
    # Establish connection to gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)    
    server.ehlo()
    
    server.starttls()
    server.ehlo()

    server.login(FROM_EMAIL, FROM_EMAIL_PW)

    subject = 'Amazon Tracker Alert! Items On Sale'
    body = ''
    i = 0
    for i in range(0, len(products)):
        if i == len(products) - 1:
            body = body + (products[i]['product_name']) + " "
        else:
            body = body + (products[i]['product_name']) + ", "
            
    body = body + "are within your desired price range. "
    body = body + "\nLinks to each Amazon product page: \n\n"
    
    for product in products:
        body = body + product['product_name'] + ":  " + product['url'] + "\n\n"
    
    msg = f'Subject: {subject}\n\n{body}'
    
    server.sendmail(FROM_EMAIL, TO_EMAIL, msg)

    print("Email Successfully Sent")


# Below there are two methods for execution. Currently the script is set to run once and end.
# If you want to use this script as a daemon or run it in the background of a project then
# you can comment the 'ONE TIME EXECECTION" block and uncomment the "BACKGROUND EXECUTION" block


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ONE TIME EXECUTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Valid products will contain all products that are below desired price target
valid_products = []

for product in product_info:
    product_name = product['product_name']
    url = product['url']
    desired_price = product['desired_price']
    
    current_price = get_product_price(url)
    if current_price is not None and current_price <= desired_price:
        valid_products.append(product)
    
    
send_email(valid_products)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BACKGROUND EXECUTION (Runs once per day) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#while True:
#    # Valid products will contain all products that are below desired price target
#    valid_products = []
#    
#    for product in product_info:
#        product_name = product['product_name']
#        url = product['url']
#        desired_price = product['desired_price']
#        
#        current_price = get_product_price(url)
#        if current_price is not None and current_price <= desired_price:
#            valid_products.append(product)
#        
#        
#    send_email(valid_products)
#    
#    # Run once a day (86,400 seconds)
#    time.sleep(86400)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# must enable less secure apps on google acc