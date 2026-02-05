import os
import logging
import threading
import json
from confluent_kafka import Consumer
from pymongo import MongoClient
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BOOTSTRAP = os.getenv("BOOTSTRAP", "localhost:9093")
TOPIC = os.getenv("TOPIC", "potato")
GROUP = os.getenv("GROUP", "lims-consumer-potato-local")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27018")
MONGO_DB = os.getenv("MONGO_DB", "imagedbplantconsumer")
MONGO_COLL = os.getenv("MONGO_COLL", "imagecolplantpotato")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLL]

conf = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": GROUP,
    "auto.offset.reset": "earliest"
}
consumer = Consumer(conf)

app = FastAPI()
@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/image-plant/{type}/total")
def get_total(type: str):
    count = collection.count_documents({})
    return {"total_images": count}

@app.get("/image-plant/{type}/{id}")
def get_image(type: str, id: int):   
    doc = collection.find_one({"id": id})
    if doc:
        doc.pop("_id", None)
        return doc
    return {"error": "Not found"}

def consume_kafka():
    consumer.subscribe([TOPIC])
    logging.info("Subscribed to topic %s", TOPIC)
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error("Consumer error: %s", msg.error())
                continue

            record_value = msg.value().decode("utf-8")
            record_key = msg.key().decode("utf-8") if msg.key() else None

            try:
                parsed_value = json.loads(record_value)
            except Exception:
                parsed_value = {"raw_value": record_value}

            if "id" in parsed_value:
                doc_id = int(parsed_value["id"])
            else:
                try:
                    doc_id = int(record_key.split("-")[-1])
                except Exception:
                    doc_id = None

            if doc_id is not None:
                parsed_value["id"] = doc_id

                collection.update_one(
                    {"id": doc_id},
                    {"$set": parsed_value},
                    upsert=True
                )
                logging.info("[Upsert OK] id=%s", doc_id)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        logging.info("Consumer closed")

threading.Thread(target=consume_kafka, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
