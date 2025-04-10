from flask import Flask, request, render_template, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask('Emotion Detector')

@app.route('/emotionDetector')
def emotion_analyzer():
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)
    
    if len(text_to_analyze) == 0:
        return 'Please provide an input'
    elif response is None:
        return 'Invalid input ! Try again'
    return response

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port = 5000,
        debug=True # Added debug mode for easier development
    )