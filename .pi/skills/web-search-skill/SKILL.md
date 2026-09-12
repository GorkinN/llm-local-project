---
name: web-search-skill
description: perform web searches and returns the main points of the search results. It uses DuckDuckGo API as primary source with Google as fallback.
disable-model-invocation: true
---

# Web Search Skill

Perform web searches and retrieve key information from search results.

## Setup

```bash
cd {baseDir}
npm install
```

## Usage

```bash
node web_search_skill.js <internet-query-text>
```

Accepts text query:

- `Greek gods`
- `information about chickens`
- `latest AI news`

## Output

Summarized result:

```
📌 Greek mythology is the body of myths originally told by the ancient Greeks...
• Zeus, the king of the gods
• Poseidon, the god of the sea
• Athena, the goddess of wisdom
• Apollo, the god of music and poetry
```

## Notes

- Uses DuckDuckGo API as primary search source
- Automatic fallback to Google Search if DuckDuckGo fails
- Returns maximum 5 most relevant results
- Supports queries in any language
- Handles network errors and timeouts gracefully
- Requires no API keys or authentication
