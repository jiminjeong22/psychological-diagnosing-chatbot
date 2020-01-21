import emoji
import random


class Response:
    def welcome_response(self):
        res_num = random.randrange(0, len(self.res_l))
        res = self.res_l[res_num]
        return res

    def mood_response(self, context_n, status):
        res_num = random.randrange(0, len(self.res_l))
        res = self.res_l[context_n][status][res_num]
        return res

    def __init__(self):
        self.res_l = []

        # first response (welcome)
        self.res_l[0] = ([
            emoji.emojize("안녕하세요, 오늘 기분은 어떠신가요? ", use_aliases=True),
            emoji.emojize("안녕하세요, 오늘 하루는 어떤 일이 있었나요?", use_aliases=True),
            emoji.emojize("안녕하세요, 오늘은 어떤 하루를 보냈나요?", use_aliases=True)
        ])

        # second response (mood_1)
        self.res_l[1] = {
            "positive": [
                emoji.emojize("그런가요? 기분이 좋으신 것 같아요 ", use_aliases=True),
                emoji.emojize("그래요? 어쩐지 기분이 괜찮아 보이셨어요 ", use_aliases=True),
                emoji.emojize("아! 기분 좋은 일이 있으셨군요! ", use_aliases=True)
            ],

            "negative": [
                emoji.emojize("아.. 기분이 좋지 않으신 것 같아 보여요. 무슨 일인지 더 들려주실 수 있으신가요?", use_aliases=True),
                emoji.emojize("저런.. 기분이 안 좋으신 것 같아요. 무슨 일인지 더 들려주실 수 있으신가요?", use_aliases=True),
                emoji.emojize("아.. 기분이 좋지 않으신가 보네요. 무슨 일인지 더 들려주실 수 있으신가요?", use_aliases=True)
            ],

            "neutral": [
                emoji.emojize("그런가요? 더 자세히 말씀해주세요", use_aliases=True),
                emoji.emojize("그래요? 무슨 일이 있었는지 더 듣고싶어요", use_aliases=True),
                emoji.emojize("그렇군요. 오늘 하루에 대해서 더 말씀해주세요", use_aliases=True)
            ]
        }

        # third response (mood_2)
        self.res_l[2] = {
            "positive": [
                emoji.emojize("기분이 좋으신 것 같아 저도 기분이 좋네요. 또 다른 일은 없었나요??", use_aliases=True),
                emoji.emojize("좋은 하루였나봐요! 또 다른 일은 없었나요??", use_aliases=True),
                emoji.emojize("그렇군요! 또 다른 일은 없었나요??", use_aliases=True)
            ],

            "negative": [
                emoji.emojize("그렇군요.. 또 다른 일은 없었나요??", use_aliases=True),
                emoji.emojize("아..이해해요. 또 다른 일은 없었나요??", use_aliases=True),
                emoji.emojize("아.. 기분이 안좋을만해요. 또 다른 일은 없었나요??", use_aliases=True)
            ],

            "neutral": [
                emoji.emojize("또 무슨 일 없었나요?", use_aliases=True),
                emoji.emojize("그래요, 또 다른 일은 없었어요??", use_aliases=True),
                emoji.emojize("그런 일이 있었어요?.", use_aliases=True)
            ]
        }

        # fourth response (mood_3 & sleep asking)
        self.res_l[3] = {
            "positive": [
                emoji.emojize("그래요? 잠은 잘 주무시나요? 몇시간 정도 주무셨어요?", use_aliases=True),
                emoji.emojize("그렇군요! 잠은 잘 주무시나요? 몇시간 정도 주무셨어요?:blush:", use_aliases=True)
            ],

            "negative": [
                emoji.emojize("그렇군요.. 잠은 잘 주무셨나요? 몇시간 정도 주무셨어요?", use_aliases=True),
                emoji.emojize("아..이해해요. 잠은 잘 주무셨나요? 몇시간 정도 주무셨어요?", use_aliases=True),
                emoji.emojize("아.. 기분이 안좋을만해요. 잠은 잘 주무셨나요? 몇시간 정도 주무셨어요?", use_aliases=True)
            ],

            "neutral": [
                emoji.emojize("그랬군요.. 잠은 잘 주무시나요? 몇시간 정도 주무셨어요?", use_aliases=True),
                emoji.emojize("그렇군요. 잠은 잘 주무시나요? 몇시간 정도 주무셨어요?", use_aliases=True)
            ]
        }
