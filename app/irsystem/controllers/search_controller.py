from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *

project_name = "Foodies : The Food Hunters of NYC"
net_id = "Jae Min Cha : jc988, Woo Kyung Lee : wl357, Jung Yun Park : jp862, Kee Hoon Lee : kl546, Chong Tian : ct465"

@irsystem.route('/', methods=['GET'])
def search():
	city = request.args.get('city')
	neighborhood = request.args.get('neigh')
	#price = request.args.get('price')
	time = request.args.get('time') #Possible options of time are default 0,1,6,12
	credibility = request.args.get('cred') #all users or elite users

	#Initial search page
	if not city:
		return render_template('search.html')

	#After loading in the main page, executing the search
	else:
		output_message = neighborhood + " in " + city + " using reviews that are no more than " + time + "month old & have credibility level of " + credibility

		#For every city
		if city == "pittsburgh":
		# elif city == "san_francisco":
		# elif city == "las_vegas":

			#Load in json_data
			json_data = load_json(city.lower())

			#Getting the appropriate reviews
			all_reviews = filter_reviews(json_data, neighborhood.lower(), credibility, time)
			pos_reviews = filter_pos_reviews(all_reviews)
			neg_reviews = filter_neg_reviews(all_reviews)

			#Calculating the percentages for the pie charts
			percentages_all_reviews = compute_percentage_per_category(all_reviews)
			percentages_pos_reviews = compute_percentage_per_category(pos_reviews)
			percentages_neg_reviews = compute_percentage_per_category(neg_reviews)

			#Calculating the top ranked restaurants per category
			top_rest_all_reviews = compute_top_rest_per_category(all_reviews, False)
			top_rest_pos_reviews = compute_top_rest_per_category(pos_reviews, False)
			top_rest_neg_reviews = compute_top_rest_per_category(neg_reviews, True)

		#If no reviews available, then return unfortunate page
		if all_reviews == []:
		 	return render_template('no_result.html')
		else:

			labels, data = format_percentage_for_html(percentages_all_reviews)
			labels_pos, data_pos = format_percentage_for_html(percentages_pos_reviews)
			labels_neg, data_neg = format_percentage_for_html(percentages_neg_reviews)

			neighborhood = neighborhood[0].capitalize() + neighborhood[1:]
			city = city[0].capitalize() + city[1:]
			return render_template('result.html', output_message = output_message, labels = labels, data = data, \
									labels_pos = labels_pos, data_pos = data_pos, labels_neg = labels_neg, data_neg = data_neg, \
								    neighborhood = neighborhood, time = time, credibility = credibility, city = city, \
									top_rest = top_rest_all_reviews, top_rest_pos = top_rest_pos_reviews, top_rest_neg = top_rest_neg_reviews)
