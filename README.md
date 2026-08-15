## 自动批量重命名图片  
### 下载 [随机](https://github.com/SadYuyuko/auto-rename-screenshots/releases/download/1.0/auto-rename.exe) | [无随机数](https://github.com/SadYuyuko/auto-rename-screenshots/releases/download/1.0/auto-rename_norandom.exe)  
将当前目录下所有图片重命名为`Screenshot_年-月-日_时分秒+随机2位数字`  
 - 命名逻辑：读取图片EXIF时间信息，EXIF为空则时间戳为文件修改日期，时间自动补零  
 - 随机2位数字用于避免同1秒的多个截图命名冲突  
 - 无随机数版在命名冲突时自动加上`_2` `_3`等后缀  
