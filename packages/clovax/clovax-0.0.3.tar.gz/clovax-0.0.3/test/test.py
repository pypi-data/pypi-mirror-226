from clovax import ClovaX

c = ClovaX()
c.get_cookie("cookies.txt")
log = c.start("Hello world!")
print(log)
