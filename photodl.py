import json, requests, argparse

def download(pics, opt):
	i = 0
	for photo in pics:
		i = i + 1
		photoUrl = photo['highres_link']

		if(opt['verbose']):
			print('Downloading ' + photoUrl + '...')
		elif(i % opt['markInterval'] == 0 and opt['markInterval'] >= 0):
			print(opt['mark'], end='', flush=True)

		presp = requests.get(photoUrl)
		filename = photoUrl.split('/')[-1]
		file = filename

		if(opt['dir']):
			file = opt['dir'] + filename

		with open(file, 'wb') as f:
			for chunk in presp.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
					f.flush()

def retrieve(opt):
	url = 'https://api.meetup.com/2/photos?'

	if(opt['key']):
	        url = url + '&key=' + opt['key']

	if(opt['aid']):
	        url = url + '&photo_album_id=' + opt['aid']

	if(opt['eid']):
	        url = url + '&event_id=' + opt['eid']

	if(opt['pageCnt']):
	        url = url + '&page=' + str(opt['pageCnt'])

	if(opt['offset']):
		url = url + '&offset=' + str(opt['offset'])
	print(url)
	return requests.get(url).json()

parser = argparse.ArgumentParser(
		prog='Meetup.com Photograph Bulk Downloader',
		description='Downloads the photographs associated with an event on meetup.com in bulk.'
	)

parser.add_argument('-k', '--apiKey', help='The API key to be used to access meetup.com to download the photographs.', dest='key')
parser.add_argument('-a', '--albumId', help='The photo album id for the album to download the photographs from.', dest='aid')
parser.add_argument('-e', '--eventId', help='The event id for the event to download the photographs from.', dest='eid')
parser.add_argument('-d', '--dir', help='The directory to put the downloaded photographs into.', dest='dir')
parser.add_argument('-p', '--page', help='The number of responses that should be returned per page.', dest='pageCnt', type=int)
parser.add_argument('-v', '--verbose', help='Runs the program in verbose mode.', action='store_true', default=0)
parser.add_argument('-o', '--offset', help='The number of pictures to skip before starting to return the photographs.', dest='offset', type=int)
parser.add_argument('-m', '--mark', help='The marker to be printed to screen to indicate activity.', dest='mark', default='.')
parser.add_argument('-n', '--markInterval', help='The intervals that an activity indicator should be printed to the screen.', dest='markInterval', type=int, default=1)
args = vars(parser.parse_args())

args['total'] = -1
args['count'] = 0
args['offset'] = 0

print('Starting the run...')

while(args['offset'] < args['total'] or args['total'] < 0):
	resp = retrieve(args)

	meta = resp['meta']
	args['count'] = int(meta['count'])
	args['offset'] = args['offset'] + int(meta['count'])
	args['total'] = int(meta['total_count'])
	args['pageCnt'] = args['total'] - args['offset']

	print()
	print('Starting the download for photographs ' + str(args['offset'] - int(meta['count'])) + ' to ' + str(args['offset']) + ' of ' + str(args['total']) + '', end='', flush=True)
	download(resp['results'], args)

print()
print('Download complete')
