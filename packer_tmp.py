import os
import traceback
import time
try:
    import cache_sum_code
except Exception as e:
	os.mkdir("logs")
	os.chdir("logs")
	with open("error-dump-"+time.strftime("%Y%m%d", time.localtime()),"w") as f:
		traceback.print_exc(file=f)
	print("\n\n"+"#"*20+"\n[BUG] 带上以下信息向作者反馈：\n"+"#"*20+"\n\n")
	traceback.print_exc()
