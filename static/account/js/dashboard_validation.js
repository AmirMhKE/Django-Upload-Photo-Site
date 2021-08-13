var change_image_input_file = document.querySelector("input[name='img']");
var post_update_form = document.forms["post_update"];
var update_btn = document.querySelector("#update");

post_update_form.oninput = postValidation;
post_update_form.onclick = postValidation;

change_image_input_file.onchange = function() {
    if(this.value !== "") {
        let options = {
            title: "اضافه کردن عکس",
            text: "آیا می خواهید این عکس را اضافه کنید؟",
            invalid_callback: () => {
                change_image_input_file.value = "";
                change_image_input_file.click();
            },
            deny_callback: () => {
                change_image_input_file.value = "";
                post_update_form.click();
            }
        };
        image_validation(this, options);
    }
}

function postValidation() {
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