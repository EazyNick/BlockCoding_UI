
import sys
import os
import logging
from pathlib import Path
from datetime import datetime
import glob

LOG = None
TIMESTAMP = None
# _TMPPATH = r'C:\\'
# _HIMGTMP = os.path.join(_TMPPATH,"temp.png") 

def Init():
    """ Logger 초기화
    """
    _init_timestamp() # _TIMESTAMP에 현재 시간을 반환
    _init_logger() #  
    LOG.debug('Logger Init function called !!!')
    
    directory = 'D:\Python\SkillUp\BlockCoding_UI\Logger\Log'  # 로그 파일이 저장된 디렉토리 경로
    max_files = 15  # 유지하고 싶은 최대 파일 수

    clean_up_logs(directory, max_files)

def _init_timestamp():
    """ 타임스탬프 초기화
    """
    global _TIMESTAMP

    _TIMESTAMP = datetime.now().strftime(f"%Y%m%d-%H%M%S")

def _init_logger():
    """ 로거 초기화
    """
    global LOG
    logger = logging.getLogger('AUTOTOOL')

    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname).1s][%(filename)s(%(funcName)s):%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
    

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)


    print(f'실행한 파일명: {os.path.basename(sys.argv[0])}')
    
    #로그 저장 주소
    logfile = f"{getTimeStamp()}_{os.path.basename(sys.argv[0])}.log"
    logpath = f"{Path(__file__).parents[1]}\\Logger\\Log"
    if os.path.isdir(logpath) != True:
        os.makedirs(logpath)

    fileHandler = logging.FileHandler(logpath + '\\' + logfile, encoding='utf-8')
    print(fileHandler)
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    print(logger)
    logger.addHandler(fileHandler)
    print(logger)
    logger.propagate = False 
    LOG = logger
    LOG.setLevel(logging.DEBUG)

def getTimeStamp() -> str:
    """ 
    시작 타임스탬프 반환

    Returns:
    str: 타임스탬프
    """
    return _TIMESTAMP

# def getImageSavePath() -> str:
#     """ 이미지 임시 저장 위치 조회용 함수

#     Returns:
#         str: 이미지 임시 저장 경로; ex) "c:\\temp.png"
#     """
#     return _HIMGTMP

def clean_up_logs(directory, max_files):
    # 디렉토리 내의 특정 패턴의 파일 목록을 가져옵니다.
    files = glob.glob(os.path.join(directory, '*_main.py.log'))
    
    # 파일을 생성 시간에 따라 정렬합니다.
    files.sort(key=os.path.getmtime)

    LOG.debug('clean_up_logs')

    # 지정된 개수를 초과하는 파일이 있다면, 가장 오래된 파일부터 삭제합니다.
    while len(files) > max_files:
        os.remove(files.pop(0))  # 가장 오래된 파일을 삭제하고 목록에서 제거합니다.


Init()
LOG.setLevel(logging.DEBUG)
LOG.debug(__file__)
#LOG.debug(getImageSavePath())
# ()안의 값을 디버깅, 그대로 출력임
