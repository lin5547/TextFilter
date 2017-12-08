import codecs

f = codecs.open("/home/lin/HS-works/gitlab/new_project/chatpair_fixed_test.txt",mode='r',encoding='utf-8')

sentences = f.readlines()

f.close()

chatpairs = []
temp=[]
for line in sentences:
    line = line.strip('\n').strip('\r')
    if line!='':
        temp.append(line)
    else:
        chatpairs.append(temp)
        temp=[]

case = 0
f = codecs.open("/home/lin/HS-works/gitlab/new_project/data/"+str(case)+'.txt',mode='w',encoding='utf-8')

for i in range(len(chatpairs)):
    if (i+1)%2500==0:
        f.close()
        case+=1
        f = codecs.open("/home/lin/HS-works/gitlab/new_project/data/" +str(case) + '.txt', mode='w', encoding='utf-8')
    else:
        for line in chatpairs[i]:
            f.write(line+'\n')
        f.write('\n')
f.close()
