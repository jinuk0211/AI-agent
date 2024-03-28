# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ufo.utils import print_with_color
from ..config.config import load_config


configs = load_config()


def get_completion(messages, agent: str='APP', use_backup_engine: bool=True):
    """
    openai api 기능 사용을 위한 함수

    Args:
        메시지 : 사용자의 메시지
        에이젼트 : 사용할 에이젼트 , app, action, backup 중 하나
        use_backup_engine : 백업 엔진 사용 여부

    Returns:
        튜플 : (응답, 비용)

    """
    if agent.lower() == "app": #app agent 반환
        agent_type = "APP_AGENT"
    elif agent.lower() == "action": # action agent 반환
        agent_type = "ACTION_AGENT"
    elif agent.lower() == "backup": #backup agent 반환
        agent_type = "BACKUP_AGENT"
    else:
        raise ValueError(f'Agent {agent} not supported')
    
    api_type =  configs[agent_type]['API_TYPE'] #api type 가져오기
    try:
        if api_type.lower() in ['openai', 'aoai', 'azure_ad']: #openai, aoai, azure_ad 중 하나인 경우
            from .openai import OpenAIService #openai 모듈 가져오기
            response, cost = OpenAIService(configs, agent_type=agent_type).chat_completion(messages)
            return response, cost
        else:
            raise ValueError(f'API_TYPE {api_type} not supported')
    except Exception as e:
        if use_backup_engine:
            print_with_color(f"The API request of {agent_type} failed: {e}.", "red")
            print_with_color(f"Switching to use the backup engine...", "yellow")
            return get_completion(messages, agent='backup', use_backup_engine=False)
        else:
            raise e