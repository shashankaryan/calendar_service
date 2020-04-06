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
+ (user, startTime, endTime)

####3. Booking: 
+ (slot,bookedBy)

### APIs:
1. USER
+ `/user/register (POST): userName`
+ `/user/logout (GET): `
+ `/user/login (POST): `
+ `/user (GET): Gets a user’s details by id`

2. SLOTS
+ `/slot: (POST): auto-authenticated. Allows a user to create a slot.`
+ `/slot: (GET): get info by slot id or by user`
+ `/slot (PUT): Edit a slot (change startTime & endTime subject to constraints)`
+ `/slot (DELETE): delete a slot subject to constraints`

3. BOOKING
+ `/booking (GET): Gets bookings by user / bookedBy`
+ `/booking (POST): Create a booking`
+ `/booking (DELETE): Delete a booking.` 


###Questions:
1. Can a slot timing be changed once defined? If yes, what all needed to be checked?
eg. if there is any booking related to that slot, so we need to check for all the booking and slot for every user involved?
- Assumption: No it can not be changed

2. Can a slot be cancelled/deleted?
- Assumption: It can be changed only when there is not any booking related to that slot. For editing a slot, first the related booking will have to be deleted.

3. Can a booking be cancelled/deleted?
- Assumption: Yes, it can be cancelled, but only before the start time of the slot i.e. startTime > currentTime
