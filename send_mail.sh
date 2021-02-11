mkdir -f "$HOME/email"
/jes/dsee6/dsrk6/bin/ldapsearch -h p4033-adm -p 3636 -Z -P /jes/dsee6/slapd-cert8.db -D "cn=directory manager" -w - -b "ou=system accounts,dc=cms,dc=hhs,dc=gov" -s sub uid=* pwdchangedtime pwdPolicySubentry uid cn sn nsaccountlock mail nsaccountlock pwdExpirationWarned passwordexpirationtime > $HOME/email/customer_records.ldif
sleep 300
python $HOME/email/main.py -fp $HOME/email/customer_records.ldif
rm -rf $HOME/email/customer_records.ldif
