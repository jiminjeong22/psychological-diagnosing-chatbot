import random
import emoji

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
        context_n = len(context_data)

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
            if mood < -1.5:  # 강한 부정
                res_list = [
                    emoji.emojize("맛있는 음식을 먹으면 기분이 좀 나아지지 않을까요? :fork_and_knife: :spaghetti: :sushi:",
                                  use_aliases=True),
                    emoji.emojize("우리 신나는 음악 들어볼래요? 기분이 나아질 거에요", use_aliases=True),
                    emoji.emojize("무엇을 하면 기분이 좋아질 수 있을까요? ", use_aliases=True),
                    emoji.emojize("재미있는 영화를 보면 기분이 나아질까요? ", use_aliases=True)
                ]

                res_num = random.randrange(0, len(res_list))
                res = res_list[res_num]
            elif mood > 1.5:  # 강한 긍정
                res_list = [
                    emoji.emojize("오늘 하루를 더 기분좋은 하루로 만들어봐요 우리!", use_aliases=True),
                    emoji.emojize("내일도 오늘처럼 기분 좋은 하루가 되길 바래요", use_aliases=True),
                ]

                res_num = random.randrange(0, len(res_list))
                res = res_list[res_num]
            else:  # 중성
                res_list = [
                    emoji.emojize("우리 오늘 하루를 기분 좋은 하루로 만들어봐요", use_aliases=True),
                    emoji.emojize("우리 기분이 좋아지기 위해서 노래를 들어보는 건 어떨까요?", use_aliases=True),
                    emoji.emojize("오늘 힐링이 필요하다면, 맛있는 음식을 먹어보는건 어때요? :fries: :doughnut:", use_aliases=True)
                ]
                res_num = random.randrange(0, len(res_list))
                res = res_list[res_num]

        t = threading.Thread(target=data_storing.Data_Storing.data_storing(),
                             args=(question, text, pos, neg, mood, sleep_disorder, how_long, eating_disorder))
        t.start()

    elif action == 'input.unknown':
        text = str(req.get('queryResult').get('queryText'))
        res_list = [
            emoji.emojize(str(text + "라고 말씀하셨는데, \n제가 말씀을 잘 못 이해 한것 같아요. \n이해할 수 있게 다시 말씀해주시겠어요?"), use_aliases=True),
            emoji.emojize(str(text + "라고 방금 하신 말씀은 \n제가 이해하지 못하는 말인 것 같아요. \n이해할 수 있는 쉬운 말로 다시 말씀해주시겠어요?"),
                          use_aliases=True)
        ]
        res_num = random.randrange(0, len(res_list))
        res = res_list[res_num]

    else:
        log.error('Unexpected action.')

    return make_response(jsonify({'fulfillmentText': res}))


if __name__ == '__main__':
    app.run(debug=True)
