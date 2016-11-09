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
        login_err => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
elsif (!($q->param('passaggio')=~m/^v[0-9]+$/) || !$doc->exists("//SetPassaggi/Passaggio[IDViaggio='".$q->param('passaggio')."']")){
    my %problems = ( DESCRIZIONE_ERRORE => "Si e' tentato di recensire un passaggio non valido.");
    $session->param('problems',\%problems);
    print $session->header(-location => "home.cgi");
}
else {
    print "Content-Type: text/html; charset=UTF-8\n\n";
    my $username=$session->param('username');
    # 'passaggio' valore appeso alla stringa URL.
    my $passaggio = $q->param('passaggio');
    my @feedback_list = research::query_feedback_da_rilasciare_viaggio($username, $passaggio);
    my $empty_feedb = "false";
    my $num_feedback = @feedback_list;
    if($num_feedback == 0){
        $empty_feedb = "true";
    }
    # Viene eliminato tutto il codice html relativo alla form di inserimento del feedback.
    # Il tag CONTENUTO (che è una stringa) viene sostituito da una lista, di nome USER_LIST, di hash, ognuno dei quali della forma:
    #   { username =>  $user_destinatario, nome => $nome_dest, cognome => $cognome_dest, numero => $num_passeggero }
    #   per ognuno degli hash viene creata la corrispondente porzione di form atta all inserimento del feedback

    my $file = "../data/HTML_TEMPLATE/feedback.html";
    open my $fh, '<:encoding(UTF-8)', $file;
    my %hash_keys = (
        NOME_UTENTE => $username,
        FEEDBACK_LIST  => \@feedback_list,
        EMPTY_FEEDB => $empty_feedb,
        PASSAGGIO => $passaggio,
        NUM_NOTIFICHE => research::conta_notifiche($username, data_registration::get_xml_doc()),
        INDEX => 9
        );
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio);
    print $foglio;
}
