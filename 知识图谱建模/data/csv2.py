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
        item = outer_item["n"]

        property = item["properties"]
        for p in property:
            add_list = []
            add_list.append(item["elementId"])
            add_list.append(p)
            add_list.append(property[p])
            dd_list.append(add_list)
        print(item)

    f.close()

func('record.json')
city = pd.DataFrame(dd_list, columns=['实体ID', '实体属性', '实体属性值'])
city.to_csv(os.path.join(cur_dir,'entities_attr.csv'),encoding='utf-8',index=False)