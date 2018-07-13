#! /usr/bin/python3
# _*_ coding:utf-8 _*_
import logging
import yaml
import pymysql


class MySql:

    FORMAT = "%(asctime)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    config = yaml.load(open("comparison_config.yaml"))
    corporate_id = config['store']['corporate_id']
    cannot_find_internal_storeid_tag = config['store']['cannot_find_internal_storeid_tag']
    mysql_connection = (config['mysql']['ip'], config['mysql']['username'], config['mysql']['password'],
                        config['mysql']['dbname'])
    corporateid = config['corporate']['id']
    position_title_map = {}
    storeid_state_map = {}

    def __init__(self):

        mysql_db = pymysql.connect(*self.mysql_connection)
        self.cursor = mysql_db.cursor()
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

    def get_position_title_mapping(self):
        logging.debug('Start to query position and title mapping of corporateId %s in mysql.', self.corporateid)
        try:
            mysql_query = 'select id, title from stfm_positions where corporate_id = (%s)'
            self.cursor.execute(mysql_query, self.corporateid)
            result = self.cursor.fetchall()
            self.position_title_map = {i[0]: str(i[1]).upper() for i in list(result)}
            logging.debug("Store position and title mapping relation is: %s", self.position_title_map)
        except Exception as errormessage:
            logging.debug('Unable to get position title mapping  %s', errormessage)
        else:
            return self.position_title_map

    def generate_storeid_stat_map(self):
        logging.debug('Start to query storeid and stat mapping of corporateId %s in mysql.', self.corporateid)
        try:
            mysql_query = 'select id, state from stfm_stores where corporate_id = (%s)'
            self.cursor.execute(mysql_query, self.corporateid)
            result = self.cursor.fetchall()
            self.storeid_state_map = {i[0]: i[1] for i in list(result)}
            logging.debug("Store storeid and state mapping relation is: %s", self.storeid_stat_map)
        except Exception as errormessage:
            logging.debug('Unable to get storeid and state mapping  %s', errormessage)
        else:
            return self.storeid_state_map

    def get_uid_title_mapping(self, uid):
        self.get_position_title_mapping()
        try:
            mysql_query = 'select position_id from stfm_staffing_roster where corporate_id = (%s) and uid = (%s)'
            args = (self.corporateid, uid)
            self.cursor.execute(mysql_query, args)
            result = self.cursor.fetchone()
            position_id = result[0]
        except Exception as errormessage:
            logging.debug('Unable to get uid title mapping  %s', errormessage)
        else:
            logging.debug('position_id is %s and title is %s', result[0], self.position_title_map[position_id])
            return self.position_title_map[position_id]

    def get_storeid_state_mapping(self, storeid):
        self.generate_storeid_stat_map()
        logging.debug('Start to query state of storeid %s of corporateId %s in mysql.', storeid, self.corporateid)
        if storeid in self.storeid_state_map.keys():
            return self.storeid_state_map[storeid]
        else:
            return None


