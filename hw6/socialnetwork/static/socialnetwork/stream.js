"use strict"

function loadPosts() {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) return;
        updatePage(xhr);
    };
    xhr.open("GET", "/socialnetwork/get-global", true);
    xhr.send();
}

function loadfollowerPosts() {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4) return;
        updatePage(xhr);
    };
    xhr.open("GET", "/socialnetwork/get-follower", true);
    xhr.send();
}

function updatePage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updateStream(response)
        return
    }

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateStream(data) {
    let allPosts = document.getElementById("my-posts-go-here");

    data.posts.forEach(post => {
        let postElement = document.getElementById(`id_post_div_${post.id}`);

        if (!postElement) {
            postElement = makePostHTML(post);
            let allComments = document.createElement("div");
            allComments.id = `my-comments-go-here_${post.id}`;

            postElement.append(allComments);
            let commentBox = makeNewCommentBoxHTML(post);
            postElement.append(commentBox);
            allPosts.prepend(postElement);
        }

        let allComments = document.getElementById(`my-comments-go-here_${post.id}`);

        data.comments.forEach(comment => {
            if (post.id === comment.post_id) {
                if (!document.getElementById(`id_comment_div_${comment.id}`)) {
                    let commentElement = makeCommentsHTML(comment);
                    commentElement.id = `id_comment_div_${comment.id}`;
                    allComments.append(commentElement);
                }
            }
        });
    });
}

function makePostHTML(post){
    let mypost = document.createElement("div");
    mypost.classList.add("id_post_div_");
    mypost.id= `id_post_div_${post.id}`;

    let postAuthor = makeProfileLinkHTML(post);
    postAuthor.id = `id_post_profile_${post.id}`;

    let postTime = makeDateTimeHTML(post);
    postTime.id = `id_post_date_time_${post.id}`;

    let message = document.createElement('span');
    message.id = `id_post_text_${post.id}`
    console.log(post.message)
    message.textContent = post.message;

    let separator1 = document.createTextNode(" - ");
    let separator2 = document.createTextNode(" - ");

    mypost.appendChild(postAuthor);
    mypost.appendChild(separator1);
    mypost.appendChild(message);
    mypost.appendChild(separator2);
    mypost.appendChild(postTime);

    return mypost;

}

function makeCommentsHTML(comment) {
    let mycomment = document.createElement("div");
    mycomment.classList.add("id_comment_div_");
    mycomment.id= `id_comment_div_${comment.id}`;

    let commentAuthor = makeCommentProfileLinkHTML(comment);
    commentAuthor.id = `id_comment_profile_${comment.id}`;

    let commentTime = makeDateTimeHTML(comment);
    commentTime.id = `id_comment_date_time_${comment.id}`;

    let message = document.createElement('span');
    message.id = `id_comment_text_${comment.id}`
    message.textContent = comment.message;
    let separator1 = document.createTextNode(" - ");
    let separator2 = document.createTextNode(" - ");

    mycomment.appendChild(commentAuthor);
    mycomment.appendChild(separator1);
    mycomment.appendChild(message);
    mycomment.appendChild(separator2);
    mycomment.appendChild(commentTime);

    return mycomment;
}

function makeDateTimeHTML(post) {
    let date = document.createElement('span');
    date.classList.add("id_post_date_time_");
    let creationTime = new Date(post.creation_time);
    let formattedTime = `${creationTime.toLocaleString('en-US', { 
        month: 'numeric', 
        day: 'numeric', 
        year: 'numeric', 
        hour: 'numeric', 
        minute: 'numeric', 
        hour12: true 
    })}`.replace(',', '');

    date.textContent = formattedTime;
    return date;

}

function makeProfileLinkHTML(post) {
    let link = document.createElement('a');
    link.classList.add('id_post_profile_');
    link.href = `/socialnetwork/follower_page/${post.user_id}`;
    link.textContent = `Post By: ${post.user_first} ${post.user_last}`;

    return link;
}

function makeCommentProfileLinkHTML(comment) {
    let link = document.createElement('a');
    link.classList.add('id_post_profile_');
    link.href = `/socialnetwork/follower_page/${comment.user_id}`;
    link.textContent = `Comment By: ${comment.user_first} ${comment.user_last}`;

    return link;
}

function makeNewCommentBoxHTML(post) {

    let comment = document.createElement("div");
    comment.classList.add("id_comment_input_text_");

    let label = document.createElement("label");
    label.setAttribute("for", `id_comment_input_text_${post.id}`); 
    label.textContent = "Comment:";

    let input = document.createElement("input");
    input.id = `id_comment_input_text_${post.id}`;
    input.type = "text";

    let button = document.createElement("button");
    button.id = `id_comment_button_${post.id}`;
    button.textContent = "Submit";


    button.onclick = function() {
        addComment(post, input)
            
    };

    comment.append(label);
    comment.append(input);
    comment.append(button);

    return comment;
    
}

function addComment(post, input) {
    let comment_text = input.value;
        input.value = ''; 
        displayError('');

        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) return;
            if (xhr.status == 200) {
                let response = JSON.parse(xhr.responseText);

                let allComments = document.getElementById(`my-comments-go-here_${post.id}`);
                if(allComments) {
                    let new_comment = makeCommentsHTML(response.comments[response.comments.length - 1]);
                    allComments.appendChild(new_comment);
                } else {
                    displayError(`Failed to add comment. Status: ${xhr.status}`)
                }
            }
        };

        xhr.open("POST", "/socialnetwork/add-comment", true);
        xhr.setRequestHeader("Content-type",  "application/x-www-form-urlencoded");
        xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        xhr.send(`comment_text=${comment_text}&post_id=${post.id}&csrfmiddlewaretoken=${getCSRFToken()}`)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}