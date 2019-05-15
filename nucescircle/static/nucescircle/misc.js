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
        inf_scroll_ajax();
    }
    var inf_scroll_ajax=function () {
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
    inf_scroll_ajax();
    function addPost() {
        count = count + posts.length;
        var curr_post_username, user_fname, content, postId, post_date, user_pic;
        for (var i = 0; i < posts.length; i++) {
            user_fname = posts[i]["full_name"];
            content = posts[i]["content"];
            postId = posts[i]["post_id"];
            curr_post_username = posts[i]["user_name"];
            post_date = posts[i]["post_date"];
            user_pic = posts[i]["user_pic"];
            //var img_id = 'img_id'+i;
            var html = "<div class=\"card gedf-card shadow-lg mb-5 bg-white\">\n" +
                "                    <div class=\"card-header\">\n" +
                "                        <div class=\"d-flex justify-content-between align-items-center\">\n" +
                "                            <div class=\"d-flex justify-content-between align-items-center\">\n" +
                // "                                <div class=\"mr-2\">\n" +
                // "                                    <img class=\"rounded-circle post-img\" src=\"{{ post.post_user.profile.image.url }}\" alt=\"\" id=" + img_id + ">\n" +
                // "                                </div>\n" +
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
            // var set_img = document.getElementById(img_id);
            // set_img.src = user_pic;
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
            inf_scroll_ajax();
        }
    };

    // $.ajax({
    //   url: "find_people/advanced_search/",
    //   type: "get", //send it through get method
    //   data: {
    //     ajaxid: 4,
    //     UserID: UserID,
    //     EmailAddress: EmailAddress
    //   },
    //   success: function(response) {
    //     //Do Something
    //   },
    //   error: function(xhr) {
    //     //Do Something to handle error
    //   }
    // });

    $(document).ready(function(){
    var $myForm = $('.advanced_search_form');
    $myForm.submit(function(event){
        event.preventDefault();
        var $formData = $(this).serialize();
        var $thisURL = 'advanced_search/' || $myForm.attr('data-url') || window.location.href; // or set your own url
        $.ajax({
            method: "GET",
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
        var users = JSON.parse(data["result"]);
        document.getElementById("load_ad_search_results").innerHTML = '';
        for (var i = 0; i < users.length ; i++)
        {
            var f_name, u_id, u_name;
            f_name = users[i]["fields"]["first_name"] + ' ' + users[i]["fields"]["last_name"];
            u_name = users[i]["fields"]["username"];
            u_id = users[i]["pk"];
            var a_id = "a_id" + i;
             var html = '    <div class="search-user-card text-center card border-dark mt-4 ml-4 mr-4 mb-4">\n' +
                    // '            <div class="card-header">\n' +
                    // '                        <img class="rounded-circle mt-4" src="{{ user.profile.image.url }}" height="120" width="120" alt="User Profile Image"/>\n' +
                    // '            </div>\n' +
                    '            <div class="card-body">\n' +
                    '                <h5 class="card-title">' + f_name + '</h5>\n' +
                    '                <a href="{% %}" class="btn btn-outline-dark" id=' + a_id + ' >View Profile</a>\n' +
                    '            </div>\n' +
                    '        </div>\n';
            document.getElementById("load_ad_search_results").innerHTML += html;
            var pro = document.getElementById(a_id);
            pro.href = 'http://127.0.0.1:8000/view_profile/current-user-id=' + u_id + '/';
        }
        $myForm[0].reset(); // reset form data
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});
