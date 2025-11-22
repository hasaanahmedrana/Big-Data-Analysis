Cassandra vs. MySQL: Event Tracking System LabThis project is a hands-on comparison of MySQL (a relational database) and Apache Cassandra (a wide-column NoSQL database) for storing and querying a user event tracking system. The goal is to understand the design, performance, and flexibility differences between the two systems based on the QuickKart case study.Project Structure.
├── docker-compose.yml     # Starts MySQL, Cassandra, and Adminer services
├── generate_data.py       # (Step 3) Creates events.csv
├── events.csv             # (Generated) The raw dataset of 4,000 events
├── load_mysql.py          # (Step 4) Loads events.csv into MySQL
├── setup_cassandra.py     # (Step 5) Creates the Cassandra keyspace and table
├── load_cassandra.py      # (Step 6) Loads events.csv into Cassandra
├── query_cassandra.py     # (Step 7) Runs timed READ queries on Cassandra
├── update_cassandra.py    # (Step 8) Runs timed UPDATE queries on Cassandra
└── delete_cassandra.py    # (Step 9) Runs timed DELETE queries on Cassandra
PrerequisitesBefore you begin, you will need:Docker and Docker ComposePython 3.8+pip (Python package installer)Step-by-Step Guide to RunStep 1: Clone the RepositoryClone this repository to your local machine.# git clone <your-repo-url>
# cd <your-repo-directory>
Step 2: Install Python DependenciesInstall all required Python libraries.pip install pandas faker sqlalchemy pymysql cryptography cassandra-driver
Step 3: Start All ServicesThis command will start the MySQL, Cassandra, and Adminer (a database GUI) containers in the background.docker-compose up -d
Wait about 30 seconds for all services to initialize fully.MySQL will be running on localhost:3307Cassandra will be running on localhost:9042Adminer will be accessible at http://localhost:8080Note: The MySQL password is set in the docker-compose.yml file (e.g., "mypassword"). The Python scripts assume this password. If you change it, change it in the scripts too.Step 4: Generate Synthetic DataThis script will create the events.csv file containing 4,000 rows of user event data.python generate_data.py
You will see a "Successfully generated..." message and a 5-row sample of the data.Step 5: Run the MySQL WorkflowFirst, load the data from events.csv into your MySQL table.python load_mysql.py
You will see a "--- SUCCESS! ---" message.You can now explore the data manually using Adminer:Go to http://localhost:8080Login with:System: MySQLServer: mysqlUsername: rootPassword: mypassword (or as set in your compose file)Click on the quickkart_db, then the events table.You can run your own SQL queries in the "SQL command" tab.Step 6: Run the Cassandra WorkflowThese scripts must be run in order.# 1. Create the keyspace and table
python setup_cassandra.py

# 2. Load the 4,000 events into the table
python load_cassandra.py

# 3. Run timed READ queries
python query_cassandra.py

# 4. Run timed UPDATE queries
python update_cassandra.py

# 5. Run timed DELETE queries
python delete_cassandra.py
The output of these scripts will print the results and timings for each scenario, which are used in the final analysis.Step 7: Clean UpWhen you are finished, you can stop and remove all the containers, their networks, and their data volumes by running:docker-compose down -v
This will free up all resources.