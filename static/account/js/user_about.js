var public_profile = $(".public-profile");
var body_profile_height = $(".about .body").outerHeight();
var public_profile_width = public_profile.outerWidth();
$(".about").outerHeight(`${body_profile_height + public_profile_width + 4}px`);
public_profile.outerHeight(public_profile_width);

$(window).resize(() => {
    body_profile_height = $(".about .body").outerHeight();
    public_profile_width = public_profile.outerWidth();
    $(".about").outerHeight(`${body_profile_height + public_profile_width + 4}px`);
    public_profile.outerHeight(public_profile_width);
});

// Show all Images
var show_all_btn = document.querySelector(".showAllImages");
show_all_btn.onclick = function () {
    window.location.pathname = this.getAttribute("target");
}