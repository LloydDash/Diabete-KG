import sys
import yaml
import pandas as pd

class DiabetesData(object):

    def __init__(self, path:str) -> None:
        self.data = pd.read_excel(path)

    def load_medicine_dict(self, path:str) -> None:
        with open(path) as f:
            self.medicine = f.read().splitlines()

    def extract_medicine(self, refine_nbr:int, start_row:int=0) -> None:
        medicine_column = [[]]*len(self.data)
        try:
            for i, diagnosis in enumerate(self.data['出院带药'][start_row:]):
                medicine_list = []
                for medicine in self.medicine:
                    if diagnosis.find(medicine) != -1:
                        medicine_list.append(medicine)
                if len(medicine_list) < refine_nbr:
                    print(f'[row {i+start_row}] diagnosis: {diagnosis}\nmedicine_list: {medicine_list}')
                    new_medicine = input('enter new medicine: ').split(',')
                    if '' in new_medicine:
                        new_medicine.remove('')
                    self.medicine.extend(new_medicine)
                    medicine_list.extend(new_medicine)
                medicine_column[i] = medicine_list
        except KeyboardInterrupt:
            print('start to quit script')
        finally:
            self.data.insert(len(self.data.columns), '药品列表', medicine_column)

    def save_data_as(self, path:str) -> None:
        self.data.to_excel(path)

    def save_dict_as(self, path:str) -> None:
        with open(path, 'w') as f:
            for medicine in self.medicine:
                f.write(f'{medicine}\n')

if __name__ == '__main__':
    with open(sys.argv[1]) as stream:
        config = yaml.load(stream, yaml.Loader)
    diabetes = DiabetesData(config['data'])
    diabetes.load_medicine_dict(config['dict'])
    diabetes.extract_medicine(int(config['refine']), int(config['start_row']))
    diabetes.save_data_as(config['data_copy'])
    diabetes.save_dict_as(config['dict_copy'])