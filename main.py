# CLI app to manage a list of test scripts
# Run: python3 main.py test [feature-name] [type]
# Example: python3 main.py calendar-import non-data-driven

import os
import sys
import time
import datetime
import subprocess
from utils.Logger import Logger

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FEATURES_PATH = os.path.join(DIR_PATH, "features")


class Tester:
    def __init__(self):
        self.logger = Logger()

    def get_feature_path(self, feature_name, type):
        return os.path.join(FEATURES_PATH, feature_name, type)

    def get_script_path(self, feature_name, type, script_name):
        return os.path.join(self.get_feature_path(feature_name, type), script_name)

    def get_script_list(self, feature_name, type):
        return os.listdir(self.get_feature_path(feature_name, type))

    def get_script(self, feature_name, type, script_name):
        return self.get_script_path(feature_name, type, script_name)

    def run_script(self, feature_name, type, script_name):
        script = self.get_script(feature_name, type, script_name)
        subprocess.run(["python3", script])
        
    def start(self):
        self.logger.log("Starting test run", "info")
        self.logger.log("Feature: {}".format(sys.argv[1]), "info")
        self.logger.log("Type: {}".format(sys.argv[2]), "info")
        #self.logger.log("Script: {}".format(sys.argv[3]))

        scripts = self.get_script_list(sys.argv[1], sys.argv[2])
        self.logger.log("Scripts: {}".format(scripts), "info")

        for script in scripts:
            try:
                self.run_script(sys.argv[1], sys.argv[2], script)
            except Exception as e:
                self.logger.log(e, "exception")
                self.logger.log("Test run failed", "error")
                return

        self.logger.log("Test run complete", "info")



def main():
    tester = Tester()
    tester.start()


if __name__ == "__main__":
    main()
