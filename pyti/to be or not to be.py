import random
letters = "qwertyuopasdfghjklizxcvbnm "
sentence = "to be or not to be"
not_found = True
k=0
kold=1
len_record=0
current=""
print("letter   order   probability    differ   ratio")
while not_found:
    len_current=0
    for i in range(len(sentence)):
        if letters[random.randint(0,len(letters)-1)] == sentence[i]:
            current += sentence[i]
            len_current+=1
        else:
            if len_current > len_record:
                len_record = len_current
                print(sentence[i],k,len(letters)**(i+1),len(letters)**(i+1)-k,"%.2f"%(k/kold))
                kold = k
            break
        if len_current==len(sentence)-1:
            not_found = False
    k+=1
