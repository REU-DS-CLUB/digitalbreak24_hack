import requests
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from transformers import AutoTokenizer, AutoModelForCausalLM


def get_t_lite(system_prompt, user_prompt):
    tokenizer = AutoTokenizer.from_pretrained("AnatoliiPotapov/T-lite-instruct-0.1")
    model = AutoModelForCausalLM.from_pretrained("AnatoliiPotapov/T-lite-instruct-0.1").cuda()

    END_OF_LINE = tokenizer('://').input_ids[0]

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": user_prompt},
    ]


    input_ids = tokenizer.apply_chat_template(messages, return_tensors='pt').cuda()
    beam_outputs = model.generate(
        input_ids,
        max_length=1800,
        do_sample=True,
        top_k=5,
        no_repeat_ngram_size=2,
        early_stopping=True,
        eos_token_id=END_OF_LINE,
    )

    answer = tokenizer.decode(beam_outputs[0], skip_special_tokens=True)

class YandexGPT:
    def __init__(self, api_key: str):

        self.api_key = api_key
        self.model_uri = "ds://bt14696sm7ggocqkreas"

    def output(self, text: str, system_prompt: str) -> str:

        self.system_prompt = system_prompt

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "x-folder-id":'b1g72uajlds114mlufqi'

        }
        data = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 6000
            },
            "messages": [
                {"role": "system", "text": self.system_prompt},
                {"role": "user", "text": text}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            message = result['result']['alternatives'][0]['message']['text']
            return message
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
class GigaChatTask:

    def __init__(self, api_gigachat: str):
        
        self.api_key = api_gigachat
        self.model = GigaChat(credentials=self.api_key, verify_ssl_certs=False)
        
        
    def output(self, text: str, system_prompt: str) -> str:
        
        self.messages = [
            SystemMessage(content=system_prompt)
        ]
        self.messages.append(HumanMessage(content=text))
        res = self.model.invoke(self.messages)
        self.messages.append(res)
        return res.content



