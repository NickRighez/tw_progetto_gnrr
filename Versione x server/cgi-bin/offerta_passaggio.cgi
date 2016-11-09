#! /usr/bin/perl -w
use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use Template;
use libreria::sessione;
use libreria::data_registration;
use libreria::research;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";
use utf8;


my $cgi = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];
my $doc = data_registration::get_xml_doc();

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Devi effettuare l'accesso per poter offrire un passaggio."
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
elsif (!($doc->exists("//SetUtenti/Utente[Username='".$session->param('username')."']/Profilo/Preferenze"))) {
    my %problems=(
        INFO_CONDUC_ERR => "Per offrire un passaggio devi inserire le informazioni per Auto, Patente e Preferenze nel profilo personale."
    );
    $session->param('problems',\%problems);
    print $session->header(-location => "modificaProfilo.cgi");
}
else {
    my $file = "../data/HTML_TEMPLATE/offri.html";
    my %hash_keys = ( NOME_UTENTE => $session->param('username'));

    if(defined($session->param('problems'))) {
        my $prob = $session->param('problems');
        my %prob_hash = %$prob;
        while( my( $key, $value ) = each %prob_hash ){
            $hash_keys{$key}="$value";
        }
    }

    if(defined($session->param('old_input'))) {
        my $old = $session->param('old_input');
        my %old_hash = %$old;
        while( my( $key, $value ) = each %old_hash ){
            $hash_keys{$key}="$value";
        }
    }

    $hash_keys{NUM_NOTIFICHE} = research::conta_notifiche($session->param('username'), $doc);
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    my $foglio = '';
    open my $fh, '<:encoding(UTF-8)', $file;
    $template_parser->process($fh,\%hash_keys,\$foglio);
 print "Content-Type: text/html; charset=UTF-8\n\n\n";
    print $foglio;


    if(defined($session->param('problems'))) {
        $session->clear(['problems']);
    }
    if(defined($session->param('old_input'))) {
        $session->clear(['old_input']);
    }
}
