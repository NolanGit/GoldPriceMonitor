# 监控国内黄金价格，一旦低于或高于期望值则发送邮件提醒
* 在黄金开盘交易期间，每十秒获取一次价格。
* 如果低于期望值，发送邮件提醒买入；高于期望值则发送邮件提醒卖出。
* 每小时至多只会发送一次邮件，晚上十二点之后休息时间不发送。
* 可设置多人接收邮件。
