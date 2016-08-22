#! /usr/bin/perl

package date_time;
use strict;
use warnings;
use Time::Local;

sub calcola_tappe {
  #data partenza
  my $din  = shift @_;
  my $min  = shift @_;
  my $yin  = shift @_;
  #
  my $hourin  = shift @_;
  my $minutein = shift @_;
  #data arrivo
  my $dfi  = shift @_;
  my $mfi  = shift @_;
  my $yfi  = shift @_;
  #
  my $hourfi  = shift @_;
  my $minutefi = shift @_;
  #numero di tappe
  my $n = shift @_;
  #########################################
  #my $dateObjin = DateTime->new(year => $yin, month => $min, day => $din,
  #                              hour => $hourin, minute => $minutein);
  #my $epoch_in = $dateObjin->epoch;
  #my $dateObjfi = DateTime->new(year => $yfi, month => $mfi, day => $dfi,
  #                              hour => $hourfi, mfiute => $mfiutefi);
  #my $epoch_fi = $dateObjfi->epoch;
  my $epoch_in = timelocal(0, $minutein, $hourin, $din, $min, $yin);
  my $epoch_fi = timelocal(0, $minutefi, $hourfi, $dfi, $mfi, $yfi);
  my $aux = ($epoch_fi - $epoch_in)/($n * 60);
  my $intervallo = ($epoch_fi - $epoch_in)/$n;
  my @ans;
  for(my $i=0;$i <$n ;$i++){
    my $date_aux = $epoch_in + ($intervallo*$i);
    #push @ans, scalar localtime($date_aux);
    my ($sec, $min, $hour, $day,$month,$year) = (localtime($date_aux))[0,1,2,3,4,5];
    if(length($sec)==1){
      $sec = join '', '0', $sec;
    }
    if(length($min)==1){
      $min = join '', '0', $min;
    }
    if(length($hour)==1){
      $hour = join '', '0', $hour;
    }
    if(length($day)==1){
      $day = join '', '0', $day;
    }
    if(length($month)==1){
      $month = join '', '0', $month;
    }
    push @ans, ($year+1900)."\-$month\-$day $hour\:$min\:$sec";
  }
  return @ans;
}


1;
