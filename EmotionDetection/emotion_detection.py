import json
import requests

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyse } }

    # store instance of response from api in 'response'
    response = requests.post(url, json=myobj, headers=header)

    # extract the text from the instance and convert to json 
    formatted_response = json.loads(response.text)

    # response.status_code returns a 3 digit number of the status of the request
    if response.status_code == 200:
        if formatted_response['emotionPredictions'][0]['emotion']:
            text = formatted_response['emotionPredictions'][0]['emotion']
            dominant_emotion = max(text, key=text.get)
            text['dominant_emotion'] = dominant_emotion
    elif response.status_code == 500:
        text = None

    return text

'''



from emotion_detection import emotion_detector
emotion_detector('I love this new technology')





'''