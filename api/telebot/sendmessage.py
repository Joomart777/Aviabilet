import requests

from api.telebot.models import TeleSettings




def sendTelegram(tg_prod, tg_qty):
    settings = TeleSettings.objects.get(pk=2)
    token = str(settings.tg_token)
    chat_id = str(settings.tg_chat_id)
    text = str(settings.tg_message)
    api = 'https://api.telegram.org/bot'
    method = api + token + '/sendMessage'

    a = text.find('{')
    b = text.find('}')
    c = text.rfind('{')
    d = text.rfind('}')
    # e = text.find('<')
    # f = text.find('>')
    # g = text.rfind('<')

    p1 = text[0:a]
    p2 = text[b+1:c]
    p3 = text[d+1:]
    # p4 = text[f+1:g]

    tx_slice = p1 + tg_prod + p2 + tg_qty + p3


    requ = requests.post(method, data={
        'chat_id': chat_id,
        'text': tx_slice
    })

# sendTelegram()

