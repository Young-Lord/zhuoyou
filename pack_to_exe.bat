python main.py --genonly
echo import os >> packer_tmp.py
echo import traceback >> packer_tmp.py
echo try: >> packer_tmp.py
echo     from cache_sum_code import * >> packer_tmp.py
echo except Exception as e: >> packer_tmp.py
echo     print("\n\n"+"#"*20+"\n[BUG] 带上以下信息向作者反馈：\n"+"#"*20+"\n\n") >> packer_tmp.py
echo     traceback.print_exc() >> packer_tmp.py
echo     os.system("pause") >> packer_tmp.py
pyinstaller packer_tmp.py -F --distpath . --clean -n game.exe
del packer_tmp.py
rmdir build /S /Q
rmdir __pycache__ /S /Q
del game.exe.spec