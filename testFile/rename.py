import os
from os import rename


dir_url = 'C:\\Users\\sanny\\Desktop\\female_40'
files = os.listdir(dir_url)
i = 1

for f in files:
    print(f)
    rename(dir_url+'\\'+f, dir_url+'\\'+'female40_'+str(i)+'.jpg')
    i += 1