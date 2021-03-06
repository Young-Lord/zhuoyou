import sys
import os
import codecs
import time
file_list = ["items", "game_config", "functions", "inits", "core"]
# 注意：此列表中的每项不带扩展名(.py)



def addfile(path):
    global sum_code
    sum_code.write(
        '#'*15+"\r\n#     Code from {}:\r\n".format(path)+'#'*15+"\r\n")
    current_file = codecs.open(path+".py", "r", encoding='utf-8')
    sum_code.write(current_file.read().replace("\xef\xbb\xbf", ''))
    current_file.close()
    sum_code.write("\r\n\r\n")


sum_code = codecs.open("cache_sum_code.py", "w", encoding='utf-8')
sum_code.write("# 警告：本文件是在每次运行时自动生成的，修改此文件没有任何意义\r\n")

# generating characters
characters_file =["Player",]
filter_files=["tempCodeRunnerFile","Player"]
for i in os.listdir(os.path.join(os.getcwd(), "characters")):
    if i[-3:] == '.py' and (i.rstrip(".py") not in filter_files):
        characters_file.append(i.rstrip(".py"))

for i in characters_file:
    addfile("characters/"+i)

for i in file_list:
    addfile(i)

sum_code.close()

if "--genonly" in sys.argv:
    sys.exit()

try:
    from cache_sum_code import *
except Exception as e:
    import traceback
    os.mkdir("logs")
    os.chdir("logs")
    with open("error-dump-"+time.strftime("%Y%m%d", time.localtime())+".txt","w",encoding="utf-8") as f:
        traceback.print_exc(file=f)
    print("\n\n"+"#"*20+"\n[BUG] 带上以下信息向作者反馈：\n"+"#"*20+"\n\n")
    traceback.print_exc()
    os.system("pause")
