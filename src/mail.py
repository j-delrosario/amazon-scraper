import smtplib
import json

accounts_path = './data/accounts.json'


def get_target_account(email):
    target_account = None
    with open(accounts_path, "r+") as f:
        accounts = json.load(f)
        for account in accounts:
            if account["email"] == email:
                target_account = account
                break
        if target_account == None:
            accounts.append({'email': email, 'notified_products_urls': []})
            f.seek(0)
            json.dump(accounts, f)
            f.truncate()
            target_account = accounts[-1]

    return target_account


def update_accounts_json(email, urls):
    with open(accounts_path, "r+") as f:
        accounts = json.load(f)
        for account in accounts:
            if account["email"] == email:
                account["notified_products_urls"] = account["notified_products_urls"] + urls
                break
        f.seek(0)
        json.dump(accounts, f)
        f.truncate()


def update_urls_to_send(urls_to_send, urls, target_account):
    for url in urls:
        if url not in target_account['notified_products_urls']:
            urls_to_send.append(url)


def send_mail(urls, email):
    urls_to_send = []
    target_account = get_target_account(email)
    update_urls_to_send(urls_to_send, urls, target_account)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('originjdel@gmail.com', 'oqyriwifawroqvvv')
    subject = 'price fell down'
    body = 'check the amazon links:' + " ".join(urls_to_send)

    msg = f"Subject: {subject}\n\n{body}"

    if len(urls_to_send) > 0:
        server.sendmail(
            'originjdel@gmail.com',
            email,
            msg
        )
        update_accounts_json(email, urls_to_send)

    print(f'Hey, {len(urls_to_send)} emails have been sent')

    server.quit()
