from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models import sentiment_analysis
from app.irsystem.models import search

project_name = "Foodies : The Food Hunters of NYC"
net_id = "Jae Min Cha : jc988, Woo Kyung Lee : wl357, Jung Yun Park : jp862, Kee Hoon Lee : kl546, Chong Tian : ct465"

@irsystem.route('/', methods=['GET'])
def search():
	city = request.args.get('city')
	neighborhood = request.args.get('neigh')
	#price = request.args.get('price')
	time = request.args.get('time') #Possible options of time are default 0,1,6,12
	credibility = request.args.get('cred') #default 0 or 1

	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
