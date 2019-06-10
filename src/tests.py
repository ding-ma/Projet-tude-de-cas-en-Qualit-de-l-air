import os

gifs = os.listdir("output")
newlst = []
for g in gifs:
    if g.endswith(".gif"):
        newlst.append(g)
print(newlst)

os.system("animate output/"+newlst[2])