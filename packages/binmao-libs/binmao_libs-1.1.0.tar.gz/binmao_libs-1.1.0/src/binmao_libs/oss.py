import qiniu
import logging

def progress_handler(percent: float) -> None:
    """进度处理
    
    Args:
        percent: 百分比, range(0, 100)
    """
    pass

class OssClient():
    """七牛云对象存储客户端
       
    Args:
        access_key: 七牛云获取

        secret_key: 七牛云获取
         
        bucket_name: 七牛云对象存储指定空间
    
    Returns:
        返回文件路径，不是完整的可访问URL。
        完整的访问URL，需要{空间域名} + {文件路径}
    
    """
    def __init__(self, access_key, secret_key, bucket_name) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name

    def upload(self, local_file, key: str, progress_handler: progress_handler) -> str:
        """上传文件
        
        Args:
            key: 文件访问相对（空间的）路径，例如: day1/shunshine.jpg
            
            local_file: 本地文件路径

            process_handler: 上传进度回调
        """
        q = qiniu.Auth(self.access_key, self.secret_key)
        token = q.upload_token(self.bucket_name, key, 3600)
        ret, info = qiniu.put_file(token, key, local_file, version='v2', progress_handler = lambda current, total: progress_handler(round(current / total, 2))) 
        logging.debug(f"上传文件:{local_file}成功, 返回结果: {info}")
        return key