import uvicorn
from fastapi import FastAPI
from Api.handlers.handlers import handlers

description = """
##### 1. Наш ИИ-секретарь с упором на безопасность автоматизирует создание протоколов совещаний, выделяя ключевые моменты и задачи, а также распределяя их между участниками с интеграцией в таск-трекере

##### 2. Локально развернутые модели: Whisper, Diarization Speaker, T-Lite. Взаимодействие по API: YandexGPT, GigaChat и EvaProjects

##### 3. Решение интегрируется с таск трекером EvaProject; используется модель LLM, выбранная на основе сравнения экономичской эффективности доступных вариантов; используются регулярные выражения для фильтрации галюцинаций; предлагаем идею шифрования конфиденциальных данных при передаче на сторонние сервисы
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
