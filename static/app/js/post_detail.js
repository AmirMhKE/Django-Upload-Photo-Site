// Image viewer
const img_size = document.getElementById("img_size").value;
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
    title: [0, (image) => `${image.alt} (${img_size})`],
    slideOnTouch: false
});

// Download image
const download_btn = document.getElementById("download");
var download_count = document.getElementById("download_count");
var is_downloaded = JSON.parse(document.getElementById("is_downloaded").value);
var download_number = Number(document.getElementById("download_number").value);

download_btn.onclick = downloadImage;

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