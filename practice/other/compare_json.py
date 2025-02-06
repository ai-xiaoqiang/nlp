import json
from typing import Dict, List, Set

def load_json_file(file_path: str) -> Dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_differences(response1: Dict, response2: Dict) -> List[Dict]:
    differences = []
    
    # 检查两个方向的差异
    for key, value in response2.items():
        if key not in response1:
            # 新增字段
            if isinstance(value, list):
                differences.append({key: value})
            else:
                differences.append({key: value})
        elif response1[key] != value:
            # 修改的字段
            if isinstance(value, list) and isinstance(response1[key], list):
                diff_items = [item for item in value if item not in response1[key]]
                if diff_items:
                    differences.append({key: diff_items})
            elif not isinstance(value, list):
                differences.append({key: value})
    
    # 检查在response1中存在但在response2中不存在的字段
    for key, value in response1.items():
        if key not in response2:
            if isinstance(value, list):
                differences.append({key: value})
            else:
                differences.append({key: value})
        elif response2[key] != value:
            if isinstance(value, list) and isinstance(response2[key], list):
                diff_items = [item for item in value if item not in response2[key]]
                if diff_items:
                    differences.append({key: diff_items})
    
    return differences

def compare_api_json(file1_path: str, file2_path: str) -> Dict:
    json1 = load_json_file(file1_path)
    json2 = load_json_file(file2_path)
    
    result = {}
    
    for url1, content1 in json1.items():
        for url2, content2 in json2.items():
            if content1.get('originUrl') == content2.get('originUrl'):
                url = content1['originUrl']
                response1 = content1.get('response', {})
                response2 = content2.get('response', {})
                
                # 找出所有差异
                differences = find_differences(response1, response2)
                if differences:
                    result[url] = differences
    
    return result

def main():
    file1_path = '/Users/bailongma/Desktop/bosProxyMapN1-swagger.json'
    file2_path = '/Users/bailongma/Desktop/bosProxyMapV8.json'
    
    try:
        differences = compare_api_json(file1_path, file2_path)
        print(json.dumps(differences, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()