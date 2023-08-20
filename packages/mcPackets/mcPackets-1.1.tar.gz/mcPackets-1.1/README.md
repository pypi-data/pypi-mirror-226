# mcPackets
一个用于处理《我的世界》数据包的Python库。

## 安装
使用以下命令通过pip安装mcPackets库：

    ```shell
    pip install mcPackets
    ```

## 环境要求

   mcPackets库的开发环境是：
    Python 3.9
    Windows 10

    mcPackets库要求使用Python 3.9或更高版本。


## 使用示例
    ```python
    from mcPackets.Packets import packets

    path = r'C:\Users\Administrator\Desktop\安装包\.minecraft\versions\1.16.5\saves\py'
    v = packets(path=path)
    ...
    ```

## 文档
# 在Packets.py文件中
    ```url
    数据来源
    wiki 中文
        https://wiki.biligame.com/mc/数据包
        https://minecraft.fandom.com/zh/wiki/Minecraft_Wiki

    wiki 英语
        https://minecraft.fandom.com/wiki/Minecraft_Wiki
    ```


## 更新
# 版本 1.1
    更新了functions方法
    更新了recipes方法
    重写了部分方法

