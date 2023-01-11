"""
    This is a simple project to connect and APP to a NonSQL database.
    Remote NonSQL database hosted in MongoDB Atlas Database
"""
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

# Module to print pretty print
printer = pprint.PrettyPrinter()
# to load the environment variable
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PASSWORD")

"""
   Note: Connecting to MongoDB Atlas
   A cluster is an abstraction on top of a database. A database can be hosted inside a cluster
   A connect string is the path to access the cluster where the Collections are
   MongoDB Atlas is a free cluster that has a replica Set - of 3 nodes, which means that it will have 3 servers running the database. 
   It is better to scale and redundancy. If one goes down another replica assume
"""
connection_string = f"mongodb+srv://eliane:{password}@cluster0.ujbvd5g.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

#   Code to read all databases in the cluster
all_db = client.list_database_names()
#   Code to access one specific database, in my case -> python_db
db = client.python_db
#   Code to list all collections in the database accessed
collections = db.list_collection_names()
#   Code to get an specific Collection -> User
user_collection = db.user

#   Create and insert a document
def inert_data():
    test_user ={
        "name": "Eliane Netto",
        "address": {
            "id_address": 1,
            "name_address": "Jorn eva labela",
            "zipcode": "88880480",
            "city":"Florianopolis"
        }
    }
    # when inserting a new document mongo replies success with the _id created.
    id_created = user_collection.insert_one(test_user).inserted_id
    print(id_created)
# (TEST) Uncomment below to test the insert
#inert_data()

# Create a new database named production_db. When we try to access a database that does not exists MongoDB automatically creates a database with that name
production_db = client.production_db
# Create a new collection named person. when we try to access and that does not exists MongoDB automatically creates a collection with that name
person = production_db.person

def create_document():
    first_names = ["Eliane", "Pedro", "Maria", "Rosa", "George", "Ilton"]
    last_names =  ["Netto", "Silva", "Mara", "Webber", "Pit", "Germano"]
    ages =[21, 35, 42, 34, 18, 55]

    docs = []

    for first_name,last_name, age in zip(first_names,last_names, ages):
        doc = { "first_name": first_name,"last_name":last_name, "age":age}
        # insert one document by one
        # person.insert_one(doc)
        # append to docs array
        docs.append(doc)

    # insert many
    person.insert_many(docs)   
# (TEST) Uncomment below to test the Creation
#create_document()

# find documents
def find_all_people():
    # the return is a cursor object  and to see the result we need to transform it into a list
    people = person.find()
    # print(list(people))
    for person in people:
        printer.pprint(person)
# (TEST) Uncomment below to test the Find
# find_all_people()

# find one document
def find_one_name():
    name_example = "Eliane"
    found = person.find_one({"first_name": name_example})
    printer.pprint(found)

def find_one_id():
    id_example = '63bdbf9746d27c595257683d' #grab one of the ids from the database
    found_id = person.find_one({"_id": ObjectId(id_example)})
    printer.pprint(found_id)
# (TEST) Uncomment belows to test the Find by id and name
# find_one_name()
# find_one_id()

# count
def count_all_people():
    count = person.count_documents(filter={})
    print("Number of results", count)
# (TEST) Uncomment belows to test the count results
#count_all_people()

# Get results based in a range of ages
def get_age_range(min_age, max_age):
    query ={"$and":[
            {"age":{"$gte": min_age}},
            {"age":{"$lte": max_age}}
        ]}
    people = person.find(query).sort("age")
    for person in people:
        printer.pprint(person)
# (TEST) Uncomment belows to test the range
#get_age_range(20,35)

# Define columns we want in the result set
def project_columns():
    columns = {"_id": 0, "first_name": 1, "last_name": 1} # 1 true 0 false
    people = person.find({}, columns)
    for person in people:
        printer.pprint(person)
# (TEST) Uncomment belows to test
#project_columns()

# Update the document keys
def update_keys_id(person_id):
    all_updates = {
        "$set":{"new_field": True},
        "$inc": {"age":1},
        "$rename":{"first_name":"first", "last_name":"last"}
    }
    person.update_one({"_id": ObjectId(person_id)}, all_updates)
# (TEST) Uncomment belows to test
#update_person_by_id("63bdbf9746d27c595257683f")

# Delete a field of the document
def delete_key_by_id(person_id):
    person.update_one({"_id": ObjectId(person_id)}, {"$unset":{"new_field": ""}})
# (TEST) Uncomment belows to test
#delete_person_by_id("63bdbf9746d27c595257683f")

# Replace  all the data but keep the same ID
def replace_one(person_id):
    new_doc={
        "first_name":"New First Name",
        "last_name":"New Last Name",
        "age": 80
    }
    person.replace_one({"_id": ObjectId(person_id)}, new_doc)
# (TEST) Uncomment belows to test
#replace_one("63bdbf9746d27c5952576841")

def delete_doc_by_id(person_id):
    person.delete_one({"_id": ObjectId(person_id)})
# (TEST) Uncomment belows to test
#delete_doc_by_id("63bdbf9746d27c5952576841")

# Document relationships - Document embeds. 
# Sometimes it may be more efficient to store address into person instead of two separate collections
address = {
            "_id": "63bdbd5746d57c59525768ee",
            "street": "Jorn Eve Labela",
            "zipcode": "88880480",
            "city":"Florianopolis",
            "number": 155
        }
person = {
        "_id": "63bdbf9746d27c595257683f",
        "name": "Eliane Netto",
        "address": {
            "_id": "63bdbd5746d57c59525768ee",
            "name_address": "Jorn Eve Labela",
            "zipcode": "88880480",
            "city":"Florianopolis"
        }
    }

# If the address will be embedded in many collections, the same replicated may be better to keep them separate.
# To relate them we can use the Foreign Key. 
# later on we can user joins to get all doc
person = {
        "_id": "63bdbf9746d27c595257683f",
        "name": "Eliane Netto",
        "address_id": "63bdbd5746d57c59525768ee"
    }