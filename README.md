Calendar Service

###Application Requirements:
1. Login & Register of users
2. A user should be able to create their own availability in hourly intervals
3. Another user can come and check for the available time for a user of their choice
4. Depending on their timings a user must be able to book others time. If booked, the timing will be occupied for both the users.
5. Show an error response when an unauthenticated user is trying to access the APIs

### MODELS:
(ID will be an auto-generated field in each model)
#### 1. User:
+ (Name, email, hashedPassword)
#### 2. Slot:
+ (user, startTime, endTime, bookedBy)

### APIs:
1. USER
+ `/user/register (POST): userName`
+ `/user/logout (GET): `
+ `/user/login (POST): `
+ `/user (GET): Gets a user’s details by id or emails`

2. SLOTS
+ `/slot: (POST): auto-authenticated. Allows a user to create a slot.`
+ `/slot: (GET): get info by slot id or by user`
+ `/slot (PUT): Edit a slot (change startTime & endTime subject to constraints)`
+ `/slot (DELETE): delete a slot subject to constraints`


###Questions:
1. Can a slot timing be changed once defined? If yes, what all needed to be checked?
eg. if there is any booking related to that slot, so we need to check for all the booking and slot for every user involved?
- Assumption: No it can not be changed

2. Can a slot be cancelled/deleted?
- Assumption: It can be changed only when there is not any booked_by user, linked to that slot.
