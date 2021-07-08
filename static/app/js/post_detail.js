// Image viewer
const viewer = new Viewer(document.getElementById('image'), {
    viewed () {
        let image = document.querySelector(".viewer-canvas img");
        let marginLeft = image.style.marginLeft;
        image.style.marginRight = marginLeft;
    },
    show () {
        document.body.style.overflowY = "hidden";
        try {
            document.querySelector(".viewer-next").remove();
            document.querySelector(".viewer-prev").remove();
        } catch (TypeError) {
            // ***
        }
    },
    hidden () {
        document.body.style.overflowY = "visible";
    },
    zoomed () {
        let image = document.querySelector(".viewer-canvas img");
        let marginLeft = image.style.marginLeft;
        image.style.marginRight = marginLeft;
    },
    title: [0, (image) => image.alt],
    slideOnTouch: false
});

// Download image
const download_btn = document.getElementById("download");
var download_count = document.getElementById("download_count");
var is_downloaded = JSON.parse(document.getElementById("is_downloaded").value);
var download_number = Number(document.getElementById("download_number").value);

download_btn.onclick = downloadImage;

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

function downloadImage() {
    if(!is_downloaded) {
        download_count.innerHTML = en_nums_to_fa_nums(download_number + 1);
    }
}

// Like image
const like_btn = document.getElementById("like");
var like_count = document.getElementById("like_count");
var is_auth = JSON.parse(document.getElementById("is_auth").value);

like_btn.onclick = likeImage;

function likeImage(e) {
    if(is_auth) {
        e.preventDefault();
        fetch(like_btn.href)
        .then(response => response.json())
        .then(data => {
            like_count.innerHTML = en_nums_to_fa_nums(data["count"]);
            if(data["action"] === "dislike")
                like_btn.innerHTML = "<span class='ml-1'><i class='fa fa-thumbs-up'></i></span> لایک کردن عکس";
            else if(data["action"] === "like")
                like_btn.innerHTML = "<span class='ml-1'><i class='fa fa-thumbs-down'></i></span> لغو لایک کردن عکس";
        })
        .catch(() => {
            Swal.fire({
                "title": "خطا",
                "icon": "error",
                "text": "درخواست با خطا مواجه شد!",
                "confirmButtonText": "باشه"
            });    
        });
    }
}