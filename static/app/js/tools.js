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
    let img_formats = JSON.parse(document.querySelector("#img_formats").innerHTML);
    let img_width = Number(document.querySelector("#img_width").value);
    let img_height = Number(document.querySelector("#img_height").value);

    let formats = [];

    for(format of img_formats) {
        formats.push(`image/${format.toLowerCase()}`);
    }

    if(instance.value !== "") {
        var preview_image = instance.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(preview_image);

        if(!formats.includes(preview_image.type)) {
            Swal.fire({
                icon: "error",
                title: "فایل با فرمت غیر مجاز",
                text: `شما باید فایلی آپلود کنید که نوع آن ${img_formats.join(" یا ")} باشد.`,
                confirmButtonText: "باشه"
            }).then(() => {
                if(options.invalid_callback) {
                    options.invalid_callback();
                }
            });
        } else {
            reader.onloadend = async () => {
                let image = new Image();
                image.src = reader.result;
    
                image.onload = function () {
                    let width = this.width;
                    let height = this.height;
    
                    if(width < img_width || height < img_height) {
                        Swal.fire({
                            icon: "error",
                            title: "فایل با اندازه غیر مجاز",
                            text: `شما باید فایلی آپلود کنید که حداقل طول آن ${en_nums_to_fa_nums(img_width)} و عرض آن ${en_nums_to_fa_nums(img_height)} باشد.`,
                            confirmButtonText: "باشه"
                        }).then(() => {
                            if(options.invalid_callback) {
                                options.invalid_callback();
                            }
                        });
                    } else {
                        Swal.fire({
                            imageUrl: reader.result,
                            imageWidth: options.width,
                            imageHeight: options.height,
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
}

function remove_url_params(path) {
    let url = new URL(`${window.location.protocol}//${window.location.host}${path}`);
    url.searchParams.forEach((value, key) => {
        url.searchParams.delete(key);
    });
    return url;
}