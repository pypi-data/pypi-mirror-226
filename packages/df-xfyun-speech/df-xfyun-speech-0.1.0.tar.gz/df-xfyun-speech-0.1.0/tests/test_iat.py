#  -*- coding: UTF-8 -*-
from df_xfyun_speech import XfIat

appId = ""
apiKey = ""
apiSecret = ""

# 创建语音识别实例
iat = XfIat(appId, apiKey, apiSecret)
print("reuslt: ", iat.recognition("Hello.wav"))