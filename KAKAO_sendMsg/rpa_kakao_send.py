'''
카카오메세지 보내기
'''

import pyautogui
import pyperclip
import uiautomation as auto

import time

# 윈도우 찾기
def active_window(window_title):
    for window in auto.GetRootControl().GetChildren():
        if str(window.Name).find(window_title) > -1:
            window.SetActive()
            print('윈도우찾기 성공')
            return
    raise

# 대화방 검색 및 예외 처리
def search(roomName):
    # 검색버튼이 이미 눌러져 있는 경우 검색창 초기화
    try:
        pyautogui.locateCenterOnScreen('KAKAO_sendMsg/image/isearch.png')
        i = pyautogui.locateCenterOnScreen('KAKAO_sendMsg/image/search.png')
        pyautogui.click(i)
        pyautogui.click(i)
    
    # 검색버튼을 최초로 누르는 경우
    except:
        i = pyautogui.locateCenterOnScreen('KAKAO_sendMsg/image/search.png')
        pyautogui.click(i)
    
    # 대화방 검색
    finally:
        pyperclip.copy(roomName)
        time.sleep(DELAY)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(DELAY)
        pyautogui.press('enter')
        time.sleep(DELAY)
        print('대화방 검색 성공')

# 메세지 보내기
def kakao_msg(msg):
    try:
        i = pyautogui.locateCenterOnScreen('KAKAO_sendMsg/image/input.png')
        pyautogui.click(i)
        pyperclip.copy(msg)
        time.sleep(DELAY)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(DELAY)
        pyautogui.press('enter')
        time.sleep(DELAY)
        print('메세지 발송 성공')
    except:
        print('메세지발송 실패')
        
########################
########################

if __name__ == '__main__':
    DELAY = 0.5
    ROOMNAME = '윤치선'
    MSG = '[TEST] 메세지를 보냅니다.'
    
    active_window('카카오톡')
    search(ROOMNAME)
    active_window(ROOMNAME)
    for _ in range(1):
        kakao_msg(MSG)
