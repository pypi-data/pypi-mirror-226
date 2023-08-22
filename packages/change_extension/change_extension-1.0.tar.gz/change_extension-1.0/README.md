## 说明
批量修改文件夹内文件的扩展名

如文件为 胖虎演唱.mp3 那么执行后可以变为 胖虎演唱.zip
## 用法
**终端进入项目位置**
**安装环境`pip install -r requirements.txt`**

**终端输入`python change_extension.py <文件夹路径> <新扩展名>`**
## 例子
```python
cd D:\change_extension
pip install -r requirements.txt  # 安装环境只需要执行一次
python change_extension.py D:\audio zip
```
