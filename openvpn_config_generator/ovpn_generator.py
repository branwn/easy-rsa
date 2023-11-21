'''

This is a script that will generate the .ovpn files from a .ovpn template file;
it will read the template.ovpn file in the current directory and insert certificates and keys into it.

the certificates are read from '../easy-rsa/easyrsa3/pki/issued'
    with names in regex pattern like r'^client.*\.crt';
correspondingly, the keys are read from the '../easy-rsa/easyrsa3/pki/private'
    with the same name as cert but in different extension name, that is in regex pattern like r'^client.*\.key';

then, insert the certificate surrounded by <cert> and </cert>,
    and the key surrounded by <key> and </key> into the template.ovpn file,
    save as a new .ovpn file with the same name in the directory ./ovpns/

'''
import os
import re

def insert_cert_and_key(template_path, certs_dir, keys_dir, output_dir):
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    for cert_filename in os.listdir(certs_dir):
        if re.match(r'^client.*\.crt$', cert_filename):
            with open(os.path.join(certs_dir, cert_filename), 'r') as cert_file:
                cert_content = cert_file.read()
            key_filename = cert_filename.replace('.crt', '.key')
            with open(os.path.join(keys_dir, key_filename), 'r') as key_file:
                key_content = key_file.read()

            ovpn_content = template_content + '\n<cert>\n' + cert_content + '\n</cert>\n' + '<key>\n' + key_content + '\n</key>\n'

            output_filename = cert_filename.replace('.crt', '.ovpn')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(os.path.join(output_dir, output_filename), 'w') as output_file:
                output_file.write(ovpn_content)

if __name__ == '__main__':
    TEMPLATE_PATH = 'template.ovpn'
    CERTS_DIR = '../easyrsa3/pki/issued'
    KEYS_DIR = '../easyrsa3/pki/private'
    OUTPUT_DIR = './ovpns/'
    insert_cert_and_key(TEMPLATE_PATH, CERTS_DIR, KEYS_DIR, OUTPUT_DIR)
