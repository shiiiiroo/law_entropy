# ЗаконоМетр (Law Entropy)

Проект для анализа противоречий в нормативно-правовых актах (НПА).

## Как запустить

1. Убедитесь, что у вас установлен Node.js.
2. Установите зависимости:
   ```bash
   npm install
   ```
3. Запустите UI сервер (Frontend):
   ```bash
   npm start
   ```

4. Для работы **Онлайн-поиска НПА** (Әділет, data.egov.kz) запустите Python-бэкенд. Откройте **новый** терминал и выполните:
   - В Windows:
     ```cmd
     cd backend
     run.bat
     ```
   - В Linux/MacOS:
     ```bash
     cd backend
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     uvicorn main:app --host 0.0.0.0 --port 8000
     ```

5. Откройте приложение в браузере: [http://localhost:3000](http://localhost:3000)

## Функции

- **Поиск противоречий**: Сравнение нескольких документов на предмет юридических коллизий.
- **Устаревшие нормы**: Поиск ссылок на утратившие силу акты.
- **Граф связей**: Визуализация зависимостей между документами с помощью D3.js.
- **Чат с документами**: Прямые вопросы к загруженным текстам.

## Поддерживаемые AI провайдеры

- Mock-режим (для демонстрации без API ключей)
- Google Gemini (1.5 Flash)
- Alem LLM (alem.ai)
- Anthropic Claude (3.5 Sonnet)
- OpenAI GPT-4o mini
