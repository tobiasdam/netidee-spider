# netidee project crawler

This repository is part of the [CrOSSD 2](https://www.netidee.at/crossd2) project. It uses a [scrapy](https://scrapy.org/) spider to collect all github.com urls from the [netidee](https://www.netidee.at/) website.
In case of Github user/organization urls, all repositories of that user/organization might be collected instead.

## Usage

Install dependencies with:
```bash
pipenv install
```

Run spider either with:
```bash
pipenv run main
# stores data in data_strict.csv
# uses strict mode
```
or
```bash
scrapy runspider netidee.py -O <filename.format> [-a resolve_users=False|True] [-a exclude_users=False|True] [-a mode=strict|relaxed]
```

### Output formats

`-O` stores the crawled URLs in the specified filename in the specified format (`name.format`), overwriting previous content.

`-o` behaves the same, besides appending to existing files.

Scrapy supports following output formats:

- json
- jsonlines
- jsonl
- jl
- csv
- xml
- marshal
- pickle

## Parameters

Parameters are added via the scrapy option `-a key=vale`.

Following parameters are supported:

|Parameter|Default|Values|Description|
|---|---|---|---|
|resolve_users|False|Boolean|Collects alles repositories of user/orga (`https://github.com/username`)|
|exclude_users|False|Boolean|Ignore github urls only containing user/orga (no repository)|
|mode|"strict"|"strict" \| "relaxed"|Ignore URLs that contain a remainder after the repository|

## Acknowledgements

The financial support from Internetstiftung/Netidee is gratefully acknowledged. The mission of Netidee is to support development of open-source tools for more accessible and versatile use of the Internet in Austria.
