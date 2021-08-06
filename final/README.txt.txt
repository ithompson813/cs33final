Introduction

Welcome to my final project!

In essence, I wanted to create a web application that functions similar to popular chat services such as Slack, Microsoft Teams, or Discord. 

Simply log in and follow the new group link to start a chat room. Invite your specified users (in this case, you may need to create multiple accounts) and give the group a name. You may then click on the group's name on the left side of your screen to begin chatting. 

The format of my project is very similar to project 4, and indeed is built off of the same distribution code. The functionality flows from JavaScript events called on HTML elements which then make API calls to views.py in the Django backend. Views.py returns the relevant info to update the HTML display for the user.


Models

There are three models involved in the project. The first is the default django User model which extends the AbstractUser. No further changes were required on my end to track users and I used the default User for all user tracking.

The remaining two models powered the database for this project. The Message model represents an individual message sent by the user, and each message is assigned to a Group.

The Message model stores the following data:
 
Author: Called the ‘creator’ in the model itself - this is a foreign key which represents the User who wrote the message.
Content: The text that the user wrote
Group: A foreign key representing the group that the message should be assigned to. 
Timestamp: When the message was written.
ID: A numerical ID is automatically assigned at creation. 

The Group model stores the following data:
	
Name: Name assigned to the group by the user at creation
Users: A many to many field representing the users who have access to the group. The user who starts the group is automatically included.
ID: A numerical ID is automatically assigned at creation.


Group Creation


As long as a user is logged into the site, they will have the option to create a new group by following the New Group link on the left side of their screen. This link will take them to the new_group.html page by following the new_group view in views.py. On this page, they will be presented with a NewGroupForm that they can use to create the group itself. The user will assign the group a name and invite their user’s of choice, and upon submission the new_group view will create the group object. The user is then returned to the index page of the site. 


Displaying Groups

On the index page, the user will be shown a list of the groups that they are a part of on the left bar. This is done by making an API call when the page is finished loading that receives a list of the group objects that contain the current user in the ‘users’ list of the group itself. This is done by following the get_groups() function in JS, which then fetches the data through the get_groups view in views.py. 

The get_groups() function then writes the group data into html elements and displays them on the page. Each element has an onclick function which will display the correct chat room to the user.


Displaying Messages

When a group html element is clicked, the onclick function for that group calls the get_messages() function. This function takes a group’s ID as an argument, which is passed by the onclick function.

The get_messages function makes an API call to the get_messages view in views.py. This view makes a security check to ensure that the current user has access to the group in question. If this passes, the get_messages view returns a JSON list of all messages assigned to the group. This data is then assigned to an html element and written to the page for the user to see. 

Messages are written to the messages-view div on the page. This div is a scrollable box to prevent the page from growing in length as more messages are written. Each message is shown in the format of (<User> said: <Content>). The newest messages are displayed at the top of the page to ensure relevant information is always displayed. The size of the messages-view scales with the screen size of the user. 


Writing Messages

As long as the user is being displayed a group of messages, they will find a chatbox in the form of a textarea pinned to the bottom of the page. Content can be typed into this chatbox, and when the onclick function of the button is triggered a new message will be created. 

This is performed by the post_chat() function and utilizes the post_chat view in views.py. The function makes an API call to POST a new message into the database. The relevant data is collected from the html elements on the page and passed to the view. The view first ensures that the user has access to the group they are trying to chat in and then creates a new message object assigned to the correct group.

The post_chat() function finishes by immediately refreshing the chat by recalling the get_messages() function on the current group.


Updating The Chat

Because many users are able to write simultaneously into one chatroom, the messages-view would need to be continuously updated to show all messages. This is done by starting an interval function as soon as the page is loaded. The update_chat() function houses this process.

Update_chat() utilizes a global variable called last_update. Last_update represents the datetime when the messages in the chatroom were last updated. Last_update is assigned to the current time whenever get_messages() is called. 

The update_chat() function makes the same API call as get_messages() to get the relevant messages for the current group. The function then checks the timestamp for the most recent message and determines if it was posted after the last_update time. If this is true, then the chat is out of date and function rewrites the chat by calling get_messages. This check is performed every two seconds. 


