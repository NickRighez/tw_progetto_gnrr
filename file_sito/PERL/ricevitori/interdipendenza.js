
function valida_tempo_passaggio(){
// partenza min 1h nel futuro. arrivo dopo partenza.
// Pre: data e ora corretti ed esistenti
var dataA = document.getElementById("dataA").value;
var dataP = document.getElementById("dataP").value;
var oraA = document.getElementById("oraA").value;
var oraP = document.getElementById("oraP").value;
//new Date(year, month, day, hours, minutes, seconds, milliseconds);
//$.datepicker.parseDate( "yy-mm-dd", "2007-01-26" );
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

////////////////////////////////////////////////////////////////////////////

function compilazione_tappe(id){
  if(id=="tappa2"){
    if(document.getElementById("tappa1").value ==""){
    document.getElementById("tappa2_err").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
  }
  else {
        document.getElementById("tappa2_err").value = "";
  }
  }
  else if (id=="tappa3") {
    if(document.getElementById("tappa1").value ==""){
    document.getElementById("tappa3_err").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
  }
  else if(document.getElementById("tappa2").value ==""){
  document.getElementById("tappa3_err").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
}
  else {
        document.getElementById("tappa3_err").value = "";
  }
  }
}

function valida_tappe(){
  var tappa1 = document.getElementById("tappa1").value;
  var tappa2 = document.getElementById("tappa2").value;
  var tappa3 = document.getElementById("tappa3").value;
  if(tappa1==''){
    document.getElementById("tappa2").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
    document.getElementById("tappa3").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
    document.getElementById("tappa2").disabled = true;
    document.getElementById("tappa3").disabled = true;
  }
  else if (tappa2=='') {
    // document.getElementById("tappa2").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
    document.getElementById("tappa3").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
    document.getElementById("tappa2").disabled = false;
    document.getElementById("tappa3").disabled = true;
  }
  else{
    document.getElementById("tappa3").disabled = false;
  }
}




////////////////////////////////////////
// Disattivazione submit per campi non completi
 /*
function disattiva_submit_at_start() {//
    document.getElementById('submitbutton').disabled = true;
    //document.getElementById('submitbutton').disabled = false;
}
*/
//ritorna bool per evento onsubmit
function verifica_submit_possibile_nomePag(){
    console.log("ecce");
    var elements = document.getElementsByTagName("input");
    console.log(elements.length);
    for(var i = 0; i < elements.length; i++)
    {
        console.log(elements[i].name);
        /* do whatever you need to do with each input */
    }
}


///////////////////////////////////////////////////////////////////
// FUNZIONI PER ONLOAD

function preparazione_tappe(){
// verifica non siano compilate
    document.getElementById("tappa2").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
    document.getElementById("tappa3").value = "Per poter inserire questa tappa, inserire prima le precedenti.";
    document.getElementById("tappa2").disabled = true;
    document.getElementById("tappa3").disabled = true;
}
