import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "youtube_transcript",
    label: "YouTube Transcript",
    description:
      "Fetch subtitles/transcript from YouTube video using the youtube-transcript skill",
    promptSnippet: "Get YouTube video transcript",
    promptGuidelines: [
      "Use youtube_transcript tool when user asks for subtitles or transcript of a YouTube video.",
    ],
    parameters: Type.Object({
      url: Type.String({ description: "YouTube video URL or video ID" }),
    }),
    async execute(_toolCallId, params, signal) {
      const { execFile } = await import("node:child_process");
      const { promisify } = await import("node:util");
      const execFileAsync = promisify(execFile);

      const skillDir = ".pi/skills/youtube-transcript";

      try {
        // Извлекаем ID из URL если нужно
        let videoId = params.url;
        if (
          params.url.includes("youtube.com") ||
          params.url.includes("youtu.be")
        ) {
          const match = params.url.match(
            /(?:v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/,
          );
          if (match) {
            videoId = match[1];
          }
        }

        // Запускаем скрипт через node с правильным путем
        const { stdout, stderr } = await execFileAsync(
          "node",
          [`${skillDir}/transcript.js`, videoId],
          {
            timeout: 60000,
            signal: signal || undefined,
            cwd: process.cwd(),
            windowsHide: true,
          },
        );

        if (stderr && stderr.trim()) {
          throw new Error(stderr.trim());
        }

        return {
          content: [{ type: "text", text: stdout }],
          details: { transcript: stdout },
        };
      } catch (error: any) {
        throw new Error(`Failed to fetch transcript: ${error.message}`);
      }
    },
  });
}
