# @Author: LiXiang
# @Time: 2023/12/22 15:32
# @version: 1.0
import os
import re
import subprocess
import threading

import pandas as pd
from flask import jsonify, request, current_app
from flask_restful import Resource

from App.models import TestProject, DataSet, Project, db
from App.utils.backend_path import BackendPath


# 实验测试操作
class TPOperation(Resource):
    # 开始执行测试实验任务
    def post(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        # 命令中的参数
        testcase_path = os.path.join(BackendPath(), DataSet.query.filter(DataSet.DS_id == tP.DS).first().DS_url)  # DS路径
        config_path = os.path.join(BackendPath(), 'App', 'data', 'config', 'config_' + tP.tP_id + '.py')  # 配置文件路径
        project_name = Project.query.filter(Project.project_id == tP.Pid).first().project_name  # 项目名称
        # 执行实验命令
        command = 'conda run -n ' + current_app.config['conda_env'] + ' gltest --testcase_path=' + testcase_path \
                  + ' --config_path=' + config_path + ' --project_name=' + project_name + ' --test_name=' + tP.tP_name \
                  + ' --test_id=' + tP.tP_id + ' --logs_path=' + os.path.join(BackendPath(), 'App', 'data')
        print(command)
        try:
            thread = threading.Thread(
                target=lambda: subprocess.run(command, shell=True, capture_output=True, text=True, check=True,
                                              encoding='utf-8'))
            thread.start()
            print("后续代码继续执行...")  # 继续执行后续的代码
            tP.tP_status = 1  # 修改实验state状态【0:待实验、1:正在实验、2:待审核、3:已完成】
            db.session.commit()
            return jsonify({'success': True})
        except subprocess.CalledProcessError as e:
            print(f"命令输出:{e.stdout}\n错误信息:{e.stderr}\n返回码:{e.returncode}")
            return jsonify({'success': False, 'message': str(e)})
        except Exception as e:  # 数据库操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 更新报告
    def put(self):
        tP = TestProject.query.filter(TestProject.tP_id == request.args['tPid']).first()
        config_path = os.path.join(BackendPath(), 'App', 'data', 'config', 'config_' + tP.tP_id + '.py')  # 配置文件路径
        # 更新报告命令
        command = 'conda run -n ' + current_app.config['conda_env'] + ' glupdate --config_path=' + config_path + \
                  ' --test_id=' + tP.tP_id + ' --logs_path=' + os.path.join(BackendPath(), 'App', 'data')
        print(command)
        try:
            subprocess.run(command, shell=True, capture_output=True, text=True, check=True, encoding='utf-8')
            return jsonify({'success': True})
        except subprocess.CalledProcessError as e:
            print(f"命令输出:{e.stdout}\n错误信息:{e.stderr}\n返回码:{e.returncode}")
            return jsonify({'success': False, 'message': str(e)})

    # 下载pdf报告
    def get(self):
        dir_r = os.path.join(BackendPath(), 'App', 'data', 'Logs', request.args['tPid'])  # 报告目录
        if request.args['choose'] == '1':  # 报告数量
            return jsonify(
                {'count': sum(1 for file in os.listdir(dir_r) if file.startswith('report-v')), 'success': True})
        if request.args['choose'] == '2':  # 报告路径
            return jsonify({'url': os.path.join('App', 'data', 'Logs', request.args['tPid'],
                                                'report-v' + request.args['n'] + '.pdf'), 'success': True})

    # 查询交互记录
    def delete(self):
        url = os.path.join(BackendPath(), 'App', 'data', 'Logs', request.args['tPid'], 'dialog.log')
        with open(url, 'r', encoding='UTF-8') as file:
            content = file.read()
        matches = re.compile(
            r'New Epoch ----------.*?INFO - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - INFO - '
            r'To LLM:	 (.*?)\n\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*?'
            r'To User:	 "(.*?)"\n(.*?)'
            r'(The model gets .*?)'
            r'(The final score of this testcase is (\d+\.\d+), in (.*?) field\.|Human Evaluation!)',
            re.DOTALL).findall(content)
        data = [{'time': m[0], 'Q': m[1], 'A': m[2], 'fin_score': m[6],
                 'keyword': re.compile(r'INFO - keyword:(.*?)\n', re.DOTALL).findall(m[3]),
                 'keywords_score': re.compile(r'The model gets (\d+\.\d+) points in this testcase by keywords method',
                                              re.DOTALL).findall(m[4]),
                 'llm_score': re.compile(r'The model gets (\d+\.\d+) points in this testcase by LLMEval method',
                                         re.DOTALL).findall(m[4]),
                 'blacklist_score': re.compile(r'The model gets (\d+\.\d+) points in this testcase by blacklist method',
                                               re.DOTALL).findall(m[4]),
                 'field': re.compile(r'method, in (.*?) field', re.DOTALL).findall(m[4])[0]
                 } for m in matches]
        return jsonify({'success': True, 'data': data})
