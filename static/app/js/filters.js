// filter
$(function () {
    let url = new URL(window.location);
    let ordering_name = url.searchParams.get("ordering");

    if(ordering_name !== null) {
        if(ordering_name.split("-").slice(-1)[0] === "created") {
            if(ordering_name.indexOf("-") !== -1) {
                $(".filter:eq(0) button").attr("state", "1");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> جدیدترین");
            } else {
                $(".filter:eq(0) button").attr("state", "2");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> قدیمی ترین");
            }

            $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> جدیدترین");
            $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i> قدیمی ترین");
            $(".filter:eq(1) button").attr("state", "1");
            $(".filter:eq(1) button").html($(".filter:eq(1) .dropdown-item[state='1']").html());
        }

        if(ordering_name.split("-").slice(-1)[0] === "hits") {
            if(ordering_name.indexOf("-") !== -1) {
                $(".filter:eq(0) button").attr("state", "1");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> پر بازدیدترین");
            } else {
                $(".filter:eq(0) button").attr("state", "2");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> کم بازدیدترین");
            }

            $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> پر بازدیدترین");
            $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i> کم بازدیدترین");
            $(".filter:eq(1) button").attr("state", "2"); 
            $(".filter:eq(1) button").html($(".filter:eq(1) .dropdown-item[state='2']").html());
        }

        if(ordering_name.split("-").slice(-1)[0] === "likes") {
            if(ordering_name.indexOf("-") !== -1) {
                $(".filter:eq(0) button").attr("state", "1");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> محبوب ترین");
            } else {
                $(".filter:eq(0) button").attr("state", "2");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> نامحبوب ترین");
            }

            $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> محبوب ترین");
            $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i> نامحبوب ترین");
            $(".filter:eq(1) button").attr("state", "3");
            $(".filter:eq(1) button").html($(".filter:eq(1) .dropdown-item[state='3']").html());
        }

        if(ordering_name.split("-").slice(-1)[0] === "downloads") {
            if(ordering_name.indexOf("-") !== -1) {
                $(".filter:eq(0) button").attr("state", "1");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> پردانلود ترین");
            } else {
                $(".filter:eq(0) button").attr("state", "2");
                $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> کم دانلود ترین");
            }

            $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> پردانلود ترین");
            $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i> کم دانلود ترین");
            $(".filter:eq(1) button").attr("state", "4");
            $(".filter:eq(1) button").html($(".filter:eq(1) .dropdown-item[state='4']").html());
        }
    }
});

$(".filter:eq(0) .dropdown-item").click(function () { 
    $(".filter:eq(0) button").attr("state", $(this).attr("state"));
    $(".filter:eq(0) button").html($(this).html());
});

$(".filter:eq(1) .dropdown-item").click(function () { 
    let state = $(this).attr("state");
    $(".filter:eq(1) button").attr("state", state);
    $(".filter:eq(1) button").html($(this).html());

    if(state === "1") {
        $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> جدیدترین");
        $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i>  قدیمی ترین ");

        if($(".filter:eq(0) button").attr("state") === "1") {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> جدیدترین");
        } else {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-down ml-1'></i> قدیمی ترین");
        }
    }

    if(state === "2") {
        $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> پر بازدیدترین");
        $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i> کم بازدیدترین ");

        if($(".filter:eq(0) button").attr("state") === "1") {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> پر بازدیدترین");
        } else {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-down ml-1'></i> کم بازدیدترین");
        }
    }

    if(state === "3") {
        $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> محبوب ترین");
        $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i> نامحبوب ترین ");

        if($(".filter:eq(0) button").attr("state") === "1") {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> محبوب ترین");
        } else {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-down ml-1'></i> نامحبوب ترین");
        }
    }

    if(state === "4") {
        $(".filter:eq(0) .dropdown-item:eq(0)").html("<i class='fa fa-arrow-up ml-1'></i> پردانلود ترین");
        $(".filter:eq(0) .dropdown-item:eq(1)").html("<i class='fa fa-arrow-down ml-1'></i> کم دانلود ترین ");

        if($(".filter:eq(0) button").attr("state") === "1") {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-up ml-1'></i> پردانلود ترین");
        } else {
            $(".filter:eq(0) button").html("<i class='fa fa-arrow-down ml-1'></i> کم دانلود ترین");
        }
    }
});

$("#filter-btn").click(function () { 
    filter();
});

function filter() {
    let url = new URL(window.location);
    let order_state = $(".filter:eq(0) button").attr("state");
    let filter_state = $(".filter:eq(1) button").attr("state");
    let filter_name = "";

    switch (filter_state) {
        case "1":
            filter_name = "-created"
            break;
        case "2":
            filter_name = "-hits";
            break;
        case "3":
            filter_name = "-likes";
            break;
        case "4":
            filter_name = "-downloads";
            break;
    }

    if(order_state === "2") {
        filter_name = filter_name.replace("-", "");
    }

    
    let scrollNum;
    try {
        scrollNum = $("#scroll-target").offset().top - 100;
    } catch (TypeError) {
        scrollNum = 0;
    }

    localStorage.setItem("scroll", scrollNum);

    url.searchParams.set("ordering", filter_name);
    window.location = url;
}