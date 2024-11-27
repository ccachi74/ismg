'''
    카카오 rest api 를 사용하기 위한 토큰파일 생성 (최초 1회만 실행)
'''

import requests

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '4803fec1ab63427fd24ecfb103628c25'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'oBe_wOWWV8ELwd3pCO4nkOAndZdnY3NXDAXPn4ZRh_drpW-DimyDFwAAAAQKPXKYAAABk2dtYxaxu3fh8M0xkQ'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
import json
#1.
with open(r"kakao_code.json","w") as fp:
    json.dump(tokens, fp)
    
    