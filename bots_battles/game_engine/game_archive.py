import datetime
from distutils.log import info
import logging
import orjson
import os
from flask import current_app

class JSONGame():
    def __init__(self, info) -> None:
        self.states = list()
        self.info = info

    def dump_to_archive(self) -> None:
        logging.info("dumping to archive")
        with current_app.app_context():
          with open(os.path.join(current_app.config['SAVED_STATES'], self.info['game_type'], f"agarnt_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"), 'wb') as archive:
              archive.write(orjson.dumps({'info': self.info, 'states':self.states}))
        logging.info("game dumped")