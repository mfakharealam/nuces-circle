// using jQuery from django docs
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
$(document).ready(function(){
    var $myForm = $('.creating_post_ajax');
    $myForm.submit(function(event){
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = 'post/new/' || $myForm.attr('data-url') || window.location.href; // or set your own url
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError
        })
    });

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        //refreshStream();
        refresh_the_stream();
        $myForm[0].reset(); // reset form data
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

var delete_post_ftn = function(){
    var $myForm = $('.delete_post_ajax');
    $myForm.submit(function(event){
        event.preventDefault();
        var $formData = $(this).serialize();
        // var post_id = $(this).find('#current_post_id').val(); for template looping, helps to find each elem uniquely
        var link = $(this);
        $.ajax({
            method: "POST",
            url:  link.attr('action'),
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError
        })
    });

    function handleFormSuccess(data, textStatus, jqXHR){
        hideModal();
        refreshStream();
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
};

var update_post_ftn = function(){
    var $myForm = $('.update_post_ajax');
    $myForm.submit(function(event){
        event.preventDefault();
        var $formData = $(this).serialize();
        var link = $(this);
        $.ajax({
            method: "POST",
            url:   link.attr('action'),
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError
        })
    });

    function handleFormSuccess(data, textStatus, jqXHR){
        hideModal();
        refreshStream();
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
};


var refreshStream = function(){
    $.ajax({
        method: 'GET',
        url: 'next_posts/0/',
        data: {},
        success: function(data){
            $('#mainFeed').replaceWith($('#mainFeed',data));
        },
        error: function(error){
            console.log(error);
            console.log("error");
        }
    });
};

function hideModal(){
  $(".modal").removeClass("in");
  $(".modal-backdrop").remove();
  $('body').removeClass('modal-open');
  $('body').css('padding-right', '');
  $(".modal").hide();
}
// var total_seconds = 0.5; // refresh every 5 seconds
//
// setInterval(function(){
//     refreshStream();
// },total_seconds * 1000);


function validateText(id){
    var txt = document.getElementById(id);
    if(txt.value == ''){
        return error('search string is empty');
    }
    return true;
}

function error(msg){
    swal("Input Error!", msg, "error");
    return false;
}

// var load_posts_scroll = function(){
    // $.ajax({
    //         method: 'GET',
    //         url: 'load_posts/',
    //         data: {
    //             csrfmiddlewaretoken: "{{ csrf_token }}",
    //         },
    //         dataType: "json",
    //         success: function(data){
    //             //alert(data.all_posts[0].fields.content);
    //             // $('#mainFeed').append($('#post_list_ajax',data.all_posts));// LoadFeed wala
    //             LoadFeed(data);
    //         },
    //         error: function(error){
    //             alert(data);
    //             alert(error);
    //             console.log(error);
    //             console.log("error");
    //         }
    //     });
    // };
    var count = 0, posts;
    function refresh_the_stream(){
        count = 0;
        document.getElementById("mainFeed").innerHTML = '';
        nextPostsAjax();
    }
    var nextPostsAjax=function () {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    posts = JSON.parse(xhr.responseText);
                    addPost();
                }
            }
        };
        // sending ajax request //
        xhr.open("GET", "next_posts/" + count, true);
        xhr.send();
    };
    nextPostsAjax();
    function addPost() {
        count = count + posts.length;
        var curr_post_username, user_fname, content, postId, post_date, user_pic;
        for (i = 0; i < posts.length; i++) {
            user_fname = posts[i]["full_name"];
            content = posts[i]["content"];
            postId = posts[i]["post_id"];
            curr_post_username = posts[i]["user_name"];
            post_date = posts[i]["post_date"];
            user_pic = posts[i]["user_pic"];
            var html = "<div class=\"card gedf-card shadow-lg mb-5 bg-white\">\n" +
                "                    <div class=\"card-header\">\n" +
                "                        <div class=\"d-flex justify-content-between align-items-center\">\n" +
                "                            <div class=\"d-flex justify-content-between align-items-center\">\n" +
                "                                <div class=\"mr-2\">\n" +
//                "                                    <img class=\"rounded-circle post-img\" src=\" " + user_pic + " \" alt=\"\">\n" +
                "                                </div>\n" +
                "                                <div class=\"ml-2\">\n" +
                "                                    <div class=\"h5 m-0\">@" + curr_post_username + "</div>\n" +
                "                                    <div class=\"h7 text-muted\">" + user_fname + "</div>\n" +
                "                                </div>\n" +
                "                            </div>\n" +
                "                                <div class=\"dropdown\">\n" +
                "                                    <button class=\"btn btn-link dropdown-toggle\" type=\"button\" id=\"gedf-drop1\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
                "                                        <i class=\"fas fa-ellipsis-h\"></i>\n" +
                "                                    </button>\n" +
                "                                        <div class=\"dropdown-menu dropdown-menu-right\" aria-labelledby=\"gedf-drop1\">\n" +
                "                                            <div class=\"h6 dropdown-header\">Configuration</div>\n" +
                "                                                <a class=\"dropdown-item\" href=\"\" data-toggle=\"modal\" data-target=\"#createPostModal{{"+postId+"}}\">\n" +
                "                                                    Edit\n" +
                "                                                </a>\n" +
                "                                                <a class=\"dropdown-item\" href=\"\" data-toggle=\"modal\" data-target=\"#deletePostModal{{"+postId+"}}\">\n" +
                "                                                    Delete\n" +
                "                                                </a>\n" +
                "                                        </div>\n" +
                "                                </div>\n" +
                "\n" +
                "                           </div>\n" +
                "\n" +
                "                    </div>\n" +
                "                    <div class=\"card-body\">\n" +
                "                        <div class=\"text-muted h7 mb-2\"> <i class=\"fas fa-clock-o\"></i>"+post_date+"</div>\n" +
                "                         <p class=\"card-text\">\n" +
                "                            "+content+"\n" +
                "                         </p>\n" +
                "                    </div>\n" +
                "                    <!--</a>-->\n" +
                "                    <div class=\"card-footer\">\n" +
                "                        <a href=\"#\" class=\"card-link\"><i class=\"fas fa-gittip\"></i> Like</a>\n" +
                "                        <a href=\"#\" class=\"card-link\"><i class=\"fas fa-comment\"></i> Comment</a>\n" +
                "                        <a href=\"#\" class=\"card-link\"><i class=\"fas fa-mail-forward\"></i> Share</a>\n" +
                "                    </div>\n" +
                "                </div>";
            document.getElementById("mainFeed").innerHTML += html;
        }
    }
    //
    // var LoadFeed = function (data)
    // {
    //     var html = "<div class=\"card gedf-card mt-4\">\n" +
    //         "                <div class=\"card-header\">\n" +
    //         "                    <div class=\"d-flex justify-content-between align-items-center\">\n" +
    //         "                        <div class=\"d-flex justify-content-between align-items-center\">\n" +
    //         "                            <div class=\"mr-2\">\n" +
    //         "                                <img class=\"rounded-circle\" width=\"45\" src=\"https://picsum.photos/50/50\" alt=\"\">\n" +
    //         "                            </div>\n" +
    //         "                            <div class=\"ml-2\">\n" +
    //         "                                <div class=\"h5 m-0\">@"+ username + "</div>\n" +
    //         "                                <div class=\"h7 text-muted\">"+ name +"</div>\n" +
    //         "                            </div>\n" +
    //         "                        </div>\n" +
    //         "                        <div>\n" +
    //         "                            <div class=\"dropdown\">\n" +
    //         "                                <button class=\"btn btn-link dropdown-toggle\" type=\"button\" id=\"gedf-drop1\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n" +
    //         "                                    <i class=\"fas fa-ellipsis-h\"></i>\n" +
    //         "                                </button>\n" +
    //         "                                <div class=\"dropdown-menu dropdown-menu-right\" aria-labelledby=\"gedf-drop1\">\n" +
    //         "                                    <div class=\"h6 dropdown-header\">Configuration</div>\n" +
    //         "                                    <a class=\"dropdown-item\" href=\"#\">Save</a>\n" +
    //         "                                    <a class=\"dropdown-item\" href=\"#\">Hide</a>\n" +
    //         "                                    <a class=\"dropdown-item\" href=\"#\">Report</a>\n" +
    //         "                                </div>\n" +
    //         "                            </div>\n" +
    //         "                        </div>\n" +
    //         "                    </div>\n" +
    //         "\n" +
    //         "                </div>\n" +
    //         "                <div class=\"card-body\">\n" +
    //         "                    <div class=\"text-muted h7 mb-2\"> <i class=\"fas fa-clock-o\"></i>10 min ago</div>\n" +
    //         "                    <a class=\"card-link\" href=\"#\">\n" +
    //         "                        <h5 class=\"card-title\">"+ postTitle +"</h5>\n" +
    //         "                    </a>\n" +
    //         "\n" +
    //         "                    <p class=\"card-text\">\n" + postContent + "</p>\n" +
    //         "                </div>\n" +
    //         "                <div class=\"card-footer\">\n" +
    //         "                    <a href=\"#\" class=\"card-link\"><i class=\"fas fa-gittip\"></i> Like</a>\n" +
    //         "                    <a href=\"#\" class=\"card-link\"><i class=\"fas fa-comment\"></i> Comment</a>\n" +
    //         "                    <a href=\"#\" class=\"card-link\"><i class=\"fas fa-mail-forward\"></i> Share</a>\n" +
    //         "                </div>\n" +
    //         "            </div>";
    //     document.getElementById("mainFeed").innerHTML+=html;
    // };

    window.onscroll = function () {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            nextPostsAjax();
        }
    };