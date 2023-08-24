# MeetHour-Python-Example

![MeetHour Logo](logo.png)

[Meet Hour - 100% free video conference solution](https://meethour.io)
Meet Hour is 100% free video conference solution with End to End Encrypted and many other features such as lobby mode, Donor box & Click&Pledge Connect for fundraising, Video call recording, Youtube Live Stream etc.

# Features:

    ✅  Free Unlimited Time Group Video Conference
    ✅  Upto 100 Participants Group Meeting
    ✅  Free Video Conference Recording
    ✅  YouTube Live Stream
    ✅  Raise funds via Click&Pledge Connect & DonorBox
    ✅  Virtual Background
    ✅  Live Pad
    ✅  Screensharing on Desktop & Mobile and many other features.

# Try out one free session -

    1. Website - https://meethour.io
    2. Android - https://bit.ly/2U239ll
    3. iOS - https://apple.co/3k8Rpbn

![ScreenShot](screenshot.png)

# MeetHour API Documentation

API Documentation Link - https://docs.v-empower.com/docs/MeetHour-API/


## Install

```
    
    poetry install
```

### Steps to run the Example

1. Go to meethour.io and signup for Developer or Higher plan. Currently we offer 28 days free trial. 
2. Go to the dashboard and then click on developers menu. 
3. Later go to constants.php and enter all the credentials of database and Meet Hour credentials as well. 
4. On Home page Click on Get Access Token 
5. Then Try Schedule a Meeting & Join Meeting. 

### Usage

Provide your credentials in the constructor of Login object and hit the login api to get your access token. Which will further be used for making rest of the api calls.

```
    import src.meethour.type.LoginType,ScheduleMeetingType, ViewMeetings
    import meethour.services.apiServices as apiServices

    apiservice = apiServices.MHApiService()

    loginBody = LoginType.LoginType('CLIENT_ID', 'CLIENT_SECRET', 'GRANT_TYPE', 'EMAIL', 'PASSWORD') # pass values
            login_response = apiservice.login(loginBody)
            print(login_response)

    scheduleMeetingBody= ScheduleMeetingType.ScheduleMeeting( )
            schedule_meeting_response = apiservice.schedule_meeting(token, scheduleMeetingBody)
            print(schedule_meeting_response)

    viewMeetingBody = ViewMeetings.ViewMeeting('meeting_id') #pass value
            view_meetings_response = apiservice.view_meetings(token, viewMeetingBody)
            print(view_meetings_response)
```

### API End Points Supported

Important points:
=> Instead of '{version}', you to pass our latest version whenever you call the given functions. Currently we are using v1.2 Same version applies to the below calls.
=> In the token section, you need to pass the received access token which is received when login api is hit, for making further api calls.
=> You can make API calls by passing required properties in the constructor. But, to meet special requirements you can set rest of the properties directly, according to your need. For more details go to https://docs.v-empower.com/docs/MeetHour-API then click on APIS section to get all the information related to each api call.

1. To Get Access Token Endpoint : => https://docs.v-empower.com/docs/MeetHour-API/a44a7d7669f91-user-login-get-access-token

   ```
        from meethour.type import LoginType
        apiservice = apiServices.MHApiService()

        loginBody = LoginType.LoginType('CLIENT_ID', 'CLIENT_SECRET', 'GRANT_TYPE', 'EMAIL', 'PASSWORD') # pass values
        login_response = apiservice.login(loginBody)
        print(login_response)

   ```

   => You have to pass respective values in the argument section. Hence, to get desired response.

2. To schedule a meeting: => https://docs.v-empower.com/docs/MeetHour-API/2de4b757a6312-meeting-schedule-meeting

   ```
        from meethour.type import ScheduleMeetingType
        apiservice = apiServices.MHApiService()

        scheduleMeetingBody= ScheduleMeetingType.ScheduleMeeting( )
        schedule_meeting_response = apiservice.schedule_meeting(token, scheduleMeetingBody)
        print(schedule_meeting_response)

   ```

3. To Generate JWT Token Endpoint => https://docs.v-empower.com/docs/MeetHour-API/b7e3d0ab3906f-generate-jwt

   ```
        from meethour.type import GenerateJwtType
        apiservice = apiServices.MHApiService()

        generateJwtBody= GenerateJwtType.GenerateJwt("meeting_id","contact_id") # pass values
        generate_jwt_response = apiservice.generate_jwt(token, generateJwtBody)
        print(generate_jwt_response)

   ```

4. To fetch User Details: => https://docs.v-empower.com/docs/MeetHour-API/ff9d0e37d9191-user-details

   ```
        from meethour.type import user_details
        apiservice = apiServices.MHApiService()

        userDetailsBody= user_details.user_details(0,0,0,0)  
        user_details_response = apiservice.user_details(token, userDetailsBody)
        print(user_details_response)

   ```

5. To fetch access Token using Refresh Token: => https://docs.v-empower.com/docs/MeetHour-API/d851be1af9804-get-access-token-using-refresh-token

```
    from meethour.type import RefreshToken
    apiservice = apiServices.MHApiService()

    refreshTokenBody= RefreshToken.RefreshToken('refresh_token','CLIENT_ID','CLIENT_SECRET','access_token') #pass values
    refresh_token_response = apiservice.refresh_token(token, refreshTokenBody)
    print(refresh_token_response)
 
```

6. To add a contact in Meet Hour database: => https://docs.v-empower.com/docs/MeetHour-API/bd1e416413e8c-add-contact

```
        from meethour.type import AddContactType
        apiservice = apiServices.MHApiService()

        addContactBody = AddContactType.AddContactType("EMAIL","Fristname","lastname","phone","country_code ","Image","1")     #pass values
        add_contact_response = apiservice.add_contact(token, addContactBody)
        print(add_contact_response)
```

7. To get Timezones of various countries: => https://docs.v-empower.com/docs/MeetHour-API/c688c29bce9b9-timezone-list

   ```
        from meethour.type import time_zone
        apiservice = apiServices.MHApiService()

        timeZoneBody= time_zone.time_zone(0,0,0)
        timeZone_response = apiservice.time_zone(token, timeZoneBody)
        print(timeZone_response)

   ```

8. To get list of all the contacts in your Meet Hour account: => https://api.meethour.io/api/{version}/customer/contacts

   ```
        from meethour.type import ContactsType
        apiservice = apiServices.MHApiService()

        contactsBody = ContactsType.ContactsType(0,0,0)
        contacts_response = apiservice.contacts(token, contactsBody)
        print(contacts_response)

   ```

9. To make changes in the existing contact details: => https://docs.v-empower.com/docs/MeetHour-API/28cae9187d215-edit-contact

   ````
        from meethour.type import EditContactType
        apiservice = apiServices.MHApiService()

        editContactsBody= EditContactType.EditContactType("id","countrycode","EMAIL", "Firstname","lastname","Image","1","phone") # pass values

        edit_contacts_response = apiservice.edit_contact(token, editContactsBody)
        print(edit_contacts_response)

   ````

10. To get Upcoming Meetings: => https://docs.v-empower.com/docs/MeetHour-API/31df88388416d-upcoming-meetings

    ```
        from meethour.type import UpcomingMeetings
        apiservice = apiServices.MHApiService()

        upcomingMeetingsBody= UpcomingMeetings.UpcomingMeetings()
        upcoming_meetings_response = apiservice.upcoming_meetings(token, upcomingMeetingsBody)
        print(upcoming_meetings_response) 

    ```

11. To archive a meeting: => https://docs.v-empower.com/docs/MeetHour-API/1dd64523cc6bf-archive-meeting

    ```
        from meethour.type import ArchiveMeeting
        apiservice = apiServices.MHApiService()

        archiveMeetingBody = ArchiveMeeting.ArchiveMeetings("id")   # pass value
        ArchiveMeeting_response = apiservice.archive_meetings(token, archiveMeetingBody)
        print(ArchiveMeeting_response)

    ```

12. To get the details of a missed meeting: => https://docs.v-empower.com/docs/MeetHour-API/92998e2dda102-missed-meetings

    ```
        from meethour.type import MissedMeeting
        apiservice = apiServices.MHApiService()

        missedMeetingsBody = MissedMeeting.MissedMeetings()
        missed_meetings_response = apiservice.missed_meetings(token, missedMeetingsBody)
        print(missed_meetings_response)

    ```

13. To get completed meetings: => https://docs.v-empower.com/docs/MeetHour-API/aa9ef6a678250-completed-meetings

    ```
        from meethour.type import CompletedMeetingsType
        apiservice = apiServices.MHApiService() 

        completedMeetingsBody = CompletedMeetingsType.CompletedMeetings()
        completed_meetings_response = apiservice.completed_meetings(token, completedMeetingsBody)
        print(completed_meetings_response)
    ```

14. To edit an existing meeting: => https://docs.v-empower.com/docs/MeetHour-API/5dedde36380b4-meeting-edit-meeting

    ```
        from meethour.type import EditMeetingType
        apiservice = apiServices.MHApiService() 

        editMeetingBody = EditMeetingType.EditMeeting('meeting_id') #pass value
        edit_meeting_response = apiservice.edit_meeting(token, editMeetingBody)
        print(edit_meeting_response)
    ```

15. To view a meeting: => https://docs.v-empower.com/docs/MeetHour-API/7e9a0a1e0da7f-meeting-view-meeting

    ```
        from meethour.type import ViewMeetings
        apiservice = apiServices.MHApiService() 

        viewMeetingBody = ViewMeetings.ViewMeeting('meeting_id') #pass value
        view_meetings_response = apiservice.view_meetings(token, viewMeetingBody)
        print(view_meetings_response)

    ```

16. To get all the recordings list: => https://docs.v-empower.com/docs/MeetHour-API/ce7c4fd8cae7e-recording-list

    ```
        from meethour.type import RecordingsList
        apiservice = apiServices.MHApiService() 

        recordingsListBody = RecordingsList.RecordingsList('Local') # storage location
        recordings_list_response = apiservice.recordings_list(token, recordingsListBody)
        print(recordings_list_response)

    ```


## Continous integration

### GitHub Actions
Tests are run whenever there is a commit, see `.github/workflows/test.py` for details.

### Code coverage
Enable code coverage reporting to [Codecov](https://codecov.io/) by creating a secret with name `CODECOV_TOKEN` in your repository settings (Settings -> Secrets -> New sectret) and value set to the token created by Codecov.
