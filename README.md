# Codeforces
利用 `python3` 编写的 Codeforces 助手

现有功能：

* 自动下载样例
* 一键测试样例
* 一键提交源码

![preview GIF](https://github.com/endiliey/idne/blob/master/preview.gif?raw=true)

## 安装

克隆仓库到本地
```bash
git clone https://github.com/AlessandroChen/Codeforces.git
```

创建虚拟环境和安装依赖 (直接运行安装脚本)

```bash
cd Codeforces
sudo bash install.sh
```

在 `utils/config.py` 设置用户名和密码
```python
username = "ababcba" # your codeforces username
password = "asdadas" # your password
```




## 使用
----------

进入虚拟环境

```bash
$ source env/bin/activate
```

下载样例 (例如下载 contest 1000)

```bash
$ parse
Please Enter Contest ID:
>> 1000
```

那将会看到当前目录下出现 文件夹 `1000`， 题目在其子文件夹

以 `A` 题为例

```bash
$ cd 1000/A
```

在这个文件夹下创建 `A.cpp` , 并在这里写代码
```bash
$ vim A.cpp
```

完成后可以用 ` ./test.sh` 检查是否通过样例
```bash
$ ./test.sh
```

如果想上传可以通过 `./submit.sh` 上传
```bash
$ ./submit.sh
```

## Credits

- [Codeforces Parser](https://github.com/johnathan79717/codeforces-parser)
- [Idne](https://github.com/endiliey/idne)
