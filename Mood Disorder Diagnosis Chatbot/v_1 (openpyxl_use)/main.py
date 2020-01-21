import random
import emoji

from flask import Flask, request, make_response, jsonify

import threading
import re

from .module import response
from .module import sentiment_analysis as sa

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

        sleep_disorder = 0
        eating_disorder = 0
        how_long = 0

        # mood calculation
        pos, neg, mood = sa.Sentiment_Analysis.calculate_result(text)

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
            neg_word = ["아니/MAG", "못/MAG", ]
            pos_word = ["응/IC"]
            high_frequency = ["많이/NNG", "완전/NNG", "진짜/MAG", "잘/NNG", "피곤/NNG"]
            low_frequency = ["조금/NNG, 조금/MAG"]
            how_long = (re.findall("\d+", text))[0]
            if how_long.isdigit():
                how_long = int(how_long)
                if (how_long > 0 and how_long < 4) or (how_long >= 11):
                    sleep_disorder = -2
                    res = "저런... 많이 피곤하실 것 같아요! 좀 더 주무셨으면 좋겠어요... 요즘 밥은 잘 드시고 계신가요? "
                elif (how_long > 3 and how_long < 6) or (how_long > 8 and how_long < 11):
                    sleep_disorder = -1
                    res = "저런... 피곤하시겠군요.. 요즘 밥은 잘 드시고 계신가요?"
                elif how_long == 6:
                    sleep_disorder = 1
                    res = "적당히 주무셨군요! 밥은 잘 드셨나요?"
                else:
                    sleep_disorder = 2
                    res = "잘 주무신 것 같아 다행이에요! 밥은 잘 드셨나요?"

            else:
                how_long = ""
                for i in range(len(text_l)):
                    if text_l[i] in neg_word:
                        if text_l[i] in high_frequency:
                            res = "저런... 많이 피곤하실 것 같아요! 좀 더 주무셨으면 좋겠어요... 요즘 밥은 잘 드시고 계신가요? "
                            sleep_disorder = -2
                        elif text_l[i] in low_frequency:
                            res = "저런... 피곤하시겠군요.. 요즘 밥은 잘 드시고 계신가요?"
                            sleep_disorder = -1
                        else:
                            res = "저런... 피곤하시겠군요.. 요즘 밥은 잘 드시고 계신가요? "
                            sleep_disorder = -1
                    elif text_l[i] in pos_word:
                        if text_l[i] in high_frequency:
                            res = "잘 주무신 것 같아 다행이에요! 밥은 잘 드셨나요?"
                            sleep_disorder = 2
                        elif text_l[i] in low_frequency:
                            res = "조금 더 잘 시간이 있으면 좋겠어요. 밥은 잘 드셨나요?"
                            sleep_disorder = 1
                        else:
                            res = "그렇군요! 밥은 잘 드셨나요?"
                            sleep_disorder = 1
                    else:
                        if text_l[i] in high_frequency:
                            res = "그렇군요! 밥은 잘 드셨나요?"
                            sleep_disorder = 1
                        elif text_l[i] in low_frequency:
                            res = "그렇군요! 밥은 잘 드셨나요?"
                            sleep_disorder = 1
                        else:
                            res = "그렇군요! 밥은 잘 드셨나요??"
                            sleep_disorder = 1

        elif len(context_data) == 5:
            question = "eat"
            neg_word = ["아니/MAG", "못/MAG", ]
            pos_word = ["응/IC"]
            high_frequency = ["많이/NNG", "완전/NNG", "진짜/MAG", "잘/NNG"]
            low_frequency = ["조금/NNG, 조금/MAG"]
            for i in range(len(text_l)):
                if text_l[i] in neg_word:
                    if text_l[i] in high_frequency:
                        res = "저런... 밥은 꼭 챙기셔야 해요! 알겠죠?"
                        eating_disorder = -2
                    elif text_l[i] in low_frequency:
                        res = "저런... 밥 꼭 잘 챙겨먹고 다니세요! 알겠죠?"
                        eating_disorder = -1
                    else:
                        res = "저런... 밥 꼭 잘 챙겨먹고 다니세요! 알겠죠?"
                        eating_disorder = -1
                elif text_l[i] in pos_word:
                    if text_l[i] in high_frequency:
                        res = "좋아요! 앞으로도 밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                        eating_disorder = 2
                    elif text_l[i] in low_frequency:
                        res = "다행이에요! 밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                        eating_disorder = 1
                    else:
                        res = "다행이에요! 밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                        eating_disorder = 1
                else:
                    if text_l[i] in high_frequency:
                        res = "그런가요?  밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                        eating_disorder = 1
                    elif text_l[i] in low_frequency:
                        res = "그런가요? :thumbsup: 사람은 밥심이에요! 밥 잘 챙겨먹고 다니세요. 알겠죠?"
                        eating_disorder = 1
                    else:
                        res = "그런가요? 사람은 밥심이에요! 밥 잘 챙겨먹고 다니세요. 알겠죠?"
                        eating_disorder = 1


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

        t = threading.Thread(target=Data_Storing,
                             args=(question, text, POS, NEG, mood, sleep_disorder, how_long, eating_disorder))
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

    print("*" * 20)
    print("\n")
    return make_response(jsonify({'fulfillmentText': res}))


if __name__ == '__main__':
    app.run(debug=True)
