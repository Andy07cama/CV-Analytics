document.addEventListener("DOMContentLoaded", () => {
    const circle = document.querySelector(".progress-ring__circle");
    const label = document.querySelector(".progress-label");

    if (!circle || !label) return;

    const porcentaje = parseFloat(label.textContent);
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;

    circle.style.strokeDasharray = `${circumference}`;
    circle.style.strokeDashoffset = `${circumference}`;

    const offset = circumference - (porcentaje / 100) * circumference;

    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
    }, 300);
});
