使用说明：

1. 请将本程序放置于独立文件夹下，并创建host文件，文件内容格式可参考
   `https://wiki.biligame.com/xxxx/api.php?`

2. 程序会自动扫描所在目录的全部文件夹上传文件，并在所在目录下生成日志文件，并自动添加编辑行为备注为"自动化编辑"。
   
3. 如果需要补充文件说明，可以在同级目录下创建`文件夹名.txt`，内容即为wikitext内容，此外可以用` %filename，%filetype，%category `来作为占位词，用于自动补充相关内容，例如：有aa/dd/cc.png，那么对于文本"{{Category:%category}}"上传说明时会变成"{{Category:dd}}"上传。

4. 本程序基于扫描Edge或者Chrome浏览器数据库进行登录（优先Edge），因此运行之前需要保证B站登录状态，且杀死所浏览器后台运行进程，比如可用```taskkill /F /IM msedge.exe```。