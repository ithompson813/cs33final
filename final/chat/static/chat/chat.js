
// gloabal variable last_update tracks the most recent time the message log was udpated
// this is used to determine if a new message is in the log and needs to be refreshed
// see update_chat functin, defined below
let last_update = new Date();


document.addEventListener('DOMContentLoaded', function(){

    //immediately load available groups for user
    get_groups();

    //begin chat update function which calls at an interval if conditions are met, defined below
    update_chat();

    //add onclick event to the chat button to post a new chat message
    document.querySelector('#chat_button').addEventListener('click', function(){

        post_chat();

    })
 
})



function get_groups(){

    // find each group that current user has access to
    // this function makes an API call to the get_groups view in views.py
    fetch(`/groups`)
    .then(response => response.json())
    .then(group => {

        //console.log(group);

        // for each group received, write data to html
        for (let i = 0; i < group.length; i++){

            let name_div = document.createElement('div')
            name_div.innerHTML = group[i]['name']

            // add event listener to display relevant chat for each group
            name_div.addEventListener('click', function(){
                
                //get_messages function defined below
                get_messages(group[i]['id']);
            })
            
            // write data to page
            document.querySelector('#groups-view').appendChild(name_div)

        }
    

    })
}



function get_messages(id){

    document.querySelector('#messages-view').setAttribute('name', `${id}`);


    // clear previous messages
    while(document.querySelector('#messages-view').firstChild) {
        document.querySelector('#messages-view').removeChild(document.querySelector('#messages-view').firstChild);
    }

    document.querySelector('#chat-view').style.display = 'block';

    // make an API call for all messages that fall under the correct group
    fetch(`/messages/${id}`)
    .then(response => response.json())
    .then(messages => {

        // display each message
        for (let i = 0; i < messages.length; i++){

            // assign data to a div
            let message_div = document.createElement('div')
            message_div.innerHTML = `${messages[i]['creator']} said: ${messages[i]['content']}`

            // write data to top of message-view box
            document.querySelector('#messages-view').insertBefore(message_div, document.querySelector('#messages-view').firstChild)

        }

        //update last_update to now
        last_update = new Date()

    })

}


function post_chat(){

    // get info from html page
    message = document.querySelector('#chatbox').value;
    group_id = document.querySelector('#messages-view').getAttribute('name');

    // pass info to database using an API call
    fetch('/post_chat', {
        method: 'POST',
        body: JSON.stringify({
            content: message,
            group: group_id
        })
    }) .then (result => {

        // refresh chat
        get_messages(group_id);

        //clear the chatbox
        document.querySelector('#chatbox').value = "";
    })
}


function update_chat(){

    // at a set interval, check if the chat needs to be refreshed
    setInterval(function(){ 

        // if a group's view is displayed
        if (document.querySelector('#messages-view').hasAttribute('name')){

            // track id
            id = document.querySelector('#messages-view').getAttribute('name')

            // call API to get messages
            fetch(`/messages/${id}`)
            .then(response => response.json())
            .then(messages => {

                // check the time of the most recent post
                let latest_time = new Date(messages[messages.length-1]['timestamp']);

                // if most recent post was made after last chat update, refresh chat
                if (last_update < latest_time){

                    // refresh messages
                    get_messages(document.querySelector('#messages-view').getAttribute('name'))

                    // update last update to now
                    last_update = new Date()

                }
                
            })
        }
      
    // this check is performed every 2 seconds
    }, 2000);

}