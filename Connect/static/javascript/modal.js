document.getElementById('button').addEventListener("click", function() {
	document.querySelector('.modal1').style.display = "flex";
});

document.querySelector('.close').addEventListener("click", function() {
	document.querySelector('.modal1').style.display = "none";
});