# from gen_news import GenerateNewsSQL

# gen = GenerateNewsSQL()

# gen.create_story(title="Hello", author="Hrlle", content="Hello", tags="hello")
# x = gen.parse_news()
# print(gen._is_archived("3pr5xNjKzt2HkLLzM63hRW"))

# from infer import perform_search

# perform_search("Donald trump is a dog", n_results=3)

# from reporters import ReportersSQL

# auth = ReportersSQL()

# print(auth.parse_reporters())

# def gen():
#     for i in range(100):
#         yield i

# x = gen()

# for n in x:
#     print(n)

from groq import Groq
from openai import OpenAI

class InferenceClient():
    def __init__(
        self,
        model: str=None,
        api_key: str=None,
        inference_url: str=None,
        max_new_tokens: int=3000,
        global_sys_prompt: str=None,
        backend: str="groq", 
        temperature: float=1.0
    ):
        if not model or not api_key:
            return ValueError("Must specify model and api_key") 

        self.backends = ['groq', 'openai']
        self.api_key = api_key
        self.model = model
        self.inference_url = inference_url
        self.max_new_tokens = max_new_tokens
        self.global_sys_prompt = global_sys_prompt
        self.backend = backend.lower()
        self.temperature = temperature

        if backend not in self.backends:
            raise ValueError(f"backend must be one of these: {self.backends}")
        
        if backend == "groq":
            self.client = Groq(api_key=api_key)
        elif backend == "openai":
            self.client = OpenAI(api_key=api_key, base_url=inference_url)


    def client_infer(self, prompt, sys_prompt:str=None, model:str=None, stream:bool=False, max_new_tokens:int=None, temperature:float=None):
        model = model or self.model
        sys_prompt = sys_prompt or self.global_sys_prompt
        max_new_tokens = max_new_tokens or self.max_new_tokens
        temperature = temperature or self.temperature

        print(stream)

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Explain the importance of fast language models",
                }
            ],
            model=model,
            temperature=temperature,
            max_tokens=max_new_tokens,
            top_p=1,
            # stop=None,
            stream=stream,
        )
        print("done")

        if stream is True:
            # Returns generator func
            return self.process_stream(response)

        elif stream is False:
            return response.choices[0].message.content

    # Function that is a generator
    def process_stream(self, stream):
        partial_message = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content
                yield partial_message
        
if __name__ == "__main__":
    # inf = InferenceClient(api_key="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",
    #                       model="gemma2-9b-it")
    import os
    inf = InferenceClient(backend="openai", api_key="rc_58c93098d1b3c0ca152c4e31f6a8f7a331c7edd4959c46a6e15898faa733a87c", inference_url="https://api.featherless.ai/v1", model="NeverSleep/Llama-3-Lumimaid-8B-v0.1")
    x = inf.client_infer("How", stream=False)
    print(x)


