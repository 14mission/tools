package matchmetree;
use strict;
use warnings;
use Text::CSV;

package readtsv;

sub new {
  my $class = shift;
  my $fn = shift;
  my $self = { fn=>$fn, fh=>undef, csv=>0, robust=>0 };
  bless($self, ref($class) || $class);
  my %name2pat = @_;
  foreach my $name (keys %name2pat) { $name2pat{$name} ||= "^$name"; }

  if($name2pat{dbgmsg}) {
    print STDERR "$name2pat{dbgmsg}\n";
    delete $name2pat{dbgmsg};
  }

  $self->{csv} = $self->{fn} =~ m/\.csv$/;
  
  my $fh;
  open($fh,$self->{fn}) || die "can't read $$self{fn}";
  binmode $fh, ":utf8";
  $self->{fh} = $fh;
  my $ln = <$fh>;
  $self->{csv} ||= ($ln !~ m/\t| / && $ln =~ m/,/);
  my @cols = 
    $self->{csv} ? csvsplit($ln) :
    $ln =~ m/\t/ ? split(/\t/,$ln) :
    split(/\s+/,$ln);
  $cols[0] =~ s/^\x{feff}//;
  $cols[-1] =~ s/\s+$//gs;
  $self->{colmap} = [ map undef, @cols ];
  #die "$$self{fn} doesn't start with #" unless $cols[0] =~ s/^#// || $ln eq uc($ln);
  $cols[0] =~ s/^#//;
  for( my $colnum = 0; $colnum < @cols; ++$colnum ) {
    foreach my $colname ( sort keys %name2pat ) { 
      if( $cols[$colnum] =~ m/$name2pat{$colname}/ ) {
        $self->{colmap}->[$colnum] = $colname;
        print STDERR "col $colnum \"$cols[$colnum]\" =~ m/$name2pat{$colname}/ -> $colname\n";
        delete $name2pat{$colname};
      }
    }
  }
  die "found no $_ col: #".join('\t',@cols) foreach ( sort keys %name2pat );
  return $self;
};

sub getln {
  my $self = shift;
  my $fh = $self->{fh};
  my $ln = <$fh> || return undef;
  my @cols = $self->{csv} ? csvsplit($ln) : split(/\t/, $ln);
  $cols[-1] =~ s/\s+$//gs;
  if(@cols != @{$self->{colmap}}) { 
    my $msg = "reading $$self{fn}: expected ".scalar(@{$self->{colmap}})." cols, only ".scalar(@cols)." in $.. @cols";
    if($self->{robust}) {warn "warning: $msg";} else {die $msg}
  }
  my $vals = { fileline => join('\t',@cols) };
  for( my $colnum = 0; $colnum < @{$self->{colmap}}; ++$colnum ) {
    if( $self->{colmap}->[$colnum] && $self->{colmap}->[$colnum] < @cols) {
      $vals->{$self->{colmap}->[$colnum]} = $cols[$colnum];
    }
  }
  return $vals;
}

sub DESTROY {
  my $self = shift;
  print STDERR "close ",$self->{fn},"\n";
  close($self->{fh});
}

sub writetsv {
  my($fn,$msg,$cols,$data) = @_;
  print STDERR "$msg\n";
  open(O,">$fn") || die "can't write $fn";
  binmode O, ":utf8";
  print O "#".join("\t",@$cols)."\n";
  foreach my $row (@$data) {
    print O join("\t",map {
      die "no $_ in ".join(",",map "$_=$$row{$_}", sort keys %$row)
        if !defined $row->{$_};
      $row->{$_}
    } @$cols),"\n";
  }
  close O;
}

sub csvsplit {
    my $line = shift;
    my $sep = ',';

    my $csv = Text::CSV->new({ sep_char => $sep });
    if ($csv->parse($line)) {
        return $csv->fields();
    } else {
        die "can't parse csv line: $line";
    }
}

return 1;
