# BalancebyEinck
背景
由于steam市场交易需要大量手续费且不可提现，便有了更为便宜的第三方交易平台。因为自由的市场交易，使得在不同平台中部分饰品即使扣除买卖的手续费仍然有着较大的差距，这就有了一定的利润空间。
程序目标
爬取第三方交易平台BUFF的售价并与steam最低售价进行比较
主要思路参考https://blog.csdn.net/weixin_43271108/article/details/106713402

访问https://buff.163.com/登陆BUFF后按F12打开开发者工具，选中网络+标头，刷新页面，找到Cookie和User-Agent
![image](https://user-images.githubusercontent.com/91471683/206141643-650b3222-e04c-44e6-ba59-245e908f3f1a.png)

