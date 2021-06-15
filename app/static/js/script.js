// other
document.oncontextmenu = (e) => e.preventDefault();

// animation
new WOW().init();

$(function () {
    $(".loading").css("display", "none");
    $("body").css("overflow-y", "visible");
});

// date
date = new Date();
formatedDate = moment(date, "YYYY/MM/DD").locale("fa").format("YYYY/MM/DD");
showDate(formatedDate.split("/"));

function showDate(input) {
    var months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"];
    $(".date p").append(`${+input[2]} ${months[+input[1] - 1]} ${input[0]}`);
}

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

$(".login-link").click(function () {
    $(".outer-login + .overlay").fadeIn(500);
    $(".outer-login").css("display", "flex");
    $(".login").removeClass("animate__slideOutUp");
    $(".login").addClass("animate__slideInDown");
    $(".login").css("display", "block");
    $("body").css("overflow-y", "hidden");
});

$(".sign-up-link").click(function () {
    $(".outer-sign-up + .overlay").fadeIn(500);
    $(".outer-sign-up").css("display", "flex");
    $(".sign-up").removeClass("animate__slideOutUp");
    $(".sign-up").addClass("animate__slideInDown");
    $(".sign-up").css("display", "block");
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

$(".sign-up .close, .outer-sign-up").click(function (e) {
    if (e.target === document.querySelector(".sign-up .close i") ||
     e.target === document.querySelector(".outer-sign-up")) {
        $(".sign-up").removeClass("animate__slideInDown");
        $(".sign-up").addClass("animate__slideOutUp");

        setTimeout(() => {
            $(".outer-sign-up + .overlay").fadeOut(300);
            $(".sign-up").css("display", "none");
            $(".outer-sign-up").css("display", "none");
            $("body").css("overflow-y", "visible");
        }, 300);
    }
});

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
    $(".all-items h2").text("همه‌ی " + $(".target-" + e.target.id.split("-")[2]).text());

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