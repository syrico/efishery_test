import json, math
import collections, functools, operator
import regex as re
import pandas as pd
import sys

path_file = sys.argv[1]

f = open(path_file)

json_data = json.load(f)

def cleaning(text:str):
    text_clean_1 = re.sub(string=text,pattern=('ik\w+|dan|,|&'), repl=' ')
    text_clean_2 = re.sub(string=text_clean_1,pattern=('^\s+'), repl='')
    text_clean = re.sub(string=text_clean_2,pattern=('\s+'), repl=' ')
    return text_clean

def typo_correction(text:str):
    text_clean_1 = re.sub(string=text, pattern = r'jaer|mu\D+',
                            repl = 'mujair')
    text_clean_2 = re.sub(string=text_clean_1, pattern = r'ton\w+|tng\w+|tingkol|eton\w+',
                            repl = 'tongkol')
    text_clean_3 = re.sub(string=text_clean_2, pattern = r'ni\D+',
                            repl = 'nila')
    text_clean_4 = re.sub(string=text_clean_3, pattern = r'sakera\w+|kra\w+|ker\D+',
                            repl = 'kerapu')    
    text_clean_5 = re.sub(string=text_clean_4, pattern = r'ke\w+|le\D+',
                            repl = 'lele')  
    text_clean_6 = re.sub(string=text_clean_5, pattern = r'gura\D+',
                            repl = 'gurame')  
    text_clean_7 = re.sub(string=text_clean_6, pattern = r'mas|eem\w+',
                            repl = 'emas')      
    text_clean = re.sub(string=text_clean_7, pattern = r'dll|gore\D+|soto\D+|pin|kepala|sate|usus|nasi|uduk|tawr|man|pecel',
                            repl = '')  
    return text_clean                        

def parsing_values(text):
    text_clean_1 = cleaning(text)
    text_clean_2 = re.sub(string=text_clean_1, pattern='rata2|rata-rata|rata\w+',repl='')
    clean_text = re.sub(string=text_clean_2, pattern='s.d|sampai|sampe| - | -|- |', repl='-')
    return clean_text
    

li = []
for dict_ in json_data:
    data = (list(dict_.values()))
    
    keys = typo_correction(cleaning(data[0])).split(' ')

    values = re.findall(string=re.sub(string=re.sub(string=data[1], pattern='sampai|\ssam\w+\s|sam\w+\D|atau|s.d', repl='-'),
                    pattern = 'rata2|rata-rata',
                    repl = ''
                    ),
                    pattern =  r'(\d+(?:[-–]\d+(?:/\d+)?)?)\s*(?:kg)?(?:\s*\d+(?:\s*\d+/\d+)?)?'
                    )

    for a in range(len(values)):

        if '-' in values[a]:
            split_clean = re.sub(string=values[a],pattern='1/2', repl='0.5')
            split_list = [float(b) for b in split_clean.split('-')]
            avg_list = math.ceil(sum(split_list)/len(split_list))
            values[a]=avg_list
        else:
            values[a] = int(values[a])

    if len(keys)==len(values):
        dict_proses = dict(zip(keys, values))
        li.append(dict_proses)
    
    elif len(keys)>1 and len(values)==1:
        # print(keys)
        keys_to_proces=[]
        values_to_proces=[]
        for a in keys:
            if len(a)>1:
                keys_to_proces.append(a)
                values_to_proces.append(values[0])

        # print(keys_to_proces,values_to_proces)        
        dict_proses = dict(zip(keys_to_proces,values_to_proces))
        li.append(dict_proses)

            # values.extend(values)
        # print(values)

    

result = dict(functools.reduce(operator.add,
         map(collections.Counter, li)))

df = pd.DataFrame({'Jenis Ikan':result.keys(),
              'Jumlah':result.values()})
df.drop(df[(df['Jenis Ikan']=='')].index, inplace=True)
print(df.sort_values(by='Jumlah', ascending=False))
