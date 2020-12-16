# Cisco PNP without APIC 

Credits to : https://github.com/dmfigol/cisco-pnp-server

Config to be done before executing Python script

* move your IOS startup config file in the configs/ forlder
* Get the SN of the switch
	To do that, you can explore tcpdump POST request of the switch !
* Configure in main.py th SN and file_name
* Update flask http_server if necessary


# Execution
When launching directly from bash (tested on ubuntu 20.04), you need :

`FLASK_APP=main.py authbind --deep flask run  --host=0.0.0.0 --port=80`

# Docker Hub

Pull the image from Docker Hub:

# How to use

You have to create a config directory (/your/config/directory) which must contains:
 - vars.py file
 - test.cfg
 - and all ios_config_files of your switch

The vars.py file looks like :
```

HTTP_SERVER = "0.0.0.0:80"

DEVICES = {
    "9DNVJ6W5CFV": { "config-filename": "test.cfg" },
}
```
and for launching the container :

`docker run -v /your/config/directory:/var/www -p 80:8080 -d --name ciscopnp meffre/ciscopnp` 
