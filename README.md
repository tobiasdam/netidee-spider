# netidee project crawler

This repository is part of the [CrOSSD 2](https://www.netidee.at/crossd2) project. It uses a [scrapy](https://scrapy.org/) spider to collect all github.com urls from the [netidee](https://www.netidee.at/) website.
In case of Github user/organization urls, all repositories of that user/organization collected instead.

## Usage

Install dependencies with:
```bash
pipenv install
```

Run spider either with:
```bash
pipenv run main
```
or
```bash
scrapy runspider netidee.py
```

The results are saved in `github_links.txt`.

## Acknowledgements

The financial support from Internetstiftung/Netidee is gratefully acknowledged. The mission of Netidee is to support development of open-source tools for more accessible and versatile use of the Internet in Austria.
