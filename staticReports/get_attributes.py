import json
# JSON keys to be deleted
delKeys = ['apkid','appsec','average_cvss','binary_analysis','browsable_activities','certificate_analysis',
	'dynamic_analysis_done','emails','exported_count','file_analysis','firebase_urls',
	'icon_found','icon_hidden','network_security','playstore_details','providers',
	'quark','receivers','secrets','sha1','sha256','size','strings','target_sdk','title',
	'version_code','virus_total']

try:
	with open('analyze.json') as json_data:
	    data = json.load(json_data)
	    for key in data.keys():
	    	if key in delKeys:
	    		del data[key]

	json_object = json.dumps(data, indent=4)
	file_name = data['md5'] + '.json'
	with open(file_name,'w') as testfile:
		testfile.write(json_object)
	print("success")
except:
	print("fail")
