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
        add_list = []
        item = outer_item["n"]

        add_list.append(item["elementId"])
        add_list.append(item["properties"]["name"])
        add_list.append(item["labels"][0])
        dd_list.append(add_list)
        print(item)

    f.close()

func('drug.json')
func('diabete_drug.json')
func('illness.json')
func('diabete.json')
func('diabete_complete.json')
func('record.json')
city = pd.DataFrame(dd_list, columns=['实体ID', '实体名称', '实体类别'])
city.to_csv(os.path.join(cur_dir,'entities.csv'),encoding='utf-8',index=False)