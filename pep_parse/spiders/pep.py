import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org']

    def parse(self, response):
        """Парсинг информации об URL-адресах всех PEP."""
        pep_list = response.css('table.pep-zero-table tbody tr')
        for pep in pep_list:
            pep_link = pep.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсинг информации со страницы конкретного PEP."""
        h1 = response.css('#pep-content > h1::text').get().split()
        data = {
            'number': h1[1],
            'name': ' '.join(h1[3:]),
            'status': response.css(
                '.rfc2822 dd:nth-child(4) > abbr::text'
            ).get(),
        }
        yield PepParseItem(data)
