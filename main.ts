import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entrypoint for gta6-meme-x-01: the house reads the X post itself from
// POST.json, so this program only copies that file to the output dir.
const root = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(root, "out");

mkdirSync(outDir, { recursive: true });
copyFileSync(join(root, "POST.json"), join(outDir, "POST.json"));
