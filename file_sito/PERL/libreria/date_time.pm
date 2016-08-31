#! /usr/bin/perl

package date_time;
use strict;
use warnings;
use Time::Local;

sub valida_data {
  my $day = shift @_;
  my $month = shift @_;
  my $year = shift @_;
  if(eval{ timelocal(0,0,0,$day, $month-1, $year); 1;}){
    return 1;
  }
  else{
    return 0;
  }
}

sub confronto_dataora {
  #data precedente
  my $din  = shift @_;
  my $min  = shift @_;
  my $yin  = shift @_;
  #
  my $hourin  = shift @_;
  my $minutein = shift @_;
  #data sucessiva
  my $dfi  = shift @_;
  my $mfi  = shift @_;
  my $yfi  = shift @_;
  #
  my $hourfi  = shift @_;
  my $minutefi = shift @_;
  my $epoch_in = timelocal(0, $minutein, $hourin, $din, $min, $yin);
  my $epoch_fi = timelocal(0, $minutefi, $hourfi, $dfi, $mfi, $yfi);
  if($epoch_fi<$epoch_in) {
    return 0;
  }
  else {
    return 1;
  }
}

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

  my $epoch_in = timelocal(0, $minutein, $hourin, $din, $min -1, $yin);
  my $epoch_fi = timelocal(0, $minutefi, $hourfi, $dfi, $mfi -1, $yfi);
  my $aux = ($epoch_fi - $epoch_in)/($n * 60);
  my $intervallo = ($epoch_fi - $epoch_in)/$n;
  my @ans;
  for(my $i=0;$i <$n ;$i++){
    my $date_aux = $epoch_in + ($intervallo*$i);
    #push @ans, scalar localtime($date_aux);
    my ($sec, $min, $hour, $day,$month,$year) = (localtime($date_aux))[0,1,2,3,4,5];
    $month = $month + 1;
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
