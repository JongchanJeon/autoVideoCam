import time
import threading
from cam import useCamera

CAMERACOUNT = 1

def main():
    try:

        # 카메라 수에 따라 스레드를 생성합니다. 
        threads = []
        for index in range(CAMERACOUNT): 
            thread = threading.Thread(target=useCamera, args=(index,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    except Exception as e:
        print(e)
                


if __name__ == "__main__":

    main()
