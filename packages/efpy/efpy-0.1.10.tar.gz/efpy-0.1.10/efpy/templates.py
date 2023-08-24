# 执行实验的模板
import os
import sys

import efpy as tef


class ExpTemplate(object):

    def __init__(self, workSpaceDir, taskConfigName, bgConfigName="bgConfig.yaml", isShowConfig=True):
        self.workSpaceDir = workSpaceDir
        self.bgConfigName = bgConfigName
        self.taskConfigName = taskConfigName
        self.isShowConfig = isShowConfig

    def setPakPath(self):
        # TODO 设置包的路径
        pass

    # 获取实验参数设置param
    def getExpParam(self):
        # TODO 获取本地参数
        # 实验参数分为背景级参数（命名为bgConfig.yaml），任务级参数（与pyName具有相同前缀，后缀由scp.py替换为config.yaml）以及本地参数（保存在param变量）
        # 三者的优先级顺序分别是 本地参数 > 任务级参数 > 背景级参数。优先级高的会覆盖优先级低的参数
        # 本地参数在分布式实验环境下由tef获取，在非分布式环境下可以直接设置
        # ！注意：层次性的参数不得连续包含下划线符号“_”，因为连续两个下划线符号“__”在后续会被解析为层次引用中的“.“
        if tef.isExpEnv():
            param = tef.getParams();
        else:
            param = None
        return param

    # 根据解析后的实验参数theConfig来执行实验，并返回一个实验结果
    def execExp(self,theConfig):
        # TODO 执行实验的代码
        return None

    # 实验执行条件是否满足，不满足即退出程序
    def expExecCond(self):
        # TODO 设置实验执行的条件
        return True

    def run(self):
        # 获取实验参数设置param
        param = self.getExpParam();
        # 实验执行条件是否满足，不满足即退出程序，并在分布式实验环境输出空实验结果
        if not self.expExecCond():
            if tef.isExpEnv():
                tef.printResult({})
            sys.exit(0)

        # 修饰实验参数设置param
        param = self.modExpParam(param)

        # 构建实验参数过程如下：
        # 得到pid，默认为0
        if 'pid' in param:
            pid = param['pid']
            del param['pid']
        else:
            pid = 0

        # 解析param中的聚合索引（格式为aggr_%d）
        # 一个聚合索引中包含多个实验参数的设置
        # 如"aggr_1":[{"dp_config__clientT":4096,"dpcr_model__args__kOrder":12},...]就表示一个实验同时设置实验参数dp_config__clientT和dpcr_model__args__kOrder
        param = tef.unpackAggrParam(param)
        # 将param值解析为层次参数结构，其中索引值内的连续下划线符号“__”会被解析为层次引用中的“.“
        varSettings = tef.convParam2Setting(param)
        # 构建实验参数
        theConfig = tef.loadSettingFromYaml(os.path.join(self.workSpaceDir, self.bgConfigName),
                                            os.path.join(self.workSpaceDir, self.taskConfigName),
                                            activeDynamicYamlId=pid, param=param, isOptionParse=True)

        # 解析动态引用
        theConfig = tef.parseConfigRef(theConfig)
        if 'optionRef' in theConfig:
            del theConfig['optionRef']
        # 移除实验参数中的空值项
        tef.removeNoneSetting(theConfig)

        # 展示实验参数
        if self.isShowConfig == True:
            print('完整参数内容信息如下：')
            for key in theConfig:
                print({key: theConfig[key]});
            if not varSettings is None and len(varSettings) > 0:
                print('其中，被本地参数修正的内容如下：')
                for key in varSettings:
                    print({key: varSettings[key]});
            else:
                print('本地参数无修正内容。')

        # 执行实验
        results = self.execExp(theConfig);

        # 输出实验结果
        if tef.isExpEnv():
            tef.printResult(results)
