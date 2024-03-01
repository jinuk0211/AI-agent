import argparse
import datetime

from .config.config import loadconfig
from .module import flow
from .utils import printwithcolor

config = loadconfig() #dict 형식의 config load
args = argparse.ArgumentParser() #args 생성 CLI로
args.add_argument()
args.add_argument()

parsedargs = args.parse_args() #  명령어인수를 여러번 사용할 떄 유용

if configs['APItype'].lower() == 'openai':
  headers = {  
              'Content-Type' : 'application/json',   #gptkey 명령인자
              'Authorization' : f'Bearer {parsedargs.gptkeys}'  }
else:
  raise ValueError('APIkey가 필요합니다')

def main():
  pass


if __name__ == "__main__":
    main()
