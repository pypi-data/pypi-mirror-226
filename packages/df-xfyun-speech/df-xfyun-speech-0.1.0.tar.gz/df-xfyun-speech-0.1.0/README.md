# DF-XFYUN-SPEECH

基于[语音听写（流式版）](https://www.xfyun.cn/doc/asr/voicedictation/API.html) 和 [语音合成（流式版）](https://www.xfyun.cn/doc/tts/online_tts/API.html) 的API来封的Python库

## 如何获取APPID\APISecret\APIKey

1. 使用手机号登录\注册[讯飞开放平台](https://console.xfyun.cn/)
2. 创建新的应用
3. 打开想要体验的API的控制台(例如: [语音听写（流式版）](https://console.xfyun.cn/services/iat)的控制台)

> 相关信息如下:

[![如何获取?](https://s1.ax1x.com/2023/08/24/pPYHcNR.png)](https://imgse.com/i/pPYHcNR)

## 示例

### 识别语音

```python
#  -*- coding: UTF-8 -*-
from df_xfyun_speech import XfIat

appId = ""
apiKey = ""
apiSecret = ""

# 创建语音识别实例
iat = XfIat(appId, apiKey, apiSecret)
print("reuslt: ", iat.recognition("Hello.wav"))
```

> 更多参数请自行查看[文档](https://www.xfyun.cn/doc/asr/voicedictation/API.html)

### 语音合成

```python
#  -*- coding: UTF-8 -*-
from df_xfyun_speech import XfTts


appId = ""
apiKey =""
apiSecret = ""
businessArgs = {"aue":"raw","vcn":"xiaoyan","tte":"utf8","speed":50,"volume":50,"pitch":50,"bgs":1}
options["business_args"] = businessArgs
tts = XfTts(appId, apiKey, apiSecret, options)
tts.synthesis("你好, 世界", "Hello.wav")
```

> 更多参数请自行查看[文档](https://www.xfyun.cn/doc/tts/online_tts/API.html)