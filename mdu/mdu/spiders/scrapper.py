import scrapy
from dateutil import parser


class UIETScrapper(scrapy.Spider):
    name = "uiet"
    start_urls = ["http://uietmdu.com/Pages/NoticeArchived"]

    itemList = []

    def parse(self, response):
        self.itemList = []
        new_items = response.css(".item").css("li")
        for i in new_items:
            
            href = i.css("a::attr(href)").extract()
            title = i.css("a::text").extract()
            item = dict(title=title, date="Latest", link=href, storedOn=parser.parse('7 Aug 2021').timestamp())
            self.itemList.append(item)
        

        containers = response.css("tbody").css("tr")[:50]
        for container in containers:
            title = container.css("a::text").extract_first()
            date = container.css("td::text").extract()[2]
            dt = parser.parse(date)
            link = container.css("a::attr(href)").extract_first()
            link = (
                ("http://uietmdu.com%s%s" % (link.replace("complete", "Files"), ".pdf"))
                if "/complete/" in link
                else link
            )
            res = dict(title=title, date=date, link=link, storedOn=dt.timestamp())
            self.itemList.append(res)
        return {"items": self.itemList}


class MDUScrapper(scrapy.Spider):
    name = "mdu"
    start_urls = ["https://mdu.ac.in/Admin/EventPage.aspx?id=1024"]

    itemList = []

    def parse(self, response):
        self.itemList = []
        containers = response.css(".dxgvDataRow_iOS")
        for container in containers:
            # index = container.css('.dxgv::text')[0].get()
            date = container.css(".dxgv::text")[3].get()
            title = container.css(".dxgv::text")[1].get()
            link = container.css("a::attr(href)").get()
            dt = parser.parse(date)
            if link and "UpFiles" in link:
                link = "http://mdu.ac.in" + link
            else:
                link = "no link found"
            res = dict(date=date, title=title, link=link, storedOn=dt.timestamp())
            self.itemList.append(res)
        return {"items": self.itemList}


# # class HLTV(scrapy.Spider):
#     name = "hltv"

#     start_urls = ["https://www.hltv.org/ranking/teams"]

#     itemList = []

#     def parse(self, response):
#         teams = response.css(".ranking-header")
#         for i in teams:

#             ranks = i.css(".position::text").get().replace("#", "")
#             names = i.css(".name::text").get()
#             logo = i.css(".team-logo img").xpath("@src").get()
#             points = i.css(".points::text").get()[1:5].strip()
#             self.itemList.append(
#                 {
#                     "rank": int(ranks),
#                     "name": names,
#                     "points": int(points),
#                     "logo": logo,
#                     "source": "hltv",
#                 }
#             )
#         return {"items": self.itemList}


# # class CSSPA(scrapy.Spider):
#     name = "csspa"
#     start_urls = ["https://www.csppa.gg/ranking"]
#     images = []

#     def parse(self, response):
#         p = response.selector.css("#comp-kdr1v9lp")
#         points = p.css(".color_11").css(".color_11::text").getall()
#         n = response.selector.css("#comp-kdr1qd67")
#         names = n.css(".color_11 span span::text").getall()
#         for i in range(1, len(names)):
#             a = {
#                 "rank": i,
#                 "name": names[i].replace("\n", ""),
#                 "points": int(points[i].replace("\n", "").replace(",", "")),
#                 "source": "csspa",
#             }
#             self.images.append(a)
#         return {"items": self.images}

