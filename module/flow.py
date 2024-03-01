import logging
import os
import time
import json
import yaml
from art import text2art
from pywinauto.uia_defines import NoPatternInterfaceError
#Windows UI 자동화를 위한 Python 모듈
from ..config.config import load_config
from ..llm import llm_call
from ..llm import prompt as prompter
from ..ui_control import control
from ..ui_control import screenshot as screen
from ..utils import (create_folder, encode_image_from_path,
                     generate_function_call, json_parser, print_with_color,
                     revise_line_breaks, yes_or_no)

configs = load_config()
BACKEND = configs["CONTROL_BACKEND"]

#세션 사용자와 시스템간의 상호작용단위, 웹브라우징,로그인,게임플레이 등
class session(object): #수행할 작업 trajectory

  def __init__(self,task):
    self.task = task
    self.step = 0
    self.round = 0
    self.actionhistory = []
    
    self.logpath = f'logs/{self.task}' #task마다 로그
    create_folder(self.logpath)
    #logging 라이브러리
    self.logger = initialize_logger(self.logpath,'response.log') #응답 로그
    self.requestlogger = initialize_logger(self.logpath,'request.log' #요청 로그
    #app agent 선택
    self.appselectprompt = yaml.safe_load(open(configs["APP_SELECTION_PROMPT"], "r", encoding="utf-8"))
    self.actionselectprompt = yaml.safe_load(open(configs["ACTION_SELECTION_PROMPT"], "r", encoding="utf-8"))
    self.status = 'APP_SELECTION'
    self.application =''
    self.appwindow = None
    self.plan = ''
    self.requests = '' 
    self.results = ''
    self.cost = 0

    self.request = input()  
    self.requesthistory = []
 
  def process_application_selection(self,headers):
              
      # 헤더 내용 - 요청 또는 응답에 대한 메타데이터
    printwithcolor('단계{step}: 어플리케이션 {application}에서 행동 수행 중.'.format(step = self.step,application = self.application),'magenta')        
    
             
  
