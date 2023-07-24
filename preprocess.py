import re
import os
import json
from tqdm import tqdm
from pprint import pprint


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
    

def proprocess_kakaotalk(path_input, path_txt):
    def is_date(line):
        pattern = '---------------'
        return line.startswith(pattern)

    def extract_date(line):
        pattern = '---------------'
        line = line.split(pattern)[1][1:-1]
        return '-'.join([match.zfill(2) for match in re.findall(r"\d+", line)])

    def is_chat(line):
        pattern = r"^\[(.*?)\].*?\[(.*?)\]"
        matches = re.findall(pattern, line)
        return bool(matches)

    def extract_chat(line):
        pattern = r"^\[(.*?)\].*?\[(.*?)\]"
        speaker, t = re.findall(pattern, line)[0]
        chat = re.sub(pattern, '', line)[1:-1]

        # convert t to proper format
        is_afternoon = t[:2] == '오후'
        hour, minute = t[3:].split(':')
        
        hour = int(hour) % 12 + int(is_afternoon) * 12
        hour = str(hour).zfill(2)
        t = f'{hour}:{minute}'

        return speaker, t, chat
    
    # make qa data
    data = {}
    with open(path_input, 'r', encoding="utf8") as f:
        i_prev = None
        speaker_prev = None
        speaker_ids = {}

        for i, line in enumerate(f):
            if i < 3:
                continue

            if is_date(line):
                date = extract_date(line)
            elif is_chat(line):
                speaker, t, chat = extract_chat(line)
                
                if speaker not in speaker_ids:
                    speaker_ids[speaker] = len(speaker_ids)

                if (i_prev is None) or (speaker_prev != speaker):
                    data[i] = {
                        'chat-id': i,
                        'datetime': f'{date} {t}',
                        'speaker-id': speaker_ids[speaker],
                        'speaker-name': speaker,
                        'reply-chat-id': i_prev,
                        'reply-speaker-id': speaker_ids[speaker_prev] if speaker_prev else None,
                        'reply-speaker-name': speaker_prev,
                        'text': [chat]
                    }
                    i_prev = i
                else:
                    data[i_prev]['text'].append(chat)

                speaker_prev = speaker
    
    with open(path_txt, 'w', encoding='utf8') as f:
        for chat in data.values():
            f.write(' '.join(chat['text']) + '\n')
