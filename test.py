t="20221230330"
p="1230"
answer=1
li=[]
for i in range(len(t)):
    a=t[i:len(p)+i]
    if len(a)==len(p):
        if int(a)<=int(p):
            li.append(a)
print(li)