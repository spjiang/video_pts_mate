# 开发者：spjiang<spjiang@aliyun.com>
# 日期：2024/8/7
import configparser


class ConfigReader:
    def __init__(self):
        self.file_path = 'config.ini'
        self.config_data = self.read_ini_config()

    def read_ini_config(self):
        # 创建配置解析器对象
        config = configparser.ConfigParser()

        # 读取 ini 文件
        config.read(self.file_path, encoding='utf-8')

        # 将配置文件内容存储在一个字典中
        config_dict = {section: dict(config.items(section)) for section in config.sections()}

        return config_dict




