from robot.api.deco import keyword
# from salabsutils import DynamicRobotApiClass,PY2
# from robotremoteserver import RobotRemoteServer
import os
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.utils import get_link_path, abspath, timestr_to_secs, is_truthy
from glob import glob
import base64
from robot.api import logger
import sys


PY2 = sys.version_info < (3,)
PY3 = sys.version_info > (2,)

class RemoteTransfer():
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def get_keyword_names(self):
        """Robot Framework dynamic API keyword collector."""
        return [name for name in dir(self) if hasattr(getattr(self, name), 'robot_name')]

    @keyword
    def transfer_files(self, pattern, path=""):
        items = {}
        path = path if path != "" else self._log_dir
        results = glob(os.path.join(path, pattern))
        items['amount'] = len(results)
        items['path'] = path
        items['files'] = []
        for item in results:
            with open(item, "rb") as input_buffer:
                buff = base64.b64encode(input_buffer.read())
                file_name = os.path.basename(item)
                items['files'].append({"name": file_name, "data": buff})
        return items

    @keyword
    def save_files(self, file_array, path=""):
        path = path if path != "" else self._log_dir
        logger.info("remote file path: [{}]".format(file_array['path']))
        for item in file_array['files']:
            logger.info("remote file name: [{}]".format(item['name']))
            local_file = os.path.join(path, os.path.basename(item['name']))
            with open(local_file, 'wb') as output_buffer:
                output_buffer.write(base64.b64decode(item['data']))
                self._link_file(local_file)

    @keyword
    def save_screenshots(self, file_array, width='800px', save_to_disk=True):
        logger.info("remote file path: [{}]".format(item['path']))
        for item in file_array['files']:
            logger.info("remote file name: [{}]".format(item['name']))
            local_file = os.path.join(self._log_dir, item['name'])
            with open(local_file, 'wb') as output_buffer:
                output_buffer.write(base64.b64decode(item['data']))
                self._embed_screenshot(local_file, width, save_to_disk)

    @keyword
    def save_videos(self, file_array, width='800px', save_to_disk=True):
        logger.info("remote file path: [{}]".format(item['path']))
        for item in file_array['files']:
            logger.info("remote file name: [{}]".format(item['name']))
            local_file = os.path.join(self._log_dir, item['name'])
            with open(local_file, 'wb') as output_buffer:
                output_buffer.write(base64.b64decode(item['data']))
                self._embed_video(local_file, width, save_to_disk)

    @property
    def _log_dir(self):
        try:
            logfile = BuiltIn().get_variable_value("${LOG FILE}")
            if logfile is None:
                return BuiltIn().get_variable_value("${OUTPUTDIR}")
            return os.path.dirname(logfile)
        except RobotNotRunningError:
            return os.getcwdu() if PY2 else os.getcwd()

    def _link_file(self, path):
        link = get_link_path(path, self._log_dir)
        logger.info("File saved to '<a href=\"%s\">%s</a>'." % (link, path), html=True)

    def _embed_screenshot(self, path, width, save_to_disk):
        link = get_link_path(path, self._log_dir)
        if save_to_disk:
            logger.info('<a href="%s"><img src="%s" width="%s"></a>' % (link, link, width), html=True)
        else:
            with open(path, "rb") as image_file:
                logger.info('<img src="data:image/png;base64, %s" width="%s">' % ((base64.b64encode(image_file.read())).decode("utf-8"), width), html=True)
            os.remove(path)

    def _embed_video(self, path, width, save_to_disk):
        link = get_link_path(path, self._log_dir)
        if save_to_disk:
            logger.info('<a href="%s"><video width="%s" autoplay><source src="%s" type="video/webm"></video></a>' %
                        (link, width, link), html=True)
        else:
            with open(path, "rb") as image_file:
                logger.info('<video width="%s" autoplay><source src="data:video/webm;base64, %s" type="video/webm"></video>' %
                            (width, (base64.b64encode(image_file.read())).decode("utf-8")), html=True)
            os.remove(path)
