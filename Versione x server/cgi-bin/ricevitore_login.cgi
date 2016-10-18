#!/usr/bin/perl
#print "Content-type: text/html\n\n";

use strict;
use warnings;
use diagnostics;
use CGI ;
use CGI::Session qw/-ip-match/;
#use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::data_registration;
#use lib "libreria";
use libreria::sessione;

my $cgi = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];

if(defined($session->param('loggedin'))) {
    print $session->header(-location => "home.cgi");
}
elsif (defined($session->param('nuova_regis'))) {
    my $aux = $session->param('nuova_regis');
    my %ute = %$aux;
    $session->param('username',$ute{'Username'});
    $session->param('loggedin','yes');
    $session->flush();
    $session->clear(['nuova_regis']);
    print $session->header(-location => "confermaRegistrazione.cgi");
}
else {
    my $doc = data_registration::get_xml_doc();;
    my $username=$cgi->param('username');
    my $psw=$cgi->param('password');
    my @ute = $doc->findnodes("//SetUtenti/Utente[Username='$username' and Password='$psw']");
    my $n = @ute;
    if($n == 0) {
        my %problems = (
            LOGIN_ERR => "Combinazione username/password non corretta."
            );
        my %old_input = (
            USERNAME => $username,
            PASSWORD => $psw
            );
        $session->param('problems',\%problems);
        $session->param('old_input',\%old_input);
        #print $cgi->redirect('http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/accedi.cgi');
        print $session->header(-location => "login.cgi");
    }
    else {
        #my $sid = $cgi->cookie("CGISESSID") || undef;

        $session->param('username',$username);
        $session->param('loggedin','yes');
        $session->expires("+2h"); # *** AGGIUNTA ***
        $session->flush();
        print $session->header(-location => "home.cgi");
        #print $cgi->redirect('http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/home.cgi');
    }
}
