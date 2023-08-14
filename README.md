# quick-linker-for-media-system
## 前言

众所周知，在媒体系统(EMBY、JellyFin、Plex)中，刮削对剧集文件的名称有一定要求，否则会影响刮削准确度。

但是直接修改文件名字又可能会影响后续做种，所以本脚本采用了**硬链接(hard link)**的方式来进行对剧集的“重命名”。

本脚本对于批量(两个以上)的剧集有较好的自动检测集数效果，可以根据集数自动地批量地进行硬链接及重命名。

本脚本仍处于测试阶段，如果有遇到bug请提交Issue或者联系作者(chrisis58@foxmail.com)，感激不尽！

## 特点

- 自动计算单集的集数
- 批量建立硬链接
- 不影响做种
- 监听模式可以实现自动化

## 使用

### 1. 下载项目代码

```shell
git clone https://github.com/Chr1sis/quick-linker-for-media-system.git
```

### 2. 检查依赖

本脚本依赖`Python`执行，作者使用的版本为3.9.6。

依赖库包括os，re，numpy和pyyaml，后两者可能需要额外安装。

```shell
pip install numpy pyyaml
```

### 3. 编写配置文件

配置文件使用YAML格式，(名字需要为`config.yaml`或者`config.yml`)的模板如下：

```yaml
config:
  watchdog:
    enable: <true | false, default to false>
    one-instance: <true | false, default to true>
tasks:
  <task1>:
    enable: <true | false, default to true>
    src: <task src path>
    dest: <task dest path>
    exclude: [<exclude>...]
    mute: [<mute>...]
    rename:
      enable: <true | false, default to true>
      name: <tv show name>
      season: <tv show season>
      meta: <tv show meta>
  <task2>:
   ...
```

- tasks.task
  - enable: 可选，是否启用该任务，默认为启用
  - src：必要，代表源文件所在目录
    - 注：脚本可以根据路径自动提取节目的部分信息，请务必按照`{path}/{tv name}/{season}/`的格式设置文件结构

  - dest：必要，代表目标目录
  - rename：可选，默认为不进行重命名
    - enable：可选，默认不进行重命名
    - name：可选，手动输入节目名字，默认由源文件目录获取
    - season：可选，手动输入节目季，默认由源文件目录获取
    - meta：可选，节目元信息，默认为空

  - exclude: 可选，在src目录下包含<exclude>的文件不会被包含进集数(episode)的计算，默认为空
  - mute：可选，在src目录下所有文件名中的<mute>都会被替换成空再进行集数的计算，默认为空
    - 例如：'abcba.mp4' ----mute('b')----> 'aca.mp4'

- config.watchdog
  - enable 可选，代表是否启用watchdog进行文件夹的监听，默认为不进行

  - one-instance 可选，是否启用单例模式(启动脚本时会自动关闭上次运行的脚本)，默认为启用


> 重命名的默认格式为`{name} - S{season}E{episode} - {meta}.{extension}`

以下为案例：

```yaml
tasks:
  mushoku:
    src: D:\Videos\Downloads\Mushoku Tensei\Season 02
    dest: D:\Videos\Bangumi\Mushoku Tensei\Season 02
    rename:
      enable: true
      meta: '[Sakurato][AVC-8bit 1080P@60FPS AAC][CHS]'
  eightysix:
    enable: false
    src: 'E:\download\Eitishikkusu\Season 01\[Sakurato][20210410] 86—Eitishikkusu— [01-23 Fin v2][TVRip][1080p][CHS&CHT]'
    dest: E:\Bangumi\Eitishikkusu\Season 01
    exclude: ['.zip']
    mute: ['v2']
    rename:
      enable: true
      name: 86—Eitishikkusu
      season: 1
      meta: '[Sakurato][HEVC-10bit 1080p AAC][CHS&CHT]'
   urusei_yatsura:
    src: 'E:\download\Urusei Yatsura(2022)\Season 01'
    dest: 'E:\Bangumi\Urusei Yatsura(2022)\Season 01'
    mute: ['2022', '[WebRip 1080p HEVC-10bit AAC ASSx2]']
    rename:
      enable: true
      name: Urusei Yatsura 2022
      season: 1
      meta: '[Nekomoe kissaten&LoliHouse][WebRip 1080p HEVC-10bit AAC ASSx2]'
```

### 4. 运行

运行前请保证配置文件(.yml或者.yaml)和脚本(.py)在同一目录下。

```shell
│
└───quick-linker-for-media-system
        config.yml
        quick-linker.py
```

直接运行py脚本即可。

### 5. 可能遇到的问题

- 如果发现脚本的做硬链接的结果与结果不符，可以直接删除目标目录下的文件后修改配置重新做硬连接。如果修改配置文件也无法按照预期运行，请提交Issue。
- 你只能在同一盘符下做硬链接(win10)
- 在集数较少(比如只有一集或者两集)的情况下本脚本对剧集的episode的判定准确率会有问题，可以添加tasks.task.mute来提高准确率
  - 例如：'Urusei Yatsura 2022 \[01]\[WebRip 1080p HEVC-10bit AAC ASSx2].mkv' \-\-mute('2022', '[WebRip 1080p HEVC-10bit AAC ASSx2]') \-\-> 'Urusei Yatsura [01].mkv'，这样可以大大提高准确率 
- 如果遇到无法启动的问题，请尝试将.py脚本同目录下的名为`pid`文件删除后重新运行
