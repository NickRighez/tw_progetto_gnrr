###################################################
# Pacchetto di gestione della sessione
###################################################

package sessione;

use strict;
use warnings;
use CGI::Session;
use CGI;
use research;

out $home = "";###############################################################################################################

sub login {
    my $username = shift @_;
    $passwd = shift @_;
    my $session = CGI::Session->load() or die $!;
    if($session->is_expired || $session->is_empty){
      $session = new CGI::Session();
    }
# verifica di non essere gia connesso!!!!
    $res = research::query_usernamepw($username,$passwd);
    if($res){
      $session->param(-nome, $username);
      $session->param(-pass, $passwd);
      return 1;
    }
    else{
      $session->close();
      return 0;
    }
}


sub logout {
    my $session = CGI::Session->load() or die $!;
    my $SID = $session->id();
    $session->close();
    $session->delete();
    $session->flush();
}

sub get_username {
    my $session = CGI::Session->load() or die $!;
    if($session->is_expired || $session->is_empty){
        #return undef;
        $cgi = new CGI;
        print $cgi->redirect($home);
        #PATH NON PORTABILE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    }
    else{
        my $utente = $session->param('nome');
        return $utente;
    }
}

sub setVar {
  my $k = shift @_;
  my $v = shift @_;
  my $session = CGI::Session->load() or die $!;
  $session->param($k,$v);
  return 0;
}

sub getVar {
  my $k = shift @_;
  my $session = CGI::Session->load() or die $!;
  my $v = $session->param($k);
  $session->clear($k);
  return $v;
}

sub getUsername {
  return $session->param($username);
}



# NOTE:
# la variabile @_ contiene i parametri della funzione
# la variabile $! contiene l'ultimo codice di errore generato

1;
