# -*- coding: utf-8 -*-
from sf_etl_py3.xml import SfXml
import xml.etree.ElementTree as ET
import json
import os


class KettleXml:
    def __init__(self, xml_path: str, project_path=None, is_run=1):
        """
        entries: list(entry): 任务列表
            <name>report.dq_mail_daily</name>
            <type>SQL</type>  (type: SQL、JOB、TRANS、SHELL)
        hops: list(hop): 依赖关系
        """
        # super().__init__(xml_path)
        self.xml_path = xml_path
        self.root_is_run = is_run
        with open(xml_path, 'r+') as r_obj:
            self.xml_obj = ET.fromstring(r_obj.read())
        if project_path is not None:
            self.project_dir = str(project_path).rstrip('/') + '/'
        else:
            self.project_dir = '/'

    def get_task_list(self) -> list:
        """
        :return [{"task_name":xx,"task_type":xx, "task_dir": xx, "task_info": xx},{}]
        """
        result_set = set()
        hop_list = self.get_hop_list()  # :return [{"from":xx,"to":xx},{}]
        task_dir = None
        if self.xml_obj.tag == 'job':
            for entry in self.xml_obj.findall('entries/entry'):
                task_name = entry.find('name').text
                task_type = entry.find('type').text
                task_from_set = set()
                task_to_set = set()
                is_run = 0
                for hop_dict in hop_list:
                    from_name = hop_dict.get('from')
                    to_name = hop_dict.get('to')
                    enabled = hop_dict.get('enabled')
                    if task_name == from_name:
                        task_to_set.add(to_name)
                        is_run = 1 if enabled == 'Y' else is_run
                    if task_name == to_name:
                        task_from_set.add(from_name)
                        is_run = 1 if enabled == 'Y' else is_run
                current_dir = self.xml_path
                if task_type == 'JOB':
                    task_job_name = entry.find('jobname').text
                    if entry.find('directory') is not None:
                        directory_ = str(entry.find('directory').text).rstrip('/') + '/'
                        _dir = str(self.project_dir + directory_).replace('//', '/')
                        task_dir = '%s%s.kjb' % (_dir, task_job_name)
                    task_info = None
                elif task_type == 'TRANS':
                    task_trans_name = entry.find('transname').text
                    if entry.find('directory') is not None:
                        directory_ = str(entry.find('directory').text).rstrip('/') + '/'
                        _dir = str(self.project_dir + directory_).replace('//', '/')
                        task_dir = '%s%s.ktr' % (_dir, task_trans_name)
                    task_info = None
                elif task_type in ('SPECIAL', 'SUCCESS'):
                    task_info = None
                elif task_type == 'SHELL':
                    # task_info = entry.find('filename').text
                    task_info = json.dumps({
                        'work_directory': entry.find('work_directory').text,
                        'filename': entry.find('filename').text,
                        'script': entry.find('script').text,
                        'insertScript': entry.find('insertScript').text,
                    })
                elif task_type in ('SQL', 'ExecSQL'):
                    task_info = entry.find('sql').text
                elif task_type == 'MAIL':
                    task_info = json.dumps({
                        'server': entry.find('server').text,
                        'port': entry.find('port').text,
                        'destination': entry.find('destination').text,
                        'destinationCc': entry.find('destinationCc').text,
                        'replyto': entry.find('replyto').text,
                        'replytoname': entry.find('replytoname').text,
                        'subject': entry.find('subject').text,
                        'auth_user': entry.find('auth_user').text,
                    })
                elif task_type == 'TypeExitExcelWriterStep':
                    task_info = json.dumps({'file_name': entry.find('file/name').text})
                else:
                    task_info = None
                is_run = 0 if self.root_is_run == 0 else is_run
                result_set.add(json.dumps(dict(task_name=task_name, task_type=task_type,
                                               task_dir=task_dir, task_info=task_info,
                                               task_from=json.dumps(list(task_from_set)),
                                               task_to=json.dumps(list(task_to_set)), is_run=is_run,
                                               task_tag=self.xml_obj.tag, current_dir=current_dir)))
        if self.xml_obj.tag == 'transformation':
            """
            <order>
                <hop> <from>account_mysql_user</from><to>pdl_pg_dw1_account_user</to><enabled>Y</enabled> </hop>
                <hop> <from>mysql_test_user_yoloan</from><to>pdl_pg_dw1_test_user_yoloan</to><enabled>N</enabled> </hop>
            </order>

            <step>
                <name>account_adjust_channel</name>
                <type>TableOutput</type>
                <connection>pg_pdl</connection>
                <schema>dw1</schema>
                <table>account_adjust_channel</table>
            </step>

            <step>
                <name>account_mysql_phone_try_register</name>
                <type>TableInput</type>
                <connection>mysql_vnm_account</connection>
                <sql>select xx</sql>
            </step>
            """
            for entry in self.xml_obj.findall('step'):
                task_name = entry.find('name').text
                task_type = entry.find('type').text
                task_from_set = set()
                task_to_set = set()
                is_run = 0
                for hop_dict in hop_list:
                    from_name = hop_dict.get('from')
                    to_name = hop_dict.get('to')
                    enabled = hop_dict.get('enabled')
                    if task_name == from_name:
                        task_to_set.add(to_name)
                        is_run = 1 if enabled == 'Y' else is_run
                    if task_name == to_name:
                        task_from_set.add(from_name)
                        is_run = 1 if enabled == 'Y' else is_run

                current_dir = self.xml_path
                if task_type == 'TableOutput':
                    table_out_connection = entry.find('connection').text
                    table_out_schema = entry.find('schema').text
                    table_out_table = entry.find('table').text

                    task_dir = None
                    task_info = json.dumps(dict(
                        table='%s.%s' % (table_out_schema, table_out_table),
                        connection=table_out_connection

                    ))
                elif task_type == 'TableInput':
                    task_dir = None
                    task_in_sql = entry.find('sql').text
                    table_in_connection = entry.find('connection').text
                    task_info = json.dumps(dict(
                        sql=task_in_sql,
                        connection=table_in_connection,
                    ))
                else:
                    task_dir = None
                    task_info = None
                is_run = 0 if self.root_is_run == 0 else is_run
                result_set.add(json.dumps(dict(task_name=task_name, task_type=task_type,
                                               task_dir=task_dir, task_info=task_info,
                                               task_from=json.dumps(list(task_from_set)),
                                               task_to=json.dumps(list(task_to_set)), is_run=is_run,
                                               task_tag=self.xml_obj.tag, current_dir=current_dir)))

        return [json.loads(i) for i in result_set]

    def get_hop_list(self) -> list:
        """
        :return [{"from":xx,"to":xx},{}]
        """
        result_set = set()
        if self.xml_obj.tag == 'job':
            hop_xml_path = 'hops/hop'
        elif self.xml_obj.tag == 'transformation':
            hop_xml_path = 'order/hop'
        else:
            return list()
        for hop in self.xml_obj.findall(hop_xml_path):
            from_name = hop.find('from').text
            to_name = hop.find('to').text
            enabled = hop.find('enabled').text
            result_set.add(json.dumps({'from': from_name, 'to': to_name, 'enabled': enabled}))
        return [json.loads(i) for i in result_set]

    def get_file_set(self, result_dict=None):
        # if result_set is None:
        #     result_set = set()
        #     result_set.add(self.xml_path)
        # for task in self.get_task_list():
        #     task_type = task.get('task_type')
        #     task_dir = task.get('task_dir')
        #     if task_type in ('JOB', 'TRANS') and task_dir is not None:
        #         if task_dir is not None:
        #             result_set.add(task_dir)
        #             self.__init__(task_dir, self.project_dir)
        #             result_set = self.get_file_set(result_set)
        if result_dict is None:
            result_dict = dict()
            result_dict[self.xml_path] = {'is_run': self.root_is_run}
        for task in self.get_task_list():
            task_type = task.get('task_type')
            task_dir = task.get('task_dir')
            is_run = task.get('is_run')
            if task_type in ('JOB', 'TRANS') and task_dir is not None:
                if task_dir in result_dict.keys() and is_run == 0:
                    pass
                else:
                    result_dict[task_dir] = {'is_run': is_run}
                self.__init__(task_dir, self.project_dir)
                result_dict = self.get_file_set(result_dict)
        return result_dict

    def get_task_list_all(self):
        result_list = list()
        for file_path, file_dict in self.get_file_set().items():
            if not os.path.exists(file_path):
                continue
            self.__init__(file_path, self.project_dir, is_run=file_dict.get('is_run'))
            result_list.extend(self.get_task_list())
        return result_list
        # file_set = set()
        # file_set.add(self.xml_path)
        # if result_list is None:
        #     result_list = list()
        # for task in self.get_task_list():
        #     task_name = task.get('task_name')
        #     task_type = task.get('task_type')
        #     task_dir = task.get('task_dir')
        #     file_set.add(task_dir)
        #     result_list.append(task)
        #     if task_type in ('JOB', 'TRANS') and task_dir is not None:
        #         # if task_name == 'vnm_trans':
        #         if task_dir is not None:
        #             self.__init__(task_dir, self.project_dir)
        #             result_list = self.get_all_list_all(result_list)
        # return result_list
