from enum import Enum
from typing import List, Union, Dict
from pydantic import BaseModel, Field
from ..util import time as time_lib


# =============
# 基础模型
# =============
class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # 主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )


class TaskType(str, Enum):
    """
    任务类型枚举
    """
    # 商品基础信息
    SKU_INFO = 'sku_info'
    # 商品价格
    SKU_PRICE = 'sku_price'
    # 商品基础信息及价格等详细信息
    SKU_FULL = 'sku_full'
    # 商品主详图
    SKU_IMAGE = 'sku_image'
    # 流式采集商品编码（如编码）
    STREAM_SKU_ID = 'stream_sku_id'
    # 流式采集商品价格信息
    STREAM_SKU_PRICE = 'stream_sku_price'
    # 流式采集商品基础信息及价格等详细信息
    STREAM_SKU_FULL = 'stream_sku_full'
    # 流式采集商品主详图
    STREAM_SKU_IMAGE = 'stream_sku_image'


# =============
# 批次采集相关模型
# =============
class BatchTaskItem(BaseModel):
    """
    任务明细模型
    """
    # 【输入】对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = None
    # 【输入】用户指定编号
    rowId: str = None
    # 【输入】商品链接
    url: str = None
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = None


class BatchTask(BaseModel):
    """
    批次任务接收模型
    """
    # 【输入】任务爬虫编码清单
    spiderId: str = None
    # 【输入】任务链接明细清单
    taskItems: List[BatchTaskItem] = []
    # 启动容器数量
    containerCount: int = 1
    # 【输入】文件名称配置键（主详图采集命名使用，非必要）
    fileNameConfig: str = 'default'


class BatchApiData(BaseModel):
    """
    批次接口接收模型
    """
    # 【输入】批次编号
    batchId: str = None
    # 【输入】应用编码
    appCode: str = None
    # 【输入】任务明细清单
    taskList: List[BatchTask] = []
    # 是否直接启动
    autoStart: bool = True


class BatchTaskNodeResp(BaseModel):
    """
    任务明细模型
    """
    # 【输出】对象唯一序列号（全局唯一，可用于主键，等于_id）
    nodeId: str = None
    # 【输出】容器编号
    containerId: str = None
    # 【输出】服务器编号
    hostId: str = None
    # 【输出】商品状态
    status: str = None
    # 【输出】商品状态描述
    statusText: str = None
    # 创建时间
    genTime: int = None
    # 更新时间
    updateTime: int = None


class BatchTaskResp(BaseModel):
    """
    批次采集结果响应模型
    """
    # 【输出】爬虫编码
    spiderId: str = None
    # 【输出】批次编号
    batchId: str = None
    # 【输出】任务链接明细清单
    nodes: List[BatchTaskNodeResp] = []


class ContainerApiData(BaseModel):
    # 【输入】容器Id
    containerId: str = None
    # 【输入】host Id
    hostId: str = None


# =============
# 流式采集相关模型
# =============
class StreamTaskItem(BaseData):
    """
    流式采集任务物料模型
    """
    # 【输入】对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = None
    # 【输入】商品链接
    url: str = None
    # 电商平台编码
    platCode: str = None
    # 【输入】来源APP（流采模式必填）
    appCode: str = None
    # 任务编号（批次）
    batchId: str = None
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = None


class StreamApiData(BaseModel):
    """
    流式采集通用数据接收模型
    """
    # 【v2输入】任务爬虫编码清单
    spiderId: str = None
    # 【v1输入】应用编码
    appCode: str = None
    # 【v1输入】任务类型
    taskType: TaskType = None
    # 【输入】任务明细清单
    taskItems: List[StreamTaskItem] = None
    # 【输入】文件名称配置键
    fileNameConfig: str = 'default'
    # 【v2输入】任务队列后缀（用于拆分某些应用专用任务队列）
    taskQueueSuffix: str = None


# =============
# 基础数据相关模型
# =============
class SupplyPlatform(BaseModel):
    """
    支持平台
    """
    # 【输入】平台编码
    platCodes: List[str] = None
    # 【输入】
    groupCode: str = None
