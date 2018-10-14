import nltk
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
from pprint import pprint
import exifread
from io import BytesIO
import traceback

nltk.download('stopwords')
nltk.download('punkt')

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def init_aws():
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = ROOT_PATH + os.sep + ".aws" + os.sep + "credentials"
    os.environ['AWS_CONFIG_FILE'] = ROOT_PATH + os.sep + ".aws" + os.sep + "config"
    return boto3.client('rekognition')


# https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
def init_google_map():
    with open('./.google/config.json') as f:
        data = json.load(f)
        return data['google_map_key']


# https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY

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


def init_text_entity_api():
    with open('./.azure/config.json') as f:
        data = json.load(f)
        header = {
            'Ocp-Apim-Subscription-Key': data['text_analytic_key'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    return header


def init_search_news_api():
    with open('./.azure/config.json') as f:
        data = json.load(f)
        header = {
            'Ocp-Apim-Subscription-Key': data['bing_image_search_key'],
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return header


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
AWS_CLIENT = init_aws()
FAKE_HEADER = init_fake_header()
GOOGLE_MAP_KEY = init_google_map()
NEWS_SEARCH_API_HEADER = init_search_news_api()
ERROR = {"code": 404}


def get_entity_by_str(string):
    sentence_list = str(string).split('.')
    documents = list(map(lambda x: {'id': x[1], 'text': x[0]}, zip(sentence_list, range(100))))
    endpoint = "https://southcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/entities"
    request_json = {"documents": documents}
    res = req.post(endpoint, headers=TEXT_ANALYTIC_API_HEADER, json=request_json)
    json_data = json.loads(res.text)
    return json_data


def get_location_by_str(string):
    string = ''.join(e for e in string if e.isalnum() or e.isspace())
    string = string.replace(' ', '+')
    res = req.get('https://maps.googleapis.com/maps/api/geocode/json',
                  params={'address': string, 'key': GOOGLE_MAP_KEY})
    json_data = json.loads(res.text)
    return json_data


# get_location_by_str("university of missouri")

def get_location_by_lat_lon(location):
    lat = location['lat']
    lon = location['lon']
    latlng = str(lat) + ',' + str(lon)
    res = req.get('https://maps.googleapis.com/maps/api/geocode/json', params={'latlng': latlng, 'key': GOOGLE_MAP_KEY})
    json_data = json.loads(res.text)
    return json_data


# get_location_by_lat_lon({'lat': '40.714224', 'lon': '-73.961452'})

def get_new_by_str(search_term):
    search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/news/search'
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    res = req.get(search_url, headers=NEWS_SEARCH_API_HEADER, params=params)
    res.raise_for_status()
    return res.json()


# pprint(get_new_by_str("Panama City residents learn harsh lesson after Hurricane Michael"))


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


def get_people_from_url(url):
    response = None
    try:
        res = req.get(url, headers=FAKE_HEADER)
        response = AWS_CLIENT.recognize_celebrities(Image={'Bytes': res.content})
    except Exception:
        pass
    return response


# pprint(get_people_from_url('https://pbs.twimg.com/profile_images/808534690957135872/bTja4Zot_200x200.jpg'))


def exifread_infos(photo):
    # Open image file for reading (binary mode)
    f = open(photo, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f)

    try:
        LatRef = tags["GPS GPSLatitudeRef"].printable
        Lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        Lat = float(Lat[0]) + float(Lat[1]) / 60 + float(Lat[2]) / float(Lat[3]) / 3600
        if LatRef != "N":
            Lat = Lat * (-1)
        LonRef = tags["GPS GPSLongitudeRef"].printable
        Lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        Lon = float(Lon[0]) + float(Lon[1]) / 60 + float(Lon[2]) / float(Lon[3]) / 3600
        if LonRef != "E":
            Lon = Lon * (-1)
        f.close()
    except:
        return "ERROR:请确保照片包含经纬度等EXIF信息。"
    else:
        return Lat, Lon


def exifread_infos_by_url(url):
    res = req.get(url, headers=FAKE_HEADER)
    buffer = BytesIO()
    buffer.write(res.content)
    buffer.seek(0)
    tags = exifread.process_file(buffer)

    try:
        LatRef = tags["GPS GPSLatitudeRef"].printable
        Lat = tags["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        Lat = float(Lat[0]) + float(Lat[1]) / 60 + float(Lat[2]) / float(Lat[3]) / 3600
        if LatRef != "N":
            Lat = Lat * (-1)
        LonRef = tags["GPS GPSLongitudeRef"].printable
        Lon = tags["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
        Lon = float(Lon[0]) + float(Lon[1]) / 60 + float(Lon[2]) / float(Lon[3]) / 3600
        if LonRef != "E":
            Lon = Lon * (-1)
    except:
        return "ERROR:请确保照片包含经纬度等EXIF信息。"
    else:
        return Lat, Lon


# print(get_image_detect_labels_by_url(""))
# print(filter_stop_word("This is a sample sentence, showing off the stop words filtration."))
# print(key_phrase("asdfasdfasdfasdfasdfasdfaasdfa"))
# print(exifread_infos_by_url('https://exposingtheinvisible.org/ckeditor_assets/pictures/32/content_example_ibiza.jpg'))
# https://raw.githubusercontent.com/ianare/exif-samples/master/jpg/gps/DSCN0010.jpg
# 12 21 25 27 29 38 40 42


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


def no_null_json(o):
    if o is None:
        return ERROR
    elif o == {}:
        return ERROR
    else:
        return o


@app.route('/hello')
def hello():
    return "Hello"


@app.route('/', methods=['POST'])
def web_get_images_by_search_text():
    result = None
    try:
        result_main = []
        result_search = []

        try:
            main_text = no_null_str(request.json["main_text"])
        except KeyError:
            main_text = ""
        try:
            search_text = no_null_str(request.json["search_text"])
        except KeyError:
            search_text = ""

        # filtered_main_words = filter_stop_word(main_text)
        # filtered_search_text = filter_stop_word(search_text)

        key_phrase_main_text_list = no_null_list(key_phrase(main_text))
        key_phrase_search_text_list = no_null_list(key_phrase(search_text))

        for query in key_phrase_main_text_list or []:
            image_results = BING_IMAGE_SEARCH_CLIENT.images.search(query=query)
            if image_results.value:
                result_main.extend(
                    list(
                        map(lambda x: {"thumbnail_url": x.thumbnail_url, "content_url": x.content_url, "detail": x.name,
                                       "description": x.description, "host_page_url": x.host_page_url,
                                       "date_published": x.date_published},
                            image_results.value)))

        for query in key_phrase_search_text_list or []:
            image_results = BING_IMAGE_SEARCH_CLIENT.images.search(query=query)
            if image_results.value:
                result_search.extend(
                    list(
                        map(lambda x: {"thumbnail_url": x.thumbnail_url, "content_url": x.content_url, "detail": x.name,
                                       "description": x.description, "host_page_url": x.host_page_url,
                                       "date_published": x.date_published},
                            image_results.value)))
        result = []
        result.extend(no_null_list(result_search[:5]))
        result.extend(no_null_list(result_main[:20]))
        result = list(filter(lambda x: is_stable_image_url(x["content_url"]), result))
        result = sorted(result, key=lambda k: k['date_published'], reverse=True)
        return jsonify(no_null_json(result[:25]))
    except Exception:
        print(traceback.format_exc())
        print("ERROR")
    return jsonify(no_null_json(None))


def is_stable_image_url(url):
    res = req.head(url, headers=FAKE_HEADER, verify=False)
    print(url)
    print(res.status_code)
    return res.status_code == 200


@app.route('/img', methods=['POST'])
def get_location_json_of_img():
    result = {}
    try:
        try:
            img_url = no_null_str(request.json["img_url"])
        except KeyError:
            img_url = ""
        lat, lon = exifread_infos_by_url(img_url)
        result['lat'] = lat
        result['lon'] = lon
    except Exception:
        pass
    return jsonify(no_null_json(result))


'''
{
    "main_text": "Panama City residents learn harsh lesson after Hurricane Michael I never would have stayedANAMA CITY, Fla.Gregg Ebersole trekked to the Panama City Marina from his devastated neighborhood on Thursday morning to find a miraculous sight: Nestled amid the twisted metal on the damaged dock was his boat, just as he had left it on a rack.Everything is tossed around like its a toy, said Ebersole, surveying the aftermath. Mine is sitting there all nice and pretty.It was a small dose of comfort after Hurricane Michael thrashed the Florida Panhandle on Wednesday and blew apart much in its path. Ebersoles single-story brick home survived, but he said he was caught flat-footed by the report that Michael had intensified into a powerful Category 4 storm quickly as it guzzled warm water on its advance up the Gulf of Mexico.If I knew it was going to be a Cat 4 with a direct hit, I never would have stayed, Ebersole said. Two days ago, we were out boating in the sunshine. This snuck up on us so quick.",
    "search_text": ""
}
'''


@app.route('/entity', methods=['POST'])
def get_entity_by_json():
    try:
        main_text = no_null_str(request.json["main_text"])
    except KeyError:
        main_text = ""
    return jsonify(no_null_json(get_entity_by_str(main_text)))


'''
{
  "lat": "40.714224",
  "lon": "-73.961452"
}
'''


@app.route('/location', methods=['POST'])
def reverse_location_search():
    return jsonify(no_null_json(get_location_by_lat_lon(request.json)))


'''
{
  "name": "University Of missouri"
}
'''


@app.route('/getlocationbyname', methods=['POST'])
def location_search():
    try:
        string = no_null_str(request.json["name"])
    except KeyError:
        string = ""
    return jsonify(no_null_json(get_location_by_str(string)))


'''
{
  "query": "Hurricane"
}
'''


@app.route('/news', methods=['POST'])
def news_search():
    try:
        string = no_null_str(request.json["query"])
    except KeyError:
        string = ""

    return jsonify(no_null_json(get_new_by_str(string)))


@app.route('/exif', methods=['GET'])
def get_example_of_exif_img():
    data = []
    for i in [10, 12, 21, 25, 27, 29, 38, 40, 42]:
        result = {}
        url = f'https://raw.githubusercontent.com/ianare/exif-samples/master/jpg/gps/DSCN00{i}.jpg'
        lat, lon = exifread_infos_by_url(url)
        result['lat'] = lat
        result['lon'] = lon
        result['url'] = url
        data.append(result)
    return jsonify(data)


@app.route('/people', methods=['POST'])
def get_people():
    try:
        string = no_null_str(request.json["img_url"])
    except KeyError:
        string = ""
    return jsonify(no_null_json(get_people_from_url(string)))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
