Linux CIS - Supports SLES12, openSUSE42.3
================
Based on the exellent work done by the MindPointGroup [Ansible Role](https://img.shields.io/ansible/role/16089.svg)](https://galaxy.ansible.com/MindPointGroup/RHEL7-CIS/)

Configure SLES12/OpenSUSE42.3 machine to be [CIS](https://www.cisecurity.org/cis-benchmarks/) compliant. Level 1 and 2 findings will be corrected by default.


## Warning on use

This role **will make changes to the system** that could break things. This is not an auditing tool but rather a remediation tool to be used after an audit has been conducted.

## IMPORTANT INSTALL STEP

If you want to install this via the `ansible-galaxy` command you'll need to run it like this:

`ansible-galaxy install -p roles -r requirements.yml`

With this in the file requirements.yml:

```
- src: https://github.com/schubergphilis/SLES12-CIS.git
```

Based on [ CIS SUSE Linux Enterprise 12 Benchmark v2.0.0 - 12-07-2016 ](https://community.cisecurity.org/collab/public/index.php).

This repo originated from work done by [Sam Doran](https://github.com/samdoran/ansible-role-stig)

Requirements
------------

You should carefully read through the tasks to make sure these changes will not break your systems before running this playbook.
If you want to do a dry run without changing anything, set the below sections (sles12cis_section1-6) to false. 

Role Variables
--------------
There are many role variables defined in defaults/main.yml. This list shows the most important.

**sles12cis_notauto**: Run CIS checks that we typically do NOT want to automate due to the high probability of breaking the system (Default: false)

**sles12cis_section1**: CIS - General Settings (Section 1) (Default: true)

**sles12cis_section2**: CIS - Services settings (Section 2) (Default: true)

**sles12cis_section3**: CIS - Network settings (Section 3) (Default: true)

**sles12cis_section4**: CIS - Logging and Auditing settings (Section 4) (Default: true)

**sles12cis_section5**: CIS - Access, Authentication and Authorization settings (Section 5) (Default: true)

**sles12cis_section6**: CIS - System Maintenance settings (Section 6) (Default: true)  

##### Disable all selinux functions
`sles12cis_selinux_disable: false`

##### Service variables:
###### These control whether a server should or should not be allowed to continue to run these services

```
sles12cis_avahi_server: false  
sles12cis_cups_server: false  
sles12cis_dhcp_server: false  
sles12cis_ldap_server: false  
sles12cis_telnet_server: false  
sles12cis_nfs_server: false  
sles12cis_rpc_server: false  
sles12cis_ntalk_server: false  
sles12cis_rsyncd_server: false  
sles12cis_tftp_server: false  
sles12cis_rsh_server: false  
sles12cis_nis_server: false  
sles12cis_snmp_server: false  
sles12cis_squid_server: false  
sles12cis_smb_server: false  
sles12cis_dovecot_server: false  
sles12cis_httpd_server: false  
sles12cis_vsftpd_server: false  
sles12cis_named_server: false  
sles12cis_bind: false  
sles12cis_vsftpd: false  
sles12cis_httpd: false  
sles12cis_dovecot: false  
sles12cis_samba: false  
sles12cis_squid: false  
sles12cis_net_snmp: false  
```  

##### Designate server as a Mail server
`sles12cis_is_mail_server: false`


##### System network parameters (host only OR host and router)
`sles12cis_is_router: false`  


##### IPv6 required
`sles12cis_ipv6_required: true`  


##### AIDE
`sles12cis_config_aide: true`

###### AIDE cron settings
```
sles12cis_aide_cron:
  cron_user: root
  cron_file: /etc/crontab
  aide_job: '/usr/sbin/aide --check'
  aide_minute: 0
  aide_hour: 5
  aide_day: '*'
  aide_month: '*'
  aide_weekday: '*'  
```

##### SELinux policy
`sles12cis_selinux_pol: targeted` 


##### Set to 'true' if X Windows is needed in your environment
`sles12cis_xwindows_required: no` 


##### Client application requirements
```
sles12cis_openldap_clients_required: false 
sles12cis_telnet_required: false 
sles12cis_talk_required: false  
sles12cis_rsh_required: false 
sles12cis_ypbind_required: false 
```

##### Time Synchronization
```
sles12cis_time_synchronization: chrony
sles12cis_time_Synchronization: ntp

sles12cis_time_synchronization_servers:
    - 0.pool.ntp.org
    - 1.pool.ntp.org
    - 2.pool.ntp.org
    - 3.pool.ntp.org  
```  
  
##### 3.4.2 | PATCH | Ensure /etc/hosts.allow is configured
```
sles12cis_host_allow:
  - "10.0.0.0/255.0.0.0"  
  - "172.16.0.0/255.240.0.0"  
  - "192.168.0.0/255.255.0.0"    
```  

```
sles12cis_firewall: firewalld
sles12cis_firewall: iptables
``` 
  

Dependencies
------------

Ansible > 2.5

Example Playbook
-------------------------

This sample playbook should be run in a folder that is above the main SLES12-CIS / SLES12-CIS-devel folder.

```
- name: Harden Server
  hosts: servers
  become: yes

  roles:
    - SLES12-CIS
```

Tags
----
Many tags are available for precise control of what is and is not changed.

Some examples of using tags:

```
    # Audit and patch the site
    ansible-playbook site.yml --tags="patch"
```

License
-------

MIT
