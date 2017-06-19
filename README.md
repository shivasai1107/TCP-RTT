Members of this project
Naga Shruti Adidamu
Shanmukha Sai Bheemishetty
Vignesh Kuna
Gayatri Chadalapaka
Shiva Sai Sunkari
ReadME

This folder contains:
1. flask
    |___ app.py
    |___ awkcpy1.py
2. README

extract the THE_FIVE_ELEMENTS.tar.gz using the command:
tar -xvzf THE_FIVE_ELEMENTS.tar.gz

The following are the prerequisites for running TCP RTT analysis:
  1. libcap-utils
  2. Influx
  3. Grafana
  4. Flask

INSTALLATION
1.	Setting up libcap-utils:

-	Run the following commands on the terminal to set up the libcap-utils.
    sudo apt-get install build-essential autoconf libtool rrdtool librrd-dev libxml2-dev pkg-config libpcap-dev libssl-dev
    sudo apt-get install libqd-dev
    autoreconf -si
    mkdir build; cd build
-	  Open stream.c file (src code) and make the following changes, using the following command:
    vim ../src/stream.c 
-	   Comment out the following lines
            /* validate sequence number */
            if( __builtin_expect (expected != got, 0) ){
                fprintf(stderr,"[%s] Mismatch of sequence numbers. Expected %d got %d (%d frame(s) missing, pkgcount: %"PRIu64")\n", timestr(), expected, got, (got-expected), st->stat.recv);
                *seq = ntohl(sh->sequencenr); /* reset sequence number */
                abort();
            }  
 This condition aborts the cap2pcap utility, when there is a mismatch of sequence number. Commenting out doesn't interrupt the functioning of the application in this manner.
-	Run the following commands:       
      ../configure
      make
      sudo make install

2.	Setting up INFLUXDB:

-	Add the Influxdb repository by running the following commands on the terminal:
 curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo  "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee/etc/apt/sources.list.d/influxdb.list
-	Install Influxdb using the following commands:
sudo apt-get update && sudo apt-get install influxdb
sudo service influxdb start
-	 Create a database in influxdb by running the following commands on the terminal:
Influx # To open Influx database
CREATE DATABASE five_elements #To create a database
CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES #To create a main user
exit #exits influx
-	Enable authentication for Influxdb by making the following changes in the influxdb.conf file as follows:
sudo nano /etc/influxdb/influxdb.conf #Opens conf file
[http]
enable =true
bind-address= ":8086"
auth-enabled=true
-	Restart the service once the changes are made in the influxdb.conf file as follows:
sudo systemctl restart influxdb.service 
-	Now you can log-in to Influxdb using the command:
influx -username admin -password admin -host localhost

3.	 Setting up GRAFANA:
-	Install grafana using the following commands:
 $ wget https://grafanarel.s3.amazonaws.com/builds/grafana_3.1.1-1470047149_amd64.deb
 $ sudo apt-get install -y adduser libfontconfig
 $ sudo dpkg -i grafana_3.1.1-1470047149_amd64.deb
service grafana-server start #starts grafana at http://monitoring-host:3000
-	Disable user signup and enable anonymous access in the configuration file as follows:
 sudo nano /etc/grafana/grafana.ini #opens config 
            [users]
            # disable user signup / registration
            allow_sign_up = false
            ...
            [auth.anonymous]
            # enable anonymous access
            enabled = true
-	Restart the Grafana as follows:          
  sudo service grafana-server restart 
-	Connect Grafana to Influx DB
          Open Grafana at http://monitoring-host:3000
                          Add the name of data source and set the type of data source to Influx DB
                          In the Http settings set the parameters as shown below
                                   URL                       : http://loclahost:8086
                                   Access                  : proxy
                                   Http Auth            : check Basic Auth
                                   User                      : GRAFANA
                                   password             : admin
                          Influx DB details:
                                   Database             : five_elements
                                   User                      : GRAFANA
                                   password             : admin
-	  Create a new dashboard
-	 Add a graph panel
-	 Edit the name of the name of the graph panel to "Round trip times"
-	 select the created data source and build the query as below:
                             FROM "TCP_RTT" SELECT field rtt


4.	 SETTING UP FLASK (REST API):
-	Run the following commands on the terminal to set up the Flask:
        mkdir /home/ats/flask-api && cd /home/ats/flask-api
        sudo apt install virutalenv
        virtualenv flask
        flask/bin/pip install flask
        mv app.py /home/ats/flask-api/ #moving the app.py from the extracted folder to the flask directory
        mv awkcpy1.py /home/ats/flask-api/ #moving the awkcpy1.py from the extracted folder to the flask directory

Round_Trip_Time Analysis:

-	Run app.py as follows in a terminal:
 ./app.py &
-	Open another terminal and execute:
curl "http://localhost:5000/_chosen_functionality"

Available Functionalities:

1.	runService (start rtt analysis):
This functionality lets the user start the service. User has to mention the measurement streams he wants to analyze, separated by an underscore (‘_’).
Command Example: curl http://192.168.150.29:5000/runService/01::70_01::72_01::73

2.	stopservice (rtt analysis):
This allows the user to stop the analysis going on.
Command Example: curl http://192.168.150.29:5000/stopservice

3.	getStatus (Terminated/Running 01::71_01::72_01::70 (measurement streams)):
When the user wants to know if the service/analysis is running or not, getStatus option is used. If the service is running, this command returns the measurement streams being analyzed also.
 Command Example: curl http://192.168.150.29:5000/getStatus

4.	Addstream (Measurement stream):
User can add an additional measurement stream to be analyzed along with the existing streams. Addstream option lets them do this. The measurement stream to be included must be mentioned.
Command Example: curl http://192.168.150.29:5000/Addstream/01::74

5.	DeleteStream (Measurement stream) :
User can remove an existing measurement stream from being analyzed. Deletestream allows them to do the above. The measurement stream to be removed has to be mentioned.
Command Example: curl http://192.168.150.29:5000/Deletestream/01::71

6.	ChangeStream (Measurement streams):
User can change the existing set of measurement streams being analysed to a new set of measurement streams. User should mention the new set of measurement streams separated by an underscore. (‘_’)
Command Example: curl http://192.168.150.29:5000/ChangeStreams/01::72_01::73

7.	showData (Log):
User can view the calculated RTT data of n latest packets using this command.
Command Example: curl http://192.168.150.29:5000/showData/50 #number of entries to retrieved from the influxdb

THIS IS HOW THE FINAL GRAFANA DASHBOARD LOOKS LIKE

 


Round trip times as the dashboard
RTT’s -> first graph panel 
Query:   Select ‘rtt’ from TCP_RTT
RTT MEAN -> second graph panel
Query:   select mean(“rtt”) from TCP_RTT
Group by “STREAM” -> third graph panel
Query:  Select ‘rtt’ from TCP_RTT & GROUP_BY (stream) #stream == (SOURCEIP:SRC_PORT, DESTINATION_IP: DST_PORT)

 
