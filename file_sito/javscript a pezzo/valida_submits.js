////////////////////////////////////////////////
// Validazione delle submits
////////////////////////////////////////////////

function valida_submit_modifica_profilo(){
    var v1 = valida_nome('nome','Nome');
    var v2 = valida_nome('cognome','Cognome');
    var v3 = valida_email('email');
    var v4 = valida_password('vecchiaPassword');
    var v5 = valida_password('nuovaPassword');
    var v6 = valida_anno_nasc();
    var v7 = verifica_blocco_modifica_profilo();
    // debugger;
    if(!v7){
        document.getElementById('submitbutton_err').innerHTML = "La sezione dei dati per guidatori va compilata in ogni sua parte o in nessuna (per i non guidatori)."
        return false;
    }
    else{
        if(v1 && v2 && v3 && v4 && v5 && v6 && v7){
            return true;
        }
        else{
            document.getElementById('submitbutton_err').innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
            return false;
        }
    }
}



// controlla che i campi dati elencati tra gli argomenti siano compilati. per onsubmit senza dettagli ---- generico
function valida_tutto_compilato(){
    var numberOfMiss = 0;
    var i;
    for (i = 0; i < arguments.length; i++) {
        var itemID = arguments[i];
        var input = document.getElementById(itemID).value;
        if(!input.length){
            document.getElementById(itemID + '_err').innerHTML = "Compilare il campo.";
            numberOfMiss = numberOfMiss + 1;
        }
        else{
            document.getElementById(itemID + '_err').innerHTML = "";
        }
    }
    if(numberOfMiss==0){
        return true;
    }
    else{
        document.getElementById('submitbutton_err').innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
        return false;
    }
}

function valida_submit_home(){
    var res1 = valida_data('data');
    var res2 = valida_nome('arrivo','Luogo di arrivo');
    var res3 = valida_nome('partenza','Luogo di partenza');
    if(!res1 || !res2 || !res3){
        document.getElementById('submitbutton_err').innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
        return false;
    }
    else{
        return true;
    }
}

function valida_submit_iscrizione(){
    var r1 = valida_nome('nome','Nome');
    var r2 = valida_nome('cognome','Cognome');
    var r3 = valida_username();
    var r4 = valida_email('email');
    var r5 = valida_password('password');
    var r6 = valida_password('conferma');
    var r7 = valida_anno_nasc();
    if(!r1 || !r2 || !r3 || !r4  || !r5 || !r6 || !r7){
        document.getElementById('submitbutton_err').innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
        return false;
    }
    else{
        return true;
    }
}



function valida_submit_offerta(){
    var r1 = valida_nome('partenza','Partenza');
    var r2 = valida_nome('arrivo','Arrivo');
    var r3 = valida_tappa(1);
    var r4 = valida_tappa(2);
    var r5 = valida_tappa(3);
    var r6 = valida_data('dataA');
    var r7 = valida_data('dataP');
    var r8 = valida_ora('oraA');
    var r9 = valida_ora('oraP');
    var r10 = valida_soldi('prezzo');
    var r11 = valida_posti('posti');
    if(!r1 || !r2 || !r3 || !r4  || !r5 || !r6 || !r7 || !r8 || !r9 || !r10 || !r11){
        //debugger;
        document.getElementById('submitbutton_err').innerHTML = "&Egrave; necessario compilare tutti i campi dati a parte la descrizione del viaggio che è opzionale.";
        return false;
    }
    else{
        if(verifica_ordine_tappe()){
            document.getElementById('submitbutton_err').innerHTML = "";
            document.getElementById('tappa1_err').innerHTML = "";
            document.getElementById('tappa2_err').innerHTML = "";
            document.getElementById('tappa3_err').innerHTML = "";
            if(verifica_ordine_orari()){
                return true;
            }
            else{
                document.getElementById('submitbutton_err').innerHTML = "La partenza deve avvenire prima dell'arrivo.";
                document.getElementById('oraA_err').innerHTML = "La partenza deve avvenire prima dell'arrivo.";
                document.getElementById('oraP_err').innerHTML = "La partenza deve avvenire prima dell'arrivo.";
                document.getElementById('dataA_err').innerHTML = "La partenza deve avvenire prima dell'arrivo.";
                document.getElementById('dataP_err').innerHTML = "La partenza deve avvenire prima dell'arrivo.";
                return false;
            }
        }
        else{
            return false;
        }
    }
}



function verifica_ordine_tappe(){
    var t1 = document.getElementById('tappa1').value.length;
    var t2 = document.getElementById('tappa2').value.length;
    var t3 = document.getElementById('tappa3').value.length;
    if(t1 && t2 && t3){
        return true;
    }
    else if (!t1 && !t2 && !t3) {
        return true;
    }
    else if(!t1 && ( t2 || t3)){
        document.getElementById('submitbutton_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        document.getElementById('tappa1_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        document.getElementById('tappa2_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        document.getElementById('tappa3_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        return false;
    }
    else if((!t1 || !t2)&& t3){
        document.getElementById('submitbutton_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        document.getElementById('tappa1_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        document.getElementById('tappa2_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        document.getElementById('tappa3_err').innerHTML = "Le tappe possono essere inserite solo nell'ordine corretto.";
        return false;
    }
    else{
        return true;
    }
}

/*
  try{
  $.datepicker.parseDate( "dd-mm-yy", stringdate );
  return true;
  }
  catch(err){
  return false;
  }
*/

// new Date(year, month, day, hours, minutes, seconds, milliseconds)

function verifica_ordine_orari(){
    var ha = document.getElementById('oraA').value.split(':');
    var hp = document.getElementById('oraP').value.split(':');
    var da = document.getElementById('dataA').value.split('-');
    var dp = document.getElementById('dataP').value.split('-');
    var part = new Date(dp[2],dp[1],dp[0],hp[1],hp[0],0,0);
    var arr = new Date(da[2],da[1],da[0],ha[1],ha[0],0,0);
    var diff = arr.getTime() - part.getTime();
    return diff>0;
}

function verifica_radio3(id){
    var v1 = document.getElementById(id + 0).checked;
    var v2 = document.getElementById(id + 1).checked;
    var v3 = document.getElementById(id + 2).checked;
    return v1 || v2 || v3;
}

function verifica_radio2(id){
    var v1 = document.getElementById(id + 0).checked;
    var v2 = document.getElementById(id + 1).checked;
    return v1 || v2;
}

function verifica_blocco_modifica_profilo(){
    var v1 = valida_anno_pat();
    var v2 = valida_auto();
    var v3 = verifica_radio3('musica');
    var v4 = verifica_radio3('chiacchiere');
    var v5 = verifica_radio2('animali');
    var v6 = verifica_radio2('fumatori');
    //debugger;
    return v1 && v2 && v3 && v4 && v5 && v6;
}


function valida_tempo_passaggio(){
    var dataA = document.getElementById("dataA").value;
    var dataP = document.getElementById("dataP").value;
    var oraA = document.getElementById("oraA").value;
    var oraP = document.getElementById("oraP").value;
    var hA = oraA.split(":");
    var hP = oraP.split(":");
    var dA = dataA.split("-");
    var dP = dataP.split("-");
    var part = new Date(dP[2], dP[1], dP[0], hP[0], hP[1], 0, 0);
    var arr= new Date(dA[2], dA[1], dA[0], hA[0], hA[1], 0, 0);
    var now = new Date();
    //--------
    if(part.getTime()<arr.getTime()){
        if(part.getTime()>now.getTime()+(1000*3600)){
            document.getElementById("dataP_err").innerHTML = "";
            document.getElementById("oraP_err").innerHTML = "";
            return true;
        }
        else {
            document.getElementById("dataP_err").innerHTML = "La partenza non può essere prima di un'ora da adesso.";
            document.getElementById("oraP_err").innerHTML = "La partenza non può essere prima di un'ora da adesso.";
            return false;
        }
    }
    else {
        document.getElementById("dataP_err").innerHTML = "La partenza non può essere dopo l'arrivo.";
        document.getElementById("oraP_err").innerHTML = "La partenza non può essere dopo l'arrivo.";
        return false;
    }
}
