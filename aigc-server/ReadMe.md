1.说明
配置文件在etc/config.yaml中
port: 网关服务端口号, 默认配置8991,可以更改.如果此处port更改, 则global.sh中的por也需要改成与该配置文件中同样的即可.
redis-cluster:
  -
    host: 
    port: 
  -
    host: 
    port: 
  -
    host: 
    port: 
  -
    host: 
    port: 
  -
    host: 
    port: 
  -
    host: 
    port: 

redis-password: 
robot_pub: AI中控公钥
robot_private: AI中控私钥
micro_pub: 微客服中控公钥
micro_private: 微客服中控私钥
bot_url: 追一机器人问答接口
version: 1 版本号为1,则走追一机器人新版本. 版本号为零, 则走追一机器人老版本
robot_url: 追一机器人老版本AI中控地址
micro_url: 追一机器人老版本微客服地址

2.启动
	执行start.sh
	查看nohup.out,出现 "BotApiGateWay server start end"则启动成功
3.停止
	执行sotp.sh即可