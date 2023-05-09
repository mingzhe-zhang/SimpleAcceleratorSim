
from enum import Enum,unique

@unique
class MemAccessType(Enum):
    # 为序列值指定value值
    Read = 0
    Write = 1