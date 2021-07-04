$(function () {
    var event = JSON.parse($("input[name='event']").val());

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