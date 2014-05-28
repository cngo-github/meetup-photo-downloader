import json, requests, argparse

def download(pics, dir, verbose):
	for photo in pics:
	        photoUrl = photo['highres_link']

	        if(verbose):
	                print('Downloading ' + photoUrl + '...')

	        presp = requests.get(photoUrl)
	        filename = photoUrl.split('/')[-1]
	        file = filename

	        if(dir):
	                file = dir + filename

	        with open(file, 'wb') as f:
        	        for chunk in presp.iter_content(chunk_size=1024):
                	        if chunk:
                        	        f.write(chunk)
                                	f.flush()

def retrieve(key, albumId, eventId, cntPerPage, offset):
	url = 'https://api.meetup.com/2/photos?'

	if(key):
	        url = url + '&key=' + key

	if(albumId):
	        url = url + '&photo_album_id=' + albumId

	if(eventId):
	        url = url + '&event_id=' + eventId

	if(cntPerPage):
	        url = url + '&page=' + str(cntPerPage)

	if(offset):
		url = url + '&offset=' + str(offset)

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
args = vars(parser.parse_args())

key = args['key']
aid = args['aid']
eid = args['eid']
pageCnt = args['pageCnt']
dir = args['dir']
verbose = args['verbose']

while((args['count'] + args['offset'] < args['total']) && args['total'] >= 0):
	resp = retrieve(args['key'], args['aid'], args['eid'], args['pageCnt'],
cnt = int(meta['count'])
total = int(meta['total_count'])


print('Starting the download of the ' + str(len(pics)) + ' photographs...')
download(pics, dir, verbose)
print('Download complete')
