package AliEn::LQ::DOCKER;

# This is an array for
# the parent classes.
@ISA = qw( AliEn::LQ );

use AliEn::LQ;
use AliEn::X509;
use AliEn::TMPFile;
use Data::Dumper;
use POSIX;
use strict;

sub submit {
    my $self = shift;
    my $classad=shift;
    my ( $command, @args ) = @_;

    my $arglist = join " ", @args;
    $self->debug(1,"*** DOCKER.pm submit ***");

    my $error=-2;
    # Open file
    local $SIG{PIPE} =sub {
        $self->info("Error submitting the job: sig pipe received!\n");
        $error=-1;
    };
    $self->{X509} or $self->{X509}=AliEn::X509->new();
    $self->{X509}->checkProxy();
    # Number of jobs submited
    $self->{COUNTER} or $self->{COUNTER}=0;
    my $cm="$self->{CONFIG}->{HOST}:$self->{CONFIG}->{CLUSTERMONITOR_PORT}";

    $self->debug(1,"new status command it $self->{STATUS_CMD} \n");

    #--> define temporary files for log, out & err
    my $n=AliEn::TMPFile->new({ttl=>'24 hours', base_dir=>$self->{PATH},filename=>$ENV{ALIEN_LOG}} );
    my $jobAgentID = $$;
    my $containerID = sprintf("%d", $$.$self->{COUNTER});
    
    # This is the real paramters for the batch system.
    # In this case, the parameters for Docker.

    my $docker_submit = " --restart-condition none --restart-max-attempts 0 ".
                        " --name alien-$containerID ".
                        " --mount type=bind,source='/var/lib/aliprod/.alien/tmp/agent.startup.$jobAgentID'".
                        ",target='/var/lib/aliprod/.alien/tmp/agent.startup.$jobAgentID' ".
                        " --mount type=bind,source='/cvmfs/alice.cern.ch'".
                        ",target='/cvmfs/alice.cern.ch'".
                        " --workdir '/var/lib/aliprod/.alien/tmp' ".
                        " --env ALIEN_CM_AS_LDAP_PROXY=$cm ".
                        " --env ALIEN_JOBAGENT_ID=$$.$self->{COUNTER} ".
                        " --env ALIEN_ALICE_CM_AS_LDAP_PROXY=$cm ".
                        " --network ufnet ".
                        " test:alien $command ";

    # One more job to submit
    $self->{COUNTER}++;
    # Make the submittion and check for errors.
    eval {
        open( BATCH,"| $self->{SUBMIT_CMD} $docker_submit") or print  "Can't send batch command: $!" and return -2;
        $self->debug(1, "Submitting the command:\n$docker_submit");
        close BATCH or return -1;
        $error=0
    };
    if ($@) {
        $self->info("DOCKER submit command died - use debug to evaluate");
        return -2;
    }

    return $error;
}

# Usually, we only want the jobs that have something like 'alien'
# or 'agent' in their names (in case the same user is submitting
# some other jobs)
sub _filterOwnJobs {
    my $self     = shift;
    my @queueids = ();
    my $rcount=0;
    foreach (@_) {
        if($_ =~ /undefined/) {
            next;
        }
        if($_ =~ /HoldReason/) {
            next;
        }
        if(($_ =~ /((alien)|(agent.startup))/i)) {
            $rcount++;
            my ($i1,$i2) = split /\ /,$_,2;
            $i1=~s/^\s*//;
            push @queueids, $i1;
        }
    }
    return @queueids;
}

sub getNumberRunning{
    my $self = shift;
    $self->deleteCompletedContainers();
    # Get the number ob jobs running by the number of PODS
    my $jobquery= "$self->{STATUS_CMD} | grep alien | awk '{print \$2}'".
                  " | while read p; do docker service tasks \$p --all; done ".
                  " | grep Running | wc -l";
    open(JOBS,"$jobquery |") or $self->info("error doing $jobquery");
    my $njobs=<JOBS>;
    close(JOBS);
    $njobs=~s/\n//;
    if($njobs < 0 ){
        $self->info("Error getting total number of jobs, unable to check DOCKER queue");
        return undef;
    }
    return $njobs;
}

sub getNumberQueued{
    my $self = shift;
    $self->deleteCompletedContainers();
    # Get the number of jobs qeued by the number of PODS
    my $jobquery= "$self->{STATUS_CMD} | grep alien | awk '{print \$2}'".
                  " | while read p; do docker service tasks \$p --all; done ".
                  " | grep Created | wc -l";
    open(JOBS,"$jobquery |") or $self->info("error doing $jobquery");
    my $njobs=<JOBS>;
    close(JOBS);
    $njobs=~s/\n//;
    if($njobs < 0 ){
        $self->info("Error getting number of queued jobs, unable to check DOCKER queue");
        return undef;
    }
    return $njobs;
}

sub deleteCompletedContainers{
    my $self = shift;
    # Get the number of pods with exit status
    my $jobquery= "$self->{STATUS_CMD} | grep alien | awk '{print \$2}'".
                  " | while read p; do docker service ps \$p; done ".
                  " | grep Complete | awk '{print \$3}' ";
    my @containers = `$jobquery`;
    foreach my $container (@containers) {
        my @result = system("$self->{KILL_CMD} $container");
    }
}

sub getStatus {
    return 'QUEUED';
}

# Tell the script what are the real batch system
# commands.
sub initialize() {
    my $self = shift;

    $self->{PATH} = $self->{CONFIG}->{LOG_DIR};
    $self->{X509}=AliEn::X509->new();

    $self->debug(1,"In DOCKER.pm initialize");

    # https://docs.docker.com/engine/reference/commandline/service_create/
    $self->{SUBMIT_CMD} =  "docker service create";

    # https://docs.docker.com/engine/reference/commandline/service_rm/
    $self->{KILL_CMD} = "docker service rm";

    # https://docs.docker.com/engine/reference/commandline/service_ls/
    $self->{STATUS_CMD} = "docker service ls";

    $self->{GET_QUEUE_STATUS}="$self->{STATUS_CMD}";
    if ( $self->{CONFIG}->{CE_STATUSARG} ) {
        $self->{GET_QUEUE_STATUS}.=" @{$self->{CONFIG}->{CE_STATUSARG_LIST}}"
    }

    $self->debug(1,"DOCKER intialize finished");
    return 1;
}

sub kill {
    my $self    = shift;
    my $queueId = shift;
    my ( $id, @rest ) = split ( ' ', `$self->{STATUS_CMD} | grep $queueId\$` );
    $id or $self->info("Command $queueId not found!!") and return -1;
    print STDERR "In DOCKER, killing process $queueId (id $id)\n";
    return ( system(" $self->{KILL_CMD} $id") );
}

sub removeKilledProcesses{
    my $self=shift;
    my @jobs=();

    foreach my $line (@_) {
        my ($id, $user, $date, $time, $cpu, $status, $rest)=split (/\s+/, $line);
        ($status  and  ($status eq "X"))
        or  push @jobs, $line;
    }
    return @jobs;
}

return 1;
