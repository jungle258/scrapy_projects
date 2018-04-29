# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.conf import settings
import pymysql


class TencentPipeline(object):

    def __init__(self):
        self.file = open('tencent_job.json', 'w')

    def process_item(self, item, spider):

        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def close_spider(self):
        self.file.close()


class DongguanPipeline(object):
    """
    写入mysql数据库
    """

    def __init__(self):
        self.con = pymysql.connect(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DB'],
            port=settings['MYSQL_PORT']
            )

    def process_item(self, item, spider):

        cursor = self.con.cursor()
        try:
            cursor.execute('insert into sundongguan_info(id,title,target,info_link,state,person,time)'
                           'values(%s,%s,%s,%s,%s,%s,%s)',
                           [item['id'].encode('utf-8'), item['title'].encode('utf-8'),
                            item['target'].encode('utf-8'), item['info_link'].encode('utf-8'),
                            item['state'].encode('utf-8'), item['person'].encode('utf-8'),
                            item['time'].encode('utf-8')]
                           )
        except Exception as e:
            print('#'*30)
            print(e)
            self.con.rollback()

        else:
            self.con.commit()

        return item

    def close_spider(self):
        self.con.close()
