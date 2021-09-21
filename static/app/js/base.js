// other
document.oncontextmenu = (e) => e.preventDefault();

$("a").click(function (e) { 
    if($(this).attr("href") === "#")
    e.preventDefault();
});

$(".profile .dropdown-item").click(function (e) { 
    e.preventDefault();

    let href = $(this).attr("href");
    let target = $(this).attr("target");

    if(target === "_blank") {
        window.open(href);
    } else {
        window.location.href = href;
    }
});

// animation
new WOW().init();

$(function () {
    $("[title]").tooltip({"placement": "bottom"});

    $(".loading").css("display", "none");
    $("body").css("overflow-y", "visible");

    // Set scroll
    let getScroll = localStorage.getItem("scroll");
    
    if(getScroll !== null) {
        $(window).scrollTop(getScroll);
    }

    localStorage.removeItem("scroll");
});

// scroll
$(window).scroll(function () {
    if ($(this).scrollTop() >= 300) {
        $("#goTop").removeClass("animate__bounceOut");
        $("#goTop").css("display", "flex");
        $("#goTop").addClass("animate__bounceIn");
    } else {
        $("#goTop").removeClass("animate__bounceIn");
        $("#goTop").addClass("animate__bounceOut");
        setTimeout(() => {
            $("#goTop").css("display", "none");
        }, 200);
    }
});

$("#goTop").click(function () {
    $(window).scrollTop(0);
});

// Scroll when page load ...
$(".page-link_, .publisher").click(function () { 
    let scrollNum = $(window).scrollTop();
    localStorage.setItem("scroll", scrollNum);
});

$(".navbar-link").click(function () {
    let href = this.href;
    let scrollNum = 0;

    try {
        scrollNum = $("#scroll-target").offset().top - 100;
    } catch(TypeError) {
        // ***
    } finally {
        localStorage.setItem("scroll", scrollNum);
        window.location = href;
    }
});

if(window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}