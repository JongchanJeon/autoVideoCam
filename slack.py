import slack_sdk

# 슬랙 메시지 전송 함수
def msgSend(msg):
    try:

        token = ""
        client = slack_sdk.WebClient(token=token)

        client.chat_postMessage(channel = "#camserver_log", text = msg)
            
    except Exception as e:
        print(e)


msgSend("test")
