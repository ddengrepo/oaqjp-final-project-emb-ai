"""
This module provides the emotion_detector function to analyze text emotion using a remote API.
"""

from collections import OrderedDict
import json
import requests

def emotion_detector(text_to_analyse):
    """
    Analyzes the emotion of the input text using a remote NLP service.

    Args:
        text_to_analyse (str): The text string to analyze for emotion.

    Returns:
        OrderedDict: A dictionary containing emotion scores and the dominant
                     emotion, with 'dominant_emotion' as the last key.
                     Returns a dictionary with None values for a 400 status,
                     or an error dictionary for other failures.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}

    # store instance of response from api in 'response'
    response = requests.post(url, json=myobj, headers=header, timeout=5)

    text = None
    dominant_emotion = None

    # response.status_code returns a 3 digit number of the status of the request
    if response.status_code == 200:
        try:
            formatted_response = json.loads(response.text)
            if (formatted_response and
                    formatted_response.get('emotionPredictions') and
                    len(formatted_response['emotionPredictions']) > 0 and
                    formatted_response['emotionPredictions'][0].get('emotion')):
                text = formatted_response['emotionPredictions'][0]['emotion']
                dominant_emotion = max(text, key=text.get)
                text['dominant_emotion'] = dominant_emotion
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Error processing successful response: {e}")
            text = {'error': 'Failed to process successful response'}
    elif response.status_code == 400:
        # Create a dictionary with None values for all potential keys
        text = OrderedDict([
            ('anger', None),
            ('disgust', None),
            ('fear', None),
            ('joy', None),
            ('sadness', None),
            ('dominant_emotion', None)
        ])
    elif response.status_code == 500:
        text = {'error': 'Emotion analysis service failed (HTTP 500)'}
    else:
        text = {'error': f'Request failed with status code: {response.status_code}'}

    return text
