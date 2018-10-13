import nltk

nltk.download('stopwords')
nltk.download('punkt')
from flask import Flask, request, jsonify
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
import os
import boto3
import functools
from flask_cors import CORS
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests as req
import json

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

'''
def init_aws():
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = ROOT_PATH + os.sep + ".aws" + os.sep + "credentials"
    os.environ['AWS_CONFIG_FILE'] = ROOT_PATH + os.sep + ".aws" + os.sep + "config"
    return boto3.client('rekognition')
'''

def init_bing_image_search_api():
    with open('./.azure/config.json') as f:
        data = json.load(f)
        subscription_key = data['bing_image_search_key']
    return ImageSearchAPI(CognitiveServicesCredentials(subscription_key))


def init_text_analytic_api():
    with open('./.azure/config.json') as f:
        data = json.load(f)
        header = {
            'Ocp-Apim-Subscription-Key': data['text_analytic_key'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    endpoint = 'https://southcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
    return header, endpoint


def init_stop_word():
    return set(stopwords.words('english'))


def init_fake_header():
    return {
        "user-agents": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache"
    }


STOP_WORD = init_stop_word()
BING_IMAGE_SEARCH_CLIENT = init_bing_image_search_api()
TEXT_ANALYTIC_API_HEADER, ENDPOINT = init_text_analytic_api()
#AWS_CLIENT = init_aws()
FAKE_HEADER = init_fake_header()


def filter_stop_word(string):
    string = str(string).lower()
    # 分词
    word_tokens = word_tokenize(string)
    # 去除停用词
    return [w for w in word_tokens if not w in STOP_WORD]


def key_phrase(string):
    request_json = {
        "documents": [
            {
                "language": "en",
                "id": 1,
                "text": string
            }
        ]
    }

    res = req.post(ENDPOINT, json=request_json, headers=TEXT_ANALYTIC_API_HEADER)
    json_data = json.loads(res.text)
    try:
        result = json_data["documents"][0]["keyPhrases"][:5]
    except Exception:
        result = None
    return result

'''
def get_image_detect_labels_by_url(url):
    result = None
    try:
        res = req.get(url, headers=FAKE_HEADER)
        res_1 = AWS_CLIENT.detect_labels(Image={'Bytes': res.content})
        result = list(res_1['Labels'])
    except Exception:
        pass
    return result
'''

# print(get_image_detect_labels_by_url(""))
# print(filter_stop_word("This is a sample sentence, showing off the stop words filtration."))
# print(key_phrase("asdfasdfasdfasdfasdfasdfaasdfa"))
app = Flask(__name__)
CORS(app)

'''
{
	"main_text" : "facebook google",
  	"search_text" : ""
}

{
  "main_text": "Panama City residents learn harsh lesson after Hurricane Michael I never would have stayedANAMA CITY, Fla.Gregg Ebersole trekked to the Panama City Marina from his devastated neighborhood on Thursday morning to find a miraculous sight: Nestled amid the twisted metal on the damaged dock was his boat, just as he had left it on a rack.Everything is tossed around like its a toy, said Ebersole, surveying the aftermath. Mine is sitting there all nice and pretty.It was a small dose of comfort after Hurricane Michael thrashed the Florida Panhandle on Wednesday and blew apart much in its path. Ebersoles single-story brick home survived, but he said he was caught flat-footed by the report that Michael had intensified into a powerful Category 4 storm quickly as it guzzled warm water on its advance up the Gulf of Mexico.If I knew it was going to be a Cat 4 with a direct hit, I never would have stayed, Ebersole said. Two days ago, we were out boating in the sunshine. This snuck up on us so quick.",
  "search_text": ""
}
'''


def no_null_str(o):
    if o is None:
        return ""
    else:
        return o


def no_null_list(o):
    if o is None:
        return []
    else:
        return o


@app.route('/hello')
def hello():
    return "Hello"


@app.route('/', methods=['POST'])
def get_json():
    result_main = []
    result_search = []

    main_text = no_null_str(request.json["main_text"])
    search_text = no_null_str(request.json["search_text"])

    # filtered_main_words = filter_stop_word(main_text)
    # filtered_search_text = filter_stop_word(search_text)

    key_phrase_main_text_list = key_phrase(main_text)
    key_phrase_search_text_list = key_phrase(search_text)

    for query in key_phrase_main_text_list or []:
        image_results = BING_IMAGE_SEARCH_CLIENT.images.search(query=query)
        if image_results.value:
            result_main.extend(
                list(map(lambda x: {"thumbnail_url": x.thumbnail_url, "content_url": x.content_url, "detail": x.name,
                                    "description": x.description, "host_page_url": x.host_page_url,
                                    "date_published": x.date_published},
                         image_results.value)))

    for query in key_phrase_search_text_list or []:
        image_results = BING_IMAGE_SEARCH_CLIENT.images.search(query=query)
        if image_results.value:
            result_search.extend(
                list(map(lambda x: {"thumbnail_url": x.thumbnail_url, "content_url": x.content_url, "detail": x.name,
                                    "description": x.description, "host_page_url": x.host_page_url,
                                    "date_published": x.date_published},
                         image_results.value)))

    result = []
    result.extend(no_null_list(result_main))
    result.extend(no_null_list(result_search))
    sorted_result = sorted(result, key=lambda k: k['date_published'], reverse=True)
    return jsonify(sorted_result[:50])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
