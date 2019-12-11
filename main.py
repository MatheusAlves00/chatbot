import telepot
import os
import cv2
import analyzeImage

botToken = '978407577:AAE-p2xXuke_SsQrxzM78QvaHprVKj3SVHc' 

#função para que mostras as imagens
def toReceive(message):
    _id = message['from']['id']
    if 'text' in message:
        text = message['text']
    try:
        if 'photo' in message:
            tele.sendMessage(_id, "Processando imagem...")
            analisar_imagem = analyzeImage.analisarDoTelegram(botToken, message, tele)
            tele.sendPhoto(_id, open(analisar_imagem, 'rb'))
            tele.sendMessage(_id, "Aí está a sua imagem!")
        elif 'Oi' in text or 'Olá' in text or 'start' in text:
            tele.sendMessage(_id, "Oi, eu sou o Zed. Me envie uma imagem para que eu possa verificar.")
        else:
            tele.sendMessage(_id, "Por favor, envie uma imagem para ser análisada.")
    except Exception as e:
        print('Erro:' + str(e))
        tele.sendMessage(_id, "Ocorreu um erro!")

tele = telepot.Bot(botToken)
print("Carregando...")
tele.message_loop(toReceive)

while True:
  pass
