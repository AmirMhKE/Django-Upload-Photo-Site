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