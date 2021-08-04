document.addEventListener('DOMContentLoaded', function(){

    get_groups();

})




function get_groups(){

    // find each group that current user has access to
    // this function makes an API call to the get_groups view in views.py
    fetch(`/groups`)
    .then(response => response.json())
    .then(group => {

        console.log(group);

        // for each group received, write data to html
        for (let i = 0; i < group.length; i++){

            let name_div = document.createElement('div')
            name_div.innerHTML = group[i]['name']

            // add event listener to display relevant chat for each group
            name_div.addEventListener('click', function(){
                
                //get_messages function defined below
                get_messages(group[i]['id'])
            })
            
            // write data to page
            document.querySelector('#groups-view').appendChild(name_div)

        }
    

    })
}



function get_messages(id){

    // clear previous messages
    while(document.querySelector('#messages-view').firstChild) {
        document.querySelector('#messages-view').removeChild(document.querySelector('#messages-view').firstChild);
    }

    document.querySelector('#chat-view').style.display = 'block';

    // make an API call for all messages that fall under the correct group
    fetch(`/messages/${id}`)
    .then(response => response.json())
    .then(messages => {

        console.log(messages)

        // display each message
        for (let i = 0; i < messages.length; i++){

            let message_div = document.createElement('div')
            message_div.innerHTML = `${messages[i]['creator']} said: ${messages[i]['content']}`

            document.querySelector('#messages-view').appendChild(message_div)

        }

    })

}