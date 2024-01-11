const img = document.querySelector('img');
const noise_img = document.querySelector('#noise-img');
const button = document.querySelector('button');
button.addEventListener("click", async function() {
    img.src = "/loading.gif";
    noise_img.src = "/loading.gif";
    const data = await fetch("/generate").then((res) => res.json());
    noise_img.src=`data:image/png;base64,${data.noise_data}`
    img.src=`data:image/png;base64,${data.image_data}`
});
