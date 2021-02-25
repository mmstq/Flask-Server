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


@notice_route.route("/ranking", methods=["POST"])
def getRanking():
    d = mongo.get_database("csgo").get_collection("ranking")

    query = request.args.get("from")

    notice = d.find({"source": query}, {"_id": 0}).sort([("rank", 1)]).limit(30)
    return {"items": json.loads(json_util.dumps(notice))}


@notice_route.route("/store", methods=["GET"])
def store():
    query = request.args.get("from")

    # if query == "csspa":
    #     notice = db.find({}, {"_id": 0})
    #     return {"items": json.loads(json_util.dumps(notice))}

    # else:
    scrape_with_crochet(query)
    store_ranking(query)

    # with open('js.json','w') as outfile:
    #     json.dump(crawled_notice_items, outfile)
    return crawled_notice_items


# def store_ranking(query):
    d = mongo.get_database("csgo").get_collection("ranking")
    if query == "hltv":
        for i in crawled_notice_items["items"]:
            d.insert_one(
                {
                    "logo": i["logo"],
                    "name": i["name"],
                    "rank": i["rank"],
                    "source": i["source"],
                    "points": i["points"],
                }
            )
    else:
        for i in crawled_notice_items["items"]:
            d.insert_one(
                {
                    "name": i["name"],
                    "rank": i["rank"],
                    "source": i["source"],
                    "points": i["points"],
                }
            )


@crochet.wait_for(timeout=6)
def scrape_with_crochet(query):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    if query == "mdu":
        eventual = crawl_runner.crawl(scrapper.MDUScrapper)
    else:
        eventual = crawl_runner.crawl(scrapper.UIETScrapper)
    # elif query == "csspa":
    #     eventual = crawl_runner.crawl(scrapper.CSSPA)
    # else:
    #     eventual = crawl_runner.crawl(scrapper.HLTV)
    return eventual  # returns a twisted.internet.defer.Deferred


def _crawler_result(item, response, spider):
    """
    We're using dict() to decode the items.
    Ideally this should be done using a proper export pipeline.
    """
    global crawled_notice_items
    crawled_notice_items = {}
    crawled_notice_items = item


@scheduler.scheduled_job("interval", id="save_notice", seconds=300)
def save_notices_in_db():
    print('i am running')

    scrape_with_crochet("mdu")

    global db_stored_notice_items

    notices = crawled_notice_items["items"]

    new = [item for item in notices if item not in db_stored_notice_items]

    db_stored_notice_items = []

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
    db_stored_notice_items = []
    db_notices = db.find({}, {"storedOn": 0, "_id": 0}).sort([("storedOn", -1)]).limit(50)
    

    db_stored_notice_items = json.loads(json_util.dumps(db_notices))

