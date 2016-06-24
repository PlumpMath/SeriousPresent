# SeriousPresent
An RPG game using Panda3D engine
## 日志模块

日志模块的名称是 serious_log,主要用来在需要的地方增加自己需要调试的信息。
发布前在每个函数的开始和结束出增加日志输出语句，以便在游戏过程中记录信息，以防游戏崩溃时可以查找问题来源。

### 具体用法

```py
import serious_log

log = serious_log.SeriousLog('testlog.dat')
log.log('debug','test')
```

以这个代码为例，引入模块，新建一个`SeriousLog`对象的实例，传进去的参数就是希望写入的日志文件的名称。
调用log方法，第一个参数是错误等级，第二个参数是希望打印的信息。
最后的结果会是这样：

```
2016-06-20 16:42:15,049 - serious_log.py:30 - debug - test
```

会显示该段代码运行的时间，运行的文件名称（调用该log的文件），错误等级，以及希望显示出来的信息。
