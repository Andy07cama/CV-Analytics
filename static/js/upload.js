document.addEventListener("DOMContentLoaded", () => {
    const cvInput = document.getElementById("cv");
    const reqInput = document.getElementById("requisitos");
    const boton = document.getElementById("boton-comparar");
    const progress = document.getElementById("progress");
    const progressText = document.getElementById("progress-text");

    function actualizarNombres() {
        [cvInput, reqInput].forEach(input => {
            const span = input.parentElement.querySelector(".file-name");
            const defaultText = span.dataset.default || "Seleccionar archivos PDF";
            if (input.files.length > 0) {
                span.textContent = input.files[0].name;
            } else {
                span.innerHTML = defaultText + "<br><small>o arrastra y suelta aquí</small>";
            }
        });
    }

    function actualizarEstado() {
        const total = (cvInput.files.length > 0 ? 1 : 0) + (reqInput.files.length > 0 ? 1 : 0);
        progressText.textContent = `${total}/2`;

        const percent = (total / 2) * 100;
        progress.style.setProperty("--progress-percent", percent + "%");

        // Cambiar apariencia del botón
        if (total === 2) {
            boton.disabled = false;
            boton.value = "COMPARAR";
            boton.classList.remove("disabled");
            boton.classList.add("ready");
        } else {
            boton.disabled = true;
            boton.value = "FALTAN ARCHIVOS";
            boton.classList.add("disabled");
            boton.classList.remove("ready");
        }

        // Aplicar borde blanco a drop-areas con archivo cargado
        document.querySelectorAll(".drop-area").forEach(area => {
            const input = document.getElementById(area.dataset.target);
            if (input.files.length > 0) {
                area.classList.add("filled");
            } else {
                area.classList.remove("filled");
            }
        });
    }

    // Inicializar eventos
    document.querySelectorAll(".drop-area").forEach(area => {
        const input = document.getElementById(area.dataset.target);

        area.addEventListener("click", () => input.click());

        area.addEventListener("dragover", e => {
            e.preventDefault();
            area.classList.add("dragover");
        });

        area.addEventListener("dragleave", () => area.classList.remove("dragover"));

        area.addEventListener("drop", e => {
            e.preventDefault();
            area.classList.remove("dragover");
            if (!e.dataTransfer.files.length) return;
            const file = e.dataTransfer.files[0];
            const data = new DataTransfer();
            data.items.add(file);
            input.files = data.files;
            actualizarNombres();
            actualizarEstado();
        });

        input.addEventListener("change", () => {
            actualizarNombres();
            actualizarEstado();
        });
    });

    // Inicializar nombres y estado
    actualizarNombres();
    actualizarEstado();
});
