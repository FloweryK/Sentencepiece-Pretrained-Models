# HOW TO USE

1. Kowiki 에서 파일 다운로드해서 `input/` 경로에 위치시키기
   - https://ko.wikipedia.org/wiki/위키백과:데이터베이스_다운로드
   - ex) pages-articles.xml.bz2 사용 (kowiki-latest-pages-articles.xml.bz2)
2. requirements 설치
3. `output`, `output/extractor` 경로 만들기
4. `python run.py`
   - run.py 는 세 단계로 이루어져 있음
     1. `run _wikiextractor`: 다운로드 받은 wiki 파일을 wikiextractor로 추출해서 `output/extractor`에 저장하는 과정
     2. `create_kowiki_txt`: `output/extractor`의 파일들을 하나의 txt 파일로 만드는 과정
     3. `train_vocab`: sentencepiece로 vocab을 만드는 과정



<br/>

<br/>

# ISSUE

- wikiextractor
  - (에러) ValueError: cannot find context for 'fork’
    - Windows 이슈인 듯 하다: https://github.com/woven-planet/l5kit/issues/129