// Pagina di modifica del profilo dell'utente

function modifica_username(){
	var input = document.getElementById('username').innerHTML;
	var patt = new RegExp("/^[A-Za-z0-9_-]{5,18}$/");
	var sol = patt.test(input);
	if(!sol){
		document.getElementById('username_err').innerHTML = "Username non valido. Caratteri ammessi lettere, numeri, trattino e underscore";
	}
}

function modifica_username_typing(){
	var input = document.getElementById('username').innerHTML;
	var n = input.length;
	if(n > 18){
		document.getElementById('username_err').innerHTML = "Username al massimo di 18 caratteri";
	}
	if(n < 5){
		document.getElementById('username_err').innerHTML = "Username minimo di 5 caratteri"; // ????????????????????????????
	}
}

function modifica_mail(){
	var input = document.getElementById('mail').innerHTML;
	var patt = new RegExp("/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/");
	var sol = patt.test(input);
	if(!sol){
		document.getElementById('mail_err').innerHTML = "Indirizzo email non valido";
	}
}

function modifica_nome(){
	var input = document.getElementById('nome').innerHTML;
	var patt = new RegExp("/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/");
	var sol = patt.test(input);
	if(!sol){
		document.getElementById('nome_err').innerHTML = "Nome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
	}
}


function modifica_cognome(){
	var input = document.getElementById('cognome').innerHTML;
	var patt = new RegExp("/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-]+$/");
	var sol = patt.test(input);
	if(!sol){
		document.getElementById('cognome_err').innerHTML = "Cognome utente non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
	}
}

function modifica_anno(){
	var input = document.getElementById('anno').innerHTML;
	var patt = new RegExp("/^[1-2][0-9][0-9][0-9]$/");
	var sol = patt.test(input);
	if(!sol){
		document.getElementById('anno_err').innerHTML = "Anno di nascita non valida, inserire l anno in formato 'aaaa'";
	}else{
		var d = new Date();
		var n = d.getFullYear(); 
		if(n-(input+18)){
			document.getElementById('anno_err').innerHTML = "Possono registrarsi solo utenti maggiorenni";	
		}
	}
}

function modifica_password(){
	var input = document.getElementById('password').innerHTML;
	var patt = new RegExp("/^[A-Za-z0-9_\.-]{8,16}$/");
	var sol = patt.test(input);
	if(!sol){
		document.getElementById('password_err').innerHTML = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto";
	}
}
