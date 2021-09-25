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
$(".search-box .dropdown-item").click(function () {
    $(".search-box .dropdown button").text($(this).text());
    $(".search-box .dropdown button").attr("state", $(this).attr("state"));
    $(".search-box .box input").remove();
    let copy_inp = $('<input type="text" autocomplete="off" spellcheck="false"/>');

    if($("#wrap-inp").length > 0) {
        $(".search-box .box input").unwrap();
        $("#wrap-inp").remove();
    }

    if($(this).attr("state") === "1") {
        let inp = copy_inp.clone();
        inp.attr("placeholder", "متن جستجوی مورد نظر خود را وارد کنید ...");
        inp.attr("name", "title");
        $(".search-box .box").prepend(inp);
    }

    if($(this).attr("state") === "2") {
        let inp = copy_inp.clone();
        inp.attr("placeholder", "نام کاربری مورد نظر خود را وارد کنید ....");
        inp.attr("name", "publisher");
        $(".search-box .box").prepend(inp);
    }

    if($(this).attr("state") === "3") {
        let inp1 = copy_inp.clone();
        inp1.attr("placeholder", "نام کاربری مورد نظر خود را وارد کنید ...");
        inp1.attr("name", "publisher");
        inp1.addClass("mr-1");
        $(".search-box .box").prepend(inp1);

        let inp2 = copy_inp.clone();
        inp2.attr("placeholder", "متن جستجوی مورد نظر خود را وارد کنید ...");
        inp2.attr("name", "title");
        $(".search-box .box").prepend(inp2);

        $(".search-box .box input").wrapAll("<div id='wrap-inp' class='col m-0 p-0'></div>");
    }
});

$("#_search_").click(function () { 
    search();
});

$(".search-box .box").keyup(function (e) { 
    if(e.keyCode === 13) {
        search();
    }
});

function search() {
    var scrollNum = 0;
    let state = $(".search-box .dropdown button").attr("state");
    let url = new URL(window.location);
    let validate = false;

    url.searchParams.delete("title");
    url.searchParams.delete("publisher");
    url.searchParams.set("search", "");

    if(state === "1") {
        let title_name = $(".search-box .box input[name='title']")
        .val().replace(/\s+/g, ' ').trim();
        url.searchParams.set("title", title_name);

        if(title_name === "") {
            Swal.fire({
                icon: "warning",
                title: "ورودی خالی",
                text: "لطفا ورودی مورد نظر را خالی نگذارید.",
                confirmButtonText: "باشه"
            });
        } else {
            validate = true;
        }
    }

    if(state === "2") {
        let publisher_name = $(".search-box .box input[name='publisher']")
        .val().replace(/\s+/g, ' ').trim();
        url.searchParams.set("publisher", publisher_name);

        if(publisher_name === "") {
            Swal.fire({
                icon: "warning",
                title: "ورودی خالی",
                text: "لطفا ورودی مورد نظر را خالی نگذارید.",
                confirmButtonText: "باشه"
            });
        } else {
            validate = true;
        }
    }

    if(state === "3") {
        let title_name = $(".search-box .box input[name='title']")
        .val().replace(/\s+/g, ' ').trim();
        let publisher_name = $(".search-box .box input[name='publisher']")
        .val().replace(/\s+/g, ' ').trim();
        url.searchParams.set("title", title_name);
        url.searchParams.set("publisher", publisher_name);

        if(title_name === "" || publisher_name === "") {
            Swal.fire({
                icon: "warning",
                title: "ورودی خالی",
                text: "لطفا ورودی های مورد نظر را خالی نگذارید.",
                confirmButtonText: "باشه"
            });
        } else {
            validate = true;
        }
    }

    try {
        scrollNum = $("#scroll-target").offset().top - 100;
    } catch(TypeError) {
        // ***
    } finally {
        if(validate) {
            localStorage.setItem("scroll", scrollNum);
            url = url.toString().replace("search=", "search");
            window.location = url;
        }
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

// other link
if($(window).outerWidth() < 1200) {
    $(".other-link").click(function () {
        if(($(".other-link > ul").attr("data-is-open")) === "false") {
            $(".other-link .fa-angle-down").removeClass("angle-down-animation");
            $(".other-link .fa-angle-down").addClass("angle-up-animation");
            $(".other-link > ul").slideDown(500);
            $(".other-link > ul").attr("data-is-open", "true");   
        } else {
            $(".other-link .fa-angle-down").removeClass("angle-up-animation");
            $(".other-link .fa-angle-down").addClass("angle-down-animation");
            $(".other-link > ul").slideUp(500);
            $(".other-link > ul").attr("data-is-open", "false");   
        }
    });
}

$(window).resize(function () { 
    if($(window).outerWidth() >= 1200) {
        $(".other-link > ul").removeAttr("style");
        $(".other-link > ul").attr("data-is-open", "false");
    }
});

$(".other-link ul").mouseenter(function () { 
    $("body").css("overflow-y", "hidden");
});

$(".other-link ul").mouseleave(function () { 
    $("body").css("overflow-y", "visible");
});