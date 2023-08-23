# -*- coding: utf-8 -*-
import json
import logging
from typing import List

from .model import StreamApiData, BatchApiData, BatchSpiderGroupQuery
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

    def batch_cancel(self, host_id: str, container_id: str):
        """
        批次采集任务取消接口
        :return:
        """
        rs = self._get(
            url=f'{self.endpoint}/api/batch/cancel',
            params={'hostId': host_id, 'containerId': container_id},
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

    # 根据爬虫组编号，获取可选的爬虫清单
    def get_support_spiders_by_group(self, api_data: BatchSpiderGroupQuery):
        rs = self._post(
            url=f'{self.endpoint}/api/meta/batch-spider/group/spiders',
            data=api_data.json()
        )
        return self._parse_result(rs)

    # 根据爬虫组编号，获取支持的平台清单
    def get_support_platforms_by_group(self, group_code: str = None):
        rs = self._post(
            url=f'{self.endpoint}/api/meta/batch-spider/group/platforms',
            params={"groupCode": group_code}
        )
        return self._parse_result(rs)
