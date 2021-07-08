// other
document.oncontextmenu = (e) => e.preventDefault();

$("a").click(function (e) { 
    if($(this).attr("href") === "#")
    e.preventDefault();
});

$(".dropdown-item").click(function (e) { 
    e.preventDefault();

    let href = $(this).attr("href");
    if(href !== "#")
    window.location.href = href;
});

// animation
new WOW().init();

$(function () {
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
    let href = this.href; 
    let scrollNum = $(window).scrollTop();
    localStorage.setItem("scroll", scrollNum);
    window.location = href;
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

// navbar
$(".search-btn").click(function () {
    $(".search-box").removeClass("animate__fadeOutRight");
    $(".search-box").addClass("animate__fadeInLeft");
    $(".search-box").css("display", "flex");
    $(".my-navbar").removeClass("sticky-top");
    $("body").css("overflow-y", "hidden");
});

$(".search-box div:eq(0) span").click(function () {
    $(".search-box").removeClass("animate__fadeInLeft");
    $(".search-box").addClass("animate__fadeOutRight");

    setTimeout(() => {
        $(".search-box").css("display", "none");
        $(".my-navbar").addClass("sticky-top");
        $("body").css("overflow-y", "visible");
    }, 1000);
});

$(".menu-bar").click(function () {
    $(".my-navbar ul").animate({ right: 0 }, 500);
    $(".overlay-nav").fadeIn(500);
    $("body").css("overflow-y", "hidden");
});

$(".my-navbar ul li:eq(0) span, .overlay-nav").click(function () {
    $(".my-navbar ul").animate({ right: "-75%" }, 500);
    $(".overlay-nav").fadeOut(500);
    $("body").css("overflow-y", "visible");
});

$(".contact-link").click(function () {
    $(".outer-contact-us + .overlay").fadeIn(500);
    $(".outer-contact-us").css("display", "flex");
    $(".contact-us").removeClass("animate__slideOutUp");
    $(".contact-us").addClass("animate__slideInDown");
    $(".contact-us").css("display", "block");
    $("body").css("overflow-y", "hidden");
});

$(".login-link").click(function (e) {
    e.preventDefault();
    $(".outer-login + .overlay").fadeIn(500);
    $(".outer-login").css("display", "flex");
    $(".login").removeClass("animate__slideOutUp");
    $(".login").addClass("animate__slideInDown");
    $(".login").css("display", "block");
    $("body").css("overflow-y", "hidden");
});

$(".contact-us .close, .outer-contact-us").click(function (e) {
    if (e.target === document.querySelector(".contact-us .close i") || e.target === document.querySelector(".outer-contact-us")) {
        $(".contact-us").removeClass("animate__slideInDown");
        $(".contact-us").addClass("animate__slideOutUp");

        setTimeout(() => {
            $(".outer-contact-us + .overlay").fadeOut(300);
            $(".contact-us").css("display", "none");
            $(".outer-contact-us").css("display", "none");
            $("body").css("overflow-y", "visible");
        }, 300);
    }
});

$(".login .close, .outer-login").click(function (e) {
    if (e.target === document.querySelector(".login .close i") ||
     e.target === document.querySelector(".outer-login")) {
        $(".login").removeClass("animate__slideInDown");
        $(".login").addClass("animate__slideOutUp");

        setTimeout(() => {
            $(".outer-login + .overlay").fadeOut(300);
            $(".login").css("display", "none");
            $(".outer-login").css("display", "none");
            $("body").css("overflow-y", "visible");
        }, 300);
    }
});

// search
$("#_search_").click(function () { 
    if($("#_search_input_").val().replace(/\s+/g, ' ').trim() === "") {
        Swal.fire({
            "title": "ورودی خالی",
            "text": "لطفا چیزی وارد کنید!",
            "icon": "warning",
            "confirmButtonText": "باشه"
        });
    } else {
        search();
    }
});

$("#_search_input_").keyup(function (e) { 
    if(e.keyCode === 13) {
        if($("#_search_input_").val().replace(/\s+/g, ' ').trim() === "") {
            Swal.fire({
                "title": "ورودی خالی",
                "text": "لطفا چیزی وارد کنید!",
                "icon": "warning",
                "confirmButtonText": "باشه"
            });
        } else {
            search();
        }
    }
});

function search() {
    let search_name = $("#_search_input_").val().replace(/\s+/g, ' ').trim();
    let url = "/search/" + search_name + "/";
    var scrollNum = 0;

    try {
        scrollNum = $("#scroll-target").offset().top - 100;
    } catch(TypeError) {
        // ***
    } finally {
        localStorage.setItem("scroll", scrollNum);
        window.location.pathname = url;
    }
}

// carousel
$(".owl-carousel").owlCarousel({
    rtl: true,
    loop: true,
    margin: 10,
    nav: true,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1,
        },
        576: {
            items: 2,
        },
        992: {
            items: 3,
        },
    },
});

$(".owl-next span").html("<i class='fa fa-angle-left'></i>");
$(".owl-prev span").html("<i class='fa fa-angle-right'></i>");

// show all images
$(".all-items div:last-child button, .all-items + .overlay").click(function () {
    $(".all-items").removeClass("animate__zoomInDown");
    $(".all-items").fadeOut(500);
    $(".all-items").scrollTop(0);
    $(".all-items + .overlay").fadeOut(500);
    $("body").css("overflow-y", "visible");
});

$("button[id*='showAllImages-btn']").click(function (e) {
    $(".all-items").addClass("animate__zoomInDown");
    showAllImages();
});

function showAllImages() {
    $(".all-items").fadeIn(500);
    $(".all-items + .overlay").fadeIn(500);
    $("body").css("overflow-y", "hidden");
}

// contact-us
$(".contact-us form button").click(function (e) {
    e.preventDefault();

    let username = $(".contact-us form input[name='username']").val();
    let message = $(".contact-us form textarea[name='message']").val();
    let usernameReg = /^[ آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ\s]+$/;

    if (username.replaceAll(" ", "") === "" || !usernameReg.test(username) || message.replaceAll(" ", "") === "") {
        if(username.replaceAll(" ", "") === "" || !usernameReg.test(username)) $(".contact-us .usernameValidate").fadeIn(0);

        if(message.replaceAll(" ", "") === "") $(".contact-us .messageValidate").fadeIn(0);

    } else {
        alert("پیام مورد نظر شما ارسال شد!(همینطوری الکی)");
        $(".outer-contact-us").click();
        $(".contact-us .usernameValidate").fadeOut(0);
        $(".contact-us .messageValidate").fadeOut(0);
    }
});

// other link
$(".angle-down").click(function () {
    if(($(".other-link > ul").attr("data-is-open")) === "false") {
        $(".other-link .angle-down i").removeClass("angle-down-animation");
        $(".other-link .angle-down i").addClass("angle-up-animation");
        $(".other-link > ul").slideDown(500);
        $(".other-link > ul").attr("data-is-open", "true");   
    } else {
        $(".other-link .angle-down i").removeClass("angle-up-animation");
        $(".other-link .angle-down i").addClass("angle-down-animation");
        $(".other-link > ul").slideUp(500);
        $(".other-link > ul").attr("data-is-open", "false");   
    }
});

$(".other-link ul").mouseenter(function () { 
    $("body").css("overflow-y", "hidden");
});

$(".other-link ul").mouseleave(function () { 
    $("body").css("overflow-y", "visible");
});