import base64

import requests
from urllib import parse
import json
import os

API_KEY = "XG1F4lrEfcZvCxajGLwlFX9l"
SECRET_KEY = "n2wUaqiqdyf9Re9eG7qPGhFva3ur5B0x"


def main():
    for i in range(1):
        prefix = 'c3p'
        word_list_name = f'{prefix}{i + 1}'
        path_prefix = f'img/{word_list_name}'
        img_list = os.listdir(path_prefix)
        for img in img_list:
            image_file = f'{path_prefix}/{img}'
            url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=" + get_access_token()

            # print(f'base64encoded_file(image_file):{base64encoded_file(image_file)}')
            # return

            payload = f'image={url_encode_string(base64encoded_file(image_file))}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            res = json.loads(response.text)

            # left_list = []
            # right_list = []
            #
            # last_top = -100
            # for w in res['words_result']:
            #     if abs(w['location']['top'] - last_top) < 20:
            #         right_list.append(w)
            #     else:
            #         left_list.append(w)
            #     last_top = w['location']['top']
            #
            # merge_list = left_list + right_list

            # print(f'merge_list:{merge_list}')

            with open(f'word_list/{word_list_name}.txt', 'a', encoding='utf-8') as f:
                for w in res['words_result']:
                    f.write(w['words'] + '\n')

            d = 3


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def base64encoded_file(file):
    with open(file, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def url_encode_string(str):
    return parse.quote(str)


if __name__ == '__main__':
    main()
