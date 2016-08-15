#!/usr/bin/perl
#use CGI::Cookie;             
 use CGI;                 
 use CGI::Session;                
 use CGI::Carp qw(fatalsToBrowser);                       
 my $cgi = new CGI;                       
 #$sid = $cgi->cookie('CGISESSID') || $cgi->param('CGISESSID') || undef;                                      
 my $session = new CGI::Session;#load CGI::Session(undef, $sid, {Directory=>'/tmp'});   
 $session->load();
 print "Content-type: text/html\n\n";
 print $session->param('username');


