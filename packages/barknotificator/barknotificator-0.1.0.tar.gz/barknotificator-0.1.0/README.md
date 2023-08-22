# BarkNotificator
- [中文](/README.md)
- [English](docs/README_EN.md)
# 使用方法
## 安装
>pip install barknotificator
## 示例
```python
from BarkNotificator import BarkNotificator

bark = BarkNotificator(device_token="your device token")
bark.send(title="welcome", content="hello world")
```
![image](/docs/inform.jpg "结果图片")
# 感谢
- [Bark官方](https://github.com/Finb/Bark)
