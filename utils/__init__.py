import base64
import json
import os
from io import BytesIO
from typing import Optional

from colorama import Fore, Style, init
from PIL import Image

init() #colorma init?
def printwithcolor(text : str, color :str = ''):
  #colorma 라이브러리의 ANSI escape code의 특정 색상을 통해 글자에 색상입혀 출력

  colormap = { 
'red' = Fore.RED,
'green' = Fore.GREEN,
"yellow": Fore.YELLOW,
"blue": Fore.BLUE,
"magenta": Fore.MAGENTA,
"cyan": Fore.CYAN,
"white": Fore.WHITE,
"black": Fore.BLACK  } #사용가능한 컬러 param

selectedcolor = colormap.get(color.lower(),'')
coloredtext =  selected_color + text + Style.RESET_ALL #원리는 모르지만 text색상이 변경됨

print(colored_text)

    
  }
