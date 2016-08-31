// Funzioni di  validazione dei campi dati

function valida_username(){
    var input = document.getElementById('username').innerHTML;
    var patt = new RegExp("/^[A-Za-z0-9_-]{5,18}$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById('username_err').innerHTML = "Username non valido. Caratteri ammessi lettere, numeri, trattino e underscore.";
        return false;
    }
    else{
        if(n==0){
            document.getElementById('username_err').innerHTML = "Username obbligatorio";
            return false;
        }
        else if(n > 18){
            document.getElementById('username_err').innerHTML = "Username al massimo di 18 caratteri";
            return false;
        }
        else if(n < 5){
            document.getElementById('username_err').innerHTML = "Username minimo di 5 caratteri";
            return false;
        }
        else{
            document.getElementById('username_err').innerHTML = '';
            return true;
        }
    }
}


function valida_nome(id, parola){
    var input = document.getElementById(id).innerHTML;
    var patt = new RegExp("/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.-']+$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById(id + '_err').innerHTML = parola + " non valido, inserire solo lettere, di cui, al più la prima lettera può essere mauiscola";
        return false;
    }
    else if(!input.length){
        document.getElementById(id + '_err').innerHTML = "Campo dati " + parola + " obbligatorio";
        return false;
    }
    else{
        document.getElementById(id + '_err').innerHTML = "";
        return true;
    }
}

function valida_anno_nasc(){
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
        }else{
            document.getElementById('anno_err').innerHTML = '';
        }
    }
}


function valida_password(){
    var input = document.getElementById('password').innerHTML;
    var patt = new RegExp("/^[A-Za-z0-9_\.-]{8,16}$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById('password_err').innerHTML = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto.";
        return false;
    }
    else if(input.length>16 || input.length <8){
        document.getElementById('password_err').innerHTML = " La password deve comprendere da 8 a 16 caratteri.";
	return false;
    }
    else{
        document.getElementById('password_err').innerHTML = '';
        return true;
    }
}

// function valida_tappa(num)
// più complicato.....

function valida_ora(id) {
    var input = document.getElementById(id).innerHTML;
    var patt = new RegExp("/^\d\d\:\d\d$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById(id + '_err').innerHTML = "Inserire un orario nel formato hh:mm.";
        return false;
    }else{
        var p = input.split(':');
        var h = p.shift();
        var m = p.shift();
        if(h<0 ||h>=24 || m<0 || m>=60){
            document.getElementById(id + '_err').innerHTML = "Inserire un orario corretto.";
            return false;
        }
        else {
            document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
            return true;
        }
    }
}

function valida_posti(id) {
    var input = document.getElementById(id).innerHTML;
    var patt = new RegExp("/^\d{1,}$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById(id + '_err').innerHTML = "Inserire un numero.";
	return false;
    }
    else {
        document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
	return true;
    }
}

function valida_soldi(id) {
    var input = document.getElementById(id).innerHTML;
    var patt = new RegExp("/^\d{1,}(\.|\,)(\d|\d\d)$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById(id + '_err').innerHTML = "Inserire una cifra con al massimo due cifre decimali.";
        return false;
    }
    else {
        //document.getElementById(id).innerHTML = input.replace(',','.'); //non importa lo fa perl in ogni caso
        document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
        return true;
    }
}

function valida_email(id) {
    var input = document.getElementById(id).innerHTML;
    var patt = new RegExp("/^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById(id + '_err').innerHTML = "Inserire un indirizzo email.";
        return false;
    }
    else {
        document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
        return true;
    }
}

function valida_anno_pat() {
    var input = document.getElementById('annoPatente').innerHTML;
    var patt = new RegExp("/^[1-2][0-9][0-9][0-9]$/");
    var sol = patt.test(input);
    if(!sol){
        document.getElementById('annoPatente_err').innerHTML = "Anno di conseguimento della patente non valido, inserire l\' anno in formato 'aaaa'";
        return false;
    }
    else{
        document.getElementById('annoPatente_err').innerHTML = '';
        return true;
    }
}

function test_data(stringdate){
  try{
    $.datepicker.parseDate( "dd-mm-yy", stringdate ) && return true;
  }
  catch(err){
    return false;
  }
}

function valida_data(id){
  var input = document.getElementById(id).innerHTML;
  var patt = new RegExp("/^[0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]$/");
  var sol = patt.test(input);
  if(!sol || !test_data(input)){
      document.getElementById(id + '_err').innerHTML = "Inserire una data in formato gg-mm-aaaa.";
      return false;
  }
  else {
      document.getElementById(id + '_err').innerHTML = "";
      return true;
  }
}
