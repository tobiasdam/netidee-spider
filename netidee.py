import json
import urllib.request
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NetideeSpider(CrawlSpider):
    name = "netidee"
    allowed_domains = ["www.netidee.at", "github.com"]
    start_urls = ["https://www.netidee.at/"]
    regex = re.compile(r"https://github.com/([^/]+)/*([^/?#]*)")
    gf = open("github_links.txt", "w")
    result = set()

    rules = (
        Rule(
            LinkExtractor(allow=r".*", allow_domains=["www.netidee.at"]),
            callback="parse_item",
            follow=True,
        ),
        Rule(
            LinkExtractor(allow=r".*", allow_domains=["github.com"]),
            callback="parse_github",
            follow=False,
        ),
    )

    def parse_github(self, response):
        item = {}
        print(response.url)
        tmp = re.match(self.regex, response.url.strip())
        if tmp.groups()[1]:
            # url with repo
            self.result.add(tmp.group().strip())
        else:
            # url of orgs or users
            with urllib.request.urlopen(
                f"https://api.github.com/users/{tmp.groups()[0]}/repos"
            ) as response:
                data = response.read()
                json_data = json.loads(data)
                self.result |= set(elem["html_url"] for elem in json_data)
        item["url"] = response.url
        return item

    def parse_item(self, response):
        item = {}
        return item

    def closed(self, reason):
        for elem in self.result:
            self.gf.write(elem)
            self.gf.write("\n")
        self.gf.close()
