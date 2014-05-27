import json, requests, argparse

parser = argparse.ArgumentParser(
		prog='Meetup.com Photograph Bulk Downloader',
		description='Downloads the photographs associated with an event on meetup.com in bulk.'
	)

parser.add_argument('api_key', help='The API key to be used to access meetup.com to download the photographs.')
parser.add_argument('event_id', help='The event id for the event to download the photographs from.')
parser.add_argument('-o', '--output', help='The directory to put the downloaded photographs into.', dest='dir')
parser.add_argument('-p', '--page', help='The number of responses that should be returned per page.', dest='pageCnt', type=int)
parser.add_argument('-v', '--verbose', help='Runs the program in verbose mode.', action='store_true', default=0)
args = vars(parser.parse_args())

url = 'https://api.meetup.com/2/photos?&key=' + args['api_key'] + '&event_id=' + args['event_id']

argVar = args['pageCnt']
if(argVar):
	url = url + '&page=' + str(argVar)
print(url)

resp = requests.get(url).json()
pics = resp['results']

argVar = args['dir']
verbose = args['verbose']

print('Starting the download of the ' + str(len(pics)) + ' photographs...')
for photo in pics:
	photoUrl = photo['highres_link']

	if(verbose):
		print('Downloading ' + photoUrl + '...')

	presp = requests.get(photoUrl)
	filename = photoUrl.split('/')[-1]
	file = filename

	if(argVar):
		file = str(argVar) + filename

	with open(file, 'wb') as f:
		for chunk in presp.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()

print('Download complete')
