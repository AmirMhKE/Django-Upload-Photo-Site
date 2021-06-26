// Get session event
window.onload = function () {
    json_object = JSON.parse($("#event").val())
    switch (json_object["type"]) {
        case "recaptcha_not_ok":
            Swal.fire({
                "title": "تایید من ربات نیستم",
                "text": "لطفا تیک من ربات نیستم را بزنید!",
                "icon": "warning",
                "confirmButtonText": "باشه"
            })
            break;
        case "user_not_exist":
            Swal.fire({
                "title": "اطلاعات اشتباه",
                "text": "نام کاربری یا ایمیلی که وارد کردید وجود ندارد!",
                "icon": "error",
                "confirmButtonText": "باشه"
            }).then(() => {
                $(".login-link").click();
            });
            break;
        case "user_wrong_password":
            Swal.fire({
                "title": "اطلاعات اشتباه",
                "text": "رمز عبوری که وارد کردید اشتباه است!",
                "icon": "error",
                "confirmButtonText": "باشه"
            }).then(() => {
                $(".login-link").click();
            });
            break;
        case "user_not_active":
            Swal.fire({
                "title": "غیر فعال بودن اکانت",
                "text": "این اکانت غیر فعال است و شما نمی توانید وارد آن شوید!",
                "icon": "warning",
                "confirmButtonText": "باشه"
            })
            break;
        case "user_login_success":
            Swal.fire({
                "title": "عملیات موفق",
                "text": "شما با موفقیت وارد اکانتتان شدید!",
                "icon": "success",
                "confirmButtonText": "باشه"
            });
            break;
        case "email_sended":
            Swal.fire({
                "title": "راهنما",
                "text": "لینک فعال سازی اکانت شما به ایمیلتان ارسال شد!",
                "icon": "info",
                "confirmButtonText": "باشه"
            });
            break; 
        case "signup_error":
            content = setContent(json_object["content"]);

            Swal.fire({
                "title": "اطلاعات اشتباه",
                "html": content,
                "icon": "error",
                "confirmButtonText": "باشه"
            }).then(() => {
                $(".sign-up-link").click();
            });
            break;
        case "activation_success":
            Swal.fire({
                "title": "عملیات موفق",
                "text": "شما با موفقیت اکانت خود را فعال کردید!\nحالا می توانید وارد شوید!",
                "icon": "success",
                "confirmButtonText": "باشه"
            }).then(() => {
                $(".login-link").click();
            });
            break;
        case "activation_invalid":
            Swal.fire({
                "title": "لینک منقضی",
                "html": "لینک فعالسازی منقضی شده است!",
                "icon": "error",
                "confirmButtonText": "باشه"
            })
            break;
        case "email_not_found":
            Swal.fire({
                "title": "پیدا نشدن ایمیل",
                "html": "کاربری با این ایمیل وجود ندارد!",
                "icon": "error",
                "confirmButtonText": "باشه"
            }).then(() => {
                $(".password-reset-link").click();
            });
            break;
        case "password_reset_email_sended":
            Swal.fire({
                "title": "عملیات موفق",
                "text": "لینک بازیابی رمز عبور اکانت شما به ایمیلتان ارسال شد!",
                "icon": "success",
                "confirmButtonText": "باشه"
            });
            break;
        case "password_reset_done":
            Swal.fire({
                "title": "عملیات موفق",
                "text": "رمز عبور جدید شما ثبت شد!",
                "icon": "success",
                "confirmButtonText": "باشه"
            }).then(() => {
                $(".login-link").click();
            });
            break;
        case "password_reset_error":
            content = setContent(json_object["content"]);

            Swal.fire({
                "title": "رمز عبور نادرست",
                "html": content,
                "icon": "error",
                "confirmButtonText": "باشه"
            })
            break;
        case "password_reset_invalid_token":
            Swal.fire({
                "title": "لینک منقضی",
                "text": "لینک بازیابی رمز عبور منقضی شده است!",
                "icon": "error",
                "confirmButtonText": "باشه"
            }).then(() => {
                window.location.pathname = "";
            });
            break;
    }
    $("#event").remove();
}

function setContent(array) {
    let ul = document.createElement("ul");
    ul.classList = "list-unstyled p-0";

    for(let item of array) {
        let li = document.createElement("li");
        li.innerHTML = `<p>${item}</p>`;
        ul.appendChild(li);
    }

    return ul;
}