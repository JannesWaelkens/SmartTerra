const IP = window.location.hostname + ':5000';
const socket = io.connect(IP);

let knopuv,
	knopwarmte,
	svg,
	temperatuurLinks,
	temperatuurSteen,
	temperatuurRechts,
	deurcontact,
	statusVorige,
	deurtabel,
	beloningen;



window.onload = function() {
	setInterval(getDataSensoren, 5000);
};

const Verwerksensordata = function(json) {
	let links = json.Links;
	let graden = '°C';
	let rechts = json.Rechts;
	let steen = json.Steen;
	let statusdeur = json.statusdeur;

	if (statusdeur === 0) {
		statusVorige = 0;
	} else {
		if (statusdeur != statusVorige) {
			socket.emit('deurtoestand');

			statusVorige = 1;
		}
	}

	for (element of deurcontact) {
		if (statusdeur === 0) {
			element.innerHTML = `<img src="img/baseline-lock-24px.svg" alt="slot gesloten">`;
		} else {
			element.innerHTML = `<img src="img/baseline-lock_open-24px.svg" alt="slot open">`;
		}
	}

	for (element of temperatuurLinks) {
		element.innerText = links + graden;
	}

	for (element of temperatuurSteen) {
		element.innerText = steen + graden;
	}

	for (element of temperatuurRechts) {
		element.innerText = rechts + graden;
	}
};

const getDataSensoren = function() {
	fetch(`http://${window.location.hostname}:5000/api/v1/sensordata`)
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				// if our own api sends an error!
				handleError(response.json());
			}
		})
		.then(data => {
			Verwerksensordata(data);
		})
		.catch(error => {
			console.error(error);
		});
};

socket.on('connect', function() {
	console.log('connected');
	socket.emit('connected', { message: "I'm connected!" });
});

socket.on('lighttempoff', function() {
	for (lightbulb of knopwarmte) {
		console.log('tempuit');
		html = `<p>WARMTE</p>
		<img src="img/heatlamp_off.svg" alt="warmtelamp uit">`;
		lightbulb.innerHTML = html;
	}
});

socket.on('lighttempon', function() {
	for (lightbulb of knopwarmte) {
		html = `<p>WARMTE</p>
		<img src="img/heatlamp_on.svg" alt="warmtelamp aan">`;
		lightbulb.innerHTML = html;
	}
});
socket.on('lightuvoff', function() {
	for (lightbulb of knopuv) {
		html = `<p>UV</p>
		<img src="img/uvlamp_off.svg" alt="uvlamp uit">`;
		lightbulb.innerHTML = html;
	}
});
socket.on('lightuvon', function() {
	for (lightbulb of knopuv) {
		html = `<p>UV</p>
		<img src="img/uvlamp_on.svg" alt="uvlamp aan">`;
		lightbulb.innerHTML = html;
	}
});

socket.on('voederluik', function(data) {
	let html = '';
	console.log('luik');
	console.log(data);
	for (gegevens of data) {
		aantal = gegevens.beloningen;
		html = ` Je hebt vandaag al <br> <b>${aantal}</b> beloningen gegeven`;
	}
	beloningen.innerHTML = html;
});

const listenToButton = function(element) {
	element.addEventListener('click', function() {
		console.log('connected');
		let data = element.innerText;

		socket.emit('clickonbutton', { drukknop: data });
		socket.emit('sensordata');
	});
};

//#region ***********  INIT / DOMContentLoaded ***********

const init = function() {
	// Get some DOM, we created empty earlier.
	knopuv = document.querySelectorAll('.o-body__content--lampen-uv');
	knopwarmte = document.querySelectorAll('.o-body__content--lampen-warmte');
	temperatuurLinks = document.querySelectorAll('#temperatuur_links');
	temperatuurSteen = document.querySelectorAll('#temperatuur_steen');
	temperatuurRechts = document.querySelectorAll('#temperatuur_rechts');
	deurcontact = document.querySelectorAll('#deurcontact');
	aanpassen = document.querySelectorAll('#aanpassen');
	beschrijving = document.querySelectorAll('#beschrijving');
	deurtabel = document.querySelector('.o-tabel-deur');
	knopbeloning = document.querySelectorAll(
		'.o-body__content--beloning-button'
	);
	beloningen = document.querySelector('#beloningen');

	for (element of knopwarmte) {
		listenToButton(element);
	}
	for (element of knopuv) {
		listenToButton(element);
	}
	for (element of knopbeloning) {
		listenToButton(element);
	}
};

document.addEventListener('DOMContentLoaded', init);
