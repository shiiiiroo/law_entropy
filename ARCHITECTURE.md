# Архитектура решения: ЗаконоМетр (Law Entropy)

Данный документ описывает высокоуровневую архитектуру прототипа системы анализа нормативно-правовых актов. 

## Общая схема архитектуры (High-Level Architecture)

Система базируется на микросервисной интеграции и разделена на клиентскую часть (Frontend), прокси-сервер (Node.js) и аналитический парсер-бэкенд (Python/FastAPI).

```mermaid
graph TD
    %% Компоненты
    User((Пользователь))
    UI[Frontend: Vanilla JS, HTML5, CSS]
    Proxy[Node.js Proxy Express]
    LLM_API((LLM Сервисы<br>Gemini, AlemLLM, OpenAI))
    Python_Backend[Python FastAPI Backend]
    
    %% Источники данных
    Adilet[(Adilet.zan.kz<br>Parser)]
    EGov[(data.egov.kz<br>API Open Data)]

    %% Взаимодействия
    User -->|Взаимодействие с UI,<br>поиск и загрузка НПА| UI
    
    UI -->|Отправка текстов<br>на анализ| Proxy
    Proxy -->|API запросы| LLM_API
    LLM_API -->|Возврат найденных<br>противоречий| Proxy
    Proxy -->|Отображение результатов| UI
    
    UI -->|Запрос поиска НПА<br>/api/search| Python_Backend
    UI -->|Запрос полного текста<br>/api/extract| Python_Backend
    
    Python_Backend -->|Web Scraping| Adilet
    Python_Backend -->|REST API v4| EGov
    
    Adilet -->|Возврат НПА| Python_Backend
    EGov -->|Возврат Датасетов| Python_Backend
    
    classDef frontend fill:#1e2d3d,stroke:#00d4ff,stroke-width:2px,color:#e8f4ff;
    classDef backend fill:#111820,stroke:#3ddc84,stroke-width:2px,color:#e8f4ff;
    classDef external fill:#1e2d3d,stroke:#f5a623,stroke-width:2px,color:#e8f4ff,shape:cylinder;
    
    class UI frontend;
    class Proxy,Python_Backend backend;
    class Adilet,EGov,LLM_API external;
```

## Описание компонентов

### 1. Client-Side (Frontend UI)
- **Стек:** HTML5, CSS (переменные, Grid/Flexbox), Vanilla JS.
- **Модули:**
  - `File Handler`: Обработка PDF/DOCX (библиотеки PDF.js, Mammoth.js).
  - `Interactive Graph`: Визуализация графа зависимостей НПА с помощью D3.js.
  - `Parsers Integration`: Прямая связь с Python бэкендом для поиска реальных правовых актов онлайн.

### 2. Node.js Proxy Server
- **Стек:** Node.js, Express, Axios.
- **Роль:** Решает проблемы CORS при обращении к внешним LLM провайдерам, выступает как легковесный шлюз между клиентом и нейросетями. Запускает статику приложения.

### 3. Data Extraction Layer (Python FastAPI Backend)
- **Стек:** Python 3, FastAPI, Uvicorn, BeautifulSoup4.
- **Роль:** Извлечение «сырых» юридических документов из открытых государственных баз для пополнения контекста RAG (Retrieval-Augmented Generation).
- **Подмодули:**
  - `adilet_parser.py`: Эмулирует поисковые GET-запросы к базе `adilet.zan.kz`, парсит HTML ветки и извлекает чистый очищенный нормативный текст. Отключена проверка SSL (GOST) для стабильного парсинга.
  - `egov_parser.py`: Интегрируется с API Открытых данных `data.egov.kz`, преобразуя сложные JSON структуры в текстовый формат.

### 4. LLM & RAG Engine (Внешние провайдеры)
- **Стек:** REST API (Google Gemini, AlemLLM, DeepSeek, OpenAI).
- **Роль:** Получив извлеченные тексты НПА, нейросеть (LLM) анализирует их на предмет юридических коллизий, дублирования и устаревших ссылок. Вердикты возвращаются в строгом JSON-формате для отображения в UI.

## Поток данных (Data Flow)
1. Пользователь вводит ключевое слово в боковой панели UI.
2. Интерфейс опрашивает **Python FastAPI Backend**.
3. Python-бэкенд делает параллельные запросы в **Әділет** и **eGov**, собирает ссылки и отдает список в UI.
4. Пользователь выбирает конкретный документ. Бэкенд выкачивает полный текст, очищает от HTML/скриптов и передает на клиентскую часть.
5. Интерфейс упаковывает текст в специализированный промпт (Prompt Engineering) и через **Node.js Proxy** отправляет в выбранную **LLM**.
6. Нейросеть отвечает списком противоречий, которые динамически отображаются на экране пользователя в виде карточек и графа.
