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
                text: event["content"],
                confirmButtonText: "باشه"
            });
            break;
        case "permission_denied":
            Swal.fire({
                title: "خطای دسترسی",
                icon: "error",
                text: "شما دسترسی ندارید!",
                confirmButtonText: "باشه"
            });
            break;
        case "post_deleted":
            Swal.fire({
                title: "عملیات موفق",
                icon: "success",
                html: en_nums_to_fa_nums(event["content"]),
                confirmButtonText: "باشه"
            });
            break;
        case "user_post_created":
            Swal.fire({
                title: "عملیات موفق",
                icon: "success",
                html: en_nums_to_fa_nums(event["content"]),
                confirmButtonText: "باشه"
            });
            break;
        case "user_post_updated":
            Swal.fire({
                title: "عملیات موفق",
                icon: "success",
                html: en_nums_to_fa_nums(event["content"]),
                confirmButtonText: "باشه"
            });
            break;
        case "max_upload_image_error":
            Swal.fire({
                title: "خطای آپلود",
                icon: "error",
                html: en_nums_to_fa_nums(event["content"]),
                confirmButtonText: "باشه"
            });
            break;
        case "similar_image_error":
            Swal.fire({
                title: "شباهت عکس",
                icon: "error",
                text: "عکسی مشابه عکس شما در سایت وجود دارد.",
                confirmButtonText: "باشه"
            });
            break;
    }
    
    $("#event").remove();
})
