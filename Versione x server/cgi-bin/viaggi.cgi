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
binmode(STDOUT, ":utf8");
use utf8;


my @s = sessione::creaSessione();
my $session = $s[0];
my $q=CGI->new;

if(!defined($session->param('username'))) {
    my %problems=(
        LOGIN_ERR => "Utente non loggato, pagina inaccessibile."
        );
    $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
else{
    print "Content-type: text/html\n\n";
    my $username=$session->param('username');

    my $doc=data_registration::get_xml_doc();

    my @viaggi_att_list = research::query_viaggi_attivi_utente($username, $doc);
    my $num_att= @viaggi_att_list;
    my $empty_att = "false"; # variabile che indica se ci sono viaggi attivi
    if($num_att == 0){
        $empty_att= "true"
    }

    my @viaggi_rec_list = research::query_viaggi_recensire_utente($username, $doc);
    my $num_rec= @viaggi_rec_list;
    my $empty_rec = "false"; # variabile che indica se ci sono viaggi da recensire
    if($num_rec == 0){
        $empty_rec= "true"
    }

    my $file = "../data/HTML_TEMPLATE/viaggi.html";
    my %hash_keys = (
        NOME_UTENTE => $username,
        VIAGGI_ATT_LIST => \@viaggi_att_list,
        EMPTY_ATTIVI => $empty_att,
        VIAGGI_REC_LIST => \@viaggi_rec_list,
        EMPTY_RECENSIRE => $empty_rec,
        NUM_NOTIFICHE => research::conta_notifiche($session->param('username'), $doc),
        INDEX => 9
        );
    my $template_parser = Template->new({ ENCODING => 'utf8' });
    open my $fh, '<:encoding(UTF-8)', $file;
    my $foglio = '';
    $template_parser->process($fh,\%hash_keys,\$foglio);
    print $foglio;

}
