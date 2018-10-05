ACRONYM - A Cool Red-Operative Network Yeeting Multitool

ACRONYM is an open-source offensive security tool meant for Red-Team operations whose engagement
parameters include the deployment of networked malware. The goal of ACRONYM is to enable efficient
code reuse, so that parts of malware do not neccessarily have to be rebuilt from scratch in the
event that malware samples are discovered by the Blue-Team, and also allows Red-Teams to create
several differing malware samples at once, but reuse certain parts of the code. For example, if
a Red Team desires to deploy two strains of malware which perform different actions but use the
same command and control scheme, the command and control scheme can be written as a component
and easily plugged into any number of samples.

To accomplish this, ACRONYM offers a package-management system where template source-code can be
plugged in to editable samples. When all desired components of a sample have been plugged in and
configured, the sample can be "built," producing real source code for the malware sample, which
can be further edited if desired before being compiled and deployed.

ACRONYM is not meant to be used for nefarious or illegal purposes such as data theft or destruction
and is intended only for legal offensive security operations or educational purposes. To this end,
ACRONYM is intended to difficult for script-kiddies to use and understand, as it requires the user
to be capable of producing functional malware samples from components. ACRONYM also does not supply
means of deploying malware onto inaccessible networks or machines, and is intended for post-exploit
use, i.e ACRONYM will not get you access to a network, but is useful for creating samples that may
be deployed onto a network that you have or will gain access to.


V1.0 target date August 8