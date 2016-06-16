###################################################
# Pacchetto di gestione della sessione
###################################################

package sessione;

use strict;
use warnings;
use CGI::Session;
use CGI;
use research;

sub login{
    my ($username, $passwd) = @_;
    my $session = new CGI::Session();
# verifica di non essere gia connesso!!!!
    $session->param(-nome, $username);
    $session->param(-pass, $passwd);
}


sub logout{
    my $session = CGI::Session->load() or die $!;
    my $SID = $session->id();
    $session->close();
    $session->delete();
    $session->flush();
}

sub get_username{
    my $session = CGI::Session->load() or die $!;
    if($session->is_expired || $session->is_empty)
    {
        #return undef;
        $cgi = new CGI;
        print $cgi->header('Redirect: /');
        #PATH NON PORTABILE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    }
    else
    {
        my $utente = $session->param('nome');
        return $utente;
    }
}

# NOTIFICHE



#NOTE:
# la variabile @_ contiene i parametri della funzione
# la variabile $! contiene l'ultimo codice di errore generato

1;
