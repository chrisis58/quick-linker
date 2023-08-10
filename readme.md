# 前言

众所周知，在媒体系统(EMBY、JellyFin、Plex)中，刮削对剧集文件的名称有一定要求，否则会影响刮削准确度。

但是直接修改文件名字又可能会影响后续做种，所以本脚本采用了**硬链接(hard link)**的方式来进行对剧集的“重命名”。

本脚本对于批量(两个以上)的剧集有较好的自动检测集数效果，可以根据集数自动地批量地进行硬链接及重命名。

本脚本仍处于测试阶段，如果有遇到bug请提交Issue或者联系作者(chrisis58@foxmail.com)，感激不尽！

# 使用

## 1. 下载项目代码

使用git的clone命令或者git网页版下载。

## 2. 检查依赖

本脚本依赖`Python`执行，作者使用的版本为3.9.6。

依赖库包括os，re，numpy和pyyaml，后两者可能需要额外安装。

```shell
pip install numpy pyyaml
```

## 3. 编写配置文件

配置文件(名字需要为`config.yaml`或者`config.yml`)的模板如下：

```yaml
tasks:
  <task1>:
    src: <task src path>
    dest: <task dest path>
    rename:
      enable: <do rename or not, default to false>
      name: <tv show name>
      season: <tv show season>
      meta: <tv show meta>
  <task2>:
   ...
```

- src：必要，代表源文件所在目录
  - 注：脚本可以根据路径自动提取节目的部分信息，请务必按照`{path}/{tv name}/{season}/`的格式设置文件结构
- dest：必要，代表目标目录
- rename：可省略，默认为不进行重命名
  - enable：可省略，默认不进行重命名
  - name：可省略，手动输入节目名字，默认由源文件目录获取
  - season：可省略，手动输入节目季，默认由源文件目录获取
  - meta：可省略，节目元信息，默认为空

> 重命名的默认格式为`{name} - S{season}E{episode} - {meta}.{extension}`

以下为案例：

```yaml
tasks:
  mushoku:
    src: D:\Videos\Downloads\Mushoku Tensei\Season 02
    dest: D:\Videos\Bangumi\Mushoku Tensei\Season 02
    rename:
      enable: true
      name: Mushoku Tensei
      season: 2
      meta: '[Sakurato][AVC-8bit 1080P@60FPS AAC][CHS]'
  zom100:
    src: D:\Videos\Downloads\Zom 100 Zombie ni Naru made ni Shitai\Season 01
    dest: D:\Videos\Bangumi\Zom 100 Zombie ni Naru made ni Shitai\Season 01
    rename:
      enable: true
      name: 僵尸百分百～变成僵尸之前想做的100件事～
      season: 1
      meta: '[ANi][1080P][Baha][WEB-DL][AAC AVC][CHT]'
```

## 4. 运行

运行前请保证配置文件(.yml或者.yaml)和脚本(.py)在同一目录下。

直接运行py脚本即可。

## 5. 可能遇到的问题

- 如果发现脚本的做硬链接的结果与结果不符，可以直接删除目标目录下的文件后修改配置重新做硬连接。如果修改配置文件也无法按照预期运行，请提交Issue。
- 你只能在同一盘符下做硬链接(win10)