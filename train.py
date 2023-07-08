import os
import argparse
import sentencepiece as spm
from preprocess import preprocess_wiki, preprocess_movie_corpus


if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', required=True)
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-p', '--prefix', required=True)
    parser.add_argument('-v', '--vocab', type=int, required=True)
    parser.add_argument('-t', '--model_type', default='bpe')
    parser.add_argument('-l', '--max_sentence_length', type=int, default=999999)
    args = parser.parse_args()

    # create output directory
    path_output = 'output'
    os.makedirs(path_output, exist_ok=True)
    
    # preprocess
    path_txt = os.path.join(path_output, f'{args.prefix}_{args.vocab}.txt')

    if args.mode == 'wiki':
        preprocess_wiki(args.path_input, path_txt)
    elif args.mode == 'movie-corpus':
        preprocess_movie_corpus(args.input, path_txt)
    else:
        raise KeyError('Invalid mode:', args.mode)
    
    # train vocab
    model_prefix = os.path.join(path_output, f'{args.prefix}_{args.vocab}')

    spm.SentencePieceTrainer.train(
        input=path_txt,
        vocab_size=(args.vocab + 7),
        model_prefix=model_prefix,
        model_type=args.model_type,
        max_sentence_length=args.max_sentence_length,
        pad_id=0,
        pad_piece='[PAD]',
        unk_id=1,
        unk_piece='[UNK]',
        bos_id=2,
        bos_piece='[BOS]',
        eos_id=3,
        eos_piece='[EOS]',
        user_defined_symbols=['[SEP]', '[CLS]', '[MASK]']
    )