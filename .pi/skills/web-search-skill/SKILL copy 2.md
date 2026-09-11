---
name: web-search-skill
description: perform web searches and returns the main points of the search results. It uses DuckDuckGo API as primary source with Google as fallback.
---

# YouTube Transcript

Fetch transcripts from YouTube videos.

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

## Output

Summarized result:

```
📌 Greek mythology is the body of myths originally told by the ancient Greeks...
• Zeus, the king of the gods
• Poseidon, the god of the sea
• Athena, the goddess of wisdom
• Apollo, the god of music and poetry
```
