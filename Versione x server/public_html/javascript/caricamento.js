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
          dateFormat: "dd-mm-yy",
          minDate: 0 /*, maxDate: +30 */ ,
          onClose: function() {
            funzioniDiValidazione.valida_data("data");
          },
          beforeShow: function() {
            setTimeout(appendsomething, 10);
          },
          onChangeMonthYear: function() {
            setTimeout(appendsomething, 10);
          }
        });
        var appendsomething = function() {
          $("#ui-datepicker-div").append("<div class='controlliDatepicker'>Utilizzare <strong>CTRL</strong> e le <strong>freccette</strong> per muoversi. Invio per confermare.</div>");
        };
      });
      // Actions
      var part = document.getElementById("partenza");
      part.onblur = function() {
        funzioniDiValidazione.valida_nome("partenza", "Luogo di partenza");
      };
      var arr = document.getElementById("arrivo");
      arr.onblur = function() {
        funzioniDiValidazione.valida_nome("arrivo", "Luogo di arrivo");
      };
      var giorno = document.getElementById("data");
      giorno.onblur = function() {
        funzioniDiValidazione.valida_data("data");
      };
      // onsubmit forse che tutto sia non nullo????
      var form = document.forms[0];
      if (typeof form != "undefined") {
        form.onsubmit = function() {
          return funzioniDiValidazioneSubmit.valida_submit_home();
        };
      } else {
        console.log("O non sono presenti forms oppure il metodo document.form non è supportato.");
      }
    } else {
      console.log("Funzioni Dom necessarie non sono supportate.");
    }
  },

  caricamento_iscrizione: function() {
    if (document.getElementById != "undefined") {
      // Actions
      var n = document.getElementById("nome");
      n.onblur = function() {
        funzioniDiValidazione.valida_nome("nome", "Nome");
      };
      var c = document.getElementById("cognome");
      c.onblur = function() {
        funzioniDiValidazione.valida_nome("cognome", "Cognome");
      };
      var u = document.getElementById("username");
      u.onblur = function() {
        funzioniDiValidazione.valida_username();
      };
      var y = document.getElementById("anno");
      y.onblur = function() {
        funzioniDiValidazione.valida_anno_nasc();
      };
      var mail = document.getElementById("email");
      mail.onblur = function() {
        funzioniDiValidazione.valida_email("email");
      };
      var pw = document.getElementById("password");
      pw.onblur = function() {
        funzioniDiValidazione.valida_password("password");
      };
      var pwc = document.getElementById("conferma");
      pwc.onblur = function() {
        funzioniDiValidazione.valida_password("conferma");
      };
      // submit
      var form = document.forms[0];
      if (typeof form != "undefined") {
        form.onsubmit = function() {
          return funzioniDiValidazioneSubmit.valida_submit_iscrizione();
        };
      } else {
        console.log("O non sono presenti forms oppure il metodo document.form non è supportato.");
      }
    } else {
      console.log("Funzioni Dom necessarie non sono supportate.");
    }
  },

  caricamento_viaggi: function() {
    $(".viaggio").css("cursor", "pointer");
    $(".viaggio").click(function() {
      window.location = $(this).find("a").attr("href");
      return false;
    });
  },

  caricamento_offerta: function() {
    if (document.getElementById != "undefined") {
      // jquery applet per calendario
      $("#dataA").datepicker({
        dateFormat: "dd-mm-yy",
        minDate: 0 /*, maxDate: +30 */ ,
        onClose: function() {
          funzioniDiValidazione.valida_data("dataA");
        },
        beforeShow: function() {
          setTimeout(appendsomething, 10);
        },
        onChangeMonthYear: function() {
          setTimeout(appendsomething, 10);
        }
      });
      $("#dataP").datepicker({
        dateFormat: "dd-mm-yy",
        minDate: 0 /*, maxDate: +30 */ ,
        onClose: function() {
          funzioniDiValidazione.valida_data("dataP");
        },
        beforeShow: function() {
          setTimeout(appendsomething, 10);
        },
        onChangeMonthYear: function() {
          setTimeout(appendsomething, 10);
        }
      });
      var appendsomething = function() {
        $("#ui-datepicker-div").append("<div class='controlliDatepicker'>Utilizzare <strong>CTRL</strong> e le <strong>freccette</strong> per muoversi. Invio per confermare.</div>");
      };
      //Actions
      var part = document.getElementById("partenza");
      part.onblur = function() {
        funzioniDiValidazione.valida_nome("partenza", "Luogo di partenza");
      };
      var arr = document.getElementById("arrivo");
      arr.onblur = function() {
        funzioniDiValidazione.valida_nome("arrivo", "Luogo di arrivo");
      };
      var giornoA = document.getElementById("dataA");
      giornoA.onblur = function() {
        funzioniDiValidazione.valida_data("dataA");
      };
      var giornoP = document.getElementById("dataP");
      giornoP.onblur = function() {
        funzioniDiValidazione.valida_data("dataP");
      };
      var oraA = document.getElementById("oraA");
      oraA.onblur = function() {
        funzioniDiValidazione.valida_ora("oraA");
      };
      var oraP = document.getElementById("oraP");
      oraP.onblur = function() {
        funzioniDiValidazione.valida_ora("oraP");
      };

      var t1 = document.getElementById("tappa1");
      t1.onblur = function() {
        funzioniDiValidazione.valida_tappa(1);
      };
      var t2 = document.getElementById("tappa2");
      t2.onblur = function() {
        funzioniDiValidazione.valida_tappa(2);
      };
      var t3 = document.getElementById("tappa3");
      t3.onblur = function() {
        funzioniDiValidazione.valida_tappa(3);
      };

      var prezzo = document.getElementById("prezzo");
      prezzo.onblur = function() {
        funzioniDiValidazione.valida_soldi("prezzo");
      };
      var posti = document.getElementById("posti");
      posti.onblur = function() {
        funzioniDiValidazione.valida_posti("posti");
      };
      var form = document.forms[0];
      if (typeof form != "undefined") {
        form.onsubmit = function() {
          return funzioniDiValidazioneSubmit.valida_submit_offerta();
        };
      } else {
        console.log("O non sono presenti forms oppure il metodo document.form non è supportato.");
      }

    } else {
      console.log("Funzioni Dom necessarie non sono supportate.");
    }
  },

  caricamento_messaggi: function() {
    // div cliccabile
    $(".conversazione").css("cursor", "pointer");
    $(".conversazione").click(function() {
      window.location = $(this).find("a").attr("href");
      return false;
    });
    ///// ok

  },

  caricamento_accesso: function() {
    if (document.getElementById != "undefined") {
      var form = document.forms[0];
      if (typeof form != "undefined") {
        form.onsubmit = function() {
          return funzioniDiValidazioneSubmit.valida_tutto_compilato("username", "password");
        };
      } else {
        console.log("O non sono presenti forms oppure il metodo document.form non è supportato.");
      }
    } else {
      console.log("Funzioni Dom necessarie non sono supportate.");
    }
  },

  caricamento_modifica_profilo: function() {
    if (document.getElementById != "undefined") {
      // Azioni
      var n = document.getElementById("nome");
      n.onblur = function() {
        funzioniDiValidazione.valida_nome("nome", "Nome");
      };
      var c = document.getElementById("cognome");
      c.onblur = function() {
        funzioniDiValidazione.valida_nome("cognome", "Cognome");
      };
      var mail = document.getElementById("email");
      mail.onblur = function() {
        funzioniDiValidazione.valida_email("email");
      };
      var pwold = document.getElementById("vecchiaPassword");
      pwold.onblur = function() {
        funzioniDiValidazione.valida_password("vecchiaPassword");
      };
      var pwnew = document.getElementById("nuovaPassword");
      pwnew.onblur = function() {
        funzioniDiValidazione.valida_password("nuovaPassword");
      };
      var anno = document.getElementById("anno");
      anno.onblur = function() {
        funzioniDiValidazione.valida_anno_nasc();
      };
      var annop = document.getElementById("annoPatente");
      annop.onblur = function() {
        funzioniDiValidazione.valida_anno_pat();
      };
      var auto = document.getElementById("auto");
      auto.onblur = function() {
        funzioniDiValidazione.valida_nome("auto", "Automobile");
      };
      // submit
      var form = document.forms[0];
      if (typeof form != "undefined") {
        form.onsubmit = function() {
          return funzioniDiValidazioneSubmit.valida_submit_modifica_profilo();
        };
      } else {
        console.log("O non sono presenti forms oppure il metodo document.form non è supportato.");
      }

      // Test con modernizr
      if (Modernizr.csstransforms && Modernizr.opacity) {
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
    $(".risultato").css("cursor", "pointer");
    $(".risultato").click(function() {
      window.location = $(this).find("a").attr("href");
      return false;
    });
  }
};
