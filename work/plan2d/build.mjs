import {build} from 'esbuild';
import {cp, mkdir, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
await build({entryPoints:['src/App.tsx'],bundle:true,minify:true,outfile:'dist/app.js',define:{'process.env.NODE_ENV':'"production"'}});
// GitHub Pages publishes main:/docs. Keep it synchronized on every build.
const pages = fileURLToPath(new URL('../../docs/', import.meta.url));
await mkdir(pages, {recursive: true});
await cp(fileURLToPath(new URL('./dist/', import.meta.url)), pages, {recursive: true});
await writeFile(new URL('../../docs/.nojekyll', import.meta.url), '');
