// news-image-20261123 entry: copies the pre-drawn front page for Monday 23 November 2026
// (drawn by build.py beside this repo's source) to /output/entry.png. Node 22, standard library only.
import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
