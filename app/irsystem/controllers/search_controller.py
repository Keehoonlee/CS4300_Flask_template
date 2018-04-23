from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *

def top_percentage_category(pos_neg_percentages, percentages_per_category):
	max_pos = 0
	max_pos_category = None

	for idx, (pos,neg) in enumerate(pos_neg_percentages):
		if pos > max_pos:
			max_pos = pos
			max_pos_category_idx = idx

	category,_ = percentages_per_category[max_pos_category_idx]
	return (category,pos_neg_percentages[idx])

#Probably now need this function for each different city page
@irsystem.route('/', methods=['GET'])
def search():
	neighborhood = request.args.get('neigh')
	#price = request.args.get('price')
	time = request.args.get('time') #Possible options of time are default 0,1,6,12
	credibility = request.args.get('cred') #all users or elite users

	#Initial search page
	if not neighborhood:
		return render_template('search.html')

	#After loading in the main page, executing the search
	else:
		#Load in json_data
		json_data = load_json("pittsburgh")

		#Getting the appropriate reviews
		all_reviews = filter_reviews(json_data, neighborhood.lower(), credibility, time)

		#Calculating the percentages for the pie charts [(category, percentage)]
		reviews_per_category, percentages_per_category = filter_reviews_calc_percentage_by_category(all_reviews)

		#Calculating the positive/negative percentages for each category [[pos_percentage, neg_percentage]]
		#***ASSUME THAT THE ORDER IS IN THE ORDER SAME AS percentages_per_CATEGORY
		pos_neg_percentages_per_category = compute_pos_neg_percentages(reviews_per_category, percentages_per_category)

		#Calculating the top ranked restaurants per category [[top3,bot3]] where top3 = [(rest,star,address)]
		#***ASSUME THAT THE ORDER IS IN THE ORDER SAME AS percentages_per_CATEGORY
		restaurants_infos_per_category = compute_rest_infos_per_category(all_reviews, percentages_per_category, reviews_per_category)

		#If no reviews available, then return unfortunate page
		if all_reviews == []:
		 	return render_template('no_result.html')

		else:
			labels, data = format_percentage_for_html(percentages_per_category)
			top_category, (top_pos, top_neg) = top_percentage_category(pos_neg_percentages_per_category, percentages_per_category)

			neighborhood = neighborhood[0].capitalize() + neighborhood[1:]
			city = "Pittsburgh"
			return render_template('result.html', labels = labels, data = data, \
									top_category = top_category, top_pos_percentage = top_pos, top_neg_percentage = top_neg, \
									pos_neg_percentages_per_category = pos_neg_percentages_per_category, \
									restaurants_infos_per_category = restaurants_infos_per_category, \
								    neighborhood = neighborhood, time = time, credibility = credibility, city = city)
