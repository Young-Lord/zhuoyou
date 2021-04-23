import sys
import os
import codecs
file_list = ["items", "game_config", "functions", "inits", "core"]
# 注意：此列表中的每项不带扩展名(.py)

current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)


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
characters_file = [i.replace(".py", "") for i in os.listdir(os.path.join(
    os.getcwd(), "characters")) if i[-3:] == '.py' and i != "tempCodeRunnerFile.py"]

for i in characters_file:
    addfile("characters/"+i)

for i in file_list:
    addfile(i)

sum_code.close()

try:
    from cache_sum_code import *
except Exception as e:
    import traceback
    print("\n\n"+"#"*20+"\n[BUG] 带上以下信息向作者反馈：\n"+"#"*20+"\n\n")
    traceback.print_exc()
    os.system("pause")
