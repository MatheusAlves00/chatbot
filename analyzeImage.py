#importar bibliotecas 
import wget
import cv2
from datetime import datetime
from google.cloud import vision
from google.cloud import translate_v2 as translate

#função para fazer análise da imagem
def analisarDoTelegram(botToken, message, tele):
    downloaded_image = download_from_telegram(botToken, message, tele)
    analyzed_image = localizarObjetos(downloaded_image)
    return analyzed_image

#função para baixar a imagem
def download_from_telegram(botToken, message, tele):
    print("Fazendo download de arquivo...")
    file_id = message['photo'][1]['file_id']
    file_path = tele.getFile(file_id)['file_path']
    url_image = "https://api.telegram.org/file/bot{}/{}".format(botToken, file_path) 
    
    image_downloaded_path = "./images/{}.jpg".format(str(datetime.now()))
    wget.download(url_image, image_downloaded_path)
    
    return image_downloaded_path

#função para localizar os objetos na imagem
def localizarObjetos(path):
    print("Localizando Objetos...")
    cliente = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = cliente.object_localization(
        image=image).localized_object_annotations

    data_objects = []
    image = cv2.imread(path)
    h, w, _ = image.shape

    print('\nNúmero de objetos encontrados: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (Confiança: {})'.format(object_.name, object_.score))        
        coordinates = []        
        for vertex in object_.bounding_poly.normalized_vertices:            
            coordinates.append((vertex.x*w, vertex.y*h))        
        data_objects.append([(coordinates[0][0], coordinates[0][1]),
                            (coordinates[2][0], coordinates[2][1]),
                            (object_.name),(object_.score)])
        
    return objetosEmpatadosAndCriarImagemNova(image, data_objects)

#função para desenhar os retangulos sobre os objetos que foram achados na imagem
def objetosEmpatadosAndCriarImagemNova(image, data_object):
    print("Desenhando retangulos e rotulando imagens...")
    for data in data_object:
        vertice_top = (int(data[0][0]), int(data[0][1]))
        vertice_bottom = (int(data[1][0]), int(data[1][1]))
        object_name = data[2]
        object_score = data[3]

        cv2.rectangle(image, vertice_top, vertice_bottom, (255, 255, 0), 3)

        x, y = int(data[0][0]), int(data[0][1])

        label = traduzirLabel(object_name)
        precision = round(object_score*100)
        label += " {}%".format(precision)

        cv2.putText(image, label, (x, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 0, 0), 1, lineType=cv2.LINE_AA)
        
    dir_image = 'resultado.jpg'
    cv2.imwrite(dir_image, image)

    return dir_image

#função para traduzir as imagens
def traduzirLabel(text):
    print("Traduzindo label...")
    translate_cliente = translate.Client()
    resultado = translate_cliente.translate(text, target_language='pt-BR')
    return resultado['translatedText']
