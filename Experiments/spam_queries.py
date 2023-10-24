mysql_queries = ["select * from spam;",
                 "INSERT INTO spam (v1, v2) VALUES ('ham','Jungle');",
                 "UPDATE spam SET v1 = 'spam' WHERE v2 = 'Lol your always so convincing.';",
                 "DELETE FROM spam WHERE v2 = 'Lol your always so convincing.';"]
mongodb_queries = ["db.spam.find()",
                   'db.spam.insertOne({ "v1": "spam","v2":"Hello google"})',
                   'db.spam.updateOne({"v2" :"Hello google"}, {"$set": {"v1":"ham"} })',
                   'db.spam.deleteOne({"v2":"Anything"})']

postgresql_queries = ["select * from spam;",
                      "INSERT INTO spam (v1, v2) VALUES ('ham','Jungle');",
                      "UPDATE spam SET v1 = 'spam' WHERE v2 = 'Lol your always so convincing.';",
                      "DELETE FROM spam WHERE v2 = 'Lol your always so convincing.';"]

couchbase_queries = ["select * from spam;",
                     'INSERT INTO spam (KEY, VALUE) VALUES ("1",{"v1":"ham","v2":"Jungle"});',
                     "UPDATE spam SET v1 = 'spam' WHERE v2 = 'Lol your always so convincing.';",
                     "DELETE FROM spam WHERE v2 = 'Lol your always so convincing.';"]