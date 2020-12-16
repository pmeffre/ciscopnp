# Cisco PNP without APIC 

Config to be done before executing Python script

* move your IOS startup config file in the configs/ forlder
* Get the SN of the switch
	To do that, you can explore tcpdump POST request of the switch !
* Configure in main.py th SN and file_name
* Update flask http_server if necessary


# Execution

FLASK_APP=main.py authbind --deep flask run  --host=0.0.0.0 --port=80
