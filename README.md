# jira dashboard


Dashboard for work jira project I made a while back.

Removed some project specific stuff such as URLs, or references to which project it is... or more accurately, was...

Tried running it again, several issues
1. Jira server that project uses is now hosted by clients on their internal network, can only be opened from a remote desktop, where I 
do not have admin rights to stand this thing up, even without docker as a development server
2. The requirements.txt is old, should have pinned the versions maybe, now installing the latest python packages
results in an invalid install that does not run due to the packages that were used having been updated since I wrote/used this dashboard


Would have been good if this thing ran, but oh well...

Since I cannot run it myself, no step-by-step guide on how to deploy this.

Honestly, the only problem I have really is the API, and I could just mock that for a demo, I do not need 100% correct data to show this off. 
 Also, could just fix the Flask backend server, but then I would need a Jira server to test this against, and due to point 1.
 that is not really possible.

So, cannot even add a current example of how this thing looks like, unfortunately.

Best thing I was able to find is from me sharing an in development version of it that I showed off to a friend way back 
that I had to dig up from the chat logs


#### early version of maintenance part, very far off from what would show now
![Alt text](docs/images/maintenance.png?raw=true)

#### change requests divided by developer, closer to current version of it
![Alt text](docs/images/change_requests.png?raw=true)

