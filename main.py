import codecs
import os
import sys
current_file = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(current_dir)

sum_code = codecs.open("cache_sum_code.py", "w", encoding='utf-8')
sum_code.write("# 警告：本文件是在每次运行时自动生成的，修改此文件没有任何意义\r\n\r\n")

# generating characters
characters_file = [i for i in os.listdir(os.path.join(os.getcwd(), "characters")) if i[-3:] == '.py' and i!="tempCodeRunnerFile.py"]
characters=list()
for i in characters_file:
    with codecs.open("characters/"+i, "r", encoding='utf-8') as f:
        cont=f.read().replace("\xef\xbb\xbf", '')
        if cont.find("class") == -1:
            continue
        name_1=cont.find("class ")+6
        name_2=cont.find(":")
        characters.append(cont[name_1:name_2].replace("(Player)",""))

#print(characters)

for i in characters_file:
    sum_code.write("#@# Code from "+":\r\n\r\n")
    with codecs.open("characters/"+i, "r", encoding='utf-8') as f:
        sum_code.write(f.read().replace("\xef\xbb\xbf", ''))

# generating functions
sum_code.write("\r\n\r\n#@# functions:\r\n")
functions_file = codecs.open("functions.py", "r", encoding='utf-8')
sum_code.write(functions_file.read().replace("\xef\xbb\xbf", ''))
functions_file.close()
sum_code.write("\r\n\r\n")

# generating items
sum_code.write("\r\n\r\n#@# Items:\r\n")
item_file = codecs.open("items.py", "r", encoding='utf-8')
sum_code.write(item_file.read().replace("\xef\xbb\xbf", ''))
item_file.close()
sum_code.write("\r\n\r\n")

# generating game_config
sum_code.write("#@# Configs:\r\n")
config_file = codecs.open("game_config.py", "r", encoding='utf-8')
sum_code.write(config_file.read().replace("\xef\xbb\xbf", ''))
config_file.close()
sum_code.write("\r\n\r\n")

# generating core code
sum_code.write("#@# Core code:\r\n")
core_file = codecs.open("core.py", "r", encoding='utf-8')
sum_code.write(core_file.read().replace("\xef\xbb\xbf", ''))
core_file.close()
sum_code.write("\r\n\r\n")
sum_code.close()

try:
    from cache_sum_code import *
except Exception as e:
    print("\n\n#####\n[BUG] 带上以下信息向作者反馈：\n#####\n\n")
    raise e