"""src/ 파일들을 합쳐서 dist/index.html 한 파일로 만든다.
순서: data_core.js -> data_gen1.js ... data_gen9.js -> i18n.js -> stats.js -> items.js -> app.js -> items_app.js
사용법: python build.py"""
import glob, os, re
here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src")
gens = sorted(glob.glob(os.path.join(src, "data_gen*.js")), key=lambda p: int(re.search(r"gen(\d+)", p).group(1)))
parts = [os.path.join(src, "data_core.js"), *gens, os.path.join(src, "i18n.js"), os.path.join(src, "stats.js"), os.path.join(src, "items.js"), os.path.join(src, "app.js"), os.path.join(src, "items_app.js")]
js = "\n".join(open(p, encoding="utf-8").read() for p in parts)
shell = open(os.path.join(src, "shell.html"), encoding="utf-8").read()
os.makedirs(os.path.join(here, "dist"), exist_ok=True)
out = os.path.join(here, "dist", "index.html")
open(out, "w", encoding="utf-8").write(shell.replace("/*DATA*/", js))
print("built", out, "from", [os.path.basename(p) for p in parts])
