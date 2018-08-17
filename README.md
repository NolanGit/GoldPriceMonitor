# 监控国内黄金价格，一旦低于或高于期望值则发送邮件提醒和微信通知
## 特性：
* 在黄金开盘交易期间，每十秒获取一次价格（可自定义频率）。
* 如果低于期望值，发送邮件提醒买入；高于期望值则发送邮件提醒卖出（可自定义阈值）。
* 每小时至多只会发送一次邮件，晚上十二点之后休息时间不发送（可自定义时间范围）。
* 可设置多人接收邮件。
* 微信通知需要在程序中登陆网页版微信（目前不支持GUI）
* 本地需要：Chrome、selenium、chromedriver
## 邮件实图：
非常适合Apple Watch的显示，38mm都可以一屏显示完整#（捂脸）
![image](https://user-images.githubusercontent.com/27627484/42225981-68ba612a-7f10-11e8-9b86-207d17de8a89.png)
## GUI：
### 界面如下图所示
![image](https://user-images.githubusercontent.com/27627484/42225568-69dea59e-7f0f-11e8-9e21-45273129d6fa.png)
![image](https://user-images.githubusercontent.com/27627484/44244268-b29d7580-a205-11e8-9966-4dcbc2f36c91.png)
### 参数说明：
* Beginning Price：买入价格（用于计算收益）
* Amount：买入金额
* Email If Higher Than：如价格高于XX则发送邮件
* Email If Lower Than：如价格低于XX则发送邮件
* Sender Address：发送人地址（默认为QQ邮箱端口，如果需要修改需要自行修改源码）
* Sender Password：发送邮箱口令（非邮箱密码，获取口令方法见：[CSDN](https://blog.csdn.net/xxzhangx/article/details/76757817)，脚本运行后会将明文密码替换为\*，无隐私泄露烦恼）
* Receiver Address：接收人地址（多个接收邮箱以英文分号隔开）
* Current Status：运行状态（没什么用）
