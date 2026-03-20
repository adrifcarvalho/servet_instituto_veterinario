function ajustarAlturaVideo() {
	const texto = document.querySelector('.hero-text');
	const video = document.querySelector('.hero-video video');

	if (!texto || !video) return;

	if (window.innerWidth >= 992) {
		// DESKTOP
		const altura = texto.offsetHeight;

		video.style.height = altura + "px";
		video.style.width = "auto";
		video.style.maxWidth = "none";
	} else {
		// MOBILE (RESET REAL)
		video.style.height = "";
		video.style.width = "";
		video.style.maxWidth = "";
		video.style.objectFit = "";
	}
}

window.addEventListener('load', () => {
	setTimeout(ajustarAlturaVideo, 100);
});

window.addEventListener('resize', ajustarAlturaVideo);