const nos = document.querySelector('img[alt="Noise"]');
const img = document.querySelector('img[alt="Generated Image"]');
const button = document.querySelector('button');
button.addEventListener("click", async function() {
    img.src = "assets/loading.gif";
    const data = await fetch("/generate").then((res) => res.json());
    nos.src=`data:image/png;base64,${data.noise}`;
    img.src=`data:image/png;base64,${data.image_data}`;
});
