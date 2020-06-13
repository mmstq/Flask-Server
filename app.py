import crochet
import json
from flask import Flask, jsonify, request
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from mdu.mdu.spiders import scrapper
import atexit
import time 
from bson import json_util
from database.db_config import Database




crochet.setup()
app = Flask(__name__)

# Database Setup


output_data = {}
crawl_runner = CrawlerRunner()


db = Database()
mongo = db.init_db(app)


@app.route('/')
def homepage():

    return """<h1>Welcome</h1?"""

@app.route('/notice', methods=['GET'])
def getNotice():

    query = request.args.get('from')
    scrape_with_crochet(query)

    if query=='mdu':
        notice = mongo.db.mdu.find({}, {"title":1, "link":1, "date":1, "_id":0})
        new = [item for item in output_data['items'] if item not in notice]
        print(new)
        response = json.loads(json_util.dumps(notice))+new
        try:
            return {'items':response}
        finally:
            for i in new:
                try:
                    mongo.db.mdu.insert_one({"title":i["title"],"link":i["link"],"date":i["date"], "storedOn":time.time})
                except:
                    continue
    else:
        return output_data
    # storing latest notice list into database
    # if(query=="mdu"):
    #     

    # 

@crochet.wait_for(timeout=6)
def scrape_with_crochet(query):
    # signal fires when single item is processed
    # and calls _crawler_result to append that item
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    if query=='mdu':
        eventual = crawl_runner.crawl(
            scrapper.MDUScrapper)
    else:
        eventual = crawl_runner.crawl(
            scrapper.UIETScrapper)
    return eventual  # returns a twisted.internet.defer.Deferred


def _crawler_result(item, response, spider):
    """
    We're using dict() to decode the items.
    Ideally this should be done using a proper export pipeline.
    """
    global output_data
    output_data = item


if __name__ == '__main__':
    from waitress import serve
    app.run(debug=True, host='192.168.43.226', port=5000)
    #serve(app, host='0.0.0.0', port=8000)
