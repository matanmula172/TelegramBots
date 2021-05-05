import requests
import time
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

# global variables
API_KEY = '03bc50ff-1d81-4d72-81dd-c879af723ca3'
bot_token = '1740115349:AAG07QZupB1h6bsghlzsItPg9z29Rv8gArU'
chat_id = '1347275938'
threshold = 50000
time_interval = 5 * 60  # in seconds
seconds_in_day = 24 * 60 * 60


def get_bitcoin_price_usd():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    # make a request to the coin market cap api
    response = requests.get(url=url, headers=headers)
    response_json = response.json()

    # extract the bitcoin price in dollars from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']


# function to send a string message through telegram
def send_message(msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)


# function to send an image through telegram
def send_image(img_name):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': open('./' + str(img_name), 'rb')}
    data = {'chat_id': chat_id}
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)


# main function
def main():
    price_list = []
    # counter that sets every 24 hours
    day_counter = 0
    while True:
        # get the updated price of the current 5 minutes
        price = get_bitcoin_price_usd()
        price_list.append([price, dt.datetime.today().strftime('%m-%d-%Y'),
                           dt.datetime.today().strftime('%H:%M:%S')])
        day_counter += time_interval

        # if the price falls below threshold, send a message
        if price < threshold:
            send_message(msg=f'BTC Price Drop Alert: {price}')

        # after 24 hours save and send a graph that shows the updates of the BTC price
        if len(price_list) >= seconds_in_day / time_interval:
            temp = np.array(price_list)
            x = temp[:, 2]
            y = temp[:, 0]
            plt.plot(x, y)
            img_name = str(price_list[0][1]) + "_BTC_price_graph.png"
            plt.savefig(img_name)
            send_image(img_name)
            plt.show()
            price_list = []

        # fetch the price for every dash minutes
        time.sleep(time_interval)


# activate the main() function
if __name__ == '__main__':
    main()
