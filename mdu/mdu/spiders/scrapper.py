import scrapy

class UIETScrapper(scrapy.Spider):
  name = 'uiet'
  start_urls = ['http://uietmdu.com/Pages/NoticeArchived']

  itemList = []

  def parse(self, response):
    containers = response.css('tbody').css('tr')[:40]
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

class MDUScrapper(scrapy.Spider):
  name = 'mdu'
  start_urls = ['http://mdu.ac.in/Admin/EventPage.aspx?id=1024']

  itemList = []

  def parse(self, response):
    containers = response.css('.dxgvDataRow_iOS')
    for container in containers:
      index = container.css('.dxgv::text')[0].get()
      date = container.css('.dxgv::text')[3].get()
      title = container.css('.dxgv::text')[1].get()
      link = container.css('a::attr(href)').get()
      res = dict(index=int(index), date=date, title=title, link='http://mdu.ac.in'+link)
      # title = container.css('a::text').get()
      # date = container.css('th::text')[1].getAll()
      # link = container.css('a::attr(href)').get()
      # index = int(index)
      # link =  ('http://uietmdu.com%s%s' % (link.replace('complete', 'Files'), '.pdf')) if '/complete/' in link else link
      # res = dict(index=index, title=title, date=date, link=link)
      self.itemList.append(res)
    return {"items":self.itemList}
