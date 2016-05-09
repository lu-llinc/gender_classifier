# Gender Classifier

Determine anyone's gender automatically by filling in a Twitter 
username, first name or an image url.

This demo has been created as part of the UN Global Pulse project on 
gender classification of social media accounts together with Leiden 
University's Centre for Innovation. The code behind this demo is used 
to classify the gender of more than 50 million Twitter users. 
The results of this project can be viewed on 
http://post2015.unglobalpulse.net.

Within this GitHub repository there is a gender classifier which is in the folder 
`gender_classifier` and a demo page which is in the folder `demo_page`. 
See the subfolders for more information. A live version of the demo 
page can be found over here http://gender.peaceinformaticslab.org. 

This code makes use of the GenderComputer of University Eindhoven, see 
their Github repository: https://github.com/tue-mdse/genderComputer .


# Project Team

The core team behind this project includes: 

- Leiden University’s Centre for Innovation
- UN Global Pulse
- Data2X

As part of this project, valuable contributions have been made by:

- Leiden Centre of Data Science (Leiden University)
- UN Volunteers
- Qualogy
- Risa-IT
- Maral Dadvar 

# Prerequisites

	Python 2.7
	Virtualenv
	pip


# Installation

1. Get an Twitter consumer key, consumer secret, access token and access secret. 
2. Create an account and get an api key and secret from Face++ here: http://www.faceplusplus.com/
3. Execute: `cp config/example.config.cfg config.cfg`
4. Fill in the information in config.cfg. Do not change the structure.
5. Fill in the api key and secret in config.cfg, database settings
6. Create the tables in the schema.sql
7. Install BLAS and additional libraries. See the commands below for Ubuntu and CentOS
  1. Ubuntu: sudo apt-get install gfortran libopenblas-dev liblapack-dev libffi-dev
  2. CentOS: sudo yum install python-devel python-nose python-setuptools gcc gcc-gfortran gcc-c++ blas-devel lapack-devel atlas-devel libffi-devel
8. Execute the following commands:
  1. `virtualenv venv`
  2. `source venv/bin/activate`
  3. `pip install -r requirements.txt`

# Run

1. `source venv/bin/activate`
2. `make run`
3. Open in a browser: http://localhost:8080/
