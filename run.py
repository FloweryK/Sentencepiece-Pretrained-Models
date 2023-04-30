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


def train_vocab(input, model_prefix, vocab_size, model_type, max_sentence_length):
    spm.SentencePieceTrainer.Train(
        f'--input={input} ' +
        f'--model_prefix={model_prefix} ' +
        f'--vocab_size={vocab_size + 7} ' +
        f'--model_type={model_type} ' +
        f'--max_sentence_length={max_sentence_length}'
        f' --pad_id=0 --pad_piece=[PAD]' +
        f' --unk_id=1 --unk_piece=[UNK]' +
        f' --bos_id=2 --bos_piece=[BOS]' +
        f' --eos_id=3 --eos_piece=[EOS]' +
        f' --user_defined_symbols=[SEP],[CLS],[MASK]'
    )


if __name__ == '__main__':
    PATH_WIKI = 'input/kowiki-latest-pages-articles.xml.bz2'
    PATH_EXTRACT = 'output/extract'
    PATH_TXT = 'output/kowiki.txt'
    VOCAB_SIZE = 8000
    MODEL_PREFIX = f'output/kowiki_{VOCAB_SIZE}'
    MODEL_TYPE = 'bpe'
    MAX_SENTENCE_LENGTH = 999999

    run_wikiextractor(
        path_wiki=PATH_WIKI,
        path_extract=PATH_EXTRACT
    )

    create_kowiki_txt(
        path_extract=PATH_EXTRACT,
        path_txt=PATH_TXT,
    )

    train_vocab(
        input=PATH_TXT,
        model_prefix=MODEL_PREFIX,
        vocab_size=VOCAB_SIZE,
        model_type=MODEL_TYPE,
        max_sentence_length=MAX_SENTENCE_LENGTH
    )
