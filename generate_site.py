#!/usr/bin/env python3
import os, html
from pathlib import Path

STRIDE = ["Spoofing","Tampering","Repudiation","Information Disclosure","Denial of Service","Elevation of Privilege"]
repo = Path("known-cyber-attacks")
outdir = Path("site_output")
outdir.mkdir(exist_ok=True)

files = sorted(repo.rglob("*.md")) if repo.exists() else []
attacks = []
for f in files:
    txt = f.read_text(encoding="utf-8", errors="ignore")
    title = (f.parent.name if f.name.lower()=="readme.md" else f.stem)
    cats = [c for c in STRIDE if c.lower() in txt.lower()]
    if not cats:
        cats = ["Uncategorized"]
    slug = (title + "-" + f.name).strip().lower().replace(" ", "-")
    attacks.append({"title": title, "cats": cats, "slug": slug, "raw": txt})

groups = {c: [] for c in STRIDE}
groups["Uncategorized"] = []
for a in attacks:
    placed = False
    for c in STRIDE:
        if c in a["cats"]:
            groups[c].append(a); placed = True
    if not placed:
        groups["Uncategorized"].append(a)

htmlp = []
htmlp.append("<!doctype html><html><head><meta charset='utf-8'><title>Attacks - STRIDE</title></head><body>")
htmlp.append("<nav><strong>STRIDE:</strong> " + " | ".join(f"<a href='#{c.replace(' ','_')}'>{c}</a>" for c in STRIDE+['Uncategorized']) + "</nav>")

for c in STRIDE+["Uncategorized"]:
    htmlp.append(f"<section id='{c.replace(' ','_')}'><h2>{c}</h2><ul>")
    items = groups.get(c,[])
    if not items:
        htmlp.append("<li><em>No attacks</em></li>")
    else:
        for it in items:
            htmlp.append(f"<li><a href='#{it['slug']}'>{html.escape(it['title'])}</a></li>")
    htmlp.append("</ul></section>")

htmlp.append("<hr><h2>Details</h2>")
for a in attacks:
    htmlp.append(f"<article id='{a['slug']}'><h3>{html.escape(a['title'])}</h3>")
    htmlp.append(f"<p><strong>Categories:</strong> {html.escape(', '.join(a['cats']))}</p>")
    htmlp.append("<pre>" + html.escape(a['raw']) + "</pre>")
    htmlp.append("</article>")

htmlp.append("</body></html>")
(outdir / "index.html").write_text("\n".join(htmlp), encoding="utf-8")
print("HTML page created:", outdir / "index.html")
