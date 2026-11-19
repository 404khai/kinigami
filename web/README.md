# Kinigami web

The project site: an overview and a blog of engineering notes on the decision log. React + Vite, no router dependency.

```sh
npm install
npm run dev      # regenerates src/generated/, then serves on :5173
npm run build    # regenerates, type-checks, builds to dist/
```

`scripts/generate.mjs` runs before every dev and build and writes `src/generated/` (git-ignored):

- `figures.ts`: the blog's isometric figures, drawn with the vendored [Anatomy](https://github.com/wheresryan22/anatomy) kit (`vendor/anatomy/`, MIT).
- `anatomy.css`: the kit's stylesheet.
- `records.ts`: the decision-log index (`../docs/decisions`) and the criteria register (`../criteria/REGISTER.md`), so the site never drifts from the records.

Posts live in `src/blog/posts.ts` as blocks. Each names the decision records it is written from; the post page lists them, and the record governs if the two disagree. Write numbers only as the records state them.

The look follows [cogs](https://github.com/404khai/cogs) (blueprint sheet, gears) and the blog layout follows [graft](https://github.com/404khai/graft/tree/main/web/src/blog).

Hosting: any static host that rewrites unknown paths to `/index.html` (`vercel.json` does this). Build from the repository root's `web/` directory; the generator reads `../docs` and `../criteria`.
