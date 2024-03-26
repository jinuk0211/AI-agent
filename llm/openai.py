import datetime
from typing import Any, Dict, List, Tuple, Optional
import openai
from openai import AzureOpenAI, OpenAI

class openaiservice:
    def __init__(self, config, agent_type: str ) 
        self.config_llm = config[agent_type] #app agent, action agent

        self.config = config
        api_type = self.config_llm['api_type'].lower()# azure, openai,azure_ad
        max_retry = self.config_llm['MAX_RETRY']
        assert api_type in ['aoai', 'openai','azure_ad'], f"잘못된 {api_type}"
        self.client : OpenAI = (
            OpenAI(
                base_url=self.config_llm['API_BASE'],
                api_key=self.config_llm['API_KEY'],
                max_retries = max_retry #최대 재시도 횟수
                timeout = self.config_llm['TIMEOUT'] #요청시간 초과시간
            )
            if api_type == 'openai'
            else AzureOpenAI(
                base_url=self.config_llm['API_BASE'],
                api_key=(self.config_llm['API_KEY'] if api_type == 'aoai' else self.get_openai_token()),
                max_retries = max_retry #최대 재시도 횟수
                timeout = self.config_llm['TIMEOUT'] #요청시간 초과시간
            )
        )
        if api_type == 'azure_ad':
            self.auto_refresh_token()

    def chat_completion(
        self,
        messages,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs: Any,
    ):

    def get_openai_token(
        self,
        token_cache_file: str = 'apim-token-cache.bin',
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> str:

    def auto_refresh_token(
        self,
        token_cache_file: str = 'apim-token-cache.bin',
        interval: datetime.timedelta = datetime.timedelta(minutes=15),
        on_token_update: callable = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> callable:
