from flask import Flask, request, make_response, jsonify

import threading

from .module import response, sentiment_analysis as sa, data_storing

app = Flask(__name__)
log = app.logger

# list stores context
context_data = []


@app.route('/', methods=['POST', 'GET'])
def webhook():
    req = request.get_json(silent=True, force=True)

    try:
        action = req.get('queryResult').get('action')
        intent = req['queryResult']['intent']['displayName']

    except AttributeError:
        return 'json error'

    respon = response.Response()

    # first chatbot response when user called the app
    if action == 'input.welcome':
        res = respon.welcome_response()
        context_data.clear()

    # second and after response to be anaylzed
    elif intent == 'Mood':

        # user input text
        text = str(req.get('queryResult').get('queryText'))

        eating_disorder = 0
        how_long = 0

        # mood calculation
        morph_l, pos, neg, mood = sa.Sentiment_Analysis.calculate_result(text)

        # setting mood standard
        negative_standard = 0
        positive_standard = 2
        if mood < negative_standard:
            status = "negative"
        elif mood > positive_standard:
            status = "positive"
        else:
            status = "neutral"

        # context adding
        context_data.append((text, mood))
        context_n = len(context_data) - 1

        if len(context_data) < 4:
            question = "mood"
            res = respon.mood_response(context_n, status)

        elif len(context_data) == 4:
            question = "sleep"
            res, sleep_disorder, how_long = respon.sleep_response(text, morph_l)

        elif len(context_data) == 5:
            question = "eat"
            res, eating_disorder = respon.sleep_response(text, morph_l)
        else:
            question = "mood"
            res = respon.mood_response(4, status)

        t = threading.Thread(target=data_storing.Data_Storing.data_storing(),
                             args=(question, text, pos, neg, mood, sleep_disorder, how_long, eating_disorder))
        t.start()

    elif action == 'input.unknown':
        text = str(req.get('queryResult').get('queryText'))
        res = respon.unknown_response(text)

    else:
        log.error('Unexpected action.')

    return make_response(jsonify({'fulfillmentText': res}))


if __name__ == '__main__':
    app.run(debug=True)
