import torch
from typing import Any, Dict, Tuple
from huggingface_hub import login
from datasets import load_dataset
from transformers import pipeline
from pyannote.audio import Pipeline as DiarizationPipeline
from speechbox import ASRDiarizationPipeline


class SpeechProcessing:
    
    def __init__(self) -> None:
        """
        Инициализирует класс SpeechProcessing с пустыми пайплайнами для диаризации и распознавания речи.
        """
        self.diarization_pipeline: DiarizationPipeline = None
        self.asr_pipeline: Any = None
    
    
    @staticmethod
    def authorization() -> None:
        """
        Авторизация на Hugging Face с использованием токена из файла.
        """
        with open("secrets/hugging_face_token.txt", "r") as file:
            hugging_face_token: str = file.read()

        login(token=hugging_face_token, add_to_git_credential=True)


    def load_diarization_model(self) -> None:
        """
        Загрузка модели для диаризации речи.
        """
        self.diarization_pipeline = DiarizationPipeline.from_pretrained(
            "pyannote/speaker-diarization@2.1", use_auth_token=True
        )


    def load_asr_model(self) -> None:
        """
        Загрузка модели для автоматического распознавания речи (ASR).
        """
        self.asr_pipeline = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-base",
        )


    def load_dataset(self) -> Dict[str, Any]:
        """
        Загрузка и получение выборки из датасета.
        
        Returns:
            Dict[str, Any]: Первое значение из стримингового датасета.
        """
        concatenated_librispeech = load_dataset(
            "sanchit-gandhi/concatenated_librispeech", split="train", streaming=True
        )
        return next(iter(concatenated_librispeech))


    def process_audio(self, sample: Dict[str, Any]) -> Tuple[Dict[str, Any], Any]:
        """
        Процессинг аудио для диаризации и распознавания речи.
        
        Args:
            sample (Dict[str, Any]): Входной аудиосэмпл.
        
        Returns:
            Tuple[Dict[str, Any], Any]: Результаты распознавания речи (ASR) и диаризации.
        """
        input_tensor = torch.from_numpy(sample["audio"]["array"][None, :]).float()
        
        diarization_result = self.diarization_pipeline(
            {"waveform": input_tensor, "sample_rate": sample["audio"]["sampling_rate"]}
        )
        
        asr_result = self.asr_pipeline(
            sample["audio"].copy(),
            generate_kwargs={"max_new_tokens": 256},
            return_timestamps=True,
        )
        
        return asr_result, diarization_result


    def combine_pipelines(self, sample: Dict[str, Any]) -> Any:
        """
        Комбинирование диаризации и распознавания речи в одну обработку.
        
        Args:
            sample (Dict[str, Any]): Входной аудиосэмпл.
        
        Returns:
            Any: Результат обработки аудиофайла с помощью объединенных пайплайнов ASR и диаризации.
        """
        pipeline = ASRDiarizationPipeline(
            asr_pipeline=self.asr_pipeline, diarization_pipeline=self.diarization_pipeline
        )
        return pipeline(sample["audio"].copy())


    @staticmethod
    def tuple_to_string(start_end_tuple: Tuple[float, float], ndigits: int = 1) -> str:
        """
        Форматирование кортежа времени в строку с указанной точностью.
        
        Args:
            start_end_tuple (Tuple[float, float]): Кортеж с началом и концом времени.
            ndigits (int): Количество знаков после запятой.
        
        Returns:
            str: Форматированная строка с округленными значениями времени.
        """
        return str((round(start_end_tuple[0], ndigits), round(start_end_tuple[1], ndigits)))


    def format_as_transcription(self, raw_segments: Any) -> str:
        """
        Форматирование сырых сегментов в текстовую транскрипцию.
        
        Args:
            raw_segments (Any): Сырые данные сегментов (речевые сегменты с текстом и временными отметками).
        
        Returns:
            str: Текстовая транскрипция всех сегментов.
        """
        return "\n\n".join(
            [
                chunk["speaker"] + " " + self.tuple_to_string(chunk["timestamp"]) + ": " + chunk["text"]
                for chunk in raw_segments
            ]
        )
