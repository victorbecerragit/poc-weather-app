
import { promises as fs } from "fs";
import path from "path";
import type { APIRoute } from "astro";

export const GET: APIRoute = async () => {
  try {
    // Use absolute path from project root to public/weather.json
    const filePath = path.resolve(process.cwd(), "public/weather.json");
    const json = await fs.readFile(filePath, "utf-8");
    return new Response(json, {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-store, must-revalidate"
      },
    });
  } catch (e) {
    console.error("Failed to read weather.json:", e);
    return new Response(JSON.stringify({ error: "Failed to load weather data" }), {
      status: 500,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-store, must-revalidate"
      },
    });
  }
};
