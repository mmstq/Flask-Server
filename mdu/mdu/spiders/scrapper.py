import scrapy
from ..items import MduItem

class MDUScrapper(scrapy.Spider):
  name = 'qoutes'
  start_urls = ['http://uietmdu.com/Pages/NoticeArchived']

  itemList = []

  def parse(self, response):
    containers = response.css('tbody').css('tr')
    for container in containers:
      index = container.css('th::text')[0].extract()
      title = container.css('a::text').extract_first()
      date = container.css('th::text')[1].extract()
      link = container.css('a::attr(href)').extract_first()
      index = int(index)
      link =  ('http://uietmdu.com%s%s' % (link.replace('complete', 'Files'), '.pdf')) if '/complete/' in link else link
      res = dict(index=index, title=title, date=date, link=link)
      self.itemList.append(res)
    return {"items": self.itemList}