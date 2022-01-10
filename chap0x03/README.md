# HTTP代理服务器实验

## 实验目的：

探究使用http代理服务器访问HTTPS站点时，代理服务器是否能获知通信传输内容.



## 实验环境：

* 主机：Windows 10； Chrome浏览器
* 虚拟机：Kali-Linux-2021.2-virtualbox-amd64
* 使用工具：tinyproxy；wireshark；SwitchyOmega(Chrome.ver)



## 实验过程：

### 1.使用tinyproxy搭建代理服务器

​	**(1)安装tinyproxy:**

```bash
sudo apt-get update && sudo apt install tinyproxy
```

​	**(2)编辑tinyproxy配置文件取消允许访问的网段注释:**

```bash
sudo vim /etc/tinyproxy/tinyproxy.conf
```

因为此处我选择的连接代理的方式是我的NAT网卡 **(其IP为10.0.2.15) ** ,因此我取消了10.0.0.0/8这一网段的注释

![change-config](D:\Code\Net_Security\chap0x03\img\change-config.png)

然后开启tinyproxy服务:

```bash
sudo systemctl start tinyproxy && sudo systemctl status tinyproxy
# 如果是kali则可以不使用sudo,因为kali会自动询问密码
```

![tinyproxy-on](D:\Code\Net_Security\chap0x03\img\tinyproxy-on.png)



**(3)设置kali虚拟机联网方式:**

设置虚拟机的网卡为NAT网卡设置端口转发, 默认tinyproxy监听8888端口:

![net-setting](D:\Code\Net_Security\chap0x03\img\net-setting.png)



**(4)设置SwitchyOmega使浏览器挂载代理:**

先下载SwitchyOmega插件: [SwichyOmega官网下载](https://proxy-switchyomega.com/download/) 本实验使用Chrome版本

下载完成后在chrome的扩展程序中,点击SwitchyOmega设置代理信息:

![proxy](D:\Code\Net_Security\chap0x03\img\proxy.png)

点左侧 `应用选项` 保存设置, 并启用SwitchyOmega

![proxy-on](D:\Code\Net_Security\chap0x03\img\proxy-on.png)

代理服务器设置完成.



### 2.Wireshark分析HTTP代理流量:

作为代理服务器的网卡是对应虚拟机的 `eth0` 因此使用wireshark对相应网卡进行抓包.

**(1)对 `eth0` 抓取的流量使用 `http.request.method eq CONNECT 查看所有HTTPS代理请求`**

![http](D:\Code\Net_Security\chap0x03\img\http.png)

对我们代理服务器获取的包进行follow:

![follow-http](D:\Code\Net_Security\chap0x03\img\follow-http.png)

追踪http流发现，访问bilibili时使用的最初并不是https协议，而是http,而且其中的内容几乎完全透明.

**(2)对 `eth0` 抓取的流量使用 `http.request.method eq GET 查看所有HTTP GET代理请求`**

![no-get](D:\Code\Net_Security\chap0x03\img\no-get.png)

很奇怪,抓了三次都没有一个get包, 我甚至开着代理看了俩视频了



**(3)使用wireshark提取pcap包中的SSL证书:**

- wireshark首选项中确认TCP协议的Allow subdissector to reassemble TCP streams选项处于启用状态

  ![ssl-1](D:\Code\Net_Security\chap0x03\img\ssl-1.png)

- 通过显示筛选过滤规则（例如：tcp.port == 443），找到SSL会话

- ![ssl-2](D:\Code\Net_Security\chap0x03\img\ssl-2.png)

- 通过packet list里的info列找到Certificate

  - 在packet details面板里依次展开Handshake Protocol: Certificate --> Certificates，如果有多个证书，会看到多个默认折叠起来的Certificate

    ![ssl-3](D:\Code\Net_Security\chap0x03\img\ssl-3.png)

  - 右键选中Certificate，在右键菜单里使用Export Selected Packet Bytes功能即可导出DER格式的[SSL证书](/packets/certificate.der)

- 使用openssl命令行工具解析DER证书 openssl x509 -in xxx.der -inform der -text -noout

  最后得到解码出的证书内容: [ssl.txt](/packets/ssl.txt)



## 实验结论:

代理服务器建立http连接并不安全。

如果该代理服务器是恶意第三方的代理，那么存在用户信息泄露的风险。

## 参考资料:

[教学文档](https://github.com/c4pr1c3/cuc-ns/blob/master/chap0x03/exp.md)