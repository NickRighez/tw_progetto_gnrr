###################################################
# Pacchetto di gestione della sessione
###################################################

package sessioneMIA;

use strict;
use warnings;
use CGI::Session;

sub login(){
    my ($username, $passwd) = @_;
    my $session = new CGI::Session();
    $session->param(-nome, $username);
    $session->param(-pass, $passwd);
}


sub logout(){
    my $session = CGI::Session->load() or die $!;
    my $SID = $session->id();
    $session->close();
    $session->delete();
    $session->flush();
}

sub get_username()
{
    my $session = CGI::Session->load() or die $!;
    if($session->is_expired || $session->is_empty)
    {
        return undef;
    }
    else
    {
        my $utente = $session->param('nome');
        return $utente;
    }
}


#NOTE:
# la variabile @_ contiene i parametri della funzione
# la variabile $! contiene l'ultimo codice di errore generato

1;
