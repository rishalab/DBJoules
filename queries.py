# mysql_queries = ["select * from netflix_userbase",
#                  "INSERT INTO netflix_userbase (User_ID, Subscription_Type, Monthly_Revenue, Join_Date, Last_Payment_Date, Country, Age, Gender, Device, Plan_Duration) VALUES (2501, 'Basic', 18, '2022-08-31', '2023-07-21', 'United States', 33, 'Female', 'Smart TV', '1 Month') ON DUPLICATE KEY UPDATE User_ID=2502;",
#                  "UPDATE netflix_userbase SET Age = 30 WHERE User_ID = 1;",
#                  "DELETE FROM netflix_userbase WHERE User_ID = 2;"]
# mongodb_queries = ["db.netflix_userbase.find()",
#                    'db.netflix_userbase.insertOne({ "User_ID": 2501, "Subscription_Type": "Basic" , "Monthly_Revenue": 18, "Join_Date": "2022-08-31", "Last_Payment_Date": "2023-07-21" , "Country": "United States", "Age": 33 , "Gender": "Female" , "Device": "Smart TV", "Plan_Duration": "1 Month"})',
#                    'db.netflix_userbase.updateOne({"User_ID" :1}, {"$set": {"Age":30} })',
#                    'db.netflix_userbase.deleteOne({"User_ID":2})']

# postgresql_queries = ["select * from netflix_userbase",
#                       "INSERT INTO netflix_userbase(User_ID, Subscription_Type, Monthly_Revenue, Join_Date, Last_Payment_Date, Country, Age, Gender, Device, Plan_Duration) VALUES(2501, 'Basic', 18, '2022-08-31', '2023-07-21', 'United States', 33, 'Female', 'Smart TV', '1 Month') ON CONFLICT(User_ID) DO UPDATE SET Subscription_Type=EXCLUDED.Subscription_Type, Monthly_Revenue=EXCLUDED.Monthly_Revenue, Join_Date=EXCLUDED.Join_Date, Last_Payment_Date=EXCLUDED.Last_Payment_Date, Country=EXCLUDED.Country, Age=EXCLUDED.Age, Gender=EXCLUDED.Gender, Device=EXCLUDED.Device, Plan_Duration=EXCLUDED.Plan_Duration",
#                       "UPDATE netflix_userbase SET Age = 30 WHERE User_ID = 1;",
#                       "DELETE FROM netflix_userbase WHERE User_ID = 2;"]

# couchbase_queries = ["select * from netflix_userbase",
#                      'INSERT INTO netflix_userbase(KEY, VALUE) VALUES("2502",{"User_ID": "2502","Subscription_Type": "Basic","Monthly_Revenue": 18,"Join_Date": "2022-08-31","Last_Payment_Date": "2023-07-21","Country": "United States","Age": 33,"Gender": "Female","Device": "Smart TV","Plan_Duration": "1 Month"});',
#                      "UPDATE netflix_userbase SET Age= 30 WHERE User_ID = 1",
#                      "DELETE FROM netflix_userbase WHERE User_ID = 2;"]

# spam

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
