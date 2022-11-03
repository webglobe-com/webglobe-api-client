#!/usr/bin/python

import urllib,requests,json
import sys, re, signal, os
import logging

from . import WebglobeAPI

def get_cert_cli():
    import getopt
    import sys
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:k:c:d:", ["username=","password=","keyout=","certout=","onchange=","domain=","cn="])
    except:
        logging.error(getopt.GetoptError)
        sys.exit(1)
    
    username = None
    password = None
    keyout = None
    certout = None
    onchange = None
    domain = None
    cn = None
    callback_login = False
    
    for opt, arg in opts:
        if opt in ('-u','--username'):
            username = arg
        elif opt in ('-p','--password'):
            password = arg
        elif opt in ('-k','--keyout'):
            keyout = arg
        elif opt in ('-c','--certout'):
            certout = arg
        elif opt in ('-d','--domain'):
            domain = arg
        elif opt in ('--cn'):
            cn = arg
        elif opt in ('--onchange',):
            onchange = arg
        else:
            raise ValueError('Invalid opt %s %s' % (opt,arg))
    
    api = WebglobeAPI('https://api.webglobe.com')
    
    api.login(username,password)
    try:
        domain = list(filter(lambda item: item[1] == domain, api.domains().items()))[0][0]
    except:
        raise
    cert_list = api.get('{domain}/ssl'.format(domain=domain))['ssls']
    if cn is not None:
        # get certificate by cn
        cert = list(filter(lambda item: item['domain_name'] == cn, cert_list))[0]
    else:
        # get certificate with shortest cn
        cert = list(sorted(cert_list, key=lambda item: len(item['domain_name'])))[0]
    
    if cert['crt'][-1] != '\n':
        cert['crt'] = cert['crt'] + '\n'
    if cert['chain'][-1] != '\n':
        cert['chain'] = cert['chain'] + '\n'
    if cert['key'][-1] != '\n':
        cert['key'] = cert['key'] + '\n'
    changed = True

    if os.path.exists(keyout) and os.path.exists(certout):
        if keyout != certout:
            if open(certout).read().strip() == (cert['crt']+cert['chain']).strip() and open(keyout).read().strip() == cert['key'].strip():
                changed = False
        else:
            if open(keyout).read().strip() ==  (cert['crt'] + cert['chain'] + cert['key']).strip():
                changed = False 
    if changed:
        if keyout != certout:
            fh = open(certout,'w')
            fh.write(cert['crt'])
            fh.write(cert['chain'])
            fh.close()
            fh = open(keyout,'w')
            fh.write(cert['key'])
            fh.close()
        else:
            fh = open(keyout,'w')
            fh.write(cert['crt'])
            fh.write(cert['chain'])
            fh.write(cert['key'])
            fh.close()
        if onchange != None:
            import subprocess
            subprocess.check_call(onchange,shell=True)
    
        