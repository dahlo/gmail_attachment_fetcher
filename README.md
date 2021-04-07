# What
A script to fetch attachments from gmail emails. Requires imap enabled.

# How
```bash
python3 gmail_attachment_fetcher.py <config file> <output dir>
```

# TODO
* Requires the user to activate support for unsecure apps, or adding a "app password" if you are using 2fa, possible to work around it with oauth2 (https://stackoverflow.com/questions/5193707/use-imaplib-and-oauth-for-connection-with-gmail). No time to figure out the tokens etc right now.
