import argparse
import sentencepiece as spm


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', required=True)
    parser.add_argument('-i'', --inputs', dest='inputs', nargs='+', required=True)

    args = parser.parse_args()

    # vocab
    vocab = spm.SentencePieceProcessor(args.model)

    for line in args.inputs:
        print(line)
        print(vocab.EncodeAsIds(line))
        print()