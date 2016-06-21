#! /usr/bin/perl

use strict;
use warnings;
use CGI::Carp 'fatalsToBrowser';

use libreria::data_registration;
use libreria::research;

print "Content-type: text/html\n\n";
my %array = ('UTENTE' => 'u1');
    #('IDUte'=> 'nick', 'Email' => 'cicciomio@tesoro.it','Nome' => 'Denis','Cognome' => 'Righez','Sesso'=> 'M','AnnoNascita'=> '1991','Telefono'=>'04980557333','Password'=>'dadadada');


print research::query_users(\%array);


#my $res = data_registration::inserisci_nuovo_utente(\%array);
#if($res)
#{
#    print "inserimento avvenuto con successo\n</br>\n";
#}
#else
#{
#    print "inserimento fallito\n</br>\n";
#}
print "done!!!\n</br>\n";

sub caesar {
    my ($message, $key, $decode) = @_;
    $key = 26 - $key if $decode;
    $message =~ s/([A-Z])/chr(((ord(uc $1) - 65 + $key) % 26) + 65)/geir;
}

print caesar("ciao bello",12,0);
print "\n";
print caesar(caesar("ciao bello",12,0),12,1);
print "\n";