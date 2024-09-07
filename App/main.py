import uvicorn
from fastapi import FastAPI
from Api.handlers.handlers import handlers

description = """
#### 1. Наш ИИ-секретарь автоматизирует создание протоколов совещаний, преобразуя аудиозаписи в текст, выделяя ключевые моменты и задачи, а также распределяя их между участниками с интеграцией в таск-трекер. Он формирует итоговые документы, что значительно ускоряет обработку данных совещаний и снижает вероятность ошибок или утечек информации, характерных для аналогичных решений

#### 2. Локально развернутые модели: Whisper (транскрибация), Diarization Speaker (диаризация), T-Lite (суммаризация).  Взаимодействие по API: YandexGPT (суммаризация), GigaChat (иные запросы) и EvaProjects (таск-трекинг)

#### 3. Решение минимизирует человеческое участие, интегрируется с таск трекером EvaProject (входит в реестр российского ПО), работает через user-friendly Telegram бота и использует несколько доступных LLM для высокоточной обработки аудио совещаний с помощью моделей, выбранных на основе сравнения экономической и технической эффективности доступных вариантов
"""

app = FastAPI(
    title="API endpoints for the AI-assistant",
    description=description,
    summary="API эндпоинты ИИ-секретаря для внутренних совещаний",
    contact={
        "name": "REU DS CLUB and BSP AI VISION"
    })
app.include_router(handlers)


def start():
    uvicorn.run(app='main:app',
                host="0.0.0.0",
                port=8000,
                workers=4,
                env_file='.env'
                )


if __name__ == '__main__':
    start()
