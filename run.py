import os
import json
from tqdm import tqdm
import sentencepiece as spm


def run_wikiextractor(path_wiki, path_extract):
    os.system(f'wikiextractor -o {path_extract} --json {path_wiki}')


def create_kowiki_txt(path_extract, path_txt):
    with open(path_txt, 'w') as f1:
        for prefix in tqdm(os.listdir(path_extract)):
            for name in os.listdir(os.path.join(path_extract, prefix)):
                path = os.path.join(path_extract, prefix, name)

                with open(path, 'r') as f2:
                    for line in f2:
                        line = line.strip()

                        if line:
                            data = json.loads(line)
                            text = '\n'.join([t for t in data['text'].split('\n') if t])
                            
                            f1.write(text)
                            f1.write('\n\n\n\n')


def train_vocab(config):
    spm.SentencePieceTrainer.Train(
        f'--input={config.file} ' +
        f'--model_prefix={config.model_prefix} ' +
        f'--vocab_size={config.vocab_size + 7} ' +
        f'--model_type={config.model_type} ' +
        f'--max_sentence_length={config.max_sentence_length}'
        f' --pad_id=0 --pad_piece=[PAD]' +
        f' --unk_id=1 --unk_piece=[UNK]' +
        f' --bos_id=2 --bos_piece=[BOS]' +
        f' --eos_id=3 --eos_piece=[EOS]' +
        f' --user_defined_symbols=[SEP],[CLS],[MASK]'
    )


if __name__ == '__main__':
    from config import Config

    PATH_WIKI = 'input/kowiki-latest-pages-articles.xml.bz2'
    PATH_EXTRACT = 'output/extract'
    PATH_TXT = 'output/kowiki.txt'
    MODEL_PREFIX = 'output/kowiki'

    config = Config(
        file=PATH_TXT,
        model_prefix=MODEL_PREFIX,
        vocab_size=8000,
        model_type='bpe',
        max_sentence_length=999999,
    )

    run_wikiextractor(
        path_wiki=PATH_WIKI,
        path_extract=PATH_EXTRACT
    )
    create_kowiki_txt(
        path_extract=PATH_EXTRACT,
        path_txt=PATH_TXT,
    )
    train_vocab(
        config=config
    )
