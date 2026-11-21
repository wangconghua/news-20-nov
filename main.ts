// news-20-nov — entrypoint for make.fun bounty news-image-20261120.
// Copies the pre-rendered infographic (entry.png, 1024x1024) into the
// output directory the platform provides. No network, no randomness:
// the output is byte-identical on every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log("entry.png written to", join(outDir, "entry.png"));
