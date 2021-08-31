// User change validation
var user_update_form = document.forms["user_update_form"];
var add_profile_fi = document.querySelector("input[name='profile_image']");
var clear_profile_ch = document.querySelector("input[name='profile_image-clear']");
var add_profile_btn = document.querySelector("#add_profile-btn");
var delete_profile_btn = document.querySelector("#delete_profile-btn");
var submit_btn = document.querySelector("#change_profile-btn");

// ? if user want update profile image default informations sends
function updateProfile() {
    user_update_form["username"].value = user_update_form["username"].getAttribute("initial");
    user_update_form["first_name"].value = user_update_form["first_name"].getAttribute("initial");
    user_update_form["last_name"].value = user_update_form["last_name"].getAttribute("initial");
    user_update_form["about_me"].value = user_update_form["about_me"].getAttribute("initial");
    user_update_form.submit();
}

// Add profile
if(add_profile_fi !== null) {
    add_profile_btn.onclick = function () {
        add_profile_fi.click();
    }

    add_profile_fi.onchange = function () {
        let options = {
            title: "اضافه کردن عکس پروفایل",
            text: "آیا می خواهید این عکس را به پروفایل خود اضافه کنید؟",
            valid_callback: updateProfile,
            invalid_callback: () => {
                add_profile_fi.value = "";
                add_profile_fi.click();
            },
            deny_callback: () => {
                add_profile_fi.value = "";
            }
        };
        image_validation(this, options);
    }
}

// Clear profile
if(clear_profile_ch !== null) {
    delete_profile_btn.onclick = function () {
        Swal.fire({
            icon: "error",
            title: "حذف عکس پروفایل",
            text: "آیا می خواهید عکس پروفایل خود را حذف کنید؟",
            showDenyButton: true,
            confirmButtonText: `حذف عکس`,
            denyButtonText: `لغو کردن`
        }).then((result) => {
            if(result.isConfirmed) {
                if(!clear_profile_ch.checked) {
                    clear_profile_ch.click();
                }
                updateProfile();
            }
        });
    };
}

// User update form validation
user_update_form.oninput = userUpdateFormValidation;

var about_me_ta = document.querySelector("#id_about_me");
var about_me_len = document.querySelector("#about_me_len");
about_me_ta.innerHTML = about_me_ta.value.trim()
about_me_ta.oninput = function () {
    about_me_len.innerHTML = en_nums_to_fa_nums(this.value.trim().length);
}

function userUpdateFormValidation() {
    let pattern = /^[آ-ی ء چ]+$/;
    let text_pattern = /^[آ-ی ء چ ، .]+$/;

    let username_condition = (
        this["username"].value.trim().toLowerCase() === this["username"].getAttribute("initial").toLowerCase()
    )
    let username_is_changed = (
        this["username"].value.trim() !== this["username"].getAttribute("initial")
    )
    
    let first_name_condition = (
        (this["first_name"].value.trim().length >= 3 && this["first_name"].value.trim().length <= 20 &&
        pattern.test(this["first_name"].value.trim()))
    )
    let first_name_is_changed = (
        this["first_name"].value.trim() !== this["first_name"].getAttribute("initial")
    )
    let first_name_is_empty = this["first_name"].value.trim() === "";

    let last_name_condition = (
        (this["last_name"].value.trim().length >= 3 && this["last_name"].value.trim().length <= 30 &&
        pattern.test(this["last_name"].value.trim()))
    )
    let last_name_is_changed = (
        this["last_name"].value.trim() !== this["last_name"].getAttribute("initial")
    )
    let last_name_is_empty = this["last_name"].value.trim() === "";

    let about_me_condition = (
        text_pattern.test(this["about_me"].value.trim()) || this["about_me"].value.trim() === ""
    )
    let about_me_is_changed = (
        this["about_me"].value.trim() !== this["about_me"].getAttribute("initial")
    )

    let superuser_is_changed, active_is_changed;
    try {
        superuser_is_changed = this["is_superuser"].checked !== JSON.parse(this["is_superuser"].getAttribute("initial"))
        active_is_changed = this["is_active"].checked !== JSON.parse(this["is_active"].getAttribute("initial"))
    } catch {
        superuser_is_changed = false;
        active_is_changed = false;
    }

    if(((username_condition && first_name_is_empty && last_name_is_empty && about_me_condition) || 
    (username_condition && about_me_condition && (!first_name_is_empty && first_name_condition) && 
    (!last_name_is_empty && last_name_condition))) && 
    (username_is_changed || first_name_is_changed || last_name_is_changed || 
    about_me_is_changed || superuser_is_changed || active_is_changed)) {
        submit_btn.removeAttribute("disabled");
    } else {
        submit_btn.setAttribute("disabled", "");
    }
}

// Remove account
const delete_account_form = document.querySelector("#delete_account-form");
const delete_account_btn = document.querySelector(".delete_account-btn");
const username = document.querySelector("input[name='username']").getAttribute("initial");
const email = document.querySelector("input#email-lbl").getAttribute("initial");

delete_account_btn.onclick = function (e) {
    e.preventDefault();
    Swal.fire({
        icon: "warning",
        title: "حذف حساب کاربری",
        html: `
        <p>
            <span>آیا می خواهید اکانت کاربری خود را حذف کنید؟ </span>
            <b>(با این کار تمام عکس های آپلود شده توسط شما پاک می شود!)</b>
        </p>
        `,
        showDenyButton: true,
        confirmButtonText: `لغو کردن`,
        denyButtonText: `حذف اکانت کاربری`
    }).then((result) => {
        if(result.isDenied) {
            Swal.fire({
                icon: "error",
                title: "تایید حذف اکانت",
                html: `برای حذف اکانت خود عبارت <b>${username + "/" + email}</b> را وارد نمایید.`,
                input: "text",
                inputAttributes: {
                    spellcheck: "false"
                },
                showCancelButton: true,
                confirmButtonText: "حذف اکانت",
                cancelButtonText: "لغو",
                customClass: {
                    confirmButton: "delete_account-btn"
                },
                inputValidator: (value) => {
                    if(value != (username + "/" + email)) {
                        return "عبارت شما با عبارت مورد نظر مطابقت ندارد!";
                    } else {
                        delete_account_form.submit();
                    }
                }
            });
        }
    });
}