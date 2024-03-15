使用说明：

2. 请将本程序放置于独立文件夹下，并创建host文件，文件内容格式可参考
   https://wiki.biligame.com/xxxx/api.php?

2. 程序会自动扫描所在目录的全部文件夹上传文件，并在所在目录下生成日志文件，并自动添加编辑行为备注为"自动化编辑"。
   
3. 如果需要补充文件说明，可以在同级目录下创建文件夹名.txt，内容即为wikitext内容，此外可以用 %filename，%filetype，%category来作为占位词，用于自动补充相关内容，例如：有aa/dd/cc.png，那么对于文本"{{Category:%category}}"上传说明时会变成"{{Category:dd}}"上传。