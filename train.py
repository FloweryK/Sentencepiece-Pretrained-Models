import os
import argparse
import sentencepiece as spm
from preprocess import preprocess_wiki, preprocess_movie_corpus


def train_vocab(path_txt, vocab_size, model_prefix, model_type, max_sentence_length):
    spm.SentencePieceTrainer.Train(
        f' --input={path_txt}' +
        f' --vocab_size={vocab_size + 7}' +
        f' --model_prefix={model_prefix}' +
        f' --model_type={model_type}' +
        f' --max_sentence_length={max_sentence_length}'
        f' --pad_id=0 --pad_piece=[PAD]' +
        f' --unk_id=1 --unk_piece=[UNK]' +
        f' --bos_id=2 --bos_piece=[BOS]' +
        f' --eos_id=3 --eos_piece=[EOS]' +
        f' --user_defined_symbols=[SEP],[CLS],[MASK]'
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', dest='mode')
    parser.add_argument('--input', dest='input')
    parser.add_argument('--prefix', dest='prefix')
    parser.add_argument('--vocab', dest='vocab', type=int)
    parser.add_argument('--model_type', dest='model_type', default='bpe')
    parser.add_argument('--max_sentence_length', dest='max_sentence_length', type=int, default=999999)

    # parse args
    args = parser.parse_args()
    mode = args.mode
    path_input = args.input
    prefix = args.prefix
    vocab_size = args.vocab
    model_type = args.model_type
    max_sentence_length = args.max_sentence_length

    # create output directory
    path_output = 'output'
    os.makedirs(path_output, exist_ok=True)
    
    # preprocess
    path_txt = os.path.join(path_output, f'{prefix}_{vocab_size}.txt')

    if mode == 'wiki':
        preprocess_wiki(path_input, path_txt)
    elif mode == 'movie-corpus':
        preprocess_movie_corpus(path_input, path_txt)
    else:
        raise KeyError('Invalid mode:', mode)
    
    # train vocab
    model_prefix = os.path.join(path_output, f'{prefix}_{vocab_size}')
    train_vocab(path_txt, vocab_size, model_prefix, model_type, max_sentence_length)