// caricamento.js

////////////////////////////////////////////////
// Funzioni onLoad
////////////////////////////////////////////////

var funzioniDiCaricamento = {
  caricamento_home: function() {
    if (document.getElementById != "undefined" /* && altri test di quello che uso */ ) {
      // jquery applet per calendario
      $(function() {
        $("#data").datepicker({
          dateFormat: 'dd-mm-yy',
          minDate: 0 /*, maxDate: +30 */
        });
      });
      // Actions
      var part = document.getElementById("partenza");
      part.onblur = funzioniDiValidazione.valida_nome("partenza", "Luogo di partenza");
      var arr = document.getElementById("arrivo");
      arr.onblur = funzioniDiValidazione.valida_nome("arrivo", "Luogo di arrivo");
      var giorno = document.getElementById("data");
      giorno.onblur = funzioniDiValidazione.valida_data("data");
      // onsubmit forse che tutto sia non nullo????
    } else {
      console.log("Funzioni Dom necessarie non sono supportate.");
    }
  },

  caricamento_offerta: function() {
    if (document.getElementById != "undefined") {
      // jquery applet per calendario
      $("#dataA").datepicker({
        dateFormat: 'dd-mm-yy',
        minDate: 0 /*, maxDate: +30 */
      });
      $("#dataP").datepicker({
        dateFormat: 'dd-mm-yy',
        minDate: 0 /*, maxDate: +30 */
      });
      //Actions
      var part = document.getElementById("partenza");
      part.onblur = funzioniDiValidazione.valida_nome("partenza", "Luogo di partenza");
      var arr = document.getElementById("arrivo");
      arr.onblur = funzioniDiValidazione.valida_nome("arrivo", "Luogo di arrivo");
      var giornoA = document.getElementById("dataA");
      giornoA.onblur = funzioniDiValidazione.valida_data("dataA");
      var giornoP = document.getElementById("dataP");
      giornoP.onblur = funzioniDiValidazione.valida_data("dataP");
      var oraA = document.getElementById("oraA");
      oraA.onblur = funzioniDiValidazione.valida_ora("oraA");
      var oraP = document.getElementById("oraP");
      oraP.onblur = funzioniDiValidazione.valida_ora("oraP");

      var t1 = document.getElementById("tappa1");
      arr.onblur = funzioniDiValidazione.valida_tappa(1);
      var t2 = document.getElementById("tappa2");
      arr.onblur = funzioniDiValidazione.valida_tappa(2);
      var t3 = document.getElementById("tappa3");
      arr.onblur = funzioniDiValidazione.valida_tappa(3);

      var prezzo = document.getElementById("prezzo");
      prezzo.onblur = funzioniDiValidazione.valida_soldi("prezzo");

    } else {
      console.log("Funzioni Dom necessarie non sono supportate.");
    }
  },

  caricamento_messaggi: function() {
    $('.conversazione').css('cursor', 'pointer');
    $('.conversazione').click(function() {
      window.location = $(this).find("a").attr("href");
      return false;
    });
  },


  caricamento_modifica_profilo: function() {
    if (document.getElementById != "undefined") {
      // Azioni
      var n = document.getElementById("nome");
      n.onblur = funzioniDiValidazione.valida_nome("nome", "Nome");
      var c = document.getElementById("cognome");
      c.onblur = funzioniDiValidazione.valida_nome('cognome','Cognome');
      // Test con modernizr
      if (Modernizr.csstransforms) {
        document.getElementById("chiacchiere0").className = "radioNascosto";
        document.getElementById("chiacchiere1").className = "radioNascosto";
        document.getElementById("chiacchiere2").className = "radioNascosto";
        document.getElementById("chiaImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("chiaImg1").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("chiaImg2").className = "preferenzeImg marginRadioNascosto";

        document.getElementById("musica0").className = "radioNascosto";
        document.getElementById("musica1").className = "radioNascosto";
        document.getElementById("musica2").className = "radioNascosto";
        document.getElementById("musImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("musImg1").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("musImg2").className = "preferenzeImg marginRadioNascosto";

        document.getElementById("animali0").className = "radioNascosto";
        document.getElementById("animali1").className = "radioNascosto";
        document.getElementById("animImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("animImg1").className = "preferenzeImg marginRadioNascosto";

        document.getElementById("fumatori0").className = "radioNascosto";
        document.getElementById("fumatori1").className = "radioNascosto";
        document.getElementById("fumImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("fumImg1").className = "preferenzeImg marginRadioNascosto";
      } else {
        console.log("csstransforms not supported");
      }
    } else {
      console.log("Funzioni Dom necessarie non sono supportate.");
    }
  },

  caricamento_risultati: function() {
    $('.risultato').css('cursor', 'pointer');
    $('.risultato').click(function() {
      window.location = $(this).find("a").attr("href");
      return false;
    });
  }
};
