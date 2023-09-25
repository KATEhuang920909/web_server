# web_server
基于tornado构建的情感分析服务框架

​		一个简单的模型服务测试框架，模型是情绪识别，基于word2vec+lstm训练。

​		训练之后的模型文件包括：

- word2vec文件：Word2vec.pkl，文件较大，可自行训练
- 参数文件、网络框架文件：lstm.h5和lstm.yml

------

加载服务脚本：

```python
python web_server.py
```

postman 测试

格式如下：

*http://localhost:9008/emotion?cust_id=23578365u&text=一般般*

postman输出：

`{"text": "一般般", "result": " negative"}`

后台日志输出：

`
trans params are##23578365u##一般般##,result is ##negative`
