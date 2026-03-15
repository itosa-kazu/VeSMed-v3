---
name: 只杀Flask进程不要杀全部Python
description: 重启Flask时只杀占用5000端口的进程，不要taskkill所有python.exe，因为用户有其他Python项目（NiceGUI on 8088）在跑
type: feedback
---

重启Flask服务器时，**绝对不要**用 `taskkill //F //IM python.exe`，这会杀掉用户所有的Python进程。

正确做法：只杀占用5000端口的进程：
```bash
netstat -ano | grep :5000 | grep LISTENING
taskkill //F //PID <具体PID>
```

原因：用户旁边有NiceGUI项目跑在8088端口，之前被误杀过。
