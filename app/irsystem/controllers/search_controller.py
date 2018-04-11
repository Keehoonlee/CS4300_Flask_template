from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models import sentiment_analysis

project_name = "Foodies : The Food Hunters of NYC"
net_id = "Jae Min Cha : jc988, Woo Kyung Lee : wl357, Jung Yun Park : jp862, Kee Hoon Lee : kl546"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
