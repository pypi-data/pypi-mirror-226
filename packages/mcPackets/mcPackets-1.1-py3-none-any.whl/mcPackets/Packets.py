from mcPackets.behind import tp
from mcPackets.packetsAfter import ap

ap(tp, 'packets')


@tp.Error
class packets:
    def __init__(self,
                 path: str = None,
                 absolute_path: str = False,
                 packet_name: str = 'test',
                 namespace: str = 'lock',
                 ):
        """
        :param path:
                path 参数为  为地图路径或者数据包路径
                    地图session.lock文件 或者
                    数据包pack.mcmeta文件
        :param absolute_path:
                absolute_path 参数为 绝对定位,给出的路径必须是 地图session.lock文件
                优先定位,当参数定位出来后则不再运行path定位
        :param packet_name:
            数据包名称
        :param namespace:
            命名空间
        """
        pass

    # 创建数据包
    def createPackets(self, packet_name: str=None, namespace: str=None, description: str='hello py!'):
        """
        创建数据包
        :param packet_name: 是数据包名
        :param namespace: 空间名
        :param description:
            pack.mcmeta文件中的描述
        :return:
        """
        pass

    # 游戏函数
    def functions(self, name: str, S: str, namespace: str=None) -> bool:
        """
        :param name: 创建游戏函数
            path 空间命名 下的functions文件夹为RootPath
            如: "top/v"
                或 name
        :param S: 内容
        :param namespace: 为数据包中的命名空间
        :return:
        """

    # 游戏配方
    def recipes(self, path, content, namespace=None):
        """
        和 functions函数 一样
        :param path:
        :param content:
        :param namespace:
        :return:
        """

    # 游戏结构
    def structures(self):
        # 没写
        return False

    # 游戏进度
    def advancements(self):
        # 没写
        return False

    # 错误
    def _verify(self, f, whether: bool=False):
        pass

    # 错误信息
    def __errorMessage(self, s: str, code_errorMessage=None):
        pass

    # 数据包 参数修改
    def parameter_modification(self, **key):
        """
        参数修改
        """
        pass
