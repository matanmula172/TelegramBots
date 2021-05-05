import time
import movie_module
import json
import requests

token = '1783124405:AAH_A5NQeOFsIbnzTah8VdrqMmLgv1Oay8s'
chat_id = '1347275938'
URL = "https://api.telegram.org/bot{}/".format(token)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


# This function gets the string response from get_url() and parses it into json
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# This function returns a JSON response of all the new messages sent to out Bot
def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


# This function retrieves the last message out of all the recent messages, and
# returns the text
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    if num_updates == 0:
        return None, None
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


# function to send a string message through telegram
def send_message(msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)


def main():
    last_title, chat_id = get_last_chat_id_and_text(get_updates())
    while True:
        title, chat_id = get_last_chat_id_and_text(get_updates())
        if title != last_title and title is not None:
            last_title = title
            movie_instance = movie_module.get_movie_instance(title)
            if len(movie_instance) > 0:
                imdb_id = movie_module.get_movie_imdb_id(movie_instance[0])
                link_lst = movie_module.get_link_list_movie(imdb_id)
                if len(link_lst) > 0:
                    for link in link_lst['movie_results']:
                        send_message(str(link['link']))
                else:
                    send_message("No links for this movie")
            else:
                send_message("Unknown movie title")
        time.sleep(0.5)


if __name__ == '__main__':
    main()
