import sentiment_analysis
from collections import defaultdict

def compare_timelimit_timeposted(time_limit, time_posted):
    """Returns true if the review's time posted satisfies the user input's time limit"""
    if time_limit == None:
        return 0

#######################################FILTERING REVIEWS############################################
def filter_reviews(j, zipcode, credibility=None, time_limit=None, price_range=None):
	"""Filter the reviews that match with user inputs.
    ***ASSUMES THAT JSON OBJECT HAS SAME TYPE AS THE INPUTS***

    Returns a list of reviews"""

    filtered_out_reviews = []
    for review in j["reviews"]:
        if (review["restaurant_zipcode"] == zipcode):
            cond1 = ((credibility != None) and (review["reviewer_credit"] == credibility)) or (credibility == None)
            #NEEDS TO HAVE A FUNCTION THAT COMPARES THIS TWO
            cond2 = ((time_limit != None) and (compare_timelimit_timeposted(time_limit, review["time_posted"]))) or (time_limit == None)
            cond3 = ((price_range != None) and (review["restaurant_price_range"] == price_range)) or (price_range == None)

            if (cond1 and cond2 and cond3):
                filtered_out_reviews.append(review)

    return filtered_out_reviews

def filter_pos_reviews(reviews):
    """Filter the reviews that are positive from [reviews].
    Review is considered positive if its sentiment intensity is >=0.1

    [reviews]: list of JSON objects"""

    pos_reviews = []
    for review in reviews:
        if (sentiment_analysis.compute_sentiment_intensity(review["text"])>=0.1):
            pos_reviews.append(review)

    return pos_reviews

def filter_neg_reviews(reviews):
    """Filter the reviews that are negative from [reviews].
    Review is considered negative if its sentiment intensity is <=-0.1

    [reviews]: list of JSON objects"""

    neg_reviews = []
    for review in reviews:
        if (sentiment_analysis.compute_sentiment_intensity(review["text"])<=0.1):
            neg_reviews.append(review)

    return neg_reviews

###############################COMPUTING PERCENTAGES OF EACH TYPE##################################
def compute_percentage_per_type(reviews):
    """Computes the percentages of the reviews for each type

    Returns a dictionary in format {\cuisine type: percentage}

    [reviews]: list of JSON objects"""

    n_reviews = len(reviews)
    percentage_dict = defaultdict(int)

    for review in reviews:
        percentage_dict[review["restaurant_type"]] += 1

    for type in percentage_dict.keys():
        percentage_dict[type] /= n_reviews

    return percentage_dict

###############################COMPUTING TOP RESTAURANTS PER TYPE##################################
def filter_reviews_type(reviews,type):
    """Filter [reviews] by [type].
    Returns a list of JSON objects."""

    reviews_of_type = []
    for review in reviews:
        if (review["restaurant_type"]==type):
            reviews_of_type.append(review)

    return reviews_of_type

def compute_top_rest(reviews):
    """Computes the top restaurant for [reviews].
    Returns a sorted list of restaurants in the order of decreasing popularity."""

    rest_stars_dict = defaultdict(int)

    for review in reviews:
        rest_stars_dict[review["restaurant"]] += review["stars_given"]

    ranked_rest_lst = [k for k in sorted(rest_stars_dict, key=rest_stars_dict.get, reverse=True)]

    return ranked_rest_lst

def compute_top_rest_per_type(reviews):
    """Computes the top restaurant list for each type in [reviews] that has
    review percentage over 1%

    Returns a dicitonary in format {\cuisine type: lst of restaurants}"""

    rest_per_type_dict = defaultdict(list)
    percentages = compute_percentage_per_type(reviews)

    for type in percentages.keys():
        if percentages[type] >= 0.01:
            reviews_of_type = filter_reviews_type(reviews,type)
            top_rest_list = compute_top_rest(reviews_of_type)
            rest_per_type_dict[type] = top_rest_list

    return rest_dict
