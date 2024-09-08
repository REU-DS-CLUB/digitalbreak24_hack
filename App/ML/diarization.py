from SpeechProcessing import SpeechProcessing

speech_processor = SpeechProcessing()

# авторизация
SpeechProcessing.authorization()

# загрузка моделей
SpeechProcessing.load_diarization_model()
SpeechProcessing.load_asr_model()


def diarization(audio_path):

    # Diarization
    sample = speech_processor.load_mp3(audio_path)
    diarization_result = speech_processor.diarize_audio(sample)

    # Функция для выделения и транскрибации сегментов по диаризации
    def transcribe_diarized_segments(speech_processor, sample, diarization_result):
        transcriptions = {}

        # Теперь метод itertracks возвращает три значения: segment, track и speaker
        for segment, _, speaker in diarization_result.itertracks(yield_label=True):
            start_time, end_time = segment.start, segment.end

            # Вырезаем нужный сегмент из общего аудиофайла
            segment_audio = {
                "audio": {
                    "array": sample["audio"]["array"][int(start_time * sample["audio"]["sampling_rate"]):int(end_time * sample["audio"]["sampling_rate"])],
                    "sampling_rate": sample["audio"]["sampling_rate"]
                }
            }

            # Транскрибация сегмента
            asr_result = speech_processor.transcribe_audio(segment_audio)
            transcriptions.update({ f"{start_time:.2f}, {end_time:.2f}": {
                'speaker': speaker,
                'text': asr_result['text']
                }
            })

        return transcriptions

    # Транскрибация каждого сегмента
    transcribed_segments = transcribe_diarized_segments(speech_processor, sample, diarization_result)
    return transcribed_segments
