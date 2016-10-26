###Fake GPS Controller Requirement

1. 生成固定路径，指定位置，速度，是否往返，往返方式（直线往返，原路往返）
2. 控制走动的启停
3. 记录路径，记录gym位置

可以在任何位置自由的控制，gpx文件不能设置多个waypoint形成路径，通过autoClick不停的更新gpx文件

client不断从server获取waypoint数据，单用户state, state lock

####功能
1. 设置自动route，点是特殊route，默认route往返移动，可以设置为直线返回起始点
2. route挂起/重启，在某个点停下来/重新移动
3. route挂起/重启，在某个点附近200m自动扫描
	1. 扫描路径作为route一种，可以挂起/重启
	2. 默认返回到原route
4. route挂起/重启，手动控制移动方向，默认返回原route
5. 设置移动速度
6. 显示实际速度

####Issue
* 速度的度量
	1. 提前计算所有点，两点之间速度为1单位，不同的速度，移动不同数目的点数，速度不连续分等级
	2. 按需计算下一个点的位置，速度可连续