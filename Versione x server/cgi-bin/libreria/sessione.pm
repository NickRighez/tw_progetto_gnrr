#! /usr/bin/perl -w
###################################################
# Pacchetto di gestione della sessione
###################################################

package sessione;

use strict;
use warnings;
use CGI::Session;
use CGI qw(-utf8);
use libreria::research;
use utf8;

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
        $header = $session->header(-type => 'text/html', -charset =>'UTF-8');
    }
    else{
        $header = $q->header(-type => 'text/html', -charset =>'UTF-8');
    }
    return ($session,$header);
}

1;
