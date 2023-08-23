import json
import pandas as pd
import re

class JsonDataHandler:

    def __init__(self, json_file):
        self.json_file = json_file    

    def read_data(self):
        with open(self.json_file, 'r') as f:
            data = json.load(f)
        return data

    def process_data(self, data):
        # ... (your existing process_data logic)
        # convert data to dataframe
        df = pd.DataFrame(data)
        df = df[['data', 'annotations']]
        df = df.explode('annotations')
        df = df.reset_index(drop=True)

        # convert annotations to dataframe
        df = pd.concat([df.drop(['annotations'], axis=1), df['annotations'].apply(pd.Series)], axis=1)
        df = df[['data', 'result']]
        df = df.explode('result')
        df = df.reset_index(drop=True)

        # get values from data column
        df = pd.concat([df.drop(['data'], axis=1), df['data'].apply(pd.Series)], axis=1)

        # get values from result column
        df = pd.concat([df.drop(['result'], axis=1), df['result'].apply(pd.Series)], axis=1)
        df = df[['text', 'value']]
        df.rename(columns={'text': 'text1'}, inplace=True)

        # get values from value column
        df = pd.concat([df.drop(['value'], axis=1), df['value'].apply(pd.Series)], axis=1)
        df = df[['text1', 'text', 'start', 'end', 'labels']]
        df.rename(columns={'text1':'text', "start":"begin", 'text': 'chunk'}, inplace=True)
        df.dropna(subset=['labels'], inplace=True)
        

        #extract values from the df.labels column
        df['labels'] = df['labels'].apply(lambda x: x[0])

        # give unique id to each text
        df['id'] = pd.factorize(df['text'])[0] + 1
        
        df.begin = df.begin.astype(int)
        df.end = df.end.astype(int)
        df.id = df.id.astype(int)
        
        return df
#*************************************************************************************
import pandas as pd
import re

class TextChunkExtractor:
    def __init__(self, data, mydict):
        self.df = pd.DataFrame(data)
        self.mydict = mydict

    @staticmethod
    def extract_info(text, chunk):
        positions = [(m.start(), m.end()) for m in re.finditer(re.escape(chunk), text)]
        return positions

    def process_text(self, text, unique_text_id):
        results = []
        for label, chunks in self.mydict.items():
            for chunk in chunks:
                extracted_positions = self.extract_info(text, chunk)
                results.extend([{
                    'id': unique_text_id,
                    'text': text,
                    'begin': begin,
                    'end': end,
                    'chunk': chunk,
                    'labels': label
                } for begin, end in extracted_positions if not any(
                    (result['begin'] <= begin < result['end'] or result['begin'] < end <= result['end'])
                    for result in results)])
        return results

    def extract_chunks(self):
        extracted_results = []
        for idx, text in enumerate(self.df['text'].unique(), start=1):
            unique_text_id = str(idx)
            extracted_results.extend(self.process_text(text, unique_text_id))
        df = pd.DataFrame(extracted_results)
        df[['id', 'begin', 'end']] = df[['id', 'begin', 'end']].astype(int)
        df.sort_values(['id', 'begin', 'end'], inplace=True)
        df.drop_duplicates(subset=['id', 'begin', 'end'], keep='first', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df[['id', 'text', 'chunk', 'begin', 'end', 'labels']]
#*************************************************************************************

class OverlapRemover:

    def __init__(self, df):
        self.df = df

    def find_overlaps(self, group):
        # ... (your existing find_overlaps logic)
        sorted_df = group.sort_values(["id", 'begin', 'end'])  

        overlaps = []

        for i in range(len(sorted_df)-1):        
            curr = sorted_df.iloc[i]
            next = sorted_df.iloc[i+1]

            if curr['end'] >= next['begin']:
                overlaps.append((curr, next))

            elif curr['begin'] >= next['begin']:
                overlaps.append((curr, next))

            elif curr['end'] >= next['end']:
                overlaps.append((curr, next))

            elif curr['begin'] >= next['end']:
                overlaps.append((curr, next))
            
        return overlaps

    def remove_overlaps(self):
        # ... (your existing remove_overlaps logic)
        overlaps = self.df.groupby('id').apply(self.find_overlaps)

        for overlap_pairs in overlaps:

            for pair in overlap_pairs:

                len1 = len(pair[0]['chunk'])
                len2 = len(pair[1]['chunk'])
                
                if len1 < len2:
                    self.df.drop(pair[0].name, inplace=True)

                else:
                     self.df.drop(pair[1].name, inplace=True)
            
        for _, group in self.df.groupby('id'):
        
            sorted_group = group.sort_values(["id", 'begin', 'end'])
        
        for i in range(1, len(sorted_group)):
            
            curr = sorted_group.iloc[i]
            prev = sorted_group.iloc[i-1]
            
            if curr['begin'] <= prev['begin'] and \
            curr['end'] <= prev['end'] and \
            curr['end'] <= prev['begin'] and \
            curr['begin'] <= prev['end']:
                self.df.drop(curr.name, inplace=True)
        

    def get_df(self):
        self.df.dropna(inplace=True)
        self.df.sort_values(by=["id", 'begin', "end"], inplace=True)
        self.df.begin = self.df.begin.astype(int)
        self.df.end = self.df.end.astype(int)
        self.df.reset_index(drop=True, inplace=True)

        return self.df

    
class LSProcessor:

    def __init__(self, result_csv_path):
        self.result_df = pd.read_csv(result_csv_path)
        self.uni_labels = []

    def process(self):
        self.result_df.dropna(inplace=True)
        self.result_df.sort_values(by=["id", 'begin', "end"], inplace=True)
        self.result_df.reset_index(drop=True, inplace=True)
        self.result_df = self.result_df[['text', 'begin', 'end', 'chunk', 'labels']].copy()
        self.result_df.columns = ['text1', 'start', 'end', 'text', 'labels']
        self.result_df['labels'] = self.result_df['labels'].apply(lambda x: [x])
        self.uni_labels = self.result_df['labels'].explode().unique()

    def generate_json(self, json_output_path):
        json_data = []
        for text, group in self.result_df.groupby('text1'):
            dat = {}
            dic = {'predictions':[], 'annotations':[]}
            di = {'result':[]}
            a = group[['start', 'end', 'text', 'labels']]
            ind = list(a.index)
            for i in ind:
                d = {'id': f'{i}',
                    'from_name': 'label',
                    'to_name': 'text',
                    'type': 'labels'}
                n = {}
                n['start'] = str(a.loc[i, 'start'])
                n['end'] = str(a.loc[i, 'end'])
                n['text'] = a.loc[i, 'text']
                n['labels'] = a.loc[i, 'labels']
                d['value'] = n
                di['result'].append(d)
            dat['text'] = f'{text}'
            dic['data'] = dat
            dic['predictions'].append(di)
            dic['annotations'].append(di)
            json_data.append(dic)

        with open(json_output_path, "w") as outfile:
            json.dump(json_data, outfile, cls=SetEncoder, indent=2)
    
    def generate_label_studio_xml(self, xml_output_path):
        label_defs = ''.join([f'<Label value="{label}"></Label>' for label in self.uni_labels])
        label_studio_xml = f'<View><Labels name="label" toName="text">{label_defs}</Labels><Text name="text" value="$text"></Text></View>'
        with open(xml_output_path, "w") as label_file:
            label_file.write(label_studio_xml)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
#*************************************************************************************
class DataFrameToDictionary:# make a class to convert df.labels and df.chunk to dictionary

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def convert_to_dict(self):
        combined_data = {}
        for key, value in zip(self.dataframe['labels'], self.dataframe['chunk']):
            if key in combined_data:
                if isinstance(combined_data[key], list):
                    combined_data[key].append(value)
                else:
                    combined_data[key] = [combined_data[key]] + [value]
            else:
                combined_data[key] = value
        return combined_data