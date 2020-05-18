# Create_MODTRAN5_tape5
创建MODTRAN5中tape5文件

MODTRAN5文档可通过搜索引擎搜到

使用TIGR大气廓线，1到872是热带，873到1260是中纬度夏季，1261到1614是中纬度冬季，1615到1718是极地夏季，1719到2311是极地冬季

dsf文件里是TIGR大气廓线数据

注意需要用马格努斯饱和水汽压公式计算饱和水汽压，从而得到RH相对湿度

TIGR中臭氧混合比是（g/g），tape5中是（g/kg），需要乘1000

创建完后每条大气廓线对应一个tape5文件，需要在mod5root.in中添加tape5绝对路径，然后可RUN

总透过率会积分在tape6文件中而不是plt文件中，可以用正则表达式提取 AVERAGE TRANSMITTANCE那行中的总透过率

![image](https://github.com/Tatjanaya/Create_MODTRAN5_tape5.git/TIGR.png)
