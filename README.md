# python-cert-exp-check

Check expiration dates of certificates.

## Explanation

  - This is a Python3 script that checks a provided list of `host:port` combinations for expired SSL/TLS certificates.
  - I use this in my homelab to check expiration for certificates generated with the [Smallstep CA](https://smallstep.com/certificates/).

## Requirements

  - Setup a Python virtual environment
  - Edit the file called `hosts.txt` to include a list of `host:port` combinations, one per line.

### Example usage

Below is an example of how to clone the repo and run the script.
```
git clone https://github.com/loganmarchione/python-cert-exp-check.git
cd python-cert-exp-check
python3 -m venv env
source env/bin/activate 
pip3 install -r requirements.txt
# Edit the hosts.txt file
python3 certcheck.py
deactivate
```

Below is the output generated.
```
+------------+------+---------------------+------------------+
| Host       | Port | Expiration date     | Day(s) remaining |
+------------+------+---------------------+------------------+
| google.com | 443  | 2021-01-20 16:18:36 | 68               |
| 1.1.1.1    | 443  | 2021-02-01 12:00:00 | 79               |
| github.com | 443  | 2022-05-10 12:00:00 | 542              |
+------------+------+---------------------+------------------+
```

## TODO
- [ ] Build Flask app to show results on a web page
- [ ] Add argument for to specify input file
- [ ] Add the ability to check a local directory for crt/key files