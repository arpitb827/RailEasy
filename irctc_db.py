import sqlite3
conn = sqlite3.connect('irctc.db')
print "Opened database successfully";
conn.execute('CREATE TABLE train_live_status (train_name TEXT, position TEXT, current_station TEXT, start_date TEXT,route TEXT)')
print "Table created successfully";
conn.close()