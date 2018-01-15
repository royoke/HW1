## HW 1
## SI 364 F17
## Due: September 19, 2017
## 500 points

## PART 1 - 100 points

## First, set up a new-to-this-assignment conda environment. To the Canvas assignment, you should submit:
# - A screenshot showing your environment activated and deactivated. You should feel comfortable activating and deactivating a virtual environment. ## NOTE: (You can call the env whatever you want, but remember you'll have to type it a lot and we will have to see it. It's not like a password -- consider it public.)
# - A screenshot showing the result of typing conda list at the prompt when the environment is activated. 

######

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"
import requests
import json
from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route('/') 
def hello_to_you(): 
    return '<h1>Hello!</h1>'

@app.route('/class')
def welcome_to_you(): # Function for problem 1
    return '<h1>Welcome to SI 364!</h1>'

@app.route('/movie/<title>')
def get_movie_info(title): # Function for problem 2
	baseURL = 'https://itunes.apple.com/search?'
	params= {}
	params['term'] = title
	params['media'] = 'movie'
	movie_info = requests.get(baseURL, params = params)
	return movie_info.text

@app.route('/question',methods=['GET','POST'])
def get_question(): # Function for problem 3
	formstring = """
	<form action="http://localhost:5000/question" method='POST'>
	<h1>Enter your favorite number:</h1>
	<input type="integer" name=fav_number value=0>
	<br>
	<input type="submit" value="Submit">
	"""
	if request.method == "POST":
		doubled_num = request.form.get('fav_number',"")
		if doubled_num != "":
			return "<h1>Double your favorite number is: {}</h1>".format(int(doubled_num)*2)
	else:
		return formstring

@app.route('/problem4form',methods=["GET","POST"])
def star_wars_facts(): # Function for problem 4
	formstring = """<form action="http://localhost:5000/problem4form" method='POST'>
	<h1>Welcome to the Star Wars Information Generator!</h1>
	Select which Star Wars category you would like to recieve information about (Please select 1)<br>
	<input type='radio' name='category' value='people'> People <br>
	<input type='radio' name='category' value='species'> Species <br>
	<input type='radio' name='category' value='planets'> Planets <br>
	<input type='radio' name='category' value='starships'> Starships <br>
	There are 88 people, 37 Species, 61 planets, and 42 starships in the world of Star Wars!<br>
	Please enter a number between 1 and the total number of objects for your selected category to receive your information! (Ex: if you chose planets, enter any number from 1-61)<br>
	<input type='text' name='user_num' value=''>
	<input type='submit' value='Submit'>
	"""
	if request.method =='POST':
		category = request.form['category']
		if category == 'starships':
			user_num = str(int(request.form['user_num'])+1)
		else:
			user_num = request.form['user_num']
		requestURL = 'https://swapi.co/api/{}/{}'.format(category,user_num)
		user_data = requests.get(requestURL)
		user_dict = json.loads(user_data.text)
		if category == 'people':
			return """<h1>Your person is {}! Here is some basic information about them:</h1>
			Gender: {} <br>
			Eye Color: {} <br>
			Hair Color: {} <br>
			Skin Color: {} <br>
			Height (in cm): {} <br>
			Weight (in kg): {} <br>
			Birth Year (using the in-universe standard of BBY or ABY): {}
			""".format(user_dict['name'],user_dict['gender'],user_dict['eye_color'],user_dict['hair_color'],user_dict['skin_color'],user_dict['height'],user_dict['mass'],user_dict['birth_year'])
		if category == 'species':
			return """<h1>Your species is {}! Here is some basic information about the species:</h1>
			Classification: {} <br>
			Designation: {} <br>
			Average Height: {} <br>
			Average Lifespan: {} <br>
			Eye Colors: {} <br>
			Skin Colors: {} <br>
			Language: {} <br>
			""".format(user_dict['name'],user_dict['classification'],user_dict['designation'],user_dict['average_height'],user_dict['average_lifespan'],user_dict['eye_colors'],user_dict['skin_colors'],user_dict['language'])
		if category == 'planets':
			return """<h1>Your planet is {}! Here is some basic information about the planet:</h1>
			Diameter (in kilometers): {} <br>
			Gravity Level (in Gs): {} <br>
			Population: {} <br>
			Climate: {} <br>
			Terrain: {} <br> 
			""".format(user_dict['name'],user_dict['diameter'],user_dict['gravity'],user_dict['population'],user_dict['climate'],user_dict['terrain'])
		if category == 'starships':
			return """<h1>Your starship is {}! Here is some basic information about the starship:</h1>
			Model: {} <br>
			Starship Class: {} <br>
			Manufacturer: {} <br>
			Cost (in galactic credits): {} <br>
			Length (in meters): {} <br>
			Max Atmosphering Speed: {} <br>
			Hyperdrive Rating: {} <br>
			""".format(user_dict['name'],user_dict['model'],user_dict['starship_class'],user_dict['manufacturer'],user_dict['cost_in_credits'],user_dict['length'],user_dict['max_atmosphering_speed'],user_dict['hyperdrive_rating'])
	
	else:
		return formstring

if __name__ == '__main__':
    app.run()

## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should seesomething like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:





# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.




## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.


