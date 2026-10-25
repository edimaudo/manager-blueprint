"""Create four Supabase demo accounts with randomized credentials. Run once in a trusted environment."""
import os, secrets, string, httpx
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
url=os.environ['SUPABASE_URL'].rstrip('/')
key=os.environ['SUPABASE_SERVICE_ROLE_KEY']
if os.getenv('DEMO_ACCOUNTS_ENABLED','false').lower()!='true': raise SystemExit('Set DEMO_ACCOUNTS_ENABLED=true explicitly before seeding demo users.')
users=[('demo-free@managerblueprint.local','user','free'),('demo-plus@managerblueprint.local','user','plus'),('demo-pro@managerblueprint.local','user','pro'),('demo-admin@managerblueprint.local','admin','pro')]
alphabet=string.ascii_letters+string.digits+'!@#$%_-'
def password(): return ''.join(secrets.choice(alphabet) for _ in range(24))
headers={'apikey':key,'Authorization':f'Bearer {key}','Content-Type':'application/json'}
credentials=[]
with httpx.Client(timeout=30) as client:
    for email,role,tier in users:
        pw=password()
        r=client.post(url+'/auth/v1/admin/users',headers=headers,json={'email':email,'password':pw,'email_confirm':True,'app_metadata':{'role':role,'tier':tier},'user_metadata':{'display_name':f'Demo {tier.title()}'}})
        if r.status_code==422 and 'already been registered' in r.text.lower():
            listing=client.get(url+'/auth/v1/admin/users?page=1&per_page=1000',headers=headers); listing.raise_for_status()
            found=next((u for u in listing.json().get('users',[]) if u.get('email')==email),None)
            if not found: raise SystemExit(f'Could not find existing user {email}')
            r=client.put(url+f"/auth/v1/admin/users/{found['id']}",headers=headers,json={'password':pw,'email_confirm':True,'app_metadata':{'role':role,'tier':tier},'user_metadata':{'display_name':f'Demo {tier.title()}'}})
        r.raise_for_status(); credentials.append((email,pw,role,tier))
out=Path('.demo-credentials.txt')
out.write_text('DEMO ONLY — rotate or delete these accounts before production.\n\n'+'\n'.join(f'{role.upper()} / {tier.upper()}\nUsername: {email}\nPassword: {pw}\n' for email,pw,role,tier in credentials))
try: out.chmod(0o600)
except OSError: pass
print(f'Created/reset {len(credentials)} accounts. Credentials written to {out.resolve()} (file mode 600 where supported). Do not commit or distribute this file.')
