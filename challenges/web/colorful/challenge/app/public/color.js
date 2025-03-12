// color.js
function changeBackgroundColor() {
    const colors = ["#FF6347", "#7FFF00", "#1E90FF", "#FFD700", "#ADFF2F", "#FF69B4","#FFFFF"];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.style.backgroundColor = randomColor;
}
changeBackgroundColor();