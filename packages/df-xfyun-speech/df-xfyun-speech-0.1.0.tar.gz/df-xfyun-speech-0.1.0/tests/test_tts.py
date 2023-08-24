#  -*- coding: UTF-8 -*-
from df_xfyun_speech import XfTts


appId = ""
apiKey =""
apiSecret = ""
businessArgs = {"aue":"raw","vcn":"xiaoyan","tte":"utf8","speed":50,"volume":50,"pitch":50,"bgs":1}
options["business_args"] = businessArgs
tts = XfTts(appId, apiKey, apiSecret, options)
tts.synthesis("你好, 世界", "Hello.wav")