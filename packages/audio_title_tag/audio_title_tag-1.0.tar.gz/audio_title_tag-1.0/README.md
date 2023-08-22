## 说明
批量设置文件夹内的mp3、flac音频文件元数据标签的标题为当前文件名称

如文件名称为 胖虎演唱.mp3 那么音频文件元数据标签的标题会设置为 胖虎演唱
## 用法
**终端进入项目位置**
**安装环境`pip install -r requirements.txt`**

**终端输入`python update_title_tag.py <文件夹路径>`**
## 例子
```python
cd D:\audio-title-tag
pip install -r requirements.txt  # 安装环境只需要执行一次
python update_title_tag.py D:\audio
```
