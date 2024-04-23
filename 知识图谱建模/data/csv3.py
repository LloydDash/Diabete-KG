import pandas as pd

import os
cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])

dd_list = []

def func(file):
    data_path = os.path.join(cur_dir,file)

    f = open(data_path,encoding='utf-8')

    import json
    data= json.load(f)

    for outer_item in data:
        seg = outer_item["p"]["segments"]
        for item in seg:
            add_list = []
            add_list.append(item["start"]["elementId"])
            add_list.append(item["relationship"]["type"])
            add_list.append(item["end"]["elementId"])
            dd_list.append(add_list)

        print(item)

    f.close()

func('relationship.json')
city = pd.DataFrame(dd_list, columns=['头实体ID', '尾实体ID', '实体关系'])
city.to_csv(os.path.join(cur_dir,'relationships.csv'),encoding='utf-8',index=False)