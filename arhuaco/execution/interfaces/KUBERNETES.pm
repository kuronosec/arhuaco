package AliEn::LQ::KUBERNETES;

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
    $self->debug(1,"*** KUBERNETES.pm submit ***");

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
    # In this case, the POD definition for kubernetes.
    (my $submit = qq{
        apiVersion: v1
        kind: Pod
        metadata:
          name: alien-$containerID
        spec:
          containers:
          - name: alien-$containerID
            image: test:alien
            command: ['$command']
            volumeMounts:
                - name: data
                  mountPath: /var/lib/aliprod/.alien/tmp/agent.startup.$jobAgentID
                  readOnly: false
                - name: cvmfs
                  mountPath: /cvmfs/alice.cern.ch
            workingDir: /var/lib/aliprod/.alien/tmp
            env:
                - name: ALIEN_CM_AS_LDAP_PROXY
                  value: '$cm'
                - name: ALIEN_JOBAGENT_ID
                  value: '$$.$self->{COUNTER}'
                - name: ALIEN_ALICE_CM_AS_LDAP_PROXY
                  value: '$cm'
          volumes:
            - name: data
              hostPath:
                path: /var/lib/aliprod/.alien/tmp/agent.startup.$jobAgentID
            - name: cvmfs
              hostPath:
                path: /cvmfs/alice.cern.ch
          restartPolicy: Never
    }) =~ s/^ {8}//mg;

    # One more job to submit
    $self->{COUNTER}++;
    # Make the submittion and check for errors.
    eval {
        open( BATCH,"| $self->{SUBMIT_CMD}") or print  "Can't send batch command: $!" and return -2;
        $self->debug(1, "Submitting the command:\n$submit");
        print BATCH $submit;
        close BATCH or return -1;
        $error=0
    };
    if ($@) {
        $self->info("KUBERNETES submit command died - use debug to evaluate");
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
    $self->deleteCompletedPods();
    # Get the number ob jobs running by the number of PODS
    my $jobquery="kubectl get pods | grep Running | wc -l ";
    open(JOBS,"$jobquery |") or $self->info("error doing $jobquery");
    my $njobs=<JOBS>;
    close(JOBS);
    $njobs=~s/\n//;
    if($njobs < 0 ){
        $self->info("Error getting total number of jobs, unable to check Kubernetes queue");
        return undef;
    }
    return $njobs;
}

sub getNumberQueued{
    my $self = shift;
    $self->deleteCompletedPods();
    # Get the number of jobs qeued by the number of PODS
    my $jobquery="kubectl get pods | grep Pending | wc -l";
    open(JOBS,"$jobquery |") or $self->info("error doing $jobquery");
    my $njobs=<JOBS>;
    close(JOBS);
    $njobs=~s/\n//;
    if($njobs < 0 ){
        $self->info("Error getting number of queued jobs, unable to check kubernetes queue");
        return undef;
    }
    return $njobs;
}

sub deleteCompletedPods{
    my $self = shift;
    # Get the number of pods with exit status
    my @pods = `kubectl get pods -a | grep Completed | awk '{ print \$1 }'`;
    foreach my $pod (@pods) {
        my @result = system("kubectl delete pod $pod");
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

    $self->debug(1,"In KUBERNETES.pm initializex");

    # Create the necessary env variables.
    $ENV{'KUBERNETES_ROOT'}="/opt/kubernetes";
    $ENV{'KUBERNETES_CONTRIB'}="mesos";
    $ENV{'KUBERNETES_MASTER_IP'}="127.0.0.1";
    $ENV{'KUBERNETES_MASTER'}="http://$ENV{'KUBERNETES_MASTER_IP'}:8888";
    $ENV{'PATH'}="/opt/kubernetes/bin/linux/amd64/:$ENV{'PATH'}";
    $ENV{'MESOS_MASTER'}="127.0.0.1:5050";

    # // Create a pod using the data in pod.json.
    # $ kubectl create -f pod.json
    # // Create a pod based on the JSON passed into stdin.
    # $ cat pod.json | kubectl create -f -
    # https://cloud.google.com/container-engine/docs/kubectl/create
    $self->{SUBMIT_CMD} =  "kubectl create -f - ";

    # https://cloud.google.com/container-engine/docs/kubectl/delete
    $self->{KILL_CMD} = "kubectl delete pod";

    # https://cloud.google.com/container-engine/docs/kubectl/get
    $self->{STATUS_CMD} = "kubectl get pods";

    $self->{GET_QUEUE_STATUS}="$self->{STATUS_CMD}";
    if ( $self->{CONFIG}->{CE_STATUSARG} ) {
        $self->{GET_QUEUE_STATUS}.=" @{$self->{CONFIG}->{CE_STATUSARG_LIST}}"
    }

    $self->debug(1,"KUBERNETES intialize finished");
    return 1;
}

sub kill {
    my $self    = shift;
    my $queueId = shift;
    my ( $id, @rest ) = split ( ' ', `$self->{STATUS_CMD} | grep $queueId\$` );
    $id or $self->info("Command $queueId not found!!") and return -1;
    print STDERR "In KUBERNETES, killing process $queueId (id $id)\n";
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
