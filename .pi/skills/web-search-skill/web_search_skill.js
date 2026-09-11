const readline = require("readline");

/**
 * Функция для вычисления экспоненциальной задержки между попытками
 * @param {number} attempt - Номер попытки (начиная с 1)
 * @param {number} minDelay - Минимальная задержка в мс
 * @param {number} maxDelay - Максимальная задержка в мс
 * @param {number} multiplier - Множитель для расчета экспоненциальной задержки
 * @returns {number} Задержка в миллисекундах
 */
function getRetryDelay(attempt, minDelay = 1000, maxDelay = 300000, multiplier = 2) {
  const delay = Math.min(minDelay * (multiplier ** (attempt - 1)), maxDelay);
  return delay;
}

/**
 * Логгер для вывода сообщений в консоль и файл логов
 */
class Logger {
  constructor(logFilePath = `.pi/skills/web-search-skill/search.log`) {
    this.logFilePath = logFilePath;
  }

  /**
   * Логирует сообщение
   * @param {string} message - Сообщение для логирования
   */
  info(message) {
    console.log(`[${new Date().toISOString()}] 🟢 ${message}`);
    try {
      const timestamp = new Date().toISOString();
      const logEntry = `${timestamp} [INFO] ${message}\n`;
      require("fs").appendFileSync(this.logFilePath, logEntry);
    } catch (error) {
      console.error(`Не удалось записать лог: ${error.message}`);
    }
  }

  /**
   * Логирует ошибку
   * @param {string} message - Сообщение об ошибке
   */
  error(message) {
    console.error(`[${new Date().toISOString()}] 🔴 ${message}`);
    try {
      const timestamp = new Date().toISOString();
      const logEntry = `${timestamp} [ERROR] ${message}\n`;
      require("fs").appendFileSync(this.logFilePath, logEntry);
    } catch (error) {
      console.error(`Не удалось записать лог: ${error.message}`);
    }
  }

  /**
   * Логирует предупреждение
   * @param {string} message - Сообщение о предупреждении
   */
  warn(message) {
    console.warn(`[${new Date().toISOString()}] 🟡 ${message}`);
    try {
      const timestamp = new Date().toISOString();
      const logEntry = `${timestamp} [WARN] ${message}\n`;
      require("fs").appendFileSync(this.logFilePath, logEntry);
    } catch (error) {
      console.error(`Не удалось записать лог: ${error.message}`);
    }
  }
}

// Экранный экземпляр логгера
const logger = new Logger();

/**
 * Навык веб-поиска для pi.dev
 */
class WebSearchSkill {
  constructor(options = {}) {
    this.baseUrl = "https://api.duckduckgo.com/";
    this.maxResults = options.maxResults || 5;
    
    // Настройки retry
    this.maxRetries = options.maxRetries || 3;
    this.minRetryDelay = options.minRetryDelay || 1000; // минимальная задержка в мс
    this.maxRetryDelay = options.maxRetryDelay || 300000; // максимальная задержка в мс
    this.retryMultiplier = options.retryMultiplier || 2;
  }

  /**
   * Выполняет поиск с повторными попытками при ошибках сети
   * @param {string} query - Поисковый запрос
   * @returns {Promise<string>} Промис с результатами поиска или ошибок
   */
  async handleRetry(query, attempt = 0) {
    const delay = getRetryDelay(attempt, this.minRetryDelay, this.maxRetryDelay, this.retryMultiplier);
    
    if (attempt >= this.maxRetries) {
      logger.error(`Max retries (${this.maxRetries}) reached for query: ${query}`);
      return `Ошибка поиска после всех повторных попыток: ${error.message || 'Неизвестная ошибка'}`;
    }

    logger.warn(`Повторная попытка #${attempt + 1} для запроса: ${query}`);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    return this.search(query).catch(error => this.handleRetry(query, attempt + 1));
  }

  /**
   * Выполняет поиск и возвращает основные результаты
   * @param {string} query - Поисковый запрос
   * @returns {Promise<string>} Промис с результатами поиска
   */
  async search(query) {
  async search(query) {
    logger.info(`Выполнение поиска: ${query}`);

    try {
      // Параметры запроса к DuckDuckGo API
      const params = new URLSearchParams({
        q: query,
        format: "json",
        no_html: "1",
        skip_disambig: "1",
      });

      const response = await fetch(`${this.baseUrl}?${params}`, {
        signal: AbortSignal.timeout(10000),
      });

      // Обработка ошибок HTTP кодов
      const errorMessages = {
        408: "Запрос истёк (Gateway Timeout)",
        429: "Слишком много запросов (Too Many Requests)",
        502: "Плохая шлюз (Bad Gateway)",
        503: "Услуга временно недоступна (Service Unavailable)",
        504: "Таймаут шлюза (Gateway Timeout)",
      };

      if (!response.ok) {
        const errorMessage = errorMessages[response.status] || `HTTP ${response.status}`;
        logger.warn(`Ошибка запроса ${response.status}: ${errorMessage}`);
        
        // Для временных ошибок 5xx и статусов API делаем повторную попытку
        if ([408, 429, 502, 503, 504].includes(response.status)) {
          return await this.handleRetry(query);
        }
      }

      if (response.ok) {
        const data = await response.json();
        let results = [];

        // Извлекаем Abstract (краткое описание)
        if (data.AbstractText) {
          results.push(`📌 ${data.AbstractText}`);
        }

        // Извлекаем RelatedTopics
        const topics = data.RelatedTopics || [];
        for (const topic of topics.slice(0, this.maxResults)) {
          if (topic.Text) {
            results.push(`• ${topic.Text}`);
          } else if (topic.Topics) {
            for (const subtopic of topic.Topics.slice(0, 2)) {
              if (subtopic.Text) {
                results.push(`• ${subtopic.Text}`);
              }
            }
          }
        }

        // Извлекаем Answer (прямой ответ)
        if (data.Answer) {
          results.push(`✅ Ответ: ${data.Answer}`);
        }

        // Если есть результаты, возвращаем их
        if (results.length > 0) {
          return results.slice(0, this.maxResults).join("\n");
        } else {
          return await this.googleFallback(query);
        }
      } else {
        return await this.googleFallback(query);
      }
    } catch (error) {
      return await this.googleFallback(query);
    }
  }

  /**
   * Запасной вариант с использованием Google
   * @param {string} query - Поисковый запрос
   * @returns {Promise<string>} Промис с результатами поиска
   */
  async googleFallback(query) {
    try {
      const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
      const headers = {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      };

      const response = await fetch(url, {
        headers,
        signal: AbortSignal.timeout(10000),
      });

      if (response.ok) {
        const html = await response.text();

        // Простой парсер HTML без внешних библиотек
        const text = this.stripHtml(html);
        const lines = text
          .split("\n")
          .map((line) => line.trim())
          .filter((line) => line.length > 0);

        // Фильтруем и возвращаем первые 5 значимых строк
        const results = [];
        const excludedPrefixes = [
          "©",
          "Help",
          "Send feedback",
          "Privacy",
          "Terms",
        ];

        for (const line of lines) {
          if (
            line.length > 10 &&
            !excludedPrefixes.some((prefix) => line.startsWith(prefix))
          ) {
            results.push(`• ${line}`);
          }
          if (results.length >= 5) {
            break;
          }
        }

        return results.length > 0
          ? results.join("\n")
          : "Не удалось найти результаты.";
      } else {
        return `Ошибка при выполнении поиска. Код: ${response.status}`;
      }
    } catch (error) {
      return `Ошибка поиска: ${error.message || "Неизвестная ошибка"}`;
    }
  }

  /**
   * Удаляет HTML теги из текста
   * @param {string} html - HTML строка
   * @returns {string} Очищенный текст
   */
  stripHtml(html) {
    // Удаляем скрипты и стили
    let text = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, " ");
    text = text.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, " ");

    // Удаляем HTML теги
    text = text.replace(/<[^>]+>/g, " ");

    // Заменяем HTML entities
    text = text
      .replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&nbsp;/g, " ");

    // Заменяем множественные пробелы на один
    text = text.replace(/\s+/g, " ");

    return text.trim();
  }

  /**
   * Выполняет однократный поиск и выводит результат
   * @param {string} query - Поисковый запрос
   */
  async searchOnce(query) {
    console.log(`🔍 Ищу: '${query}'`);
    console.log("-".repeat(60));

    const result = await this.search(query);
    console.log(result);

    console.log("-".repeat(60));
  }

  /**
   * Запускает интерактивный режим
   */
  async startInteractive() {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    console.log("=".repeat(60));
    console.log("🔍 НАВЫК ВЕБ-ПОИСКА ДЛЯ PI.DEV");
    console.log("=".repeat(60));
    console.log("Введите 'выход' или 'exit' для завершения\n");

    while (true) {
      try {
        const query = await new Promise((resolve) => {
          rl.question("🔎 Введите запрос: ", resolve);
        });

        const trimmedQuery = query.trim();

        if (
          ["выход", "exit", "quit", "q"].includes(trimmedQuery.toLowerCase())
        ) {
          console.log("\n👋 До свидания!");
          break;
        }

        if (!trimmedQuery) {
          console.log("⚠️ Пожалуйста, введите запрос.\n");
          continue;
        }

        console.log(`\n🔍 Ищу: '${trimmedQuery}'`);
        console.log("-".repeat(60));

        const result = await this.search(trimmedQuery);
        console.log(result);

        console.log("-".repeat(60));
        console.log();
      } catch (error) {
        console.log(`❌ Ошибка: ${error.message || "Неизвестная ошибка"}\n`);
      }
    }

    rl.close();
  }
}

/**
 * Главная функция
 */
async function main() {
  const skill = new WebSearchSkill();

  // Получаем аргументы командной строки
  const args = process.argv.slice(2);

  if (args.length > 0) {
    // Режим однократного поиска с аргументами
    const query = args.join(" ");
    await skill.searchOnce(query);
  } else {
    // Интерактивный режим без аргументов
    await skill.startInteractive();
  }
}

// Обработка Ctrl+C
process.on("SIGINT", () => {
  console.log("\n\n👋 Программа прервана.");
  process.exit(0);
});

// Запуск программы
if (require.main === module) {
  main().catch((error) => {
    console.error("Критическая ошибка:", error);
    process.exit(1);
  });
}

module.exports = WebSearchSkill;
