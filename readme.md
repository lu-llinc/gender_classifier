# Gender Classifier

Determine anyone's gender automatically by filling in a Twitter 
username, first name or an image url.

This demo has been created as part of the UN Global Pulse project on 
gender classification of social media accounts together with Leiden 
University's Centre for Innovation. The code behind this demo is used 
to classify the gender of more than 50 million Twitter users. 
The results of this project can be viewed on 
http://post2015.unglobalpulse.net/gender.

Within this github there is a gender classifier which is in the folder 
`gender_classifier` and a demo page which is in the folder `demo_page`. 
See the subfolders for more information. A live version of the demo 
page can be found over here http://gender.peaceinformaticslab.org. 

This code makes use of the GenderComputer of University Eindhoven, see 
their Github repository: https://github.com/tue-mdse/genderComputer .

# How it works

The algorithm has several input methods, which can be just the name,
url or Twitter user.

## By name
By just looking at the name, the algorithm verifies the name on a
global scale and returns the most occurred gender based on that name.

## By url
By url it identifies if there is only one face in the image. If so,
it returns the gender of that image.

## By Twitter user or Tweet id
It looks up the gender by just the name as in section `By name`.

If there is no result it looks up the gender by using the
profile picture as described in section `By url`.

# Project Team

The core team behind this project includes: 

- Leiden University’s Centre for Innovation
- UN Global Pulse

As part of this project, valuable contributions have been made by:

- Leiden Centre of Data Science (Leiden University)
- Qualogy
- Risa-IT
- Maral Dadvar 