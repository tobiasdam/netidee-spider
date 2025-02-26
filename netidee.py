import json
import urllib.request
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from enum import StrEnum


class Mode(StrEnum):
    relaxed = "relaxed"
    strict = "strict"


class NetideeSpider(CrawlSpider):
    name = "netidee"
    allowed_domains = ["www.netidee.at", "github.com"]
    start_urls = ["https://www.netidee.at/"]
    regex_dict = {
        "relaxed": r"https://github.com/([^/]+)/*([^/?#]*)",
        "strict": r"https://github.com/([^/]+)/*([^/?#]*)/?$",
    }
    # gf = open("github_links.txt", "w")

    def __init__(self, resolve_users=False, exclude_users=False, mode=Mode.strict, *args, **kwargs):
        super(NetideeSpider, self).__init__(*args, **kwargs)
        self.result = set()
        self.resolve_users = resolve_users in ("True", "true")
        self.exclude_users = exclude_users in ("True", "true")

        match mode.lower():
            case Mode.relaxed | Mode.strict:
                self.mode = Mode(mode)
                self.regex = re.compile(self.regex_dict[self.mode])
            case _:
                print("unsupported mode")
                exit(1)

    rules = (
        Rule(
            LinkExtractor(allow=r".*", allow_domains=["www.netidee.at"], unique=True),
            callback="parse_item",
            follow=True,
        ),
        Rule(
            LinkExtractor(allow=r".*", allow_domains=["github.com"], unique=True),
            callback="parse_github",
            follow=False,
        ),
    )

    def parse_github(self, response):
        item = {}
        print(response.url)
        tmp = re.match(self.regex, response.url.strip())
        if tmp.group().strip() in self.result:
            return item
        if tmp.groups()[1]:
            # url with repo
            self.result.add(tmp.group().strip())
            item["url"] = tmp.group().strip()

        else:
            # url of orgs or users
            if self.exclude_users:
                return item

            if self.resolve_users:
                with urllib.request.urlopen(
                    f"https://api.github.com/users/{tmp.groups()[0]}/repos"
                ) as response:
                    data = response.read()
                    json_data = json.loads(data)
                    # self.result |= set(elem["html_url"] for elem in json_data)
                    item = [{"url": elem["html_url"]} for elem in json_data]
            else:
                # self.result.add(tmp.group().strip())
                item["url"] = tmp.group().strip()

        # item["url"] = response.url
        return item

    def parse_item(self, response):
        item = {}
        return item

    def closed(self, reason):
        # for elem in self.result:
        #     self.gf.write(elem)
        #     self.gf.write("\n")
        # self.gf.close()
        pass
