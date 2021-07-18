$(function () {
    var event = JSON.parse($("#event").val());

    switch (event["type"]) {
        case "login_required":
            Swal.fire({
                title: "ورود به سیستم",
                icon: "warning",
                text: "شما ابتدا باید وارد شوید!",
                confirmButtonText: "باشه"
            }).then(() => {
                $(".login-link").click();
            });
            break;
        case "user_profile_updated":
            Swal.fire({
                title: "ویرایش حساب کاربری",
                icon: "success",
                text: "حساب کاربری شما با موفقیت ویرایش شد.",
                confirmButtonText: "باشه"
            });
            break;
    }
    
    $("#event").remove();
})
