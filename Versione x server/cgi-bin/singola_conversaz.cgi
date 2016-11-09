#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Carp qw(fatalsToBrowser);
use libreria::research;
use libreria::data_registration;
use CGI::Session;
use libreria::sessione;
use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";

my @s = sessione::creaSessione();
my $session = $s[0];
my $q=CGI->new;
my $doc = data_registration::get_xml_doc();

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
elsif(!($q->param('utente')=~m/^[A-Za-z0-9_-]{5,18}$/) ||
        !($doc->exists("//SetUtenti/Utente[Username=\"".$q->param('utente')."\"]"))){
    my %problems=(
      DESCRIZIONE_ERRORE => "Tentativo di visualizzare una conversazione con un utente inesistente."
      );
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    my $username = $session->param('username');
    my $utente = $q->param('utente');
    
    my $node = $doc->findnodes("//SetUtenti")->get_node(1);
   
        #print "Content-Type: text/html; charset=UTF-8\n\n";
	#print $q->header(-charset => 'UTF-8');
binmode(STDOUT, ":utf8");
	print "Content-Type: text/html; charset=UTF-8\n\n\n";

	
        my $username=$session->param('username');
        my $contenuto;
        my %Conversazione=(
            UTENTE => $utente,
            MYSELF => $username
            );
        $contenuto = research::query_conversazione(\%Conversazione);

        if($doc->exists("//SetMessaggi/Conversazione[\@User1=\"$utente\" and \@User2=\"$username\"] | //SetMessaggi/Conversazione[\@User1=\"$username\" and \@User2=\"$utente\"]")) {
            data_registration::aggiorna_messaggi_letti($session->param('username'), $q->param('utente'));
        }
        
        

        my $file = "../data/HTML_TEMPLATE/singolaConversazione.html";
        my %hash_keys = (
            NOME_UTENTE => $session->param('username'),
            CONTENUTO => $contenuto,
            CONVERSATORE => $q->param('utente'),
            NUM_NOTIFICHE => research::conta_notifiche($session->param('username'), $doc)
            );
        my $template_parser = Template->new({ ENCODING => 'utf8' });

        open my $fh, '<:encoding(UTF-8)', $file;
        my $foglio = '';
        $template_parser->process($fh,\%hash_keys,\$foglio);
        print $foglio;

    
}
