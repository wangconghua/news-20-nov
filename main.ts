// news-20-nov — make.fun entry for news-image-20261120.
// The entry is a pre-rendered infographic (entry.png, 1024x1024).
// This script just drops that image into the output directory the
// platform hands us. Deterministic: same bytes out on every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log("entry.png written to", join(outDir, "entry.png"));
