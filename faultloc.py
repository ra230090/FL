import os,subprocess,time,sys
#需要檔案或資訊：usercode,problemID,problemInput,problemOutput
#file_name=input() #usercode
#file_ID=10400
#file_ID=input()
file_name=sys.argv[1]
file_ID=int(sys.argv[2]) #problemID
timelimit=5
totalline = 0
D=1
Nus=[0]
Ncs=[0]
Nuf=[0]
Ncf=[0]
result=[0]
resultt=[0]
resulttt=[0]
wrong_answer=[]
f = open('./ucodes/'+ file_name, 'r')
while True :
    line = f.readline()
    if line=='': break
    totalline+=1
    Nus.append(0)
    Ncs.append(0)
    Nuf.append(0)
    Ncf.append(0)
    result.append(0)
    resultt.append(0)
    resulttt.append(0)
f.close()

name=os.path.splitext(file_name)
path=os.getcwd()
os.system('mkdir ufiles')
os.chdir(path+'/ufiles')
os.system('mkdir %s'%name[0])
os.system('cp -p ../ucodes/%s %s'%(file_name,name[0]))
os.chdir(os.getcwd()+'/'+name[0])

#print('開始跑user code...')
for i in range(1,7):
    ###
    ###  STEP 1 跑USER的CODE並用GCOV指令來產生GCOV檔
    ###
    #compile with gcov
    if name[1]=='.c':os.system('gcc -fprofile-arcs -ftest-coverage %s %s/mystart.c -o %s\n'%(file_name,path,name[0]))
    elif name[1]=='.cpp':os.system('g++ -fprofile-arcs -ftest-coverage %s -o %s\n'%(file_name,name[0]))
    elif name[1]=='.java':print('not support yet\n')
    else :
        print('not c|cpp|java file\n')
        break
    p = subprocess.Popen('./%s'%(name[0]), stdin = subprocess.PIPE, 
            stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    #get input
    f = open('%s/problemIO/%d/%d_input%d.txt'%(path,file_ID,file_ID,i), 'r')
    data = f.read()
    f.close()
    #feed the input
    #p.stdin.write(data.encode('utf-8'))
    #p.stdin.close()
    time_out=0
    try:
        s = p.communicate(input =data.encode('utf-8'),timeout = timelimit)
    except:
        time_out=1
        print(p.pid)
        print('user time out')
        #print(s[0])
        wrong_answer.append('t%d'%i)
        f = open('%d_useroutput%d.txt'%(file_ID,i), 'w')
        f.write('user time out')
        f.close()
        
        #if name[1]=='.c':p.send_signal('SIGUSR1')
        if name[1]=='.c':
            os.system("bash -c 'kill -s SIGUSR1 %i'" %p.pid)
            #p.kill()
            os.system('kill %i' %p.pid)
        else:
            continue
    #驗證結果(correct/wrong)
    if time_out ==0:
        f = open('%d_useroutput%d.txt'%(file_ID,i), 'w')
        f.write(s[0].decode('utf-8','ignore'))
        f.close()
    #cmd gcov
    os.system('gcov %s\n'%(file_name))
    ###
    ###  STEP 2 記下.gcov內容稍後來分析哪一行最可能錯
    ###
    os.system('diff %d_useroutput%d.txt %s/problemIO/%d/%d_output%d.txt >output_same%d.txt'%(file_ID,i,path,file_ID,file_ID,i,i))
    os.system('diff -w -B %d_useroutput%d.txt %s/problemIO/%d/%d_output%d.txt >output_same_ignore%d.txt'%(file_ID,i,path,file_ID,file_ID,i,i))
    f = open('output_same%d.txt'%i, 'r')
    line=f.read()
    f.close()
    f = open('output_same_ignore%d.txt'%i, 'r')
    line_g=f.read()
    f.close()
    output_same=0
    #if answer==data: output_same=1
    if line=='':output_same=1
    else:
        if line_g=='':
            print('presentation error\n')
            wrong_answer.append('p%d'%i)
            continue
    file_gcov=file_name+'.gcov'
    f = open(file_gcov, 'r')
    if output_same==1:
        for line in f:
            LOC=line.split(':')
            if int(LOC[1])==0:continue
            if line.find('-:')==-1 and line.find('#:')==-1:
                #correct and pass
                Ncs[int(LOC[1])]+=int(LOC[0])
            else:
                #correct not pass
                Nus[int(LOC[1])]+=1        
    else:
        if time_out==0:wrong_answer.append('w%d'%i)
        for line in f:
            LOC=line.split(':')
            if int(LOC[1])==0:continue
            if line.find('-:')==-1 and line.find('#:')==-1:
                #wrong and pass
                Ncf[int(LOC[1])]+=int(LOC[0])
            else:
                #wrong not pass
                Nuf[int(LOC[1])]+=1
        os.system('lcov -c -o converge%d.info -d .'%i)
        os.system('genhtml converge%d.info -o w%d'%(i,i))
    f.close()
###
###  STEP 4 分析 (  (Ncf)*D/(Ncs+Nuf)  )
###  correct-0:Nus #correct-1:Ncs #wrong-0:Nuf #wrong-1:Ncf
i=0
for i in range(0,totalline):
    if Ncf[i]==0: continue
    elif (Ncs[i]+Nuf[i] == 0): 
        result[i]=4294967296
        resultt[i]=4294967296
        resulttt[i]=4294967296
    else : 
        result[i] = round((Ncf[i])*D/(Ncs[i]+Nuf[i]),3)
        resultt[i] = round((Ncf[i])*(Ncf[i])/(Ncs[i]+Nuf[i]),3)
        resulttt[i] = round((Ncf[i])*(Ncf[i])*(Ncf[i])/(Ncs[i]+Nuf[i]),3)
m=[]
m=m+result
mm=[]
mm=mm+resultt
mmm=[]
mmm=mmm+resulttt
m.sort()
mm.sort()
mmm.sort()
#print('result\n',result)
#print('sort\n',m)
possible_txt = open('fault.txt', 'w')
if not wrong_answer:
    possible_txt.write('correct')
else:
    for i in wrong_answer:
        possible_txt.write('%s\n'%i)
possible_txt.write('D1:\n')
i=10
while i!=0:
    if m[i-11]==0: break
    j=result.index(m[i-11])
    possible_txt.write('possible line:%d\n'%j)
    result[j]=0
    i-=1
possible_txt.write('D2:\n')
i=10
while i!=0:
    if mm[i-11]==0: break
    j=resultt.index(mm[i-11])
    possible_txt.write('possible line:%d\n'%j)
    resultt[j]=0
    i-=1
possible_txt.write('D3:\n')
i=10
while i!=0:
    if mmm[i-11]==0: break
    j=resulttt.index(mmm[i-11])
    possible_txt.write('possible line:%d\n'%j)
    resulttt[j]=0
    i-=1
possible_txt.close()
