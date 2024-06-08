Needs in order for website to be functional: 
 
- Secure money transferring system (percentage that we take automatically gets taken out) 
  - solution: stripe connect
- File transferring system (preferably some type of cloud system where I can upload raw footage that clients send and they upload finished files)   
  - Amazon s3 for downloading all the videos into storage and a db to have stuff like references to the video and other meta data. Downloading and uploading can be done using a queue to ensure that it doesn't burden the system too much
- Message system for Editors
  - sockets, database shit not bad
- Client message system
  - same as above
- Way for me to match editors with clients who are applying using the website.
  - admin page where dwight reviews clients and matches to an editor
- Client application page, they list what they need, a reference if needed, and budget. This will reach my POV and I can match them with the editor that fits their needs the best
  - just database stuff and some sort of admin page for dwight that can view applications
    - `GET /api/applications/`
- Editor application page. Here will be where future editors can apply. There will be sample footage that I already got agreed to use and editors can submit their application along with an edited test/sample vid so I can see what they can do. This page will be super useful later on but its not as important as the other pages because we can just submit job postings on other sites at the start.
  - same thing as application page except for editors 
  
tech semantics
MongoDB for the main database
Amazon s3 for file transfering 
Websocket for realtime messaging
admin page for viewing applications for clients and editors 
seperate application pages for client/editors

roadmap
flask routes crud routes for
- applications
- messaging
- file transfering 
- stripe connect
- add queue to file transfering

frontend next

mongodb creds
justin03tubay
j4podRLoAb7pZVJt

jwt
u0GJPnC7BX89TXoykxo3D7zR7rdORWXGkhR7kxuToHI=

currently working on
folder
file
message

editor applies to be cool editor on cool team
client posts job
dote picks editor for job
client can message editor



- make a route that gets folders shared with you and display those on folder page
- client sees users that are interested and can start a chat with them
- messaging