import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  // Уведомление при старте
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.notify("👋 Здарова сайпал!", "info");
  });

  // Команда /hi
  pi.registerCommand("hi", {
    description: "Say hi",
    handler: async (args, ctx) => {
      const name = args || "world";
      ctx.ui.notify(`Hi, ${name}!`, "info");
    },
  });
}
