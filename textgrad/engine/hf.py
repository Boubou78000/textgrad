try:
    import transformers
except ImportError:
    raise ImportError("If you'd like to use HuggingFace models, please install the transformers package by running `pip install transformers`.") #, and add 'HUGGINGFACEHUB_API_TOKEN' to your environment variables

import os
import platformdirs
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

from .base import EngineLM, CachedEngine

class ChatHF(EngineLM, CachedEngine):
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, creative, and smart assistant."

    def __init__(
        self,
        model_string="google/gemma-2-9b-it",
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        **kwargs):
        """
        :param model_string:
        :param system_prompt:
        """
        root = platformdirs.user_cache_dir("textgrad")
        cache_path = os.path.join(root, f"cache_hf_{model_string}.db")
        super().__init__(cache_path=cache_path)

        self.system_prompt = system_prompt

        self.pipeline = transformers.pipeline("text-generation", model_string, **kwargs)

        self.model_string = model_string

    def generate(
        self, prompt, system_prompt=None, temperature=0, max_tokens=2000, top_p=0.99, do_sample=True
    ):
        print(prompt)

        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt

        cache_or_none = self._check_cache(sys_prompt_arg + prompt)
        if cache_or_none is not None:
            return cache_or_none

        response = self.pipeline(
            {
                "role": "system", "content": sys_prompt_arg,
                "role": "user", "content": prompt
            },
            temperature=None if temperature == 0 else temperature,
            max_lenght=max_tokens,
            top_p=top_p,
            do_sample=do_sample
        )

        print(response)

        self._save_cache(sys_prompt_arg + prompt, response)
        return response

    @retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(5))
    def __call__(self, prompt, **kwargs):
        return self.generate(prompt, **kwargs)

