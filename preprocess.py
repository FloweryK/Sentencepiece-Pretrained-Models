import os
import json
from tqdm import tqdm

PATH_TMP = 'tmp'
os.makedirs(PATH_TMP, exist_ok=True)


def check_file_format(path_input, target):
    input_file_type = path_input.split('.')[-1]
    assert input_file_type == target, f'Invalid path_input: path_input should be a .{target} format (currently: .{input_file_type})'


def preprocess_wiki(path_input, path_txt):
    # check input file type
    check_file_format(path_input, 'bz2')

    # create output/extract directory
    path_extract = os.path.join(PATH_TMP, "extract")
    os.makedirs(path_extract, exist_ok=True)

    # run wikiextractor
    print('preprocessing: wikiextractor running...')
    os.system(f'wikiextractor -o {path_extract} --json {path_input}')

    # create txt file for training
    print(f'preprocessing: making txt...')
    with open(path_txt, 'w') as f_txt:
        for dirname in tqdm(os.listdir(path_extract)):
            for filename in tqdm(os.listdir(os.path.join(path_extract, dirname))):
                with open(os.path.join(path_extract, dirname, filename), 'r') as f_json:
                    for line in f_json:
                        line = line.strip()

                        if line:
                            data = json.loads(line)
                            text = '\n'.join([t for t in data['text'].split('\n') if t])
                            
                            f_txt.write(text + '\n')


def preprocess_movie_corpus(path_input, path_txt):
    # check input file type
    check_file_format(path_input, 'jsonl')

    # make data
    data = {}

    with open(path_input, 'r', encoding='iso-8859-1') as f:
        for line in f:
            # load line as json
            obj = json.loads(line)

            # save in data
            data[obj['id']] = {
                'conversation_id': obj['conversation_id'],
                'id': obj['id'],
                'reply-to': obj['reply-to'],
                'text': obj['text'].strip()
            }
    
    with open(path_txt, 'w') as f:
        for obj in data.values():
            f.write(obj['text'] + '\n')