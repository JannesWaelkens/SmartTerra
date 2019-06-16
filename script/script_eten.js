const IP = window.location.hostname + ':5000';
const socket = io.connect(IP);

let svg,
	aanpassen,
	beschrijving;

window.onload = function() {
	listenToAanpassen(aanpassen);
};

const listenToKeuze = function(dag) {
	let keuze;
	let html = '';
	keuze = document.querySelector('#dag' + dag);
	keuze.addEventListener('change', function() {
		gekozen = keuze.value;

		socket.emit('aanpassen', { dag, gekozen });
		beschrijving[dag].innerHTML = html;
	});
};

const pasAan = function(dag) {
	let html = '';
	html = `<select id='dag${dag}'>
	<option value="0">Selecteer Eten</option>
	<option value="Groente">Groente</option>
	<option value="Korrel">Korrel</option>
	<option value="Krekel">Krekel</option>
	<option value="Sprinkhaan">Sprinkhaan</option>
	<option value="Meelworm">Meelworm</option>
  </select>`;
	beschrijving[dag].innerHTML = html;
	listenToKeuze(dag);
};

const listenToAanpassen = function(dag) {
	dag[0].addEventListener('click', function() {
		pasAan(0);
	});
	dag[1].addEventListener('click', function() {
		pasAan(1);
	});
	dag[2].addEventListener('click', function() {
		pasAan(2);
	});
	dag[3].addEventListener('click', function() {
		pasAan(3);
	});
	dag[4].addEventListener('click', function() {
		pasAan(4);
	});
	dag[5].addEventListener('click', function() {
		pasAan(5);
	});
	dag[6].addEventListener('click', function() {
		pasAan(6);
	});
};

const VerwerkVoedingschema = function(data) {
	beschrijving[0].innerHTML = data[0].beschrijving;
	beschrijving[1].innerHTML = data[1].beschrijving;
	beschrijving[2].innerHTML = data[2].beschrijving;
	beschrijving[3].innerHTML = data[3].beschrijving;
	beschrijving[4].innerHTML = data[4].beschrijving;
	beschrijving[5].innerHTML = data[5].beschrijving;
	beschrijving[6].innerHTML = data[6].beschrijving;
};

socket.on('tabelaanpassen', function(data) {
	VerwerkVoedingschema(data);
});

const init = function() {
	// Get some DOM, we created empty earlier.
	aanpassen = document.querySelectorAll('#aanpassen');
	beschrijving = document.querySelectorAll('#beschrijving');
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
