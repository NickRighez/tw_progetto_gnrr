
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
    # my $SID = $session->id();
    $session->close();
    $session->delete();
    $session->flush();
    return 0;
}


sub creaSessione {
  my $q=CGI->new();
  my $header;
  my $session = CGI::Session->load() or die CGI::Session->errstr();
  if($session->is_expired || $session->is_empty){
    $session = new CGI::Session(undef,$q, {Directory=>"/tmp"});
    $header = $session->header();
  }
  else{
    $header = $q->header();
  }
  return ($session,$header);
}

1;
