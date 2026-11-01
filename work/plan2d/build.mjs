import {build} from 'esbuild';
await build({entryPoints:['src/App.tsx'],bundle:true,minify:true,outfile:'dist/app.js',define:{'process.env.NODE_ENV':'"production"'}});
