var lines = document.querySelectorAll(".line");
set_random_color_lines(lines, ["blue", "red"]);

function set_random_color_lines(lines, colors_) {    
    for(line of lines) {
        let colors = colors_.slice(); // copy of list
        let line_number = colors.length;
        let col_number = 12;
        line.innerHTML = "";
        
        for(let i = 1; i <= line_number; i++) {
            let random_color = colors.splice(Math.floor(Math.random() * colors.length), 1)[0];
            let random_col = i != line_number ? Math.floor(Math.random() * (col_number - 1)) + 1 : col_number;
            let innerLine = `<div class='${random_color} p-0 col-${String(random_col)}'></div>`;

            col_number = col_number - random_col;
            line.innerHTML += innerLine;
            line.classList.add("p-0");
        }
    }
}