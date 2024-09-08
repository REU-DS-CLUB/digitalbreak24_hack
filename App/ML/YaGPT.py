import requests
from secrets.api import YANDEXGPT_KEY


class YaGPT:
    """
    Класс YaGPT предназначен для взаимодействия с API Yandex и выполнения задач по суммаризации текста с использованием GPT.

    Атрибуты:
    ----------
    api_key : str
        API ключ для доступа к Yandex Cloud.
    system_prompt : str
        Системный промпт, который определяет контекст и задачи для модели.
    model_uri : str
        URI модели для запроса.

    Методы:
    -------
    __init__(self, api_key: str, system_prompt: str, model_uri: str)
        Инициализирует класс YaGPT с заданным API ключом, системным промптом и URI модели.
    summarize(self, text: str) -> str
        Выполняет суммаризацию текста с использованием модели GPT от Yandex.
    """

    def __init__(self, api_key: str, system_prompt: str):
        """
        Инициализирует класс YaGPT.

        Параметры:
        ----------
        api_key : str
            API ключ для доступа к Yandex Cloud.
        system_prompt : str
            Системное сообщение, определяющее контекст и задачи для модели.
        model_uri : str
            URI модели, которая будет использоваться для выполнения запросов.
        """
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.model_uri = "gpt://b1g72uajlds114mlufqi/yandexgpt/latest"

    def summarize(self, text: str) -> str:
        """
        Выполняет суммаризацию текста с использованием модели GPT от Yandex.

        Параметры:
        ----------
        text : str
            Текст, который необходимо суммировать.

        Возвращаемое значение:
        ----------------------
        str
            Результат суммаризации текста, возвращаемый моделью GPT от Yandex.
        """
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
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
        

def making_speaker_mapping():
    pass

def convert_diarisation_to_text(diarisation_result: dict, speaker_mapping: dict) -> str:
    """
    diarisation_result - JSON передаваемый из сервиса Диаризации
    Пример:
    diarisation_result = {
        (15.0, 17.9): {"speaker": "SPEAKER0", "text": "i want sleep"},
        (18.5, 18.9): {"speaker": "SPEAKER1", "text": "i too"},
    
    }

    speaker_mapping - dict с полем спикера после диаризации и его настоящис именем
    Пример:
    speaker_mapping = {
        'SPEAKER0':"Настя",
        'SPEAKER1':"Андрей"
    }    


    """

    result = []
    for (start_time, end_time), details in diarisation_result.items():
        speaker = speaker_mapping[details["speaker"]]
        text = details["text"]
        result.append(f"{start_time} - {end_time} - {speaker}: {text}")
    return "\n".join(result)


diarisation_result =  {
        (15.0, 17.9): {"speaker": "SPEAKER0", "text": "i want sleep"},
        (18.5, 18.9): {"speaker": "SPEAKER1", "text": "i too"},
    
    }
speaker_mapping = {
        'SPEAKER0':"Настя",
        'SPEAKER1':"Андрей"
}

print(convert_diarisation_to_text(diarisation_result, speaker_mapping))

