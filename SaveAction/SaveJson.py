import os
import json

def save_json(data):
    """
    data를 json 파일로 저장
    경로는 Data 하위에 생성됨
    """
    # directory 경로 조합
    dir_path = os.path.join(os.getcwd(), 'Data')
    
    # 해당 directory가 존재하지 않으면 생성
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    # 파일 경로 조합
    file_path = os.path.join(dir_path, 'nodes_state.json')
    
    # JSON 데이터를 파일에 저장
    with open(file_path, 'w') as file:
        json.dump(data, file)
    
    print(f'File saved: {file_path}')

# 사용 예시
if __name__ == '__main__':
    data = {'name': 'John Doe', 'age': 30, 'city': 'New York'}
    save_json(data)