from clovax import ClovaX
import json

c = ClovaX()
c.get_cookie("cookies.txt")
log = c.start("Hello world!")
with open("log.json", "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=4)
