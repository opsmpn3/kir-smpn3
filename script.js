document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const room = params.get("room");

    if (room) {
        document.getElementById("room-name").textContent = room;

        // Ketika tombol KIR diklik, tampilkan PDF di dalam halaman
        document.getElementById("kir-btn").addEventListener("click", function () {
            const pdfViewer = document.getElementById("pdf-viewer");
            pdfViewer.src = `pdfs/${room.replace(/\s/g, "_")}.pdf`;
            document.getElementById("pdf-container").style.display = "block";
        });
    }

    // Tombol Perawatan (Google Form - link sama untuk semua)
    document.getElementById("maintenance-btn").addEventListener("click", function () {
        window.location.href = "https://forms.google.com/perawatan"; // Ganti dengan link Google Form
    });
});
