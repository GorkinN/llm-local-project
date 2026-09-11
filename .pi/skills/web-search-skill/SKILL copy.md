# Web Search Skill

## Description

This skill allows you to perform web searches and returns the main points of the search results. It uses DuckDuckGo API as primary source with Google as fallback.

## Features

- Interactive search with multiple queries
- Returns top 5 main points from search results
- Automatic fallback to Google if DuckDuckGo fails
- Support for Russian and English queries
- Error handling and network timeout protection
- Pure JavaScript with no external dependencies
- Uses native fetch API

## Usage

1. Run the script: `npm start` or `node web_search_skill.js`
2. Enter your search query when prompted.
3. The script will return the top 5 main points from the search results.
4. Enter 'exit' or 'выход' to quit the program.

## Example

```bash
$ node web_search_skill.js
============================================================
🔍 НАВЫК ВЕБ-ПОИСКА ДЛЯ PI.DEV
============================================================
Введите 'выход' или 'exit' для завершения

🔎 Введите запрос: Greek gods
🔍 Ищу: 'Greek gods'
------------------------------------------------------------
📌 Greek mythology is the body of myths originally told by the ancient Greeks...
• Zeus, the king of the gods
• Poseidon, the god of the sea
• Athena, the goddess of wisdom
• Apollo, the god of music and poetry
------------------------------------------------------------
```
