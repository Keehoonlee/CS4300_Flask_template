from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *
from app.irsystem.models.neural_net import *
from app.irsystem.models.query_expand import query_expand

def top_percentage_category(pos_neg_percentages, percentages_per_category):
	max_pos = 0
	max_pos_category = None

	for idx, lst in enumerate(pos_neg_percentages):
		pos = lst[0]
		neg = lst[1]
		if pos > max_pos:
			max_pos = pos
			max_pos_category_idx = idx

	category,_ = percentages_per_category[max_pos_category_idx]
	return (category,pos_neg_percentages[max_pos_category_idx])

#Probably now need this function for each different city page
@irsystem.route('/', methods=['GET'])
def search():
	neighborhood = request.args.get('neigh')
	#price = request.args.get('price')
	time = request.args.get('time') #Possible options of time are default 0,1,6,12
	credibility = request.args.get('cred') #all users or elite users

	query = request.args.get('query')
	#Initial search page
	if not neighborhood:
		return render_template('search.html')

	#After loading in the main page, executing the search
	else:
		#Load in json_data
		json_data = load_json("pittsburgh")

		tf = load_json("tf")

		idf = load_json("idf")

		doc_norm = load_json("doc_norm")

		neigh_idx_lst = load_json("neighborhood_idx_dict")

		#Getting the appropriate reviews
		all_reviews, review_idx_lst = filter_reviews_and_filtered_review_idx_lst(json_data, neighborhood.lower(), credibility, time)

		#Get the index of the filtered reviews to compute SIMILARITY SCORE between filtered review and the quer
		#eigh_filtered_review_idx_to_all_review_idx = {filtered_idx:full_review_idx for filtered_idx,full_review_idx in (enumerate(review_idx_lst))}

		result_list = compute_similarity(query,tf[neighborhood],idf[neighborhood],doc_norm[neighborhood], neigh_idx_lst, neighborhood)

		#Calculating the percentages for the pie charts [(category, percentage)]
		reviews_per_category, percentages_per_category = filter_reviews_calc_percentage_by_category(all_reviews)

		#Calculating the positive/negative percentages for each category [[pos_percentage, neg_percentage]]
		#***ASSUME THAT THE ORDER IS IN THE ORDER SAME AS percentages_per_CATEGORY
		pos_neg_percentages_per_category = compute_pos_neg_percentages(reviews_per_category, percentages_per_category)

		#Calculating the top ranked restaurants per category [top3] where top3 = [(rest,star,address,and other infos)]
		#***ASSUME THAT THE ORDER IS IN THE ORDER SAME AS percentages_per_CATEGORY
		top_restaurants_infos_per_category_1, top_restaurants_infos_per_category_2 = compute_rest_infos_per_category(all_reviews, percentages_per_category, reviews_per_category, time)

		# get a list expanded queries
		expanded_query = query_expand(query)

		#If no reviews available, then return unfortunate page
		if all_reviews == []:
		 	return render_template('no_result.html')

		else:
			labels, data = format_percentage_for_html(percentages_per_category)
			top_category, lst = top_percentage_category(pos_neg_percentages_per_category, percentages_per_category)

			neighborhood = neighborhood[0].capitalize() + neighborhood[1:]
			city = "Pittsburgh"
			return render_template('result.html', labels = labels, data = data, \
									top_category = top_category, top_pos_percentage = lst[0], top_neg_percentage = lst[1], \
									pos_neg_percentages_per_category = pos_neg_percentages_per_category, \
									top_restaurants_infos_per_category_1 = top_restaurants_infos_per_category_1, \
									top_restaurants_infos_per_category_2 = top_restaurants_infos_per_category_2, \
								    neighborhood = neighborhood, time = time, credibility = credibility, city = city)

@irsystem.route('pred_stars', methods=['POST'])
def pred_stars():
	"""return the predicted stars from the input"""
	test = [34,24.0,29.7,96]
	res = request.get_json()


	name = res['rest_name']
	name_chars = name[:5]
	name_value = 0
	for i in name_chars:
		name_value += ord(i) - 69
	name_value = name_value / 5
	test[0] = name_value

	test[3] = int(res['rest_reviews'].strip())

	return pred(test)
