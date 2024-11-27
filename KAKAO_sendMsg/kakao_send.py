'''
REST API 를 이용한 카카오톡 메세지 보내기
토큰 유효시간은 12시간으로, 유효시간 경과 후 토큰 재생성 해야함.
'''

import requests
import webbrowser

# 1. 카카오 REST API 키와 리다이렉트 URI 설정
REST_API_KEY = '4803fec1ab63427fd24ecfb103628c25'
REDIRECT_URI = 'https://example.com/oauth'
AUTH_URL = f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
TOKEN_URL = "https://kauth.kakao.com/oauth/token"

# 2. 자동 토큰 발급 함수
def get_access_token():
    # 사용자 인증 URL 열기
    print("브라우저에서 사용자 인증을 진행하세요...")
    webbrowser.open(AUTH_URL)

    # 사용자 입력으로 인증 코드를 받아옴
    auth_code = input("인증 코드 입력: ")

    # 액세스 토큰 요청
    token_data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": auth_code,
    }
    response = requests.post(TOKEN_URL, data=token_data)
    if response.status_code == 200:
        tokens = response.json()
        print("토큰 발급 성공:", tokens)
        return tokens["access_token"]
    else:
        print("토큰 발급 실패:", response.json())
        return None

# 3. 메시지 전송 함수
def send_message(access_token):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "template_object": """{
            "object_type": "text",
            "text": "안녕하세요! 자동화된 메시지 전송입니다.",
            "link": {
                "web_url": "https://www.example.com",
                "mobile_web_url": "https://m.example.com"
            }
        }"""
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("메시지 전송 성공")
    else:
        print("메시지 전송 실패:", response.json())

# 4. 자동화된 실행
if __name__ == "__main__":
    # 토큰 발급
    token = get_access_token()
    if token:
        # 메시지 전송
        send_message(token)
