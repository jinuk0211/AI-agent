import ast
import time
import warnings
from typing import List
from pywinauto import Desktop
# Desktop 클래스를 사용하면 다음과 같은 작업을 수행할 수 있습니다:

# 데스크톱 창과 컨트롤을 찾기: find_window 메서드를 사용하여 데스크톱 창과 컨트롤을 찾을 수 있습니다.
# 컨트롤 조작: click, type, set_focus 등의 메서드를 사용하여 컨트롤을 조작할 수 있습니다.
# 스크린샷 캡처: capture_screenshot 메서드를 사용하여 데스크톱 스크린샷을 캡처할 수 있습니다.

from ..config.config import load_config

configs = load_config()

BACKEND = config['CONTROL_BACKEND']

def get_desktop_app_info(remove_empty : bool = True):
  # 데스크탑에 있는 모든 application의 타이틀과 control type을 return
  # remove_empty param은 empty title을 지우기 위한 용도
    applist = Desktop(backend=BACKEND).windows()
    apptitles = [app.window_text() for app in applist]
    appcontrol_types = [app.element_info.control_type for app in applist]
  # control type에는 버튼 , 콤보박스, 리스트, edit, 텍스트등이 있음-  GUI와 상호작용
# if control_type == "Button":
#     # Click the button
    #     button.click()
    if remove_empty:                #타이틀이 없는 것의 control type 삭제
            appcontrol_types = [appcontrol_types[i] for i, title in enumerate(apptitles) if title != ""]
            apptitles = [title for title in apptitles if title != ""]
        return [apptitles, appcontrol_types]

def get_desktop_app_info_dict(remove_empty = True,fieldlist : List[str] = ['controltext','controltype'])
  desktopwindows = Desktop(BACKEND).windows() #데스크탑 윈도우를 가져옴 
  if remove_empty: 
     desktop_windows = [app for app in desktop_windows if app.window_text()!= "" and app.element_info.class_name not in ["IME", "MSCTFIME UI", "TXGuiFoundation"]]
  desktop_windows_dict = dict(zip([str(i+1) for i in range(len(desktop_windows))], desktop_windows))
  desktop_windows_info = get_control_info_dict(desktop_windows_dict, field_list)
  return desktop_windows_dict, desktop_windows_info

# IME은 컴퓨터에서 한글, 일본어, 중국어와 같은 표음 문자를 입력하는 데 사용하는 소프트웨어입니다. 키보드 입력 대신 다양한 방식으로 문자를 입력할 수 있도록 도와줍니다.
# IME의 주요 기능:

# 한글, 일본어, 중국어와 같은 표음 문자 입력
# 자동 완성 및 맞춤법 검사
# 키보드 단축키 및 제스처 지원
# 다양한 입력 방식 제공 (예: 부호 입력, 필기 입력)
# MSCTFIME UI

# MSCTFIME UI는 Microsoft Windows에서 제공하는 IME 사용자 인터페이스입니다. 다음과 같은 기능을 제공합니다.

# IME 설정 및 구성
# 입력 방식 선택
# 언어 바 전환
# 후보 목록 표시 및 선택
# 입력 모드 변경 (예: 한글, 영어)
# TXGuiFoundation

# TXGuiFoundation은 텍스트 입력 시스템을 위한 오픈 소스 라이브러리입니다. 다음과 같은 기능을 제공합니다.

# 다양한 IME 엔진 지원
# 사용자 인터페이스 개발 도구
# 입력 방식 관리
# 맞춤법 검사 및 자동 완성

def find_control_elements_in_descendants(window,controltypelist : List[str] = [],classnamelist = [], titlelist = [],isvisible=True,isenabled=True,depth=0)
#   parameter 설명
# window = app 을 찾을 window를 불러옴 
# controltypelist = 찾기위한 컨트롤 타입 리스트
# classnamelist = 
# isvisible = control요소들이 보이는가
# isenabled = control 요소들이 사용가능한가
# depth = 찾을 descendant의 깊이
  controlelements=[]
  if len(controltypelist)==0:
    controlelements += window.descendants() 
  else: 
    for controltype = 
