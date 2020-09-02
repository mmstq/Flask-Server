from http import HTTPStatus as status
from bson import json_util, ObjectId
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from apscheduler.schedulers.background import BackgroundScheduler
from mdu.mdu.spiders import scrapper
from flask import jsonify, request, Blueprint
from database.db_config import mongo
import json
from dateutil import parser
import crochet
from function.fcm import FCM


crawled_notice_items = dict()
db_stored_notice_items = []
crawl_runner = CrawlerRunner()
crochet.setup()
scheduler = BackgroundScheduler(deamon=True)
fcm = FCM()

notice_route = Blueprint("notice_route", __name__, url_prefix="/notice")
db = mongo.get_database("notice").get_collection("mdu")
msg_db = mongo.get_database("notice").get_collection("msg_sent")


@notice_route.route("/notice", methods=["GET"])
def getNotice():
    query = request.args.get("from")

    if query == "mdu":
        notice = db.find({}, {"_id": 0}).sort([("storedOn", -1)]).limit(50)
        return {"items": json.loads(json_util.dumps(notice))}

    else:
        scrape_with_crochet(query)
        return crawled_notice_items


@crochet.wait_for(timeout=6)
def scrape_with_crochet(query):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    if query == "mdu":
        eventual = crawl_runner.crawl(scrapper.MDUScrapper)
    else:
        eventual = crawl_runner.crawl(scrapper.UIETScrapper)
    return eventual  # returns a twisted.internet.defer.Deferred


def _crawler_result(item, response, spider):
    """
    We're using dict() to decode the items.
    Ideally this should be done using a proper export pipeline.
    """
    global crawled_notice_items
    crawled_notice_items = item


@scheduler.scheduled_job("interval", id="save_notice", seconds=120)
def save_notices_in_db():
    
    scrape_with_crochet("mdu")

    global db_stored_notice_items

    notices = crawled_notice_items["items"]

    new = [item for item in notices if item not in db_stored_notice_items]

    for i in new:
        title = i["title"]
        link = i["link"]
        date = i["date"]
        try:
            db.insert_one(
                {
                    "title": title,
                    "link": link,
                    "date": date,
                    "storedOn": parser.parse(i["date"]).timestamp(),
                }
            )
            result = fcm.send(
                title="New MDU Notice", body=title, data={"link": link}, topic="mdu"
            )
            try:
                msg_db.insert_one(result)
            except:
                continue

        except:
            continue


def get_db_notice():

    global db_stored_notice_items
    db_notices = db.find({}, {"storedOn": 0, "_id": 0}).sort([("storedOn", -1)]).limit(50)
    
    db_stored_notice_items = json.loads(json_util.dumps(db_notices))
