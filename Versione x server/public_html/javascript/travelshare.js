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
// validazione.js

////////////////////////////////////////////////
// Validazione dei singoli campi dati
////////////////////////////////////////////////

var funzioniDiValidazione = {
  valida_username: function() {
    var input = document.getElementById('username').value;
    var sol = /^[A-Za-z0-9_-]+$/.test(input);
    if (!sol) {
      document.getElementById('username_err').innerHTML = "Username non valido. Caratteri ammessi lettere, numeri, trattino e underscore.";
      return false;
    } else {
      var n = input.length;
      if (n === 0) {
        document.getElementById('username_err').innerHTML = "Username obbligatorio";
        return false;
      } else if (n > 18) {
        document.getElementById('username_err').innerHTML = "Username al massimo di 18 caratteri"; // NON QUI!!!!!
        return false;
      } else if (n < 5) {
        document.getElementById('username_err').innerHTML = "Username minimo di 5 caratteri";
        return false;
      } else {
        document.getElementById('username_err').innerHTML = '';
        return true;
      }
    }
  },


  valida_nome: function(id, parola) {
    var input = document.getElementById(id).value;
    var sol = /^(\u0027|\u002C|\u002D|\u002F|[\u0030-\u0039]|[\u0041-\u005A]|[\u0061-\u007A]|[\u00C0-\u00FF]|\s)+$/.test(input);
    if (!sol) {
      document.getElementById(id + '_err').innerHTML = parola + " non valido, inserire solo lettere, trattini, apostrofi, punti e spazi.";
      return false;
    } else if (!input.length) {
      document.getElementById(id + '_err').innerHTML = "Campo dati " + parola + " obbligatorio";
      return false;
    } else {
      document.getElementById(id + '_err').innerHTML = "";
      return true;
    }
  },


  valida_auto: function() {
    var input = document.getElementById('auto').value;
    var sol = /^[A-Za-z0-9,\s-]+$/.test(input);
    if (!sol) {
      document.getElementById('auto_err').innerHTML = "Nome dell'auto non valido, inserire solo lettere, trattini, apostrofi, punti e spazi.";
      return false;
    } else if (!input.length) {
      document.getElementById('auto_err').innerHTML = "Campo dati " + 'auto' + " obbligatorio";
      return false;
    } else {
      document.getElementById('auto_err').innerHTML = "";
      return true;
    }
  },


  valida_area_testo: function(id, obbl) {
    var input = document.getElementById(id).innerHTML;
    var sol = /^(\u0027|\u002C|\u002D|\u002F|[\u0030-\u0039]|[\u0041-\u005A]|[\u0061-\u007A]|[\u00C0-\u00FF]|\s)+$/.test(input);
    if (!sol) {
      document.getElementById(id + '_err').innerHTML = "Testo non valido, inserire solo lettere, trattini, apostrofi, punti e spazi.";
      return false;
    } else if (!input.length && obbl) {
      document.getElementById(id + '_err').innerHTML = "Testo obbligatorio";
      return false;
    } else {
      document.getElementById(id + '_err').innerHTML = "";
      return true;
    }
  },

  valida_tappa: function(num) {
    var input = document.getElementById('tappa' + num).value;
    var sol = /^(\u0027|\u002C|\u002D|\u002F|[\u0030-\u0039]|[\u0041-\u005A]|[\u0061-\u007A]|[\u00C0-\u024F]|\s)*$/.test(input);
    if (!sol) {
      document.getElementById('tappa' + num + '_err').innerHTML = "Nome tappa non valido, inserire solo lettere, trattini, apostrofi, punti e spazi.";
      return false;
    } else {
      document.getElementById('tappa' + num + '_err').innerHTML = "";
      return true;
    }
  },

  valida_anno_nasc: function() {
    var input = document.getElementById('anno').value;
    var sol = /^[1-2][0-9][0-9][0-9]$/.test(input);
    if (!sol) {
      document.getElementById('anno_err').innerHTML = "Anno di nascita non valida, inserire l anno in formato 'aaaa'";
      return false;
    } else {
      var d = new Date();
      var n = d.getFullYear();
      if ((Number(n) - (Number(input) + 18)) < 0) {
        document.getElementById('anno_err').innerHTML = "Possono registrarsi solo utenti maggiorenni";
        return false;
      } else {
        document.getElementById('anno_err').innerHTML = '';
        return true;
      }
    }
  },


  valida_password: function(id) {
    var input = document.getElementById(id).value;
    var sol = /^[A-Za-z0-9_\.-]{8,16}$/.test(input);
    if (!sol) {
      if (input.length > 16 || input.length < 8) {
        document.getElementById(id + '_err').innerHTML = " La password deve comprendere da 8 a 16 caratteri.";
      } else {
        document.getElementById(id + '_err').innerHTML = "Password non valida, sono permesse lettere maiuscole o minuscole, e i caratteri underscore, hyphen o punto.";
      }
      return false;
    } else {
      if (id == 'conferma') {
        if (document.getElementById(id).value == document.getElementById('password').value) {
          document.getElementById(id + '_err').innerHTML = '';
          return true;
        } else {
          document.getElementById(id + '_err').innerHTML = 'La password e la conferma devono essere uguali.';
          return false;
        }
      } else {
        document.getElementById(id + '_err').innerHTML = '';
        return true;
      }
    }
  },


  valida_ora: function(id) {
    var input = document.getElementById(id).value;
    var sol = /^\d\d\:\d\d$/.test(input);
    if (!sol) {
      document.getElementById(id + '_err').innerHTML = "Inserire un orario nel formato hh:mm.";
      return false;
    } else {
      var p = input.split(':');
      var h = p.shift();
      var m = p.shift();
      if (h < 0 || h >= 24 || m < 0 || m >= 60) {
        document.getElementById(id + '_err').innerHTML = "Inserire un orario corretto.";
        return false;
      } else {
        document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
        return true;
      }
    }
  },

  valida_posti: function(id) {
    var input = document.getElementById(id).value;
    var sol = /^\d{1,}$/.test(input);
    if (!sol) {
      document.getElementById(id + '_err').innerHTML = "Inserire un numero.";
      return false;
    } else {
      document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
      return true;
    }
  },

  valida_soldi: function(id) {
    var input = document.getElementById(id).value;
    var sol = /^\d{1,}(\.|\,)*(\d|\d\d){0,1}$/.test(input);
    if (!sol) {
      document.getElementById(id + '_err').innerHTML = "Inserire una cifra con al massimo due cifre decimali.";
      return false;
    } else {
      document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
      return true;
    }
  },

  valida_email: function(id) {
    var input = document.getElementById(id).value;
    var sol = /^([a-zA-Z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/.test(input);
    if (!sol) {
      document.getElementById(id + '_err').innerHTML = "Inserire un indirizzo email.";
      return false;
    } else {
      document.getElementById(id + '_err').innerHTML = ""; // per rimuovere eventuali segnalazioni precendenti
      return true;
    }
  },

  valida_anno_pat: function() {
    var input = document.getElementById('annoPatente').value;
    var sol = /^[1-2][0-9][0-9][0-9]$/.test(input);
    if (!sol) {
      document.getElementById('annoPatente_err').innerHTML = "Anno di conseguimento della patente non valido, inserire l\' anno in formato 'aaaa'";
      return false;
    } else {
      document.getElementById('annoPatente_err').innerHTML = '';
      return true;
    }
  },

  test_data: function(stringdate) {
    try {
      $.datepicker.parseDate("dd-mm-yy", stringdate);
      return true;
    } catch (err) {
      return false;
    }
  },

  valida_data: function(id) {
    var input = document.getElementById(id).value;
    if (!funzioniDiValidazione.test_data(input) || !input.length) {
      document.getElementById(id + '_err').innerHTML = "Inserire una data in formato gg-mm-aaaa.";
      return false;
    } else {
      document.getElementById(id + '_err').innerHTML = "";
      return true;
    }
  }
};
// valida_submits.js

////////////////////////////////////////////////
// Validazione delle submits
////////////////////////////////////////////////

var funzioniDiValidazioneSubmit = {
  valida_submit_modifica_profilo: function() {
    var res = false;
    var v1 = funzioniDiValidazione.valida_nome("nome", "Nome");
    var v2 = funzioniDiValidazione.valida_nome("cognome", "Cognome");
    var v3 = funzioniDiValidazione.valida_email("email");
    var v4 = funzioniDiValidazione.valida_password("vecchiaPassword");
    var v5 = funzioniDiValidazione.valida_password("nuovaPassword");
    var v6 = funzioniDiValidazione.valida_anno_nasc();
    var v7 = funzioniDiValidazioneSubmit.verifica_blocco_modifica_profilo();
    if (!v7) {
      document.getElementById("submitbutton_err").innerHTML = "La sezione dei dati per guidatori va compilata in ogni sua parte o in nessuna (per i non guidatori).";
      res = false;
    } else {
      if (v1 && v2 && v3 && v4 && v5 && v6 && v7) {
        res = true;
      } else {
        document.getElementById("submitbutton_err").innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
        res = false;
      }
    }
    return res;
  },

  // controlla che i campi dati elencati tra gli argomenti siano compilati. per onsubmit senza dettagli ---- generico
  valida_tutto_compilato: function() {
    var numberOfMiss = 0;
    var i;
    for (i = 0; i < arguments.length; i++) {
      var itemID = arguments[i];
      var input = document.getElementById(itemID).value;
      if (!input.length) {
        document.getElementById(itemID + "_err").innerHTML = "Compilare il campo.";
        numberOfMiss = numberOfMiss + 1;
      } else {
        document.getElementById(itemID + "_err").innerHTML = "";
      }
    }
    if (numberOfMiss === 0) {
      return true;
    } else {
      document.getElementById("submitbutton_err").innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
      return false;
    }
  },

  valida_submit_home: function() {
    var res1 = funzioniDiValidazione.valida_data("data");
    var res2 = funzioniDiValidazione.valida_nome("arrivo", "Luogo di arrivo");
    var res3 = funzioniDiValidazione.valida_nome("partenza", "Luogo di partenza");
    if (!res1 || !res2 || !res3) {
      document.getElementById("submitbutton_err").innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
      return false;
    } else {
      return true;
    }
  },

  valida_submit_iscrizione: function() {
    var r1 = funzioniDiValidazione.valida_nome("nome", "Nome");
    var r2 = funzioniDiValidazione.valida_nome("cognome", "Cognome");
    var r3 = funzioniDiValidazione.valida_username();
    var r4 = funzioniDiValidazione.valida_email("email");
    var r5 = funzioniDiValidazione.valida_password("password");
    var r6 = funzioniDiValidazione.valida_password("conferma");
    var r7 = funzioniDiValidazione.valida_anno_nasc();
    if (!r1 || !r2 || !r3 || !r4 || !r5 || !r6 || !r7) {
      document.getElementById("submitbutton_err").innerHTML = "&Egrave; necessario compilare tutti i campi dati.";
      return false;
    } else {
      return true;
    }
  },

  valida_submit_offerta: function() {
    var r1 = funzioniDiValidazione.valida_nome("partenza", "Partenza");
    var r2 = funzioniDiValidazione.valida_nome("arrivo", "Arrivo");
    var r3 = funzioniDiValidazione.valida_tappa(1);
    var r4 = funzioniDiValidazione.valida_tappa(2);
    var r5 = funzioniDiValidazione.valida_tappa(3);
    var r6 = funzioniDiValidazione.valida_data("dataA");
    var r7 = funzioniDiValidazione.valida_data("dataP");
    var r8 = funzioniDiValidazione.valida_ora("oraA");
    var r9 = funzioniDiValidazione.valida_ora("oraP");
    var r10 = funzioniDiValidazione.valida_soldi("prezzo");
    var r11 = funzioniDiValidazione.valida_posti("posti");
    if (!r1 || !r2 || !r3 || !r4 || !r5 || !r6 || !r7 || !r8 || !r9 || !r10 || !r11) {
      document.getElementById("submitbutton_err").innerHTML = "&Egrave; necessario compilare tutti i campi dati a parte la descrizione del viaggio che è opzionale.";
      return false;
    } else {
      if (funzioniDiValidazioneSubmit.verifica_ordine_tappe()) {
        document.getElementById("submitbutton_err").innerHTML = "";
        document.getElementById("tappa1_err").innerHTML = "";
        document.getElementById("tappa2_err").innerHTML = "";
        document.getElementById("tappa3_err").innerHTML = "";
        if (funzioniDiValidazioneSubmit.verifica_ordine_orari()) {
          return true;
        } else {
          document.getElementById("submitbutton_err").innerHTML = "La partenza deve avvenire prima dell\'arrivo.";
          document.getElementById("oraA_err").innerHTML = "La partenza deve avvenire prima dell\'arrivo.";
          document.getElementById("oraP_err").innerHTML = "La partenza deve avvenire prima dell\'arrivo.";
          document.getElementById("dataA_err").innerHTML = "La partenza deve avvenire prima dell\'arrivo.";
          document.getElementById("dataP_err").innerHTML = "La partenza deve avvenire prima dell\'arrivo.";
          return false;
        }
      } else {
        return false;
      }
    }
  },

  verifica_ordine_tappe: function() {
    var t1 = document.getElementById("tappa1").value.length;
    var t2 = document.getElementById("tappa2").value.length;
    var t3 = document.getElementById("tappa3").value.length;
    if (t1 && t2 && t3) {
      return true;
    } else if (!t1 && !t2 && !t3) {
      return true;
    } else if (!t1 && (t2 || t3)) {
      document.getElementById("submitbutton_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      document.getElementById("tappa1_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      document.getElementById("tappa2_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      document.getElementById("tappa3_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      return false;
    } else if ((!t1 || !t2) && t3) {
      document.getElementById("submitbutton_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      document.getElementById("tappa1_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      document.getElementById("tappa2_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      document.getElementById("tappa3_err").innerHTML = "Le tappe possono essere inserite solo nell\'ordine corretto.";
      return false;
    } else {
      return true;
    }
  },

  verifica_ordine_orari: function() {
    var ha = document.getElementById("oraA").value.split(":");
    var hp = document.getElementById("oraP").value.split(":");
    var da = document.getElementById("dataA").value.split("-");
    var dp = document.getElementById("dataP").value.split("-");
    var part = new Date(dp[2], dp[1], dp[0], hp[0], hp[1], 0, 0);
    var arr = new Date(da[2], da[1], da[0], ha[0], ha[1], 0, 0);
    var diff = arr.getTime() - part.getTime();
    return diff > 0;
  },

  verifica_radio3: function(id) {
    var v1 = document.getElementById(id + 0).checked;
    var v2 = document.getElementById(id + 1).checked;
    var v3 = document.getElementById(id + 2).checked;
    return v1 || v2 || v3;
  },

  verifica_radio2: function(id) {
    var v1 = document.getElementById(id + 0).checked;
    var v2 = document.getElementById(id + 1).checked;
    return v1 || v2;
  },

  verifica_blocco_modifica_profilo: function() {
    var v1 = funzioniDiValidazione.valida_anno_pat();
    var v2 = funzioniDiValidazione.valida_auto();
    var v3 = funzioniDiValidazioneSubmit.verifica_radio3("musica");
    var v4 = funzioniDiValidazioneSubmit.verifica_radio3("chiacchiere");
    var v5 = funzioniDiValidazioneSubmit.verifica_radio2("animali");
    var v6 = funzioniDiValidazioneSubmit.verifica_radio2("fumatori");
    return v1 && v2 && v3 && v4 && v5 && v6;
  },


  valida_tempo_passaggio: function() {
    var dataA = document.getElementById("dataA").value;
    var dataP = document.getElementById("dataP").value;
    var oraA = document.getElementById("oraA").value;
    var oraP = document.getElementById("oraP").value;
    var hA = oraA.split(":");
    var hP = oraP.split(":");
    var dA = dataA.split("-");
    var dP = dataP.split("-");
    var part = new Date(dP[2], dP[1], dP[0], hP[0], hP[1], 0, 0);
    var arr = new Date(dA[2], dA[1], dA[0], hA[0], hA[1], 0, 0);
    var now = new Date();
    //--------
    if (part.getTime() < arr.getTime()) {
      if (part.getTime() > now.getTime() + (1000 * 3600)) {
        document.getElementById("dataP_err").innerHTML = "";
        document.getElementById("oraP_err").innerHTML = "";
        return true;
      } else {
        document.getElementById("dataP_err").innerHTML = "La partenza non può essere prima di un\'ora da adesso.";
        document.getElementById("oraP_err").innerHTML = "La partenza non può essere prima di un\'ora da adesso.";
        return false;
      }
    } else {
      document.getElementById("dataP_err").innerHTML = "La partenza non può essere dopo l\'arrivo.";
      document.getElementById("oraP_err").innerHTML = "La partenza non può essere dopo l\'arrivo.";
      return false;
    }
  }
};
