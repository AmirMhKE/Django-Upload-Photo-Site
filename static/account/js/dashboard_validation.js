var image_input_file = document.querySelector("input[name='img']");
var post_create_form = document.forms["post_create"];
var post_update_form = document.forms["post_update"];
var create_btn = document.querySelector("#create");
var update_btn = document.querySelector("#update");


try {
    post_create_form.oninput = postCreateValidation;
    post_create_form.onclick = postCreateValidation;
} catch (TypeError) {}

try {
    post_update_form.oninput = postUpdateValidation;
    post_update_form.onclick = postUpdateValidation;
} catch (TypeError) {}

image_input_file.onchange = function() {
    if(this.value !== "") {
        let options = {
            title: "اضافه کردن عکس",
            text: "آیا می خواهید این عکس را اضافه کنید؟",
            width: 300,
            height: "auto",
            valid_callback: () => {
                try {
                    post_create_form.click();
                    post_update_form.click();
                } catch (TypeError) {}
            },
            invalid_callback: () => {
                image_input_file.value = "";
                image_input_file.click();
            },
            deny_callback: () => {
                image_input_file.value = "";
                try {
                    post_create_form.click();
                    post_update_form.click();
                } catch (TypeError) {}
            }
        };
        image_validation(this, options);
    }
}

function postCreateValidation() {
    let title_condition = (
        this["title"].value.trim() !== ""
    )

    let category_condition = (
        this["category"].value !== ""
    )

    let image_file_condition = (
        this["img"].value !== ""
    )

    if((title_condition && category_condition && image_file_condition)) {
        create_btn.removeAttribute("disabled");
    } else {
        create_btn.setAttribute("disabled", "");
    }
}

function postUpdateValidation() {
    let title_condition = (
        this["title"].value.trim() !== ""
    )
    let title_is_changed = (
        this["title"].value.trim() !== this["title"].getAttribute("initial")
    )

    let category_condition = (
        this["category"].value !== ""
    )
    let category_is_changed = (
        this["category"].value !== this["category"].getAttribute("initial")
    )

    let image_file_is_changed = (
        this["img"].value !== ""
    )

    if((title_condition && category_condition) && 
    (title_is_changed || category_is_changed || image_file_is_changed)) {
        update_btn.removeAttribute("disabled");
    } else {
        update_btn.setAttribute("disabled", "");
    }
}