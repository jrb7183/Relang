import json
import sys

# Add phoneme correspondences to the json
def jsonify(path) -> None:
    corresp_dict = {}
    if path:
        with open(path, 'r') as f:
            corresp_dict = json.load(f)

    with open("utils/tempIPAHex.txt", "r", encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        temp_lst = line[:-1].split("	")
        if temp_lst[0] not in corresp_dict:
            print(temp_lst)
            corresp_dict[temp_lst[0]] = temp_lst[1]

    new_json = json.dumps(corresp_dict)
    if not path:
        with open("utils/correspondences.json", 'w') as g:
            g.write(new_json)

    else:
        with open(path, 'w') as h:
            h.write(new_json)

if __name__ == "__main__":
    path = ''
    if len(sys.argv) > 1:
        path = sys.argv[1]
    jsonify(path)
    