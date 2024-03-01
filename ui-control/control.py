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
