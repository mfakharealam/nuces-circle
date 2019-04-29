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
        refreshStream();
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
        url: '/',
        data: {},
        success: function(data){
            $('#post_list_ajax').replaceWith($('#post_list_ajax',data));
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

