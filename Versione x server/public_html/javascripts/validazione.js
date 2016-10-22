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
    var sol = /^(\u0027|\u002C|\u002D|\u002F|[\u0030-\u0039]|[\u0041-\u005A]|[\u0061-\u007A]|[\u00C0-\u024F]|\s)+$/.test(input);
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
    var sol = /^(\u0027|\u002C|\u002D|\u002F|[\u0030-\u0039]|[\u0041-\u005A]|[\u0061-\u007A]|[\u00C0-\u024F]|\s)+$/.test(input);
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
    console.log('tappa' + num);
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
    var sol = /^([a-z0-9_\.-]+)@([a-z]+)\.([a-z]{2,6})$/.test(input);
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
