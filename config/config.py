import os
import yaml
import json
from .utils import print_with_color

def load_config(config_path = 'ufo/config/'):
  # 환경변수랑 yaml 파일로부터 configuaration 로드
  configs = dict.(os.environ)
  path = config_path

  try:
    with open(path + 'config.yaml','r') as file:
      yaml_data = yaml.safe_load(file) #yaml 함수

    if yaml_data:
      configs.update(yaml_data) #yaml데이터가 있을 시 config 업데이트

    with open(path + 'config_dev.yaml','r') as file:
      yaml_dev_data = yaml.safe_load(file)

    if yaml_dev_data:
      configs.update(yaml_dev_data)
  except FileNotFoundError:
    print_with_color(
      f'config 파일이 {config_path}에 없음. 환경변수만을 사용'.'yellow' )
  return optimize_configs(configs)


def update_api_base(configs, agent):

def optimize_configs(configs):
    update_api_base(configs,'APP_AGENT') #app agent용
    update_api_base(configs,'ACTION_AGENT') #action agent 용
    
    return configs

def get_offline_learner_indexer_config():
  
