#!/usr/bin/python
# encoding=utf-8

import os
import inspect
from pathlib import Path
from pitrix import __image__
from pitrix.utils.log import logger
from pitrix.cache import Config,Cache,Schema
from pitrix.utils.yaml_tool import load_yaml
from pitrix.constants.constants import PitrixConf,TargetConf
from pitrix.extension.allure_report import mk_allure_report,categories,AllureGetData


global db_cache,db_config,db_schema


def fixture_paths():
    """
    fixture路径，1、项目下的fixtures；2、pitrix 下的fixture；
    @return:
    """
    _fixtures_dir = TargetConf.FIXTURES
    paths = []
    for root, _, files in os.walk(_fixtures_dir):
        for file in files:
            if file.startswith("fixture_") and file.endswith(".py"):
                full_path = os.path.join(root, file)
                import_path = full_path.replace(_fixtures_dir, "").replace("\\", ".")
                import_path = import_path.replace("/", ".").replace(".py", "")
                paths.append("fixtures" + import_path)
    paths.append("pitrix.fixture")
    return paths

class Plugin:

    @staticmethod
    def pytest_collection_modifyitems(items):
        """
        解决中文乱码
        @param items:
        @return:
        """
        for item in items:
            item.name = item.name.encode("utf-8").decode("unicode_escape")
            item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    @staticmethod
    def pytest_configure(config):
        """
        目的是生成allure源文件，用于生成HTML报告
        @param config:
        @return:
        """
        logger.info("========= Pitrix Pytest Configure ==============")
        root_dir = config.__dict__['_rootpath']

    @staticmethod
    def pytest_unconfigure(config):
        """
        发送测试报告
        @param config:
        @return:
        """
        logger.info("========= Pitrix Pytest Unconfigure ==============")
        root_dir = config.__dict__['_rootpath']

    @staticmethod
    def pytest_sessionstart(session):
        """
        在创建“Session”对象之后和执行收集之前调用并进入运行测试循环。
        @param session: pytest.Session session: pytest 会话对象.
        @return:
        """
        logger.info("========= Pitrix Pytest Session Start ==============")
        root_dir = session.config.rootdir

    @staticmethod
    def pytest_sessionfinish(session):
        """
        测试运行结束后生成allure报告
        @param session:
        @return:
        """
        logger.info("========= Pitrix Pytest Session Finish ==============")
        root_dir = session.config.rootdir
        if mk_allure_report(TargetConf):
            write_environment(db_config)
            from pitrix.extension.wechat import WeChatSend
            WeChatSend().send_detail_msg()


def recursive_search(conftest_path_dir,filename='pytest.ini'):
    """
    自动寻找项目根目录,根目录的判定条件是项目下存在pytest.ini 文件,并且初始化项目各路径
    :param conftest_path_dir: conftest.py 文件的父目录,项目下可能存在多个此类文件,故需要递归往上级目录去查找,直到查找到符合条件为止
    :param filename: pytest.ini
    :return:
    """
    current_dir = Path(conftest_path_dir)
    if current_dir.exists() and current_dir.is_dir():
        while True:
            if current_dir.exists() and (current_dir / filename).exists():
                configure_project_dir(current_dir)

                global db_cache, db_config, db_schema
                db_cache = Cache(TargetConf.DB_PATH)
                db_config = Config(TargetConf.DB_PATH)
                db_schema = Schema(TargetConf.DB_PATH)

                env_info = load_yaml(TargetConf.CONF_YAML)
                db_config.set("current_env", env_info[TargetConf.CURRENT_ENV_KEY])
                current_env_conf_dict = env_info[db_config.get('current_env')]
                for k, v in current_env_conf_dict.items():
                    db_config.set(k, v)
                return current_dir
            parent_dir = current_dir.parents[0]
            if parent_dir == current_dir:
                break
            current_dir = parent_dir
    return None

def pitrix_plugins():
    """
    引入插件
    @return:
    """
    print(__image__)
    caller = inspect.stack()[1]
    recursive_search(Path(caller.filename).cwd())
    plugins = fixture_paths()
    return plugins


def configure_project_dir(root_dir):
    """
    动态配置项目目录
    @param root_dir:
    @return:
    """
    TargetConf.PROJECT_DIR = root_dir
    TargetConf.FIXTURES = os.path.join(root_dir, "fixtures")
    TargetConf.CONF_DIR = os.path.join(root_dir, "config")
    TargetConf.DATA_DIR = os.path.join(root_dir, "datas")
    TargetConf.LOG_DIR = os.path.join(root_dir, "logs")
    TargetConf.REPORT_DIR = os.path.join(root_dir, "reports")
    TargetConf.CASE_DIR = os.path.join(root_dir, "testcases")
    TargetConf.PYTEST_INI = os.path.join(root_dir, "pytest.ini")
    TargetConf.DB_PATH = os.path.join(root_dir, "database", "pitrix.db")
    TargetConf.CONF_YAML = os.path.join(root_dir, "config", "config.yaml")
    TargetConf.LOG_FILE = os.path.join(TargetConf.LOG_DIR, "pitrix.log")
    TargetConf.ALLURE_RESULTS = os.path.join(TargetConf.REPORT_DIR, "json")
    TargetConf.ALLURE_REPORT = os.path.join(TargetConf.REPORT_DIR, "html")
    TargetConf.ALLURE_SUMMARY_FILE = os.path.join(TargetConf.ALLURE_REPORT, "widgets","summary.json")
    TargetConf.ALLURE_ENV_FILE = os.path.join(TargetConf.ALLURE_RESULTS, 'environment.properties')
    TargetConf.ALLURE_TYPE_FILE = os.path.join(TargetConf.ALLURE_RESULTS, 'categories.json')
    TargetConf.NOTIFICATION_YAML = os.path.join(TargetConf.CONF_DIR,'notification.yaml.temp')

def write_environment(_db_config):
    """
    写测试环境信息到文件
    @param db_config:
    @return:
    """
    env_infos = _db_config.get_all()
    if env_infos:
        content = ""
        for k, v in env_infos.items():
            content += f"{k}={v}\n"
        with open(TargetConf.ALLURE_ENV_FILE, 'w') as f:
            f.write(content)
        return True
    else:
        return False