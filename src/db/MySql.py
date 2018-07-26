#! /usr/bin/python3
# _*_ coding:utf-8 _*_
import logging
import yaml
import pymysql
import pandas as pd


class MySql:
    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    config = yaml.load(open("comparison_config.yaml"))
    corporate_id = config['store']['corporate_id']
    cannot_find_internal_storeid_tag = config['store']['cannot_find_internal_storeid_tag']
    mysql_connection = (config['mysql']['ip'], config['mysql']['username'], config['mysql']['password'],
                        config['mysql']['dbname'])
    corporateid = config['corporate']['id']

    def __init__(self):
        logging.debug('Begin to connect mysql.')
        self.mysql_db = pymysql.connect(*self.mysql_connection)
        self.cursor = self.mysql_db.cursor()
        logging.debug('Connecting mysql successfully.')

    def get_storeid(self):
        logging.debug('Start to query storeID of corporateId %s in mysql.', self.corporateid)
        try:
            mysql_query = 'SELECT DISTINCT id from stfm_stores where corporate_id = (%s)'
            self.cursor.execute(mysql_query, self.corporateid)
            result = self.cursor.fetchall()
        except Exception as errormessage:
            logging.debug('Unable to query mysql storeid %s', errormessage)
        else:
            return [i[0] for i in list(result)]

    def generate_storeid_state_map(self):
        mysql_query = "select id, state from stfm_stores " \
                      "where corporate_id = {corporate_id}".format(corporate_id=self.corporate_id)
        id_state_dataframe = pd.read_sql_query(mysql_query, self.mysql_db)
        id_state_dict = dict(zip(id_state_dataframe['id'], id_state_dataframe['state']))
        return id_state_dict

    def generate_uid_title_map(self, uid_list):
        uid_list_str = '(' + ','.join(uid_list) + ')'
        mysql_query = """select a.uid, b.title from stfm_staffing_roster a, stfm_positions b where a.corporate_id = b.corporate_id
                         and a.corporate_id = {corporate_id} and a.position_id = b.id
                         and a.uid in {uid_str}""".format(corporate_id=self.corporate_id, uid_str=uid_list_str)
        uid_list_dataframe = pd.read_sql_query(mysql_query, self.mysql_db)
        uid_list_dict = dict(zip(uid_list_dataframe['uid'], uid_list_dataframe['title']))
        return uid_list_dict




