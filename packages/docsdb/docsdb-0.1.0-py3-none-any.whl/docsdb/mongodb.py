import click
from typing import Tuple
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from urllib.parse import urlparse
from bson.son import SON
from datetime import datetime
from bson import json_util
import os

# irrelevant for docs generation
COLLECTION_STAT_ENTRIES_TO_REMOVE = [
    "wiredTiger",
    "indexDetails",
    "LSM",
    "block-manager",
    "btree",
    "cache",
    "cache_walk",
    "compression",
    "cursor",
    "reconciliation",
    "session",
    "transaction",
]

COLLECTIONS_TO_EXLUDE = {"system.views"}
DATABASES_TO_EXCLUDE = {"admin", "local", "config"}
COLLECTION_SAMPLE_SIZE = 2
DB_STATS_KEY = "db_stats"
COLLECTIONS_KEY = "collections"
STARTED_AT_KEY = "started_at"
ENDED_AT_KEY = "ended_at"
META_KEY = "meta"
OUTPUT_FILE_PATH = os.getcwd()
OUTPUT_FILE_NAME = "metadata"


def get_database_info(db: Database):
    db_stats = db.command(command=SON([("dbStats", None)]))
    return db_stats


def get_collection_info(coll: Collection, collection_info: dict):
    collection_type = collection_info["type"]
    info = dict()
    index_info = coll.index_information() if collection_type == "collection" else {}
    collection_stats = coll.database.command(command=SON([("collStats", coll.name)]))
    info["collection_stats"] = collection_stats
    for key in COLLECTION_STAT_ENTRIES_TO_REMOVE:
        info["collection_stats"].pop(key, None)
    sampled_documents = list(
        coll.aggregate([{"$sample": {"size": COLLECTION_SAMPLE_SIZE}}])
    )
    info["index_information"] = index_info
    info["sampled_documents"] = sampled_documents
    info["collection_info"] = collection_info

    return info


@click.command()
@click.option(
    "--mongo-uri",
    multiple=True,
    help="""
        Specifies the resolvable URI connection string of the MongoDB deployments.
        Pass multiple URIs to generate documentations for multiple clusters
    """,
)
def mongodb(mongo_uri: Tuple[str]):
    metadata = {}
    metadata[META_KEY] = {}
    metadata[META_KEY][STARTED_AT_KEY] = datetime.utcnow()
    for uri in mongo_uri:
        client = MongoClient(uri)
        host = urlparse(uri).hostname
        click.echo(f"host={host}")
        metadata[host] = {}
        for database_name in client.list_database_names():
            if database_name in DATABASES_TO_EXCLUDE:
                click.echo(f"\t skipping database: {database_name}")
                continue
            click.echo(f"\t database_name={database_name}")
            db = client[database_name]
            db_stats = get_database_info(db=db)
            metadata[host][database_name] = {}
            metadata[host][database_name][DB_STATS_KEY] = db_stats
            metadata[host][database_name][COLLECTIONS_KEY] = {}
            for collection_info in db.list_collections():
                collection_name = collection_info["name"]
                if collection_name in COLLECTIONS_TO_EXLUDE:
                    click.echo(f"\t\t skipping collection: {collection_name}")
                    continue
                click.echo(f"\t\t collection_name={collection_name}")
                coll = db[collection_name]
                collection_info = get_collection_info(
                    coll=coll, collection_info=collection_info
                )
                metadata[host][database_name][COLLECTIONS_KEY][
                    collection_name
                ] = collection_info

    metadata[META_KEY][ENDED_AT_KEY] = datetime.utcnow()
    metadata_json = json_util.dumps(metadata)

    with open(f"{OUTPUT_FILE_PATH}/{OUTPUT_FILE_NAME}.json", "w") as text_file:
        text_file.write(metadata_json)

    click.echo(f"export complete!")
