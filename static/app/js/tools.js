function en_nums_to_fa_nums(value) {
    result = "";
    shapes = {"0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴", "5": "۵",
            "6": "۶", "7": "۷", "8": "۸", "9": "۹"}

    for(item of String(value)) {
        if(shapes[item] !== undefined) {
            result += shapes[item]
        } else {
            result += item
        }
    }

    return result;
}

function image_validation(instance, options) {
    if(instance.value !== "") {
        var preview_image = instance.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(preview_image);

        reader.onloadend = async () => {
            let image = new Image();
            image.src = reader.result;

            image.onload = function () {
                let width = this.width;
                let height = this.height;

                if(width < 300 || height < 300) {
                    Swal.fire({
                        icon: "error",
                        title: "فایل با اندازه غیر مجاز",
                        text: "شما باید فایلی آپلود کنید که حداقل طول و عرض آن ۳۰۰ باشد.",
                        confirmButtonText: "باشه"
                    }).then(() => {
                        if(options.invalid_callback) {
                            options.invalid_callback();
                        }
                    });
                } else if(!["image/jpeg", "image/png"].includes(preview_image.type)) {
                    Swal.fire({
                        icon: "error",
                        title: "فایل با فرمت غیر مجاز",
                        text: "شما باید فایلی آپلود کنید که نوع آن JPEG یا PNG باشد.",
                        confirmButtonText: "باشه"
                    }).then(() => {
                        if(options.invalid_callback) {
                            options.invalid_callback();
                        }
                    });
                } else {
                    Swal.fire({
                        imageUrl: reader.result,
                        imageWidth: 300,
                        imageHeight: 300,
                        title: options.title,
                        text: options.text,
                        showDenyButton: true,
                        confirmButtonText: `اضافه کردن عکس`,
                        denyButtonText: `لغو کردن`
                    }).then((result) => {
                        if(result.isConfirmed) {
                            if(options.valid_callback) {
                                options.valid_callback();
                            }
                        } else {
                            if(options.deny_callback) {
                                options.deny_callback();
                            }
                        }
                    });
                }
            }                
        }
    }
}

function remove_url_params(path) {
    let url = new URL(`${window.location.protocol}//${window.location.host}${path}`);
    url.searchParams.forEach((value, key) => {
        url.searchParams.delete(key);
    });
    return url;
}