
###################################################
# Pacchetto di gestione della sessione
###################################################

package sessione;

use strict;
use warnings;
use CGI::Session;
use CGI;
use research;

sub distruzione {
    my $session = CGI::Session->load() or die $!;
    my $SID = $session->id();
    $session->close();
    $session->delete();
    $session->flush();
    return 0;
}

sub createSess {
  my $cgi = new CGI;
  my $sid = $cgi->cookie("CGISESSID") || undef;
  my $session = new CGI::Session("driver:File", $sid, {Directory=>"/var/www/html"});
  if(defined $sid){
    return $session->id();
  }
  else{
    return $cgi->header();
  }

}


sub setVar {
  my $k = shift @_;
  my $v = shift @_;
  my $cgi = new CGI;
  my $session = CGI::Session->load() or die CGI::Session->errstr();
  if($session->is_expired || $session->is_empty){
    return undef;
  }
  $session->param($k,$v);
  return 1;
}

sub getVar {
  my $k = shift @_;
  my $session = CGI::Session->load() or die CGI::Session->errstr();
  if($session->is_expired || $session->is_empty){
    return "vvv";
  }
  my $v = $session->param($k);
  if(!defined($v)) {
    return -1;
  }
  #$session->clear($k);
  return $v;
}

sub login {
  my $uname = shift @_;
  my $upass = shift @_;
  my $res = research::query_usernamepw($uname,$upass);
  if($res){
    #do
  }
  else{
    # dont 
  }
}

sub get_username {
  my $session = my $s = CGI::Session->load() or die CGI::Session->errstr();
  if($session->is_expired || $session->is_empty){
    return undef;
  }
  my $v = $session->param("username");
  return -1 unless defined $v;
  return $v;
}



# NOTE:
# la variabile @_ contiene i parametri della funzione
# la variabile $! contiene l'ultimo codice di errore generato

1;
