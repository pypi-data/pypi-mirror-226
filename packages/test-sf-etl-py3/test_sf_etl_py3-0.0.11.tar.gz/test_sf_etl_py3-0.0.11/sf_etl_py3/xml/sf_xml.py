# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET


class SfXml:
    def __init__(self, xml_info, xml_type='text'):
        """ xml_type: text or path
        ET.fromstring(xml_str) 等价 ET.parse(xml_str).getroot()
        Element tag: str 标签名 (根标签: workbook-tableau; job-kettle;
        Element attrib: dict 属性
        """
        self.xml_path = None
        self.xml_obj = None

        if xml_type == 'text':
            self.xml_obj = ET.fromstring(xml_info)
        elif xml_type == 'path':
            self.xml_path = xml_info
            with open(xml_info, 'r+') as r_obj:
                self.xml_obj = ET.fromstring(r_obj.read())

    def get_xml_tag(self): return self.xml_obj.tag

    def test(self):
        print(self.xml_obj.tag)
        pass
