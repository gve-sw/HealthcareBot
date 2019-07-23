from webexteamssdk import WebexTeamsAPI

api = WebexTeamsAPI()

all_rooms = api.rooms.list()
print("one ---------------")
for room in all_rooms:
	print(room.title)

all_memberships=api.memberships.list()
print("one ---------------")
for memeber in all_memberships:
	for element in memeber:
		print(element+":"+memeber[element])



special_membership=api.memberships.list(personEmail='agabdelb@cisco.com')
print("one ---------------")
for user in special_membership:
	print(user.personId)

