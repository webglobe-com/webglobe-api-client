#!/usr/bin/python

def get_cert_cli():
    from . import WebglobeAPI
    from argparse import ArgumentParser
    import os

    parser = ArgumentParser()
    parser.add_argument('-u', '--username', required=True)
    parser.add_argument('-p', '--password', required=True)
    parser.add_argument('-c', '--certout', required=True)
    parser.add_argument('-k', '--keyout', required=True)
    parser.add_argument('-d', '--domain', required=True)
    parser.add_argument('--cn')
    parser.add_argument(('--onchange'))

    args = parser.parse_args()
    
    api = WebglobeAPI('https://api.webglobe.com')
    
    api.login(args.username,args.password)
    try:
        domain = list(filter(lambda item: item[1] == args.domain, api.domains().items()))[0][0]
    except:
        raise
    cert_list = api.get('{domain}/ssl'.format(domain=domain))['ssls']
    if args.cn is not None:
        # get certificate by cn
        cert = list(filter(lambda item: item['domain_name'] == args.cn, cert_list))[0]
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

    if os.path.exists(args.keyout) and os.path.exists(args.certout):
        if args.keyout != args.certout:
            if open(args.certout).read().strip() == (cert['crt']+cert['chain']).strip() and open(args.keyout).read().strip() == cert['key'].strip():
                changed = False
        else:
            if open(args.keyout).read().strip() ==  (cert['crt'] + cert['chain'] + cert['key']).strip():
                changed = False 
    if changed:
        if args.keyout != args.certout:
            fh = open(args.certout,'w')
            fh.write(cert['crt'])
            fh.write(cert['chain'])
            fh.close()
            fh = open(args.keyout,'w')
            fh.write(cert['key'])
            fh.close()
        else:
            fh = open(args.keyout,'w')
            fh.write(cert['crt'])
            fh.write(cert['chain'])
            fh.write(cert['key'])
            fh.close()
        if args.onchange != None:
            import subprocess
            subprocess.check_call(args.onchange,shell=True)
    
        