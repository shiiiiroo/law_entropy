# Архитектура решения: Law Entropy

Данный документ описывает высокоуровневую архитектуру системы анализа нормативно-правовых актов (НПА) Республики Казахстан.

## Общая схема архитектуры (High-Level Architecture)

Система базируется на микросервисной интеграции и разделена на клиентскую часть (Frontend SPA), прокси-сервер (Node.js) и аналитический парсер-бэкенд (Python/FastAPI).

```mermaid
graph TD
    %% Компоненты
    User((Пользователь))
    UI[Frontend SPA: Vanilla JS, HTML5, CSS]
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

## Структура репозитория

```text
.
├── backend/                # Сердце системы (Python/FastAPI)
│   ├── main.py             # Точка входа в API (FastAPI)
│   ├── parsers/            # Логика скрейпинга и парсинга
│   │   ├── adilet_parser.py # Парсер портала adilet.zan.kz
│   │   └── egov_parser.py   # Парсер открытых данных eGov
│   ├── Dockerfile          # Сборка бэкенда
│   └── requirements.txt    # Зависимости Python
├── tests/                  # Автоматизированные тесты (Playwright)
├── legal-entropy.html      # Фронтенд (Single Page Application)
├── server.js               # Прокси-сервер и статика (Node.js/Express)
├── package.json            # Зависимости Node.js
├── Dockerfile              # Сборка фронтенд-прокси
├── docker-compose.yml      # Оркестрация контейнеров
└── README.md               # Общее описание проекта
```

## Описание компонентов

### 1. Client-Side (Frontend SPA)
- **Стек:** HTML5, CSS (Grid/Flexbox), Vanilla JS.
- **Модули:**
  - `File Handler`: Обработка PDF/DOCX (библиотеки PDF.js, Mammoth.js).
  - `Interactive Graph`: Визуализация графа зависимостей НПА с помощью D3.js.
  - `Parsers Integration`: Связь с Python бэкендом для поиска правовых актов в реальном времени.

### 2. Node.js Proxy Server
- **Стек:** Node.js, Express, Axios.
- **Роль:** Решает проблемы CORS при обращении к внешним LLM провайдерам, выступает как шлюз безопасности и сервер статики.

### 3. Data Extraction Layer (Python FastAPI Backend)
- **Стек:** Python 3.11, FastAPI, BeautifulSoup4.
- **Роль:** Извлечение и очистка юридических документов из открытых государственных баз (Adilet, eGov) для пополнения контекста LLM.

### 4. LLM Engine (Внешние провайдеры)
- **Стек:** REST API (Google Gemini, AlemLLM, DeepSeek, OpenAI, Anthropic).
- **Роль:** Анализ текстов НПА на предмет коллизий, дублирования и устаревших ссылок.

## Потоки данных (Data Flow)

1.  **Запрос:** Пользователь вводит запрос в `legal-entropy.html`.
2.  **Поиск:** Фронтенд отправляет запрос на `backend/main.py` (FastAPI).
3.  **Сбор:** FastAPI запускает поиск через `AdiletParser` и `EGovParser`.
4.  **Анализ:** После выбора документа текст отправляется через **Node.js Proxy** в выбранную **LLM**.
5.  **Результат:** Нейросеть возвращает структурированный JSON с найденными противоречиями для визуализации.
