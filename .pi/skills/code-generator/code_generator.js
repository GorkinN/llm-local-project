"use strict";

const http = require("http");

const OLLAMA_HOST = "localhost";
const OLLAMA_PORT = 11434;
const TIMEOUT_MS = 120000;

const DEFAULT_MODEL = "qwen2.5-coder:14b-instruct";
const DEFAULT_SYSTEM =
  "You are a code generator. Output only code without explanations, " +
  "without markdown wrappers, and without introductions.";
const DEFAULT_TEMPERATURE = 0.2;
const DEFAULT_MAX_TOKENS = 8192;

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

function parseInput(raw) {
  const trimmed = (raw || "").trim();
  if (!trimmed) {
    throw new Error(
      "No input provided. Pass a JSON object as the first argument or via stdin.",
    );
  }
  try {
    return JSON.parse(trimmed);
  } catch (err) {
    throw new Error(`Invalid JSON input: ${err.message}`);
  }
}

function stripMarkdownFences(text) {
  if (!text) return "";
  const fenceRegex = /^```[a-zA-Z0-9_+-]*\s*\n([\s\S]*?)\n```\s*$/;
  const match = text.match(fenceRegex);
  if (match) return match[1];
  return text
    .replace(/^```[a-zA-Z0-9_+-]*\s*\n/, "")
    .replace(/\n```\s*$/, "")
    .trim();
}

function callOllama(payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload);
    const req = http.request(
      {
        host: OLLAMA_HOST,
        port: OLLAMA_PORT,
        path: "/api/generate",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
        timeout: TIMEOUT_MS,
      },
      (res) => {
        let data = "";
        res.setEncoding("utf8");
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode < 200 || res.statusCode >= 300) {
            return reject(
              new Error(
                `Ollama returned HTTP ${res.statusCode}: ${data.slice(0, 500)}`,
              ),
            );
          }
          try {
            resolve(JSON.parse(data));
          } catch (err) {
            reject(
              new Error(`Failed to parse Ollama response: ${err.message}`),
            );
          }
        });
      },
    );

    req.on("timeout", () => {
      req.destroy(new Error(`Request timed out after ${TIMEOUT_MS} ms`));
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  let input;
  try {
    const argInput = process.argv[2];
    const raw = argInput !== undefined ? argInput : await readStdin();
    input = parseInput(raw);
  } catch (err) {
    process.stdout.write(
      JSON.stringify({ success: false, error: err.message }),
    );
    process.exit(1);
  }

  const prompt = input.prompt;
  if (!prompt || typeof prompt !== "string") {
    process.stdout.write(
      JSON.stringify({
        success: false,
        error: "Field 'prompt' is required and must be a string.",
      }),
    );
    process.exit(1);
  }

  const model = input.model || DEFAULT_MODEL;
  const system = input.system || DEFAULT_SYSTEM;
  const temperature =
    typeof input.temperature === "number"
      ? input.temperature
      : DEFAULT_TEMPERATURE;
  const maxTokens =
    typeof input.max_tokens === "number"
      ? input.max_tokens
      : DEFAULT_MAX_TOKENS;

  const payload = {
    model,
    prompt: `${system}\n\n${prompt}`,
    stream: false,
    options: {
      temperature,
      num_predict: maxTokens,
    },
  };

  try {
    const response = await callOllama(payload);
    const rawCode = response.response || "";
    const code = stripMarkdownFences(rawCode);

    process.stdout.write(
      JSON.stringify({
        success: true,
        model,
        code,
        tokens_generated: response.eval_count || 0,
      }),
    );
  } catch (err) {
    process.stdout.write(
      JSON.stringify({ success: false, error: err.message }),
    );
    process.exit(1);
  }
}

main();
