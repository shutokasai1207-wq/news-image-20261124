// The World in One Page — make.fun news-image-20261124 entry.
//
// Copies the pre-rendered front page (entry.png, 1024x1024) to the
// output directory. Node 22, standard library only, no network.
// Running this twice produces byte-identical output.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR
  ? resolve(process.env.MAKEFUN_OUTPUT_DIR)
  : "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts: ${source}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// A plain copy is byte-identical by construction; report the size so a
// caller can confirm the output matches the bundled entry.png.
const bytes = statSync(target).size;
console.log(`wrote ${target} (${bytes} bytes)`);
