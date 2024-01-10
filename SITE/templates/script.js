const img = document.querySelector('img');
const button = document.querySelector('button');
button.addEventListener("click", async function() {
    const image_data = await fetch("/generate").then((res) => res.text());
    img.src=`data:image/png;base64,${image_data}`
});