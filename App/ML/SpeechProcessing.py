import torch
import numpy as np
from typing import Any, Dict, Tuple
from pydub import AudioSegment
from huggingface_hub import login

from transformers import pipeline
from pyannote.audio import Pipeline as DiarizationPipeline
from speechbox import ASRDiarizationPipeline
from pyannote.audio import Pipeline


class SpeechProcessing:
    
    def __init__(self) -> None:
        """
        Инициализирует класс SpeechProcessing с пустыми пайплайнами для диаризации и распознавания речи.
        """
        self.diarization_pipeline: DiarizationPipeline = None
        self.asr_pipeline: Any = None

        # Определение устройства (GPU или CPU)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")

    @staticmethod
    def authorization() -> None:
        """
        Авторизация на Hugging Face с использованием токена из файла.
        """
        login(token="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")

    @classmethod
    def load_diarization_model(cls) -> None:
        """
        Загрузка модели для диаризации речи.
        """
        cls.diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.0",
        )
        
    @classmethod
    def load_asr_model(cls) -> None:
        """
        Загрузка модели для автоматического распознавания речи (ASR).
        """
        cls.asr_pipeline = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-medium",
            device='cuda' if torch.cuda.is_available() else 'cpu' # Используем GPU, если доступен
        )

    def load_mp3(self, file_path: str) -> Dict[str, Any]:
        """
        Загрузка аудиофайла в формате MP3 и конвертация его в нужный формат.
        
        Args:
            file_path (str): Путь к файлу MP3.
        
        Returns:
            Dict[str, Any]: Словарь с аудиоданными и частотой дискретизации.
        """
        # Загружаем MP3 файл
        audio = AudioSegment.from_mp3(file_path)
        
        # Конвертируем в моно и частоту дискретизации 16kHz
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # Нормализация громкости
        audio = audio.normalize()  
        
        # Применение низкочастотного фильтра для удаления шума
        audio = audio.low_pass_filter(3000)  
        
        # Преобразуем в numpy массив
        samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
        
        # Возвращаем данные в нужном формате
        return {
            "audio": {
                "array": samples,
                "sampling_rate": 16000
            }
        }

    def diarize_audio(self, sample: Dict[str, Any]) -> Tuple[Dict[str, Any], Any]:
        """
        Процессинг аудио для диаризации и распознавания речи.
        
        Args:
            sample (Dict[str, Any]): Входной аудиосэмпл.
        
        Returns:
            Tuple[Dict[str, Any], Any]: Результаты распознавания речи (ASR) и диаризации.
        """
        self.__class__.diarization_pipeline.to(self.device)
        
        # Преобразование аудио в тензор и перемещение на GPU/CPU
        input_tensor = torch.from_numpy(sample["audio"]["array"][None, :]).float().to(self.device)
        
        # Диаризация
        diarization_result = self.__class__.diarization_pipeline(
            {"waveform": input_tensor, "sample_rate": sample["audio"]["sampling_rate"]}
        )
        
        return diarization_result

    def transcribe_audio(self, sample):
        
        # Распознавание речи
        asr_result = self.__class__.asr_pipeline(
            sample["audio"]["array"].copy(),
            generate_kwargs={"max_new_tokens": 256, "language": "ru"},
            return_timestamps=True
        )
        return asr_result

    def combine_pipelines(self, sample: Dict[str, Any]) -> Any:
        """
        Комбинирование диаризации и распознавания речи в одну обработку.
        
        Args:
            sample (Dict[str, Any]): Входной аудиосэмпл.
        
        Returns:
            Any: Результат обработки аудиофайла с помощью объединенных пайплайнов ASR и диаризации.
        """
        pipeline = ASRDiarizationPipeline(
            asr_pipeline=self.__class__.asr_pipeline, diarization_pipeline=self.__class__.diarization_pipeline
        )
        print(pipeline)
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

    def format_as_transcription(self, raw_segments: Any):
        """
        Форматирование сырых сегментов в текстовую транскрипцию.
        
        Args:
            raw_segments (Any): Сырые данные сегментов (речевые сегменты с текстом и временными отметками).
        
        Returns:
            str: Текстовая транскрипция всех сегментов.
        """
        return {
            str(chunk["timestamp"][0], chunk["timestamp"][1]) : {"speaker": chunk["speaker"], "text": chunk["text"]} for chunk in raw_segments
        }
