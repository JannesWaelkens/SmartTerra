const IP = window.location.hostname + ':5000';
const socket = io.connect(IP);

let svg,
	deurtabel,
	dagen = {
		Monday: 'Maandag',
		Tuesday: 'Dinsdag',
		Wednesday: 'Woensdag',
		Thursday: 'Donderdag',
		Friday: 'Vrijdag',
		Saturday: 'Zaterdag',
		Sunday: 'Zondag'
	};

window.onload = function() {
	setInterval(getDataSensoren, 100);
};

const verwerkTabelDeur = function(json) {
	data = json.tabel

	let html = '';
	let htmlpart2 = '';
	for (let element of data) {
		dag = element['dayname(tijdstip)'];
		dag = dagen[dag];
		uur = element['extract(hour from tijdstip)'];
		minuut = element['extract(minute from tijdstip)'];
		htmlpart2 += `<tr class="o-tabel--content">
		<td class="o-tabel--deur-dag o-tabel--left-first"> <b>${dag}</b></th>
		<td class="o-tabel--tijdstip o-tabel--right-first">${uur}u${minuut}</td>
	  </tr>`;
	}
	html = `<div class="o-tabel--deur-text">
	Deur geopend (deze week)
  </div>
  <table>

	<tr class="o-tabel--title">

	  <th class="o-tabel--deur-dag">Dag</th>
	  <th class="o-tabel--deur-tijdstip">Tijdstip</th>
	</tr>
</div>`;

	deurtabel.innerHTML = html + htmlpart2;
};

const getDataSensoren = function() {
	fetch(`http://${window.location.hostname}:5000/api/v1/deurc`)
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				// if our own api sends an error!
				handleError(response.json());
			}
		})
		.then(data => {
			verwerkTabelDeur(data);
		})
		.catch(error => {
			console.error(error);
		});
};

const init = function() {
	// Get some DOM, we created empty earlier.
	deurtabel = document.querySelector('.o-tabel-deur');
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
