import emoji
import re
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

    def suggestion_response(self, context_n, status):
        res_num = random.randrange(0, len(self.res_l))
        res = self.res_l[context_n][status][res_num]
        return res

    def sleep_response(self, text, morph_l):
        res = ""
        
        sleep_disorder = 0
       
        # if sleep hours are expressed as numbers
        how_long = (re.findall("\d+", text))[0]
        if how_long.isdigit():
            how_long = int(how_long)
            if (0 < how_long < 4) or (how_long >= 11):
                sleep_disorder = -2
                res = "저런... 많이 피곤하실 것 같아요! 좀 더 주무셨으면 좋겠어요... 요즘 밥은 잘 드시고 계신가요? "
            elif (3 < how_long < 6) or (8 < how_long < 11):
                sleep_disorder = -1
                res = "저런... 피곤하시겠군요.. 요즘 밥은 잘 드시고 계신가요?"
            elif how_long == 6:
                sleep_disorder = 1
                res = "적당히 주무셨군요! 밥은 잘 드셨나요?"
            else:
                sleep_disorder = 2
                res = "잘 주무신 것 같아 다행이에요! 밥은 잘 드셨나요?"

        # if sleep hours are expressed as words
        else:
            how_long = ""
            for i in range(len(morph_l)):
                if morph_l[i] in self.neg_word:
                    if morph_l[i] in self.high_frequency:
                        res = "저런... 많이 피곤하실 것 같아요! 좀 더 주무셨으면 좋겠어요... 요즘 밥은 잘 드시고 계신가요? "
                        sleep_disorder = -2
                    elif morph_l[i] in self.low_frequency:
                        res = "저런... 피곤하시겠군요.. 요즘 밥은 잘 드시고 계신가요?"
                        sleep_disorder = -1
                    else:
                        res = "저런... 피곤하시겠군요.. 요즘 밥은 잘 드시고 계신가요? "
                        sleep_disorder = -1
                elif morph_l[i] in self.pos_word:
                    if morph_l[i] in self.high_frequency:
                        res = "잘 주무신 것 같아 다행이에요! 밥은 잘 드셨나요?"
                        sleep_disorder = 2
                    elif morph_l[i] in self.low_frequency:
                        res = "조금 더 잘 시간이 있으면 좋겠어요. 밥은 잘 드셨나요?"
                        sleep_disorder = 1
                    else:
                        res = "그렇군요! 밥은 잘 드셨나요?"
                        sleep_disorder = 1
                else:
                    if morph_l[i] in self.high_frequency:
                        res = "그렇군요! 밥은 잘 드셨나요?"
                        sleep_disorder = 1
                    elif morph_l[i] in self.low_frequency:
                        res = "그렇군요! 밥은 잘 드셨나요?"
                        sleep_disorder = 1
                    else:
                        res = "그렇군요! 밥은 잘 드셨나요??"
                        sleep_disorder = 1
        return res, sleep_disorder, how_long

    def eating_response(self, morph_l):
        res = ""

        eating_disorder = 0

        for i in range(len(morph_l)):
            if morph_l[i] in self.neg_word:
                if morph_l[i] in self.high_frequency:
                    res = "저런... 밥은 꼭 챙기셔야 해요! 알겠죠?"
                    eating_disorder = -2
                elif morph_l[i] in self.low_frequency:
                    res = "저런... 밥 꼭 잘 챙겨먹고 다니세요! 알겠죠?"
                    eating_disorder = -1
                else:
                    res = "저런... 밥 꼭 잘 챙겨먹고 다니세요! 알겠죠?"
                    eating_disorder = -1
            elif morph_l[i] in self.pos_word:
                if morph_l[i] in self.high_frequency:
                    res = "좋아요! 앞으로도 밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                    eating_disorder = 2
                elif morph_l[i] in self.low_frequency:
                    res = "다행이에요! 밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                    eating_disorder = 1
                else:
                    res = "다행이에요! 밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                    eating_disorder = 1
            else:
                if morph_l[i] in self.high_frequency:
                    res = "그런가요?  밥은 꼭 잘 챙겨먹고 다니셔야해요! 알겠죠?"
                    eating_disorder = 1
                elif morph_l[i] in self.low_frequency:
                    res = "그런가요? 사람은 밥심이에요! 밥 잘 챙겨먹고 다니세요. 알겠죠?"
                    eating_disorder = 1
                else:
                    res = "그런가요? 사람은 밥심이에요! 밥 잘 챙겨먹고 다니세요. 알겠죠?"
                    eating_disorder = 1
                    
        return res, eating_disorder

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

        self.neg_word = ["아니/MAG", "못/MAG", ]
        self.pos_word = ["응/IC"]

        self.high_frequency = ["많이/NNG", "완전/NNG", "진짜/MAG", "잘/NNG", "피곤/NNG"]
        self.low_frequency = ["조금/NNG, 조금/MAG"]
