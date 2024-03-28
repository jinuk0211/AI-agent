# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from .basic import BasicPrompter #BasicPrompter 가져오기
import json


class ApplicationAgentPrompter(BasicPrompter):
    
# • Desktop Screenshots: 현재 데스크탑의 스크린샷, 여러 화면이 하나의 이미지로 연결됨. 
    
# application agent를 위한 prompter 

    def __init__(self, is_visual: bool, prompt_template: str, example_prompt_template: str, api_prompt_template: str):
        """
        :param is_visual: 요청이 시각 모델을 위한 것인지 여부
        :param prompt_template: 프롬프트 템플릿의 경로
        :param example_prompt_template: 예시 프롬프트 템플릿의 경로
        :param api_prompt_template: api 프롬프트 템플릿의 경로
        """
        super().__init__(is_visual, prompt_template, example_prompt_template)
        self.api_prompt_template = self.load_prompt_template(api_prompt_template)


    def system_prompt_construction(self) -> str:
        """
        app 선택을 위한 프롬프트 구성
        반환 : app 선택을 위한 프롬프트
        """

        apis = self.api_prompt_helper(verbose = 0)
        examples = self.examples_prompt_helper()     

        return self.prompt_template["system"].format(apis=apis, examples=examples)
    


    def user_prompt_construction(self, request_history: list, action_history: list, control_item: list, prev_plan: str, user_request: str, retrieved_docs: str="") -> str:
        """
        action 선택을 위한 프롬프트 구성
        :param action_history: action 히스토리
        :param control_item: 제어 아이템
        :param user_request: 사용자 요청
        :param retrieved_docs: 검색된 문서
        return: action 선택을 위한 프롬프트
        """
        prompt = self.prompt_template["user"].format(action_history=json.dumps(action_history), request_history=json.dumps(request_history), 
                                            control_item=json.dumps(control_item), prev_plan=prev_plan, user_request=user_request, retrieved_docs=retrieved_docs)
        
        return prompt
    


    def user_content_construction(self, image_list: list, request_history: list, action_history: list, control_item: list, prev_plan: str, user_request: str, retrieved_docs: str="") -> list[dict]:
        """
        LLMS를 위한 프롬프트 구성
        :param image_list: image 리스트
        :param action_history: action 히스토리
        :param control_item: 제어 아이템
        :param user_request: 사용자 요청
        :param retrieved_docs: 검색된 문서
        return: LLMS를 위한 프롬프트
        """

        user_content = []


        if self.is_visual:
            screenshot_text = ["Current Screenshots:"] #현재 스크린샷
        
            for i, image in enumerate(image_list):
                user_content.append({
                    "type": "text",
                    "text": screenshot_text[i]
                })
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image
                    }
                })

        user_content.append({
            "type": "text",
            "text": self.user_prompt_construction(request_history, action_history, control_item, prev_plan, user_request, retrieved_docs)
        })

        return user_content
    


    def examples_prompt_helper(self, header: str = "## Response Examples", separator: str = "Example") -> str:
        """
        예시를 위한 프롬프트 구성
        :param examples: 예시
        :param header: 프롬프트의 헤더
        :param separator: 프롬프트의 구분자
        return: 예시를 위한 프롬프트
        """
        
        template = """
        [사용자 요청]: 
            {request}
        [응답]: 
            {response}"""
        example_list = []

        for key in self.example_prompt_template.keys():
            if key.startswith("example"):
                example = template.format(request=self.example_prompt_template[key].get("Request"), response=json.dumps(self.example_prompt_template[key].get("Response")))
                example_list.append(example)

        return self.retrived_documents_prompt_helper(header, separator, example_list)



    def api_prompt_helper(self, verbose: int = 1) -> str:
        """
        API를 위한 프롬프트 구성
        :api
        :param verbose: The verbosity level.
        return: The prompt for APIs.
        """

        # Construct the prompt for APIs
        api_list = ["- The action type are limited to {actions}.".format(actions=list(self.api_prompt_template.keys()))]
        
        # Construct the prompt for each API
        for key in self.api_prompt_template.keys():
            api = self.api_prompt_template[key]
            if verbose > 0:
                api_text = "{summary}\n{usage}".format(summary=api["summary"], usage=api["usage"])
            else:
                api_text = api["summary"]
                
            api_list.append(api_text)

        api_prompt = self.retrived_documents_prompt_helper("", "", api_list)
            
        return api_prompt
    


class ActionAgentPrompter(BasicPrompter):
    """
    The ActionAgentPrompter class is the prompter for the action agent.
    """

    def __init__(self, is_visual: bool, prompt_template: str, example_prompt_template: str, api_prompt_template: str):
        """
        Initialize the ApplicationAgentPrompter.
        :param is_visual: 요청이 시각 모델을 위한 것인지 여부
        :param prompt_template: 프롬프트 템플릿의 경로
        :param example_prompt_template: 프롬프트 예시 템플릿의 경로
        :param api_prompt_template: api 프롬프트 템플릿의 경로
        """
        super().__init__(is_visual, prompt_template, example_prompt_template)
        self.api_prompt_template = self.load_prompt_template(api_prompt_template)


    def system_prompt_construction(self, additional_examples: list =[], tips: list =[]) -> str:
        """
        Construct the prompt for app selection.
        return: The prompt for app selection.
        """

        apis = self.api_prompt_helper(verbose = 1)
        examples = self.examples_prompt_helper(additional_examples=additional_examples)
        tips_prompt = "\n".join(tips)

        # Remove empty lines
        tips_prompt = '\n'.join(filter(None, tips_prompt.split('\n')))

        return self.prompt_template["system"].format(apis=apis, examples=examples, tips=tips_prompt)
    


    def user_prompt_construction(self, request_history: list, action_history: list, control_item: list, prev_plan: str, user_request: str, retrieved_docs: str="") -> str:
        """
        Construct the prompt for action selection.
        :param prompt_template: The template of the prompt.
        :param action_history: The action history.
        :param control_item: The control item.
        :param user_request: The user request.
        :param retrieved_docs: The retrieved documents.
        return: The prompt for action selection.
        """
        prompt = self.prompt_template["user"].format(action_history=json.dumps(action_history), request_history=json.dumps(request_history), 
                                            control_item=json.dumps(control_item), prev_plan=prev_plan, user_request=user_request, retrieved_docs=retrieved_docs)
        
        return prompt
    


    def user_content_construction(self, image_list: list, request_history: list, action_history: list, control_item: list, prev_plan: str, user_request: str, retrieved_docs: str="", include_last_screenshot: bool=True) -> list[dict]:
        """
        Construct the prompt for LLMs.
        :param image_list: The list of images.
        :param action_history: The action history.
        :param control_item: The control item.
        :param user_request: The user request.
        :param retrieved_docs: The retrieved documents.
        return: The prompt for LLMs.
        """

        user_content = []


        if self.is_visual:

            screenshot_text = []
            if include_last_screenshot:
                screenshot_text += ["Screenshot for the last step:"]

                screenshot_text += ["Current Screenshots:", "Annotated Screenshot:"]
        
            for i, image in enumerate(image_list):
                user_content.append({
                    "type": "text",
                    "text": screenshot_text[i]
                })
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image
                    }
                })

        user_content.append({
            "type": "text",
            "text": self.user_prompt_construction(request_history, action_history, control_item, prev_plan, user_request, retrieved_docs)
        })

        return user_content
        
    
    def examples_prompt_helper(self, header: str = "## Response Examples", separator: str = "Example", additional_examples: list[str] = []) -> str:
        """
        Construct the prompt for examples.
        :param examples: The examples.
        :param header: The header of the prompt.
        :param separator: The separator of the prompt.
        return: The prompt for examples.
        """
        
        template = """
        [User Request]:
            {request}
        [Response]:
            {response}"""
        
        example_list = []

        for key in self.example_prompt_template.keys():
            if key.startswith("example"):
                example = template.format(request=self.example_prompt_template[key].get("Request"), response=json.dumps(self.example_prompt_template[key].get("Response")))
                example_list.append(example)

        example_list += [json.dumps(example) for example in additional_examples]

        return self.retrived_documents_prompt_helper(header, separator, example_list)


    def api_prompt_helper(self, verbose: int = 1) -> str:
        """
        Construct the prompt for APIs.
        :param apis: The APIs.
        :param verbose: The verbosity level.
        return: The prompt for APIs.
        """

        # Construct the prompt for APIs
        api_list = ["- The action type are limited to {actions}.".format(actions=list(self.api_prompt_template.keys()))]
        
        # Construct the prompt for each API
        for key in self.api_prompt_template.keys():
            api = self.api_prompt_template[key]
            if verbose > 0:
                api_text = "{summary}\n{usage}".format(summary=api["summary"], usage=api["usage"])
            else:
                api_text = api["summary"]
                
            api_list.append(api_text)

        api_prompt = self.retrived_documents_prompt_helper("", "", api_list)
            
        return api_prompt
    