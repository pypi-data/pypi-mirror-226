__all__ = ['XfIat', 'XfTts']

import hashlib
import base64
import hmac
import json
import ssl
import time
import threading
from urllib.parse import urlencode
import wave
import websocket

import os
import shutil

def convert_pcm_to_wav(pcm_file, wav_file, channels=1, sample_width=2, frame_rate=16000, frames=0, comptype="NONE", compname="NONE"):
    with open(pcm_file, 'rb') as pcm:
        pcm_data = pcm.read()

    with wave.open(wav_file, 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(sample_width)
        wav.setframerate(frame_rate)
        wav.setnframes(frames)
        wav.setcomptype(comptype, compname)
        wav.writeframes(pcm_data)

def print_err(sid, code, message):
    print("Session ID: ", sid)
    print("Error Code: ", code)
    print("Error Message: ", message)

class WebSocketConnection:
    # 是否空闲
    STATE_IDLE = "Idle"
    STATE_RUNNING = "Running"
    STATE_COMPLETED = "Completed"
    STATE_ERROR = "Error"

    def __init__(self, appId=str, apiKey=str, apiSecret=str, options:dict={}):
        self.appId = appId
        self.apiKey = apiKey
        self.apiSecret = apiSecret

        # 是否开发调试
        self.debug = options.get('debug', False)

        # 是否运行结束、结果如何标识符
        self.state = self.STATE_IDLE

        # 公共参数(common)
        self.common_args = { "app_id": self.appId }

    # 生成websocket url
    # 支持 iat 和 tts
    def create_url(self, tp=str):
        url = f"wss://{tp}-api.xfyun.cn/v2/{tp}"

        # 获取当前时间的秒数
        timestamp = int(time.time())
        # 使用 time 模块格式化时间戳为 RFC1123 格式
        date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(timestamp))

        # 拼接字符串
        signature_origin = "host: " + f"{tp}-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + f"/v2/{tp} " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.apiSecret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')

        # authorization_origin = f"api_key=\"{self.apiKey}\",algorithm=\"hmac-sha256\",headers=\"host date request-line\",signature=\"{signature_sha}\""
        authorization_origin = (
            f'api_key="{self.apiKey}",'
            f'algorithm="hmac-sha256",'
            f'headers="host date request-line",'
            f'signature="{signature_sha}"'
        )
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": f"{tp}-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print('websocket url :', url)
        return url

    def connect(self, url, on_message, on_open):
        ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_open=on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    # 收到websocket错误的处理
    # 已知 1.0.0 和 1.2.3 和 1.5.0 不会在正常程序运行中触发on error
    def on_error(self, ws, error):
        if '[Errno 11001] getaddrinfo failed' in str(error) or '[Errno -3] Temporary failure in name resolution' in str(error):
            print('Network is not available.')
        else:
            print("ws error: ", error)

    # 收到websocket关闭的处理
    def on_close(self, ws, close_status_code, close_msg):
        if close_status_code or close_msg:
            print("on_close args:")
            print("close status code: " + str(close_status_code))
            print("close message: " + str(close_msg))

    def get_status(self):
        return self.state

# 语音识别
class XfIat(WebSocketConnection):
    STATUS_FIRST_FRAME = 0  # 第一帧的标识
    STATUS_CONTINUE_FRAME = 1  # 中间帧标识
    STATUS_LAST_FRAME = 2  # 最后一帧的标识

    def __init__(self, appId:str, apiKey:str, apiSecret:str, options:dict={}):
        super().__init__(appId, apiKey, apiSecret, options)
        self.url = self.create_url("iat")
        self.result = ""

        # 业务参数(business)，更多个性化参数可在官网查看
        self.business_args = {
            "domain": "iat",
            "language": "zh_cn",
            "accent": "mandarin",
            "vinfo": 1,
            "vad_eos": 10000
        }

    def recognition(self, audio:str):
        self.result = ""
        if self.state == self.STATE_RUNNING:
            print("IAT process is already running.")
            return

        # 检查音频文件是否存在
        if not os.path.exists(audio):
            print(f"Audio file '{audio}' does not exist.")
            return

        websocket.enableTrace(self.debug)
        self.connect(self.url, on_message=self.on_message, on_open=lambda ws: self.on_open(ws, audio))
        return self.result

    # 收到websocket消息的处理
    def on_message(self,ws, message):
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            if code != 0:
                errMsg = message["message"]
                print_err(sid, code, errMsg)
            else:
                data = message["data"]["result"]["ws"]
                # print(json.loads(message))
                for i in data:
                    for w in i["cw"]:
                        self.result += w["w"]
        except json.JSONDecodeError as json_error:
            print("JSON decode error:", json_error)
        except KeyError as key_error:
            print("Key error:", key_error)
        except Exception as e:
            print("Receive message, but other exception:", e)

    def on_open(self, ws, audio:str):
        def run(*args):
            frameSize = 8000  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            data_format = {
                "status": self.STATUS_FIRST_FRAME, # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
                "format": "audio/L16;rate=16000",
                "encoding": "raw"
            }

            with open(audio, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    if not buf: data_format["status"] = self.STATUS_LAST_FRAME

                    data_format["audio"] = str(base64.b64encode(buf), 'utf-8')
                    data = {"data": data_format}

                    # 发送第一帧音频，带business 参数
                    if data_format["status"] == self.STATUS_FIRST_FRAME:
                        data["business"] = self.business_args 
                        data["common"] = self.common_args
                        # 进入中间帧，开始一直循环，直到最后一部分
                        data_format["status"] = self.STATUS_CONTINUE_FRAME

                    ws.send(json.dumps(data))

                    if data_format["status"] == self.STATUS_LAST_FRAME:
                        time.sleep(1)
                        break

                    # 模拟音频采样间隔
                    time.sleep(intervel)
            ws.close()

        threading.Thread(target=run).start()

# 语音合成
class XfTts(WebSocketConnection):
    MAX_TEXT_LENGTH = 8000  # 最大长度，根据需求调整

    def __init__(self, appId: str, apiKey: str, apiSecret: str, options: dict = {}):
        super().__init__(appId, apiKey, apiSecret, options)
        self.url = self.create_url("tts")

        # 配置业务参数(business)
        default_business_args = {
            "aue": "raw",
            "auf": "audio/L16;rate=16000",
            "vcn": "xiaoyan",
            "tte": "utf8"
        }
        self.business_args  = options.get('business_args ', default_business_args )

    def synthesis(self, text: str, path: str):
        temp_name = path + ".pcm"
        if self.state == self.STATE_RUNNING:
            print("TTS process is already running.")
            return

        if os.path.exists(path):
            # 目前采用覆盖
            # print(f"This {path} file already exists")
            os.remove(path)

        if os.path.exists(temp_name):
            # 删除临时文件
            os.remove(temp_name)

        # 确保文本长度不超过限制
        text_length = len(text.encode('utf-8'))
        if text_length > self.MAX_TEXT_LENGTH:
            raise ValueError(f"Text length {text_length} exceeds maximum limit of {self.MAX_TEXT_LENGTH} bytes")

        # 将文本进行编码并添加到 data 字典中
        data = {
            "status": 2,
            "text": base64.b64encode(text.encode('utf-8')).decode("utf-8")
        }

        self.state = self.STATE_RUNNING
        websocket.enableTrace(self.debug)
        self.connect(self.url, on_message=lambda ws, message: self.on_message(ws, message, path), on_open=lambda ws: self.on_open(ws, data))

    def on_message(self, ws:str, message:str, path:str):
        temp_name = path + ".pcm"
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]

            if code != 0:
                self.state = self.STATE_ERROR
                errMsg = message["message"]
                print_err(sid, code, errMsg)
            else:
                data = message["data"]
                audio = data["audio"]
                audio = base64.b64decode(audio)
                # 识别结果是否结束标识
                # 0：识别的第一块结果
                # 1：识别中间结果
                # 2：识别最后一块结果
                status = data["status"]
                with open(temp_name, 'ab') as f:
                    f.write(audio)

                if status == 2:
                    ws.close()
                    convert_pcm_to_wav(temp_name, path)
                    print(f"save file to {path}")
                    os.remove(temp_name)
                    self.state = self.STATE_COMPLETED

        except json.JSONDecodeError as json_error:
            print("JSON decode error:", json_error)
        except KeyError as key_error:
            print("Key error:", key_error)
        except Exception as e:
            print("Receive message, but other exception:", e)

    # 收到websocket连接建立的处理
    def on_open(self, ws, data):
        self.state = self.STATE_RUNNING
        body = {
            "common": self.common_args,
            "business": self.business_args ,
            "data": data
        }
        body = json.dumps(body)
        ws.send(body)