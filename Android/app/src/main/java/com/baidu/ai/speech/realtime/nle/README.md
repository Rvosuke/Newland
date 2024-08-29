# NewLandEdu(NLE) 用户登录

本目录中是NLE登录逻辑的实现，我们基于NewLand Cloud平台，设计了简单的通信逻辑。

## 各文件内容

NleManager中包含了登录逻辑，类中的构造函数就会构建一个retrofit实例，并设计了doLogin方法，来验证用户名和密码是否正确.
