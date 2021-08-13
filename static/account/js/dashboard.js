
$(function () {
    if($(".top-bar .active").length > 0) {
        $(".tubelight").css("display", "block");
        set_new_active_item();
    }
})

$(window).resize(function () { 
    if($(".top-bar .active").length > 0) {
        set_new_active_item();
    }
});

// Show tooltip on active topbar item
if($(".top-bar .active").length > 0) {
    $(".tubelight").mouseenter(function () { 
        $(".top-bar .active span").tooltip("show");
    });
    
    $(".tubelight").mouseleave(function () { 
        $(".top-bar .active span").tooltip("hide");
    });
}

// Set new active topbar item
$(".top-bar ul li span").click(function () {   
    $(".tubelight").css("display", "block");

    if($(".top-bar .active").length > 0) {
        $(".top-bar .active").removeClass("active");
    }

    $(this).parent().addClass("active");
    set_new_active_item();

    setTimeout(() => {
        if($(this).parent().attr("target")) {
            window.location.pathname = $(this).parent().attr("target");
        }
    }, 500);
});

function set_new_active_item() {
    let tubeLightLeft = $(".top-bar .active").position().left + $(".top-bar .active").outerWidth() + 5;
    $(".tubelight").css("left", `${tubeLightLeft}px`);
}

// delete post
$(".delete span").click(function (e) {
    e.preventDefault();
    let title = $(this).parent().prevAll()[10].innerHTML;
    
    Swal.fire({
        title: "حذف عکس",
        icon: "error",
        html: `<p>آیا مطمئین هستید که عکسی را با عنوان <b>${title}</b> را حذف کنید؟</p>`,
        showDenyButton: true,
        confirmButtonText: "حذف عکس",
        denyButtonText: "لغو کردن"
    }).then((result) => {
        if(result.isConfirmed) {
            $(`form.delete-${$(this).parent().attr("id")}`).submit();
        }
    });
});