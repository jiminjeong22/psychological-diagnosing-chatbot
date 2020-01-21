## I. Abstract
In this project, a new form of an AI speaker-based mood disorder diagnosis service is proposed to remove barriers of previous mental counseling systems such as social prejudice against mental illness, and time/space/cost constraints, which were conducted by human health professionals. AI-based mood disorder diagnosis service induces natural emotional responses from users to AI speakers' questions, analyzes the current state of mood based on natural language processing and the Korean emotion dictionary and comprehensively diagnoses mood disorders by examining the degree of sleep and eating disorders, which are typical symptoms of mood disorder.

## II. Methodology
![ex_screenshot](./figures/figure_img/Process%20of%20mood%20disorder%20diagnosis%20chatbot%20service%20with%20AI%20speaker.jpg) 

**Fig1. Process of AI speaker based Psychological Diagnostic Service**

### 1. 텍스트 기반 감정 인식
#### 1.1. 구글 어시스턴트 앱 개발
AI 스피커로 인식된 사용자의 반응을 추출하기 위해 구글의 챗봇 개발 플랫폼인 Dialogflow를 사용하였다. Dialogflow는 쉽고 간편하게 챗봇을 설계할 수 있으며, 구글의 어시스턴트 앱을 포함하여 페이스북이나 텔레그램 등 주요 메신저 플랫폼과의 연동도 매우 쉬워 다양한 챗봇 구현이 가능하다. 본 연구에서는 구글의 AI스피커인 구글 홈 내 앱을 개발하기 위해 Dialogflow를 사용하였다.

#### 1.2. 사용자 응답 텍스트 자연어 처리
사용자가 AI 스피커에서 서비스를 호출하면, 에이전트는 ‘안녕하세요, 오늘 기분은 어떤가요?’와 같은 질문을 통해 감정 표현을 유도하며 발화한다. 한국어 처리기인 Konlpy 모듈의 Komoran 클래스를 활용하여 사용자의 응답 텍스트를 형태소 처리하였다.  Konlpy 모듈은 형태소를 비롯하여, 어근, 접두사/접미사, 품사 등 주어진 텍스트의 다양한 언어적 속성의 구조를 빠르게 파악하며, 형태소의 뜻과 문맥을 고려하여 품사를 자동적으로 연결시켜준다는 이점이 있다. Konlpy 모듈 중 Komoran 클래스는 로딩시간이 길다는 점에도 불구하고 품사 연결 알고리즘 측면에서 가장 뛰어난 성능을 보여주어 채택하였다.[4]

![ex_screenshot](./figures/figure_img/sample%20of%20Konlpy%20natural%20language%20processing.png) 

**Fig 2. Sample of Konlpy natural language processing**

#### 1.3. 한국어 감성 사전
KOSAC한국어 감정 분석 코퍼스와 KNU 한국어 감성사전에 비교하여 감정 분석 결과를 도출하였다[5-6]. 한국 감정 분석 코퍼스(Korean Sentiment Analysis Corpus, KOSAC)는 한국어로 감정표현과 그 패턴을 포착하고 품사 태깅을 통해 컴퓨터에 해석 가능한 의미를 표현하기 위해 만들어졌다. KNU 한국어 감성사전은 표준국어대사전을 구성하는 각 단어의 뜻풀이를 분석하여 긍부정어를 추출하였으며, 어떤 도메인에도 사용될 수 있는 보편적인 긍부정어로 구성된 감성사전이다. KNU 한국어 감성사전의 경우, 형태소와 품사로 구분되지 않은 자연어로 구성되었기 때문에 Konlpy 모듈을 통해 형태소를 분석한 가공된 데이터를 KOSAC 한국어 감성사전와 종합하는 과정을 거쳤다.

![ex_screenshot](./figures/figure_img/Sample%20of%20Korean%20Sentiment%20Dictionary.png) 

**Fig 3. Sample of Korean Sentiment Dictionary**

### 2. 정서 표현 유도 알고리즘
감정 분석 결과는 크게 명백한 정서를 드러내는 응답을 강한 긍정 혹은 부정, 정서 표현이 모호한 응답을 중성으로 나눈다. 강한 긍정/부정의 정서 표현은 이후, 가상 에이전트의 사용자의 발화에 대한 적극적인 위로/호감 표시 및 이모티콘을 통해 지속적인 대화를 가능하게 한다. 반면 분석 결과가 중성인 경우, 구체적 표현을 유도하는 질문을 생성한다. 사용자의 정서 반응 분석은 최소 3번 이상 반복하여, 문맥을 고려한 분석이 가능하게 한다. 예를 들어, 반어법의 경우 텍스트 분석 시 긍정의 결과값을 나타낼 가능성이 있지만, 실제 부정적 정서를 포함하고 있다. 따라서 문맥을 고려하여, 이전의 분석 값과 상반되는 결과값이 도출된 경우, 추가적인 질문을 통해 분석의 정확도를 높였다. 분석된 감정 데이터는 구글 스프레드 시트에 자동으로 업로드 된다.

### 3. 기분장애 증상 진단
사용자의 응답 내 정도 분사 분석을 통해 기분장애의 징후인 수면장애와 섭식장애의 심각성을 파악한다. 잠은 잘 주무셨나요? 몇시간 정도 주무셨나요?의 질문에 대한 응답의 긍정과 부정, 정도성의 높낮음을 분석한다. 질문에 대한 응답의 지속적인 ‘응, 아니’ 등의 긍정/부정 분석을 통해 수면장애의 유무를 파악하고, 활용된 ‘많이, 좀’과 같은 정도부사로부터 그 심각성을 파악할 수 있다. 예를 들어, 응 제법 잘 잤어라는 응답에서 응은 긍정을 표현하는 것으로, 제법, 잘은 높은 정도성을 표현하는 것으로 분석한다. 그다지 잘 자진 못 했어와 같은 문맥상 부정 응답은 정도성을 역측정한다. 구체적인 시간을 응답한 경우, 응답 내 숫자를 인식하여 수면의 질을 파악하며, 9시간 이상의 초과 수면은 우울증의 또 다른 징후의 가능성이 있기 때문에 부정적으로 진단한다. 수면 및 섭식 질문과 관련하여 해당 정도를 매우 좋음(2), 좋음(1), 좋지 않음(-1), 매우 좋지 않음(-2)로 나타내 구분하였다. [7]


## III. RESULT
심리 진단 서비스 프로토타입을 개발하여, 이를 각각 구글 어시스턴트 어플과 구글 AI 스피커인 구글 홈 미니에서 실행해보았으며, 서비스 사용데이터를 구글 스프레드시트에 실시간으로 저장하였다. 

구글 어시스턴트 어플에서 나의 상담사라는 어플이 호출되어 가상 에이전트가 사용자와 응답을 주고 받을 수 있는 것을 확인할 수 있다. AI 스피커 앱과는 달리 어시스턴트 앱 내에서는 앱의 대표 사진, 이모티콘과 같은 시각적인 요소들을 활용하여 사용자의 더욱 적극적인 응답을 얻어낼 수 있도록 구현하였다.
사용자가 AI 스피커와 의사소통을 진행하게 되면, 사용자의 응답을 자연어 처리하고, 감정값을 분석하는 과정을 볼 수 있다. 이러한 데이터는 구글 스프레드 시트에 자동적으로 저장되고 실시간으로 감정 상태 그래프가 변하게 되어 그동안의 감정 변화 추이를 시각적으로 확인할 수 있다.

서비스를 활용하여 축적한 응답 시각, 텍스트, 감정 분석 값을 구글 스프레드시트에 저장하였으며, 시간에 따른 감정 변화를 그래프로 나타냈다. 빨간, 파란 선은 각각 긍정값, 부정값을 나타내며, 굵은 검은 선은 이를 종합한 최종 감정 분석 값이다. 일상 생활에서 보이는 일반적인 감정 변화는 대략 -5~5 사이를 오가는 것을 확인할 수 있었으며, 이후 추가적인 실험연구를 통해 정신병리적 기분변화 추이에 대해 분석할 예정이다.
- 구글 스프레드 시트
https://docs.google.com/spreadsheets/d/1fh8clk72yW412m1lIWnHc4LUA8GF4lYHanwSuQe3Bkc/edit#gid=0


<img src="https://github.com/jiminjeong22/Psychological_Diagnosing_Chatbot/blob/master/Mood%20Disorder%20Diagnosis%20Chatbot/figures/app_screenshots/screenchot_1.jpg?raw=true" width="40%"><img src="https://github.com/jiminjeong22/Psychological_Diagnosing_Chatbot/blob/master/Mood%20Disorder%20Diagnosis%20Chatbot/figures/app_screenshots/screenshot_2.jpg?raw=true" width="30%">

**Fig 4. Simulation of Psychological Diagnostic Service on Google Assistant App**

![ex_screenshot](./figures/figure_img/Accumulated%20psycho-diagnosis%20data%20on%20Google%20Spread%20Sheet.jpg) 

**Fig 5. Accumulated psycho-diagnosis data on Google Spread Sheet**

![ex_screenshot](./figures/figure_img/Curve%20graph%20of%20the%20user's%20emotional%20state.jpg) 
 
**Fig 6. Curve graph of the user's emotional state**

 
![ex_screenshot](./figures/figure_img/Graph%20of%20the%20user's%20sleep%20quality.jpg) 

**Fig 6. Graph of the user's sleep quality**


## 참고문헌
[1] Lee, C. H., Sim, J. M., & Yoon, A. (2005). The review about the development of Korean linguistic inquiry and word count. Korean journal of cognitive science, 16(2), 93-121.

[2] Al Hanai, T., Ghassemi, M., & Glass, J. (2018). Detecting depression with audio/text sequence modeling of interviews. In Proc. Interspeech (pp. 1716-1720).

[3] Jong-Jin Park. (2018). A Development of Chatbot for Emotional Stress Recognition and Management using NLP. The Korean Institute of Electrical Engineers, 67(7), 954-961.

[4] Eunjeong L. Park, & Sungzoon Cho. (2014). Korean natural language processing in Python. Proceedings of the 26th Annual Conference on Human and Cognitive Language Technology, pp. 133-136,

[5] Shin, Hyopil, Munhyong Kim, Yu-Mi Jo, Hayeon Jang, & Andrew Cattle. (2013). KOSAC(Korean Sentiment Analysis Corpus): Information and Compuation, 181-190.

[6] Byung-Won On, Sangmin Park, & Chulwon Na, KNU Korean sentiment lexicon, Software Copyright Registration (No. C-2018-012645), Korea Copyright Commission, May 14, 2018

[7] Sung-hoon Jung. (2014). The usage patterns of modern Korean orthodontics and their classification. Journal of Academic Conference of the Korean Language Society,47-67.

## 참고 사이트 
[1] https://github.com/dialogflow/fulfillment-weather-python/blob/master/main.py


## 학술
2019 ICCT 국제 융합 학술대회에 본 연구와 관련하여 논문을 투고하였으며, 게제 승인을 받았다. 

 
