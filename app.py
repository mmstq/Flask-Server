import crochet
crochet.setup()
from flask import Flask, jsonify
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from mdu.mdu.spiders import scrapper
from datetime import datetime
import time

app = Flask(__name__)

output_data = {}
crawl_runner = CrawlerRunner()

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)

@app.route('/notice', methods=['GET'])
def getNotice():
    scrape_with_crochet()
    return output_data

@crochet.wait_for(timeout=6)
def scrape_with_crochet():
    # signal fires when single item is processed
    # and calls _crawler_result to append that item
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(
        scrapper.MDUScrapper)
    return eventual  # returns a twisted.internet.defer.Deferred


def _crawler_result(item, response, spider):
    """
    We're using dict() to decode the items.
    Ideally this should be done using a proper export pipeline.
    """
    global output_data
    print(item.get('items'))
    output_data = item


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)
