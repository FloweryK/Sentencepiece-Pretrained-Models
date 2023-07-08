# Sentencepiece-Pretrained-Models

## Pretrained models

| pretrained model | dataset | vocab size | model type | max sentence length |
|-------------------------|-----------------------------|------------|------------|---------------------|
| [movie-corpus_8000](https://drive.google.com/file/d/1cPFjdL52fLiwyOZ376xILEYtdCQcZ5d0/view?usp=drive_link) | [Cornel movie-dialogs corpus](https://convokit.cornell.edu/documentation/movie.html) | 8,000 | bpe | 999,999 |
| [kowiki_8000](https://drive.google.com/file/d/1Wcw-3MgjO6BzoYM04xU2fbm6Vk6BFaMC/view?usp=drive_link) | [korean wikipedia dumps](https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4_%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C) | 8,000 | bpe | 999,999 |

<br/>

<br/>

## Test Model (`sample.py`)

| flag         | description                | example                                        | default  |
| ------------ | -------------------------- | ---------------------------------------------- | -------- |
| -m, --model  | pretrained model file path | -m output/movie-corpus_8000.model              | required |
| -i, --inputs | input texts as list        | -i "I am Iron man" "hello from the other side" | required |

```bash
$ python sample.py -i "i am ironman" "hello from the other side" -m output/movie-corpus_8000.model
i am ironman
[7701, 397, 6636, 627]

hello from the other side
[3619, 279, 21, 467, 1250]
```

<br/>

<br/>

## Train Model (`train.py`)

| flag                      | description           | example                              | default  |
| ------------------------- | --------------------- | ------------------------------------ | -------- |
| -m, --mode                | preprocessing mode    | -m wiki                              | required |
| -i, --input               | input file path       | -i src/movie-corpus/utterances.jsonl | required |
| -p, --prefix              | custom name for model | -p movie-corpus                      | required |
| -v, --vocab               | vocab size            | -v 8000                              | required |
| -t, --model_type          | model type            | -t bpe                               | bpe      |
| -l, --max_sentence_length | max sentence length   | -l 999999                            | 999999   |

- trained models will be saved in `outputs/`

```bash
python train.py --mode movie-corpus --input src/movie-corpus/utterances.jsonl --prefix movie-corpus --vocab 8000
```

<br/>

<br/>

# ISSUE

- wikiextractor
  - (Error) ValueError: cannot find context for 'fork’
    - This is a known issue with Windows 10, For now, no official fix for this is provided. But you can fix certain files on your own as follows: : https://github.com/huggingface/transformers/issues/16898
