# CLI app to manage a list of test scripts
# Run: python3 main.py test [feature-name] [type]
# Example: python3 main.py calendar-import non-data-driven

import os
import sys
import subprocess
from utils.logger import Logger

# refresh dependencies -- supress output
# subprocess.run(["pip3", "install", "-r", "requirements.txt"], stdout=subprocess.DEVNULL)


# import rich modules
from rich.panel import Panel
#from rich.traceback import install
from rich import print

#install()

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FEATURES_PATH = os.path.join(DIR_PATH, "features")

USAGE_STR = Panel(
    r"""
    Usage: python3 main.py <feature-name> <type>

    - feature-name: The name of the feature to test
    - type: The type of test to run (data-driven or non-data-driven)

    Example: python3 main.py calendar-import non-data-driven
    """,
    title="Info",
    title_align="left",
    expand=True,
    style="green",
)


class FileTree:
    """A data structure which maps all features, types, and scripts

    Attributes:
    - tree (dict): A tree of features, types, and scripts

    """

    def __init__(self):
        self.tree = {}
        self.build_file_tree()

    def build_file_tree(self):
        # iterate through features folder
        # for each feature, iterate through data-driven and non-data-driven folders
        # for each folder, iterate through scripts
        # build a tree of features, types, and scripts

        for feature in os.listdir(FEATURES_PATH):
            self.tree[feature] = {}
            for type in os.listdir(os.path.join(FEATURES_PATH, feature)):
                self.tree[feature][type] = []
                for script in os.listdir(os.path.join(FEATURES_PATH, feature, type)):
                    self.tree[feature][type].append(script)

    def get_file_tree(self):
        return self.tree

    def get_file_list(self):
        return list(self.tree.keys())

    def get_type_list(self, feature):
        return list(self.tree[feature].keys())

    def get_script_list(self, feature, type):
        return self.tree[feature][type]

    def print_file_tree(self):
        print(self.tree)


class TestRunner:
    """A class to manage running test scripts

    Attributes:
    - logger (Logger): A logger instance
    - file_tree (FeatureTree): A feature tree
    - feature (str): The name of the feature to test
    - type (str): The type of test to run (data-driven or non-data-driven)
    """

    def __init__(self):
        self.logger = Logger()
        self.file_tree = FileTree()
        self.feature = None
        self.type = None

    def get_feature_path(self, feature_name, type):
        #return os.path.join(FEATURES_PATH, feature_name, self.type)
        for feature in self.file_tree.get_file_list():
            if feature == feature_name:
                for type in self.file_tree.get_type_list(feature):
                    if type == self.type:
                        return os.path.join(FEATURES_PATH, feature, type)
        return None

    def get_script_path(self, feature_name, type, script_name):
        #return os.path.join(self.get_feature_path( feature_name, self.type), script_name)
        for feature in self.file_tree.get_file_list():
            if feature == feature_name:
                for type in self.file_tree.get_type_list(feature):
                    if type == self.type:
                        for script in self.file_tree.get_script_list(feature, type):
                            if script == script_name:
                                return os.path.join(FEATURES_PATH, feature, type, script)
        return None

    def get_script_list(self, feature_name, type):
        #return os.listdir(self.get_feature_path(feature_name, self.type))
        for feature in self.file_tree.get_file_list():
            if feature == feature_name:
                for type in self.file_tree.get_type_list(feature):
                    if type == self.type:
                        return self.file_tree.get_script_list(feature, type)
        return None

    def get_script(self, feature_name, type, script_name):
        #return self.get_script_path(feature_name, self.type, script_name)
        for feature in self.file_tree.get_file_list():
            if feature == feature_name:
                for type in self.file_tree.get_type_list(feature):
                    if type == self.type:
                        for script in self.file_tree.get_script_list(feature, type):
                            if script == script_name:
                                return self.get_script_path(feature_name, self.type, script_name)
        return None

    def run_script(self, feature_name, type, script_name):
        script = self.get_script(feature_name, self.type, script_name)
        subprocess.run(["python3", script])

    def start(self):
        if len(sys.argv) != 3:
            print(USAGE_STR)
            sys.exit(1)

        self.feature = sys.argv[1]
        self.type = sys.argv[2]

        if self.type not in ["data-driven", "non-data-driven"]:
            self.logger.log("Bad test type", "error")
            sys.exit(1)

        if not self.get_feature_path(self.feature, self.type):
            self.logger.log("Bad test path", "error")
            print(USAGE_STR)
            sys.exit(1)

        script_list = self.get_script_list(self.feature, self.type)
        if script_list is None:
            self.logger.log("Bad test path", "error")
            print(USAGE_STR)
            sys.exit(1)

        if len(script_list) == 0:
            self.logger.log("No scripts found", "error")
            self.logger.log("Test run failed", "error")
            sys.exit(1)

        self.logger.log("Starting test run", "info")
        self.logger.log(f"Feature: {self.feature}", "info")
        self.logger.log(f"Type: {self.type}", "info")

        for script in script_list:
            # run only files with *.py extension
            if script.endswith(".py"):
                self.logger.log(f"Running script: {script}", "info")
                self.run_script(self.feature, self.type, script)

        self.logger.log("Test run complete", "info")


def main():
    tester = TestRunner()
    #tester.file_tree.print_file_tree()
    try:
        tester.start()
    except Exception as e:
        if hasattr(e, "errno"):
            # if FileNotFoundError:
            if e.errno == 2:
                tester.logger.log("Bad test path", "error")
                tester.logger.log("Test run failed", "error")

                print(USAGE_STR)
            else:
                tester.logger.log(e, "error")
                tester.logger.log("Test run failed", "error")
        else:
            tester.logger.log(e, "error")
            tester.logger.log("Test run failed", "error")


if __name__ == "__main__":
    main()


# TODO:
# - Add support for running all features tests
# - Move webdriver setup to global
