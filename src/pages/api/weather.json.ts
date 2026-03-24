import fs from "fs";
import path from "path";
import type { APIRoute } from "astro";

export const GET: APIRoute = async () => {
  try {
    // Use absolute path from project root
    const filePath = path.resolve(process.cwd(), 'src/public/weather.json');
    const json = fs.readFileSync(filePath, "utf-8");
    return new Response(json, {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-store"
      },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: "No weather data" }), {
      status: 404,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-store"
      },
    });
  }
};
