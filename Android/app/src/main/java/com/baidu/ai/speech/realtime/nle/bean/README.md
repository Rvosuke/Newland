在Android项目中，`Bean`文件夹通常用于存放数据模型类，也称为**POJO**（Plain Old Java Object）类。
本目录下的文件如`UserBean.java`、`BaseBean.java`、`UserInfoBean.java`，是用来封装数据的，以下是它们的常见作用：

1. **`UserBean.java`**：
    - 这个类通常用来表示用户的基本信息。例如，`UserBean`可能包含用户的ID、姓名等属性。
    - 这些属性通常会有对应的`getter`和`setter`方法，用于访问和修改数据。

2. **`BaseBean.java`**：
    - 这个类通常作为其他Bean类的基类（父类），定义一些所有Bean类都会用到的通用属性或方法。例如，状态码、消息信息、时间戳等。
    - 继承自`BaseBean`的类可以复用这些通用的属性或方法，避免代码重复。

3. **`UserInfoBean.java`**：
    - 这个类可能是一个更加详细的用户信息类，包含`UserBean`之外的更多用户信息。例如，可能包括用户的地址、电话号码、年龄等。
    - 有时`UserInfoBean`可能会包含`UserBean`作为其一个属性，以扩展用户信息的层次。

### 总结
这些`Bean`类的主要作用是作为数据的载体，在应用的不同部分之间传递数据。
通过这种方式，数据可以被封装、保护，并且方便在不同的组件之间使用。