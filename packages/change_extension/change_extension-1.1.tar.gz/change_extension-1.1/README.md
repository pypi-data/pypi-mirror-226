## 说明
批量修改文件夹内文件的扩展名

如文件为 胖虎演唱.mp3 那么执行后可以变为 胖虎演唱.zip
## 用法1
**终端进入项目位置**

**终端输入`python change_extension.py <文件夹路径> <新扩展名>`**
### 例子
```python
cd D:\change_extension
python change_extension.py D:\audio zip
```
## 用法2
**`pip install change_extension`**
```python
import change_extension
change_extension.batch_change_extension('<文件夹路径> <新扩展名>')