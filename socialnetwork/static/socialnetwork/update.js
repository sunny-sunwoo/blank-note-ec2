// var prev_posts;
// var this_user;

// Sends a new request to update the post list
function getList() {
    $.ajax({
        url: "/socialnetwork/get-list-json",
        dataType : "json",
        success: function(response) {
            updatePost(response);
            updateComment(response);
            // updateFollowingPost(response);
        }
    });
}



function updatePost(response) {
    // 1. check if there are new posts
    // 2. prepend new ones and draw comment box for each
    var posts = JSON.parse(response['posts']);
    var this_user = response['this_user'];
    var len = posts.length;
    var authors = response['author_username'];
    // var date = moment().format('lll');  
    // console.log(date);
    for(i=pk; i<=len; i++){
        
    // Adds each new post item to the list
        $(posts[i]).each(function() {
        // if this_user == this.fields.author : <a>my_profile
        // else : <a>other_profile
        if(this.fields.author == this_user){
            $("#post-list").prepend(
                "<li id='post-item' class='post__item mb-5 row'>" 
                + "<div class=\"d-block col-12 col-md-10 col-lg-6 push-md-1 push-lg-3 py-4\">"
                + "<a href=\"/socialnetwork/my_profile\">"
                + "<h4 class=\"post__title mb-4\">"
                + sanitize(this.fields.text) 
                + "</h4>"
                + "<p class=\"post__text\">"+ authors[this.pk-1] + "</p>"
                + "<p class=\"post__date\">" + sanitize(this.fields.published_date) + "</p>"
                +"</a>" +
                "<div class=\"py-2 my-3 prev-comments\">" + "<ul class=\"comment-block\" id = \"" +this.pk + "\">" + "</ul>" + "</div>"
                + "<div class = 'comment-create'>" + 
                "<input id=\"comment-" +this.pk + "\" class=\"new-comment my-2\" name=\"comment\" type=\"text\" placeholder=\"Any Comment?\" size=\"40\">" +
                "<button onclick=\"addComment( "+ this.pk + ")\" class=\"btn__logout mx-2\">Add here</button>" +
                "<span id=\"error\" class=\"error\"></span>" + "</div>" 
                + "</li>");
        } else {
            $("#post-list").prepend(
                "<li id=\"post-item\" class=\"post__item mb-5 row\">" 
                + "<div class=\"d-block col-12 col-md-10 col-lg-6 push-md-1 push-lg-3 py-4\">"
                + "<a href=\"/socialnetwork/other_profile?last=" + this.fields.author + "\">"
                + "<h4 class=\"post__title mb-4\">"
                + sanitize(this.fields.text) 
                + "</h4>"
                + "<p class=\"post__text\">"+ authors[this.pk-1] + "</p>"
                + "<p class=\"post__date\">" + sanitize(this.fields.published_date) + "</p>"
                +"</a> "
                + "<div class=\"py-2 my-3 prev-comments\">" + "<ul class=\"comment-block\" id = \"" +this.pk + "\" >" + "</ul>" + "</div>" 
                + "<div class = 'comment-create'>" + 
                "<input id=\"comment-" +this.pk + "\" class=\"new-comment my-2\" name=\"comment\" type=\"text\" placeholder=\"Any Comment?\" size=\"40\">" +
                "<button onclick=\"addComment( "+ this.pk + ")\" class=\"btn__logout mx-2\">Add here</button>" +
                "<span id=\"error\" class=\"error\"></span>" + "</div>" + "</div>" 
                + "</li>");
        }
            });
    }
    // console.log(new_posts)
  
        pk=len;

}

function updateComment(response){
    var comments = JSON.parse(response['comments']);
    var this_user = response['this_user'];
    var commenters = response['commenter_username'];
    var len_com = comments.length;
    
        // $("li .comm-list").remove();
    for(i=pk_com; i<=len_com; i++){

        $(comments[i]).each(function() {
        if(this.fields.commenter == this_user){
            $("#"+this.fields.post).append(
                "<li class=\"comm-list\" id = \"" +this.pk + "\">" +
              "<a href=\"/socialnetwork/my_profile\">"
            + "<p class=\"comment__text\">"  
            + "<em>"+ commenters[this.pk-1] +"</em>" + " -- "
            + sanitize(this.fields.text) + " --- "
            + sanitize(this.fields.published_date)
            + "</p></a></li>" 
            );
        } else{
            $("#"+this.fields.post).append(
                "<li class=\"comm-list\" id = \"" +this.pk + "\">" +
              "<a href=\"/socialnetwork/other_profile?last=" + this.fields.commenter + "\">"
            + "<p class=\"comment__text\">"  
            + "<em>"+ commenters[this.pk-1]  +"</em>" + " -- "
            + sanitize(this.fields.text) + " --- "
            + sanitize(this.fields.published_date)
            + "</p></a></li>" 
            );
        }
    });


    }
        
    pk_com = len_com;
    
}

// function updateFollowingPost(response){

//        // 1. check if there are new posts
//     // 2. prepend new ones and draw comment box for each
//     var f_posts = JSON.parse(response['following_posts']);
//     var this_user = response['this_user'];
//     var len_f = f_posts.length;
//     var authors = response['following_authors'];
//     // var date = moment().format('lll');  
//     // console.log(date);
//     for(i=pk_f; i<=len_f; i++){
        
//     // Adds each new post item to the list
//         $(f_posts[i]).each(function() {
//         // if this_user == this.fields.author : <a>my_profile
//         // else : <a>other_profile
//         if(this.fields.author == this_user){
//             $("#following-post-list").prepend(
//                 "<li id='following-post-item' class='post__item mb-5 row'>" 
//                 + "<div class=\"d-block col-12 col-md-10 col-lg-6 push-md-1 push-lg-3 py-4\">"
//                 + "<a href=\"/socialnetwork/my_profile\">"
//                 + "<h4 class=\"post__title mb-4\">"
//                 + sanitize(this.fields.text) 
//                 + "</h4>"
//                 + "<p class=\"post__text\">"+ authors[this.pk-1] + "</p>"
//                 + "<p class=\"post__date\">" + sanitize(this.fields.published_date) + "</p>"
//                 +"</a>" +
//                 "<div class=\"py-2 my-3 prev-comments\">" + "<ul class=\"comment-block\" id = \"" +this.pk + "\">" + "</ul>" + "</div>"
//                 + "<div class = 'comment-create'>" + 
//                 "<input id=\"comment-" +this.pk + "\" class=\"new-comment my-2\" name=\"comment\" type=\"text\" placeholder=\"Any Comment?\" size=\"40\">" +
//                 "<button onclick=\"addComment( "+ this.pk + ")\" class=\"btn__logout mx-2\">Add here</button>" +
//                 "<span id=\"error\" class=\"error\"></span>" + "</div>" 
//                 + "</li>");
//         } else {
//             $("#following-post-list").prepend(
//                 "<li id=\"following-post-item\" class=\"post__item mb-5 row\">" 
//                 + "<div class=\"d-block col-12 col-md-10 col-lg-6 push-md-1 push-lg-3 py-4\">"
//                 + "<a href=\"/socialnetwork/other_profile?last=" + this.fields.author + "\">"
//                 + "<h4 class=\"post__title mb-4\">"
//                 + sanitize(this.fields.text) 
//                 + "</h4>"
//                 + "<p class=\"post__text\">"+ authors[this.pk-1] + "</p>"
//                 + "<p class=\"post__date\">" + sanitize(this.fields.published_date) + "</p>"
//                 +"</a> "
//                 + "<div class=\"py-2 my-3 prev-comments\">" + "<ul class=\"comment-block\" id = \"" +this.pk + "\" >" + "</ul>" + "</div>" 
//                 + "<div class = 'comment-create'>" + 
//                 "<input id=\"comment-" +this.pk + "\" class=\"new-comment my-2\" name=\"comment\" type=\"text\" placeholder=\"Any Comment?\" size=\"40\">" +
//                 "<button onclick=\"addComment( "+ this.pk + ")\" class=\"btn__logout mx-2\">Add here</button>" +
//                 "<span id=\"error\" class=\"error\"></span>" + "</div>" + "</div>" 
//                 + "</li>");
//         }
//             });
//     }
//     // console.log(new_posts)
  
//         pk_f=len_f;

// }


function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}


function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function addPost() {
    var itemTextElement = $("#post");
    var itemTextValue   = itemTextElement.val();

    // Clear input box and old error message (if any)
    itemTextElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/create",
        type: "POST",
        data: { post: itemTextValue,
                csrfmiddlewaretoken: getCSRFToken()
                },
        dataType : "json",
        success: function(response) {
            if ('error' in response){
                displayError(response.error);
            } else {
                updatePost(response);
            }
        }
    });
}



function addComment(this_post) {
    var commentTextElement = $("#comment-" + this_post);
    var commentTextValue   = commentTextElement.val();

    // Clear input box and old error message (if any)
    commentTextElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment/"+this_post,
        type: "POST",
        data: { comment: commentTextValue,
                this_post: this_post,
                csrfmiddlewaretoken: getCSRFToken()
                },
        dataType : "json",
        success: function(response) {
            if ('error' in response){
                displayError(response.error);
            } else {
                updateComment(response);
            }
        }
    });
}


// function addFollowingPost() {

//     $.ajax({
//         url: "/socialnetwork/follow_stream",
//         type: "GET",
//         dataType : "json",
//         success: function(response) {
//             if ('error' in response){
//                 displayError(response.error);
//             } else {
//                 updateFollowingPost(response);
//             }
//         }
//     });
// }


// The index.html does not load the list, so we call getList()
// as soon as page is finished loading



window.onload = function(){
    getList();
    pk=0;
    pk_com=0;
    // pk_f=0;
}

// window.onload = getList;

// causes list to be re-fetched every 5 seconds
window.setInterval(getList, 5000);

