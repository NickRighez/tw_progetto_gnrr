#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::research;
use libreria::data_registration;
use CGI::Session;
#use lib "../libreria";
use libreria::sessione;

my @s = sessione::creaSessione();
my $session = $s[0];
my $q=CGI->new;

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else {
    my $username = $session->param('username');
    my $utente = $q->param('utente');
    my $doc = data_registration::get_xml_doc();
    my $node = $doc->findnodes("//SetUtenti")->get_node(1);
    if(!($doc->exists("//SetUtenti/Utente[Username=\"".$q->param('utente')."\"]"))) {
        my %problems=(
            DESCRIZIONE_ERRORE => "<div class=\"errore\"><p>Impossibile visualizzare la conversazione. Utente inesistente</p></div>"
            );
        $session->param('problems',\%problems);
        print $session->header(-location => "home.cgi");
    }
    else {
        print "Content-type: text/html\n\n";
        my $username=$session->param('username');
        my $contenuto;
        my %Conversazione=(
            UTENTE => $utente,
            MYSELF => $username
            );
        $contenuto = research::query_conversazione(\%Conversazione);
        $contenuto = $contenuto."\n
        <form action=\"ricevitore_messaggio_privato.cgi\" method=\"post\">
          <input type=\"hidden\" name=\"destinatario\" value=\"$utente\" />
          <textarea rows=\"0\" cols=\"0\" name=\"messaggio\" tabindex=\"11\" title=\"Inserisci un messaggio\"></textarea>
          <div><input type=\"submit\" value=\"Invia\" tabindex=\"12\" ></input></div>
        </form> ";

        if($doc->exists("//SetMessaggi/Conversazione[\@User1=\"$utente\" and \@User2=\"$username\"] | SetMessaggi/Conversazione[\@User1=\"$username\" and \@User2=\"$utente\"]")) {
            data_registration::aggiorna_messaggi_letti($session->param('username'), $q->param('utente'));
        }
        
        

        my $file = "../data/HTML_TEMPLATE/singolaConversazione.html";
        my %hash_keys = (
            NOME_UTENTE => $session->param('username'),
            CONTENUTO => $contenuto,
            DESTINATARIO_MESS_P => $q->param('utente'),
            CONVERSATORE => $q->param('utente'),
            NUM_NOTIFICHE => research::conta_notifiche($session->param('username'), $doc)
            );
        my $template_parser = Template->new;
        open my $fh, '<', $file;
        my $foglio = '';
        $template_parser->process($fh,\%hash_keys,\$foglio);
        print $foglio;
    }
    
}
