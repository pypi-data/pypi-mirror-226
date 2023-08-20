# -*- coding: utf-8 -*-
import json
import logging
from typing import List
from .model import StreamApiData, BatchApiData, SupplyPlatform, ContainerApiData
from . import http_client
from . import exceptions

LOGGER = logging.getLogger(__name__)


class _Base(object):
    def __init__(self, auth, endpoint, session=None, app_name='', timeout=60):
        self.auth = auth
        self.session = session or http_client.Session()
        self.endpoint = endpoint.strip().strip('/')
        self.timeout = timeout
        self.app_name = app_name

    def _send_request(self, method, url, **kwargs):
        req = http_client.Request(method, url, app_name=self.app_name, **kwargs)
        # 加入鉴权参数
        self.auth.sign_request(req)
        resp = self.session.send_request(req, timeout=self.timeout)
        if resp.status != 200:
            raise exceptions.BizException(resp)

        return resp

    def _get(self, url, **kwargs):
        return self._send_request('GET', url, **kwargs)

    def _post(self, url, **kwargs):
        return self._send_request('POST', url, **kwargs)

    @staticmethod
    def _parse_result(rs):
        if not rs or not rs.response_text:
            raise exceptions.BizException(rs, '响应内容为空')
        js = json.loads(rs.response_text)
        if not js or not js.get('success', False) or js.get('code', -1) < 0:
            raise exceptions.BizException(rs, '业务操作失败')

        return js.get('data', {})


class ZcbotApi(_Base):

    # ====================
    # 批次采集接口
    # ====================
    def batch_publish(self, api_data: BatchApiData):
        """
        批次采集任务发布接口（创建+启动）
        :param api_data:
        :return:
        """
        rs = self._post(
            url=f'{self.endpoint}/api/batch/publish',
            data=api_data.json()
        )
        return self._parse_result(rs)

    def batch_publish_create(self, api_data: BatchApiData):
        """
        批次采集任务发布接口
        :param api_data:
        :return:
        """
        # rs = self._post(
        #     url=f'{self.endpoint}/api/batch/publish',
        #     data=api_data.json()
        # )
        # return self._parse_result(rs)
        rs = self._post(
            url=f'{self.endpoint}/api/batch/publish/create',
            json=api_data.dict()
        )
        return self._parse_result(rs)

    def batch_publish_start(self, api_datas: List[ContainerApiData]):
        """
        批次采集任务发布接口
        :param api_datas:
        :return:
        """
        api_datas = [x.dict() for x in api_datas]
        rs = self._post(
            url=f'{self.endpoint}/api/batch/publish/start',
            json=api_datas
        )
        return self._parse_result(rs)

    def batch_cancel(self, node: str):
        """
        批次采集任务取消接口
        :param node:
        :return:
        """
        rs = self._get(
            url=f'{self.endpoint}/api/batch/cancel',
            params={'node': node},
        )
        return self._parse_result(rs)

    # ====================
    # 流式采集接口
    # ====================
    def stream_publish(self, api_data: StreamApiData):
        """
        流式采集发布采集任务接口
        :param api_data:
        :return:
        """
        rs = self._post(
            url=f'{self.endpoint}/api/stream/publish',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # ============================
    # 获取所有平台
    def get_all_platforms(self):
        rs = self._get(
            url=f'{self.endpoint}/api/meta/platforms',
        )
        return self._parse_result(rs)

    # 获取所有平台
    def get_platforms_by_spider_group(self, spider_group: str):
        rs = self._get(
            url=f'{self.endpoint}/api/meta/platforms/batch',
            params={'spider_group': spider_group},
        )
        return self._parse_result(rs)

    # 获取细粒度的爬虫组（新方案）
    def get_spider_group(self, plat_data: SupplyPlatform):
        rs = self._post(
            url=f'{self.endpoint}/api/meta/platforms/supply_type',
            json=plat_data.dict()
        )
        return self._parse_result(rs)

    def get_supply_platforms_by_group_code(self, group_code: str):
        """
        根据任务类型，获取目前支持的所有平台
        """
        rs = self._post(
            url=f'{self.endpoint}/api/meta/platforms/supply_platform',
            params={"groupCode": group_code}
        )
        return self._parse_result(rs)
