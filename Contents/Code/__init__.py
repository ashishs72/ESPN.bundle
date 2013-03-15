TITLE = 'ESPN'
ART = 'art-default.jpeg'
ICON = 'icon-default.png'
ESPN_LIVE = "http://espn.go.com/watchespn/feeds/startup?action=live&channel=%s"
ESPN_PLAYER = "http://espn.go.com/watchespn/player/_/id/"

####################################################################################################
def Start():

	Plugin.AddPrefixHandler('/video/espn', MainMenu, TITLE, ICON, ART)
	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	ObjectContainer.view_group = 'InfoList'

	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)

####################################################################################################
def MainMenu():

	oc = ObjectContainer()
	oc.add(DirectoryObject(key = Callback(GetEvents, title = "espn1"), title = 'ESPN'))
	oc.add(DirectoryObject(key = Callback(GetEvents, title = "espn2"), title = 'ESPN 2'))
	oc.add(DirectoryObject(key = Callback(GetEvents, title = "espn3"), title = 'ESPN 3'))
	oc.add(DirectoryObject(key = Callback(GetEvents, title = "espnu"), title = 'ESPN U'))
	return oc

####################################################################################################
@route('/video/espn/getevents')
def GetEvents(title):

	oc = ObjectContainer()

	for item in XML.ElementFromURL(ESPN_LIVE % (title), cacheTime=300).xpath('//events/event'):
		item_title = item.xpath('./name')[0].text
		league = item.xpath('./league')[0].text
		oc.add(VideoClipObject(
		        url = ESPN_PLAYER + item.get('id'),
		        title = (league + " - " + item_title) if league != "" else (item_title),
		        summary = item_title,
		        thumb = Resource.ContentsOfURLWithFallback(url=item.xpath('./thumbnail/large')[0].text, fallback=ICON)))

	return oc