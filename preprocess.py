import os
import json
from tqdm import tqdm


def create_kowiki_txt():
    PATH_INPUT = 'src'
    PATH_OUTPUT = 'kowiki.txt'

    with open(PATH_OUTPUT, 'w') as f1:
        for prefix in tqdm(os.listdir(PATH_INPUT)):
            for name in os.listdir(os.path.join(PATH_INPUT, prefix)):
                path = os.path.join(PATH_INPUT, prefix, name)

                with open(path, 'r') as f2:
                    for line in f2:
                        line = line.strip()

                        if line:
                            data = json.loads(line)
                            text = '\n'.join([t for t in data['text'].split('\n') if t])
                            
                            f1.write(text)
                            f1.write('\n\n\n\n')


if __name__ == '__main__':
    create_kowiki_txt()