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
        login_err => "Utente non loggato, pagina inaccessibile"
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else {
    print "Content-type: text/html\n\n";
    my $username=$session->param('username');
    my $passaggio = $q->param('passaggio');
    my $contenuto;

    my $doc=data_registration::get_xml_doc();
    my $conducente = $doc->findnodes("//SetPassaggi/Passaggio[IDViaggio='$passaggio']/Conducente")->get_node(1)->textContent;
    my @destinatari = $doc->findnodes("//SetUtenti/Utente[Username='$username']/Notifiche/FeedDaRilasciare[\@Passaggio='$passaggio']/\@Destinatario");
    my $num = @destinatari;
    my $ind = 1;
    $contenuto = $contenuto. "<h1>Inserisci i feedback dei tuoi compagni di viaggioooooooooooooo</h1>
                <form action=\"ricevitore_feedback.cgi\" method=\"post\">";
    $contenuto = $contenuto. "<input type=\"hidden\" name=\"passaggio\" value=\"$passaggio\"></input>";
    for(my $i=0; $i<$num; $i++){
        my $dest = $destinatari[$i]->textContent;
        my $nome = $doc->findnodes("//SetUtenti/Utente[Username='$dest']/Nome")->get_node(1)->textContent;
        my $cognome = $doc->findnodes("//SetUtenti/Utente[Username='$dest']/Cognome")->get_node(1)->textContent;
        if($conducente eq $dest) {
            $contenuto = $contenuto."
                \n <fieldset><legend>Valutazioni del conducente Nome C.</legend>
                                <h2>$nome $cognome - Conducente</h2>
                                <input type=\"hidden\" name=\"G\" value=\"$conducente\"></input>
                                <p>Compagnia</p>
                                <div class=\"votiGroup\">
                                <input type=\"radio\" name=\"CompagniaG\" id=\"gCompagnia1\" value=\"1\"></input><label  for=\"gCompagnia1\">1</label>
                                <input type=\"radio\" name=\"CompagniaG\" id=\"gCompagnia2\" value=\"2\"></input><label  for=\"gCompagnia2\">2</label>
                                <input type=\"radio\" name=\"CompagniaG\" id=\"gCompagnia3\" value=\"3\" tabindex=\"9\" checked=\"checked\"></input><label  for=\"gCompagnia3\">3</label>
                                <input type=\"radio\" name=\"CompagniaG\" id=\"gCompagnia4\" value=\"4\"></input><label  for=\"gCompagnia4\">4</label>
                                <input type=\"radio\" name=\"CompagniaG\" id=\"gCompagnia5\" value=\"5\"></input><label  for=\"gCompagnia5\">5</label>
                                </div>
                                <p>Puntualit&agrave;</p>
                                <div class=\"votiGroup\">
                                <input type=\"radio\" name=\"PuntualitaG\" id=\"gPuntualita1\" value=\"1\"></input><label  for=\"gPuntualita1\">1</label>
                                <input type=\"radio\" name=\"PuntualitaG\" id=\"gPuntualita2\" value=\"2\"></input><label  for=\"gPuntualita2\">2</label>
                                <input type=\"radio\" name=\"PuntualitaG\" id=\"gPuntualita3\" value=\"3\" tabindex=\"10\" checked=\"checked\"></input><label  for=\"gPuntualita3\">3</label>
                                <input type=\"radio\" name=\"PuntualitaG\" id=\"gPuntualita4\" value=\"4\"></input><label  for=\"gPuntualita4\">4</label>
                                <input type=\"radio\" name=\"PuntualitaG\" id=\"gPuntualita5\" value=\"5\"></input><label  for=\"gPuntualita5\">5</label>
                                </div>
                                <p>Guida</p>
                                <div class=\"votiGroup\">
                                <input type=\"radio\" name=\"Guida\" id=\"Guida1\" value=\"1\"></input><label  for=\"Guida1\">1</label>
                                <input type=\"radio\" name=\"Guida\" id=\"Guida2\" value=\"2\"></input><label  for=\"Guida2\">2</label>
                                <input type=\"radio\" name=\"Guida\" id=\"Guida3\" value=\"3\" tabindex=\"11\" checked=\"checked\"></input><label  for=\"Guida3\">3</label>
                                <input type=\"radio\" name=\"Guida\" id=\"Guida4\" value=\"4\"></input><label  for=\"Guida4\">4</label>
                                <input type=\"radio\" name=\"Guida\" id=\"Guida5\" value=\"5\"></input><label  for=\"Guida5\">5</label>
                                </div>
                                <p>Pulizia</p>
                                <div class=\"votiGroup\">
                                <input type=\"radio\" name=\"Pulizia\" id=\"Pulizia1\" value=\"1\"></input><label  for=\"Pulizia1\">1</label>
                                <input type=\"radio\" name=\"Pulizia\" id=\"Pulizia2\" value=\"2\"></input><label  for=\"Pulizia2\">2</label>
                                <input type=\"radio\" name=\"Pulizia\" id=\"Pulizia3\" value=\"3\" tabindex=\"12\" checked=\"checked\"></input><label  for=\"Pulizia3\">3</label>
                                <input type=\"radio\" name=\"Pulizia\" id=\"Pulizia4\" value=\"4\"></input><label  for=\"Pulizia4\">4</label>
                                <input type=\"radio\" name=\"Pulizia\" id=\"Pulizia5\" value=\"5\"></input><label  for=\"Pulizia5\">5</label>
                                </div>

                                <textarea rows=\"\" cols=\"\" name=\"commentoG\" tabindex=\"13\" title=\"Inserisci un commento facoltativo\">Commento facoltativo</textarea>

                                </fieldset>
                        ";
        }
        else {
            $contenuto = $contenuto."\n
                                <fieldset><legend>Valutazioni del passeggero Nome C.</legend>
                        <h2>$nome $cognome - Passeggero ($ind)</h2>
                        <input type=\"hidden\" name=\"P"."$ind\" value=\"$dest\"></input>
                        <p>Compagnia</p>
                        <div class=\"votiGroup\">
                        <input type=\"radio\" name=\"CompagniaP"."$ind\" id=\"p"."$ind"."Compagnia1\" value=\"1\"></input><label  for=\"p"."$ind"."Compagnia1\">1</label>
                        <input type=\"radio\" name=\"CompagniaP"."$ind\" id=\"p"."$ind"."Compagnia2\" value=\"2\"></input><label  for=\"p"."$ind"."Compagnia2\">2</label>
                        <input type=\"radio\" name=\"CompagniaP"."$ind\" id=\"p"."$ind"."Compagnia3\" value=\"3\"  checked=\"checked\"></input><label  for=\"p"."$ind"."Compagnia3\">3</label>
                        <input type=\"radio\" name=\"CompagniaP"."$ind\" id=\"p"."$ind"."Compagnia4\" value=\"4\"></input><label  for=\"p"."$ind"."Compagnia4\">4</label>
                        <input type=\"radio\" name=\"CompagniaP"."$ind\" id=\"p"."$ind"."Compagnia5\" value=\"5\"></input><label  for=\"p"."$ind"."Compagnia5\">5</label>
                        </div>
                        <p>Puntualit&agrave;</p>
                        <div class=\"votiGroup\">
                        <input type=\"radio\" name=\"PuntualitaP"."$ind\" id=\"p"."$ind"."Puntualita1\" value=\"1\"></input><label  for=\"p"."$ind"."Puntualita1\">1</label>
                        <input type=\"radio\" name=\"PuntualitaP"."$ind\" id=\"p"."$ind"."Puntualita2\" value=\"2\"></input><label  for=\"p"."$ind"."Puntualita2\">2</label>
                        <input type=\"radio\" name=\"PuntualitaP"."$ind\" id=\"p"."$ind"."Puntualita3\" value=\"3\" checked=\"checked\"></input><label  for=\"p"."$ind"."Puntualita3\">3</label>
                        <input type=\"radio\" name=\"PuntualitaP"."$ind\" id=\"p"."$ind"."Puntualita4\" value=\"4\"></input><label  for=\"p"."$ind"."Puntualita4\">4</label>
                        <input type=\"radio\" name=\"PuntualitaP"."$ind\" id=\"p"."$ind"."Puntualita5\" value=\"5\"></input><label  for=\"p"."$ind"."Puntualita5\">5</label>
                        </div>

                        <textarea rows=\"\" cols=\"\" name=\"commentoP1\" title=\"Inserisci un commento facoltativo\">Commento facoltativo</textarea>

                        </fieldset>
                        ";
            $ind++;
        }

    }

    # print "<div><input type=\"submit\" value=\"Invia\" tabindex=\"21\"></input></div> \n</form>";


    my $file = "../data/HTML_TEMPLATE/feedback.html";
    open my $fh, '<', $file;
    my $cont = research::query_notifiche_utente($username, $doc);
    my %hash_keys = (
        NOME_UTENTE => $username,
        CONTENUTO => $contenuto,
        PASSAGGIO => $passaggio,
        NUM_NOTIFICHE => @$cont[1]
        );
    my $template_parser = Template->new;
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio);
    print $foglio;
}
