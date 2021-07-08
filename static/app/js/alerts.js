$(function () {
    var event = JSON.parse($("#event").val());

    switch (event["type"]) {
        case "login_required":
            Swal.fire({
                "title": "ورود به سیستم",
                "icon": "warning",
                "text": "شما ابتدا باید وارد شوید!",
                "confirmButtonText": "باشه"
            }).then(() => {
                $(".login-link").click();
            });
            break;
    }
})