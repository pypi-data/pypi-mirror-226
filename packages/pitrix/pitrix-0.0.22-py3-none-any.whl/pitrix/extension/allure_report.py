#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import os
import json
import time
import shutil
from collections import namedtuple

categories_json = [
        {
            "name": "忽略的测试",
            "matchedStatuses": ["skipped"]
        },
        {
            "name": "基础设施问题",
            "matchedStatuses": ["broken", "failed"],
            "messageRegex": ".*bye-bye.*"
        },
        {
            "name": "过期的测试",
            "matchedStatuses": ["broken"],
            "traceRegex": ".*FileNotFoundException.*"
        },
        {
            "name": "产品缺陷",
            "matchedStatuses": ["failed"]
        },
        {
            "name": "测试缺陷",
            "matchedStatuses": ["broken"]
        }
    ]

def mk_trend(config):
    """
    将上次测试报告中的测试历史数据拷贝到最新的生成的历史数据中
    @param config: 项目配置类
    @return:
    """
    ALLURE_REPORT_HISTORY_PATH = os.path.join(config.ALLURE_REPORT, 'history')
    ALLURE_RESULTS_HISTORY_PATH = os.path.join(config.ALLURE_RESULTS, 'history')
    if os.path.exists(ALLURE_RESULTS_HISTORY_PATH):
        shutil.rmtree(ALLURE_RESULTS_HISTORY_PATH)
    shutil.copytree(ALLURE_REPORT_HISTORY_PATH, ALLURE_RESULTS_HISTORY_PATH)

def mk_allure_report(config):
    """
    生成allure测试报告
    @param config: 项目配置类
    @return:
    """
    try:
        mk_report_cmd = f"allure " \
                        f"generate " \
                        f"-c {config.ALLURE_RESULTS} " \
                        f"-o {config.ALLURE_REPORT}"
        os.system(mk_report_cmd)
        time.sleep(3)
        mk_trend(config)
        categories(config)
        return True
    except Exception as e:
        return False

def categories(config):
    """
    写类型信息到allure测试报告
    @param config:
    @return:
    """
    with open(config.ALLURE_TYPE_FILE, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(categories_json, indent=2, ensure_ascii=False))

class AllureGetData:

    @staticmethod
    def get_summary(allure_summary_json):
        """
        获取所有 allure 报告中执行用例的情况
        @param allure_summary_json: 文件地址,位于allure report/widgets/summary.json
        @return:
        """
        Summary = namedtuple('Summary', ['total', 'passed', 'broken', 'failed', 'skipped',
                                         'passed_rate', 'failed_rate', 'run_time', 'unknown'])

        if os.path.exists(allure_summary_json):
            with open(allure_summary_json, "r", encoding='utf-8') as f:
                data = json.load(f)
            total = data['statistic']['total'] if data['statistic']['total'] is not None else 0
            passed = data['statistic']['passed'] if data['statistic']['passed'] is not None else 0
            broken = data['statistic']['broken'] if data['statistic']['broken'] is not None else 0
            failed = data['statistic']['failed'] if data['statistic']['failed'] is not None else 0
            skipped = data['statistic']['skipped'] if data['statistic']['skipped'] is not None else 0
            unknown = data['statistic']['unknown'] if data['statistic']['unknown'] is not None else 0
            passed_rate = round(passed / (total - skipped))
            failed_rate = round(failed / (total - skipped))
            run_time = round(data['time']['duration'] / 1000, 2)

            summary = Summary(total=total,passed=passed,failed=failed,
                              broken=broken,unknown=unknown,skipped=skipped,
                              passed_rate=passed_rate,failed_rate=failed_rate,run_time=run_time
                              )
            return summary