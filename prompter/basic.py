# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from abc import ABC, abstractmethod
import os
import yaml
from ..utils import print_with_color


class BasicPrompter(ABC):
    """
    추상 클래스 BasicPrompter
        """

    def __init__(self, is_visual: bool, prompt_template: str, example_prompt_template: str):
        """
        Initialize the BasicPrompter.
        :param is_visual: 요청이 시각 모델인지 여부.
        :param prompt_template: 프롬프트 템플릿의 경로.
        :param example_prompt_template: 예제 프롬프트 템플릿의 경로.
        """
        self.is_visual = is_visual
        if prompt_template:
            self.prompt_template = self.load_prompt_template(prompt_template) #
        else:
            self.prompt_template = "" #프롬프트 템플릿이 없는 경우 빈 문자열로 초기화
        if example_prompt_template: #예제 프롬프트 템플릿이 있는 경우
            self.example_prompt_template = self.load_prompt_template(example_prompt_template) 
        else:
            self.example_prompt_template = ""



    def load_prompt_template(self, template_path: str) -> dict:
        """
        Load the prompt template.
        :return: The prompt template.
        """

        if self.is_visual == None:
            path = template_path
        else:
            path = template_path.format(mode = "visual" if self.is_visual == True else "nonvisual")
            #visual 모델인 경우 visual, 아닌 경우 nonvisual로 포맷팅
        if os.path.exists(path):
            try:
                prompt = yaml.safe_load(open(path, "r", encoding="utf-8")) #yaml 파일 로드
            except yaml.YAMLError as exc: #yaml 파일 로드 중 오류 발생시
                print_with_color(f"Error loading prompt template: {exc}", "yellow") 
        else:
            raise FileNotFoundError(f"Prompt template not found at {path}")
        
        return prompt
    
    
    @staticmethod
    def prompt_construction(system_prompt:str, user_content:list) -> list[dict]:
        """
        경험을 예제로 요약하는 프롬프트로 변환합니다.
        :param user_content: 사용자의 입력 내용
        return: The prompt for summarizing the experience into an example.
        """
    
        system_message = {
            "role": "system",
            "content": system_prompt
        }

        user_message = {
            "role": "user", 
            "content": user_content
            }
        
        prompt_message = [system_message, user_message]

        return prompt_message
    

    @staticmethod
    def retrived_documents_prompt_helper(header: str, separator: str, documents: list) -> str:
        """
        반환된 문서에 대한 프롬프트를 생성합니다. retrieved document
        :param header: 프롬프트의 헤더.
        :param separator: 프롬프트의 구분자.
        :param documents: 반환된 문서.
        return: 반환된 문서에 대한 프롬프트.
        """

        if header:
            prompt = "\n<{header}:>\n".format(header=header)
        else:
            prompt = ""
        for i, document in enumerate(documents):
            if separator:
                prompt += "[{separator} {i}:]".format(separator=separator, i=i+1)
                prompt += "\n"
            prompt += document
            prompt += "\n\n"
        return prompt
    
    
    @abstractmethod
    def system_prompt_construction(self) -> str:

        pass
    
    
    @abstractmethod
    def user_prompt_construction(self) -> str:

        pass


    @abstractmethod
    def user_content_construction(self) -> str:

        pass


    def examples_prompt_helper(self) -> str:
        
        pass

    
    def api_prompt_helper(self) -> str:
        
        pass


    