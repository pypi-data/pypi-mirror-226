# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from sf_etl_py3.xml import SfXml
import re
import json


class TableauXml(SfXml):
    """
    data_source
    work_sheet
    dashboard
    windows
    """
    def __init__(self, xml_str: str):
        super().__init__(xml_str)
        # self.xml_obj = ET.fromstring(xml_str)

    def get_dashboard(self): pass

    def get_windows(self): pass

    # noinspection PyBroadException
    def _relation_element(self, connection_element: ET.Element, relation_str_list=None) -> list:
        if relation_str_list is None:
            relation_str_list = ['_.fcp.ObjectModelEncapsulateLegacy.false...relation',
                                 '_.fcp.ObjectModelEncapsulateLegacy.true...relation',
                                 'relation',
                                 ]
        try:
            relation_element = connection_element.findall(relation_str_list[0])
        except Exception:
            if len(relation_str_list) > 1:
                relation_element = self._relation_element(connection_element, relation_str_list[1:])
            else:
                return list()
        return relation_element

    def get_work_sheets(self) -> list:
        """
        :return [{name,source_name_list}]
        """
        work_sheet_dict_list = list()
        worksheet_list = self.xml_obj.findall('worksheets/worksheet')
        for worksheet in worksheet_list:
            worksheet_name = worksheet.get('name')  # 工作表的名称：P04_当日用户请求转化信息-新
            source_name_set = set()
            for worksheet_data_source in (worksheet.findall('table/view/datasources/datasource')):
                source_name_set.add(worksheet_data_source.get('caption'))
            work_sheet_dict_list.append(dict(name=worksheet_name,
                                             source_name_list=list(source_name_set),
                                             ))
        return work_sheet_dict_list

    def get_data_sources(self) -> list:
        """
        :return [{name,id,sql,table_list,connection}]
        """
        data_source_dict_list = list()
        data_sources_list = self.xml_obj.findall('datasources/datasource')
        # for data_sources in data_sources_list:
        #     for data_source in data_sources.findall('datasource'):
        for data_source in data_sources_list:
            data_source_name = data_source.get('caption')  # R35 -- report.r35
            if data_source_name is None:
                continue
            data_source_id = data_source.get('name')  # federated.01x2id5194ck3m1ac1ql90c58mea

            # 一个数据源可能会有多个连接, 这里只写第一个...如果有多个的场景,则需要调整
            relation_list = self._relation_element(data_source.find('connection'))
            if relation_list is None or len(relation_list) == 0:
                continue
            relation = relation_list[0]
            """ relation_type
            : text: 自定义sql
            : table: 拖进去的表
            : union: 多种组合, 目前只考虑table
            """
            relation_type = relation.get('type')
            if relation_type == 'text':
                data_source_sql = relation.text
            elif relation_type == 'table':
                data_source_sql = relation.get('table').replace('[', '').replace(']', '')
            elif relation_type == 'union':
                data_source_sql = relation.find('relation').get('table').replace('[', '').replace(']', '')
            else:
                data_source_sql = 'The value of type is not "text" or "table"'
            table_list = self._sql2table_list(data_source_sql)
            connection_xml = data_source.find('connection/named-connections/named-connection/connection')
            # init sql
            one_time_sql = connection_xml.get('one-time-sql')
            db_connection = json.dumps(connection_xml.attrib)

            data_source_dict_list.append(dict(
                name=data_source_name,
                id=data_source_id,
                sql=data_source_sql,
                table_list=table_list,
                connection=db_connection,
                one_time_sql=one_time_sql,
            ))
        return data_source_dict_list

    @staticmethod
    def _sql2table_list(sql: str) -> list:
        sql = sql.lower()
        table_set = set()
        fix_sql = re.sub(' +', ' ', sql.replace('\n', ' '))
        # for from_table in re.findall(' from \\w+\\.\\w+', fix_sql):
        for from_table in re.findall(' from [^\\s]+\\.[^\\s]+', fix_sql):
            table_name = (from_table.split('from')[1].strip())
            table_set.add(table_name)
        if len(table_set) == 0:
            if re.fullmatch('\\s*[^\\s]+\\.[^\\s]+\\s*', fix_sql):
                table_set.add(sql.strip())
        return list(table_set)
