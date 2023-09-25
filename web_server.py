# -*- coding: utf-8 -*-
# @Time : 2021/10/25 15:05
# @Author : huangkai
# @Email : huangkai@mucfc.com

import sys
import requests
import numpy as np
from gensim.models.word2vec import Word2Vec
import tornado.httpserver
import yaml
from keras.models import model_from_yaml
np.random.seed(1337)  # For Reproducibility
import sys
import main
sys.path.append("../")
sys.path.append("../utils")

import tornado.ioloop
import tornado.web
import tornado.httpclient
import json
from utils.data_helper import base_logger, DataProcessors
# env_list = get_option_values("post_server")
# if FLAGS.env not in env_list:
#     raise Exception("请输入正确的环境（int/test/prd中的一种）")

# 获取post地址
# post_server = get_config_values("post_server", FLAGS.env)
# base_logger.info("connect post_server is: %s" % (post_server))
# 初始化全局类
# dat = Data(FLAGS.env)
dp = DataProcessors()

# filter = Filter()


# 聚类工作池服务
# def es_update():
#     # 是否 全量更新es子问题
#     try:
#         base_logger.info("start es full sub question update")
#         eu = Es_Update()
#         eu.update_total_sub_question()
#         base_logger.info("update success ")
#     except Exception as e:
#         base_logger.info(str(e))
# def __init__(self):
print('loading model......')
with open('model/lstm.yml', 'r') as f:
    yaml_string = yaml.load(f, yaml.FullLoader)
model = model_from_yaml(yaml_string)
w2v_model = Word2Vec.load('model/Word2vec_model.pkl')
print('loading weights......')
model.load_weights('model/lstm.h5')


def test():
    print('this is a test')
    # sleep(100)


class ClusterPoolHandler(tornado.web.RequestHandler):

    def post(self):
        self._process()

    def _process(self):
        try:
            # 此处执行具体的任务

            cust_id = self.get_argument("cust_id")
            text = self.get_argument("text")
            # start_time = self.get_argument("start_time")
            # end_time = self.get_argument("end_time")

            if not cust_id or not text:
                raise Exception('必填参数为空')
            # base_logger.info("聚类处理的sn编号是：%s，阈值是：%s" % (sn, thres))

            # 聚类分析
            # 获取数据

            # df =df.sample(frac=0.05)
            # 若查询数据为空直接返回空列表
            # 匹配主问题,返回语义匹配值
            result = main.lstm_predict(text, model, w2v_model)
            # 新问题发现
            # json_data = ca.new_question_cluster(sn, partition_df, feature_matrix, thres)
            # json_data["sub_question"] = sub_json
            reply_idx = ["text", "result"]
            # print(result)
            json_data = dict(zip(reply_idx, list(result)))
            # 异步post方式将结果数据返回给kdb接口

            # url = "http://" + post_server + "/robotkdb/cluster/receiveClusterResult"
            # base_logger.info("Post回调地址：%s" % (url))

            # 将数据转换为json格式
            json_data = json.dumps(json_data, ensure_ascii=False)
            # headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
            # res = requests.post(url, data=data.encode("utf-8"), headers=headers)
            # base_logger.info("回调执行结果为：%s" % (res.text))
            base_logger.info(f"trans params are##{cust_id}##{text}##,result is ##{json_data}")
            length = 4
            list_num = np.arange(0, 100)
            num_l = len(list_num)
            # loop_n = num_l // length
            i = 0
            # tmp_dic = {}

            self.write(json_data)
            self.write("\n")
            # self.write(json_data+"v2")
            # self.write(json_data + "v3")
            self.finish()


        except Exception as e:
            # url = "http://" + post_server + "/robotkdb/cluster/receiveClusterResult"
            json_data_res = {"message": str(e), "cust_id": cust_id}
            data_res = json.dumps(json_data_res, ensure_ascii=False)
            # headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
            # res = requests.post(url, data=data_res.encode("utf-8"), headers=headers)
            #
            # base_logger.info("异常信息：%s" % (json_data_res))
            # json_data = {"object": "", "msg": str(e), "success": False}
            self.write(data_res)


# 创建web服务
class WebServerApplication(object):
    def __init__(self, port):
        self.port = port
        self.settings = {"debug": False}

    def make_app(self):
        """ 构建Handler
        (): 一个括号内为一个Handler
        """
        return tornado.web.Application(
            [(r"/emotion", ClusterPoolHandler)],
            **self.settings
        )

    def process(self):
        """ 构建app, 监听post, 启动服务 """
        app = self.make_app()
        app.listen(self.port)
        tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    # 定义服务端口
    server_port = 9008
    base_logger.info('==========================start emotion server==========================')
    server = WebServerApplication(server_port)

    # tornado.ioloop.PeriodicCallback(es_update, 604800000).start()  # 一周604800000

    server.process()
