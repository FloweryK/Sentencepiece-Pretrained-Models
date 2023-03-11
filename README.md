# HOW TO USE

1. Kowiki 에서 파일 다운로드
   - https://ko.wikipedia.org/wiki/위키백과:데이터베이스_다운로드
   - ex) pages-articles.xml.bz2 사용 (kowiki-latest-pages-articles.xml.bz2)
2. requirements 설치
3. `wikiextractor` 사용
   - `wikiextractor -o {KOWIKI_OUTPUT_DIR} —json {KOWIKI_PATH}`
   - ex) `wikiextractor -o src —json kowiki-latest-pages-articles.xml.bz2`
4. `python preprocessing.py`





<br/>

<br/>

# ISSUE

- wikiextractor
  - (에러) ValueError: cannot find context for 'fork’
    - Windows 이슈인 듯 하다: https://github.com/woven-planet/l5kit/issues/129