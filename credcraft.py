
import itertools
import os
from datetime import datetime

BANNER = r"""
    █████████                         █████   █████████                         ██████   █████   
  ███░░░░░███                       ░░███   ███░░░░░███                       ███░░███ ░░███    
 ███     ░░░  ████████   ██████   ███████  ███     ░░░  ████████   ██████    ░███ ░░░  ███████  
░███         ░░███░░███ ███░░███ ███░░███ ░███         ░░███░░███ ░░░░░███  ███████   ░░░███░   
░███          ░███ ░░░ ░███████ ░███ ░███ ░███          ░███ ░░░   ███████ ░░░███░      ░███    
░░███     ███ ░███     ░███░░░  ░███ ░███ ░░███     ███ ░███      ███░░███   ░███       ░███ ███
 ░░█████████  █████    ░░██████ ░░████████ ░░█████████  █████    ░░████████  █████      ░░█████ 
  ░░░░░░░░░  ░░░░░      ░░░░░░   ░░░░░░░░   ░░░░░░░░░  ░░░░░      ░░░░░░░░  ░░░░░        ░░░░░  
                                                                                                
                                                                                                
                                                                                                
      Intelligent Credential Wordlist Generator
     [ For Authorized Penetration Testing ONLY ]
"""

LEET_MAP = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7'],
    'b': ['b', '8'],
    'g': ['g', '9'],
    'l': ['l', '1'],
    'z': ['z', '2'],
}

COMMON_SUFFIXES = [
    '', '1', '2', '3', '12', '21', '123', '321', '1234', '12345', '123456',
    '1234567', '12345678', '0', '00', '000', '01', '007',
    '111', '222', '333', '444', '555', '666', '777', '888', '999',
    '100', '101', '110', '786', '420', '69', '99', '88', '77', '11', '22',
    '2024', '2023', '2022', '2021', '2020', '2019',
    '!', '!!', '@', '@@', '#', '##', '$', '$$', '*', '**', '?', '.', '_',
    '!1', '!123', '@123', '#123', '!@#', '!@#$', '@!', '#!',
]

COMMON_PREFIXES = [
    '', 'the', 'mr', 'mrs', 'miss', 'ms', 'dr', 'prof',
    'admin', 'user', 'root', 'super', 'its', 'iam', 'im', 'hey',
    'real', 'official', 'only', 'just',
]

SEP = ['', '.', '_', '-', '@', '#', '~', '+']


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def c(code, text):
    return f"\033[{code}m{text}\033[0m"


def get_input(prompt):
    return input(f"  {c('96', prompt)} ").strip()


def get_yes_no(prompt):
    while True:
        v = input(f"  {c('96', prompt + ' [y/n]:')} ").strip().lower()
        if v in ('y', 'yes'): return True
        if v in ('n', 'no'):  return False
        print(f"  {c('91', '[!] Enter y or n.')}")


def normalize_dob(dob):
    clean = ''.join(filter(str.isdigit, dob))
    parts = []
    if len(clean) >= 8:
        dd, mm, yy, yyyy = clean[0:2], clean[2:4], clean[4:6], clean[4:8]
        parts += [
            dd, mm, yy, yyyy,
            dd+mm, mm+dd, dd+mm+yy, dd+mm+yyyy,
            mm+dd+yy, mm+dd+yyyy,
            yyyy+mm+dd, yy+mm+dd,
            clean,
        ]
    elif len(clean) >= 4:
        parts += [clean[:2], clean[2:4], clean[4:], clean]
    elif clean:
        parts.append(clean)
    return list(dict.fromkeys(p for p in parts if p))


def phone_parts(phone):
    d = ''.join(filter(str.isdigit, phone))
    parts = [d]
    for n in (4, 5, 6, 7, 8, 10):
        if len(d) >= n:
            parts.append(d[-n:])
            parts.append(d[:n])
    return list(dict.fromkeys(p for p in parts if p))


def email_parts(email):
    parts = []
    if '@' in email:
        local, domain = email.split('@', 1)
        parts.append(local)
        parts.append(domain.split('.')[0])
        parts.append(email)
    return parts


def cap_variants(w):
    if not w:
        return []
    w = str(w)
    return list(dict.fromkeys([
        w.lower(),
        w.upper(),
        w.capitalize(),
        w[0].upper() + w[1:] if len(w) > 1 else w.upper(),
        w[0].lower() + w[1:] if len(w) > 1 else w.lower(),
        w.title(),
    ]))


def leet_variants(word):
    word = word.lower()
    subs = {i: LEET_MAP[ch] for i, ch in enumerate(word) if ch in LEET_MAP}
    if not subs:
        return [word]
    if len(subs) > 7:
        subs = dict(list(subs.items())[:7])
    results = set()
    positions = list(subs.keys())
    choices   = [subs[p] for p in positions]
    for combo in itertools.product(*choices):
        chars = list(word)
        for pos, rep in zip(positions, combo):
            chars[pos] = rep
        results.add(''.join(chars))
    return list(results)

def collect_target_info():
    div = c('97', '━' * 62)
    print(f"\n{div}")
    print(c('1', c('97', '  TARGET PROFILE COLLECTION')))
    print(div)
    print("  (Press Enter to skip any field)\n")

    info = {}

    def ask(key, label):
        info[key] = get_input(f"{label}:")

    print(f"  {c('93','[ Personal ]')}")
    ask('first_name',   'First name')
    ask('last_name',    'Last name')
    ask('nickname',     'Nickname / alias')
    ask('dob',          'Date of birth (DDMMYYYY)')
    ask('age',          'Age')

    print(f"\n  {c('93','[ Contact & Online ]')}")
    ask('email',        'Email address')
    ask('phone',        'Phone number')
    ask('username',     'Known username / handle')
    ask('instagram',    'Instagram handle')
    ask('twitter',      'Twitter / X handle')

    print(f"\n  {c('93','[ Interests ]')}")
    ask('fav_color',    'Favourite color')
    ask('fav_food',     'Favourite food')
    ask('fav_place',    'Favourite place / city')
    ask('fav_sport',    'Favourite sport')
    ask('fav_team',     'Favourite team / club')
    ask('fav_movie',    'Favourite movie / show')
    ask('fav_music',    'Favourite artist / band')
    ask('hobby',        'Main hobby')
    ask('pet_name',     'Pet name')

    print(f"\n  {c('93','[ Professional ]')}")
    ask('company',      'Company / organisation')
    ask('job_title',    'Job title')
    ask('school',       'School / university')
    ask('city',         'City')
    ask('country',      'Country')

    print(f"\n  {c('93','[ Other ]')}")
    ask('id_number',    'ID / employee number')
    ask('car_plate',    'Vehicle plate')
    ask('partner_name', 'Partner / spouse name')
    ask('child_name',   "Child's name")
    ask('lucky_number', 'Lucky number')
    ask('custom1',      'Extra keyword 1')
    ask('custom2',      'Extra keyword 2')
    ask('custom3',      'Extra keyword 3')

    return info

def build_base_tokens(info):
    raw = set()
    simple = [
        'first_name', 'last_name', 'nickname', 'age', 'username',
        'instagram', 'twitter', 'fav_color', 'fav_food', 'fav_place',
        'fav_sport', 'fav_team', 'fav_movie', 'fav_music', 'hobby',
        'pet_name', 'company', 'job_title', 'school', 'city', 'country',
        'id_number', 'car_plate', 'partner_name', 'child_name',
        'lucky_number', 'custom1', 'custom2', 'custom3',
    ]
    for key in simple:
        v = info.get(key, '').strip()
        if v:
            raw.add(v)
            for part in v.split():
                raw.add(part)

    if info.get('dob'):
        raw.update(normalize_dob(info['dob']))
    if info.get('phone'):
        raw.update(phone_parts(info['phone']))
    if info.get('email'):
        raw.update(email_parts(info['email']))

    raw.discard('')
    return [t for t in raw if t]

def generate_usernames(info, tokens):
    result = set()

    fn = info.get('first_name', '').strip().lower()
    ln = info.get('last_name', '').strip().lower()
    nn = info.get('nickname', '').strip().lower()
    dob_parts = normalize_dob(info.get('dob', '')) if info.get('dob') else []
    ph_parts  = phone_parts(info.get('phone', '')) if info.get('phone') else []

    for t in tokens:
        for v in cap_variants(t):
            result.add(v)

    if fn and ln:
        for s in SEP:
            result.add(f"{fn}{s}{ln}")
            result.add(f"{ln}{s}{fn}")
            result.add(f"{fn[0]}{s}{ln}")
            result.add(f"{ln[0]}{s}{fn}")
            result.add(f"{fn}{s}{ln[0]}")
            result.add(f"{ln}{s}{fn[0]}")
            result.add(f"{fn[0]}{s}{ln[0]}")

    for name in [fn, ln]:
        if name and nn:
            for s in SEP:
                result.add(f"{nn}{s}{name}")
                result.add(f"{name}{s}{nn}")

    for base in [fn, ln, nn]:
        if not base: continue
        for d in dob_parts:
            for s in ['', '_', '.', '-']:
                result.add(f"{base}{s}{d}")
                result.add(f"{d}{s}{base}")

    for base in [fn, ln, nn]:
        if not base: continue
        for p in ph_parts:
            for s in ['', '_', '.']:
                result.add(f"{base}{s}{p}")
                result.add(f"{p}{s}{base}")

    for extra in [info.get('age','').strip(), info.get('lucky_number','').strip()]:
        if not extra: continue
        for base in [fn, ln, nn]:
            if base:
                for s in ['', '_', '.']:
                    result.add(f"{base}{s}{extra}")
                    result.add(f"{extra}{s}{base}")

    for t in tokens:
        if len(t) <= 15:
            for pre in COMMON_PREFIXES:
                result.add(f"{pre}{t.lower()}")

    if info.get('email') and '@' in info['email']:
        result.add(info['email'].split('@')[0])

    plain = [t.lower() for t in tokens if t.isalpha() and 3 <= len(t) <= 12]
    for t1, t2 in itertools.permutations(plain, 2):
        for s in ['', '_', '.', '-']:
            result.add(f"{t1}{s}{t2}")
            result.add(f"{t1.capitalize()}{s}{t2.capitalize()}")

    result.discard('')
    return sorted(result)

def generate_passwords(info, tokens):
    result = set()

    dob_parts    = normalize_dob(info.get('dob', '')) if info.get('dob') else []
    ph_parts     = phone_parts(info.get('phone', '')) if info.get('phone') else []
    word_tokens  = [t for t in tokens if any(ch.isalpha() for ch in t)]
    num_tokens   = [t for t in tokens if t.isdigit()]

    for t in tokens:
        for v in cap_variants(t):
            for suf in COMMON_SUFFIXES:
                result.add(f"{v}{suf}")

    for t in word_tokens:
        for leet in leet_variants(t):
            for v in cap_variants(leet):
                result.add(v)
                for suf in COMMON_SUFFIXES:
                    result.add(f"{v}{suf}")

    for t in word_tokens:
        for d in dob_parts:
            for v in cap_variants(t):
                for s in ['', '_', '.', '-']:
                    result.add(f"{v}{s}{d}")
                    result.add(f"{d}{s}{v}")

            for leet in leet_variants(t):
                result.add(f"{leet}{d}")
                result.add(f"{d}{leet}")
                for suf in COMMON_SUFFIXES[:15]:
                    result.add(f"{leet}{d}{suf}")

    for t in word_tokens:
        for p in ph_parts:
            for v in cap_variants(t):
                for s in ['', '_', '.', '-']:
                    result.add(f"{v}{s}{p}")
                    result.add(f"{p}{s}{v}")

    for t1, t2 in itertools.permutations(word_tokens, 2):
        for v1 in cap_variants(t1):
            for v2 in cap_variants(t2):
                for s in SEP:
                    base = f"{v1}{s}{v2}"
                    result.add(base)
                    for suf in COMMON_SUFFIXES:
                        result.add(f"{base}{suf}")

    for wt in word_tokens:
        for nt in num_tokens:
            for v in cap_variants(wt):
                for s in ['', '_', '.', '-']:
                    result.add(f"{v}{s}{nt}")
                    result.add(f"{nt}{s}{v}")
                    for suf in COMMON_SUFFIXES[:15]:
                        result.add(f"{v}{s}{nt}{suf}")

    short = [t for t in word_tokens if 3 <= len(t) <= 7]
    for t1, t2, t3 in itertools.permutations(short, 3):
        for s in ['', '_', '.']:
            base = f"{t1.capitalize()}{s}{t2.capitalize()}{s}{t3.capitalize()}"
            result.add(base)
            for suf in ['', '1', '123', '!', '@', '2024', '2023']:
                result.add(f"{base}{suf}")
    
        for l1 in leet_variants(t1)[:3]:
            result.add(f"{l1}{t2.capitalize()}{t3}")

    for d in dob_parts:
        for suf in COMMON_SUFFIXES:
            result.add(f"{d}{suf}")

    for p in ph_parts:
        for suf in COMMON_SUFFIXES[:20]:
            result.add(f"{p}{suf}")

    for t in word_tokens:
        for pre in COMMON_PREFIXES:
            if pre:
                for v in cap_variants(t):
                    for suf in COMMON_SUFFIXES[:20]:
                        result.add(f"{pre}{v}{suf}")

    fn = info.get('first_name', '').strip()
    interests = [
        info.get(k, '').strip() for k in
        ['fav_color','fav_food','fav_place','fav_sport','fav_team',
         'fav_music','pet_name','hobby'] if info.get(k,'').strip()
    ]
    for interest in interests:
        iword = interest.split()[0] if ' ' in interest else interest
        if fn:
            for v1 in cap_variants(fn):
                for v2 in cap_variants(iword):
                    for suf in COMMON_SUFFIXES[:25]:
                        result.add(f"{v1}{v2}{suf}")
                        result.add(f"{v2}{v1}{suf}")
        for d in dob_parts[:4]:
            for v in cap_variants(iword):
                result.add(f"{v}{d}")
                result.add(f"{d}{v}")

    result.discard('')
    result = {p for p in result if 4 <= len(p) <= 32}
    return sorted(result)


def save_wordlist(words, filename):
    path = os.path.join(os.getcwd(), filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(words) + '\n')
    return path, len(words)


def print_stats(label, count, path):
    print(f"\n  {c('92','[✓]')} {label} saved!")
    print(f"      File  : {c('97', path)}")
    print(f"      Words : {c('97', f'{count:,}')}")


def main():
    clear()
    print(c('92', BANNER))
    print(c('93', '  [!] LEGAL NOTICE: Use ONLY on systems you own or have explicit'))
    print(c('93', '      written permission to test. Unauthorized use is illegal.\n'))

    if not get_yes_no('Do you confirm you have authorization to test the target?'):
        print(f"\n  {c('91','Exiting. Only use this tool on authorized targets.')}\n")
        return

    div = c('97', '━' * 62)
    print(f"\n{div}")
    print(f"  {c('93','What do you want to generate?')}")
    print(f"  {c('97','[1]')} Username list only")
    print(f"  {c('97','[2]')} Password list only")
    print(f"  {c('97','[3]')} Both")
    while True:
        ch = input(f"\n  {c('96','Choice [1/2/3]:')} ").strip()
        if ch in ('1', '2', '3'): break
        print(f"  {c('91','[!] Invalid choice.')}")

    gen_u = ch in ('1', '3')
    gen_p = ch in ('2', '3')

    info   = collect_target_info()
    tokens = build_base_tokens(info)

    print(f"\n  {c('93','[*] Analysing profile...')}")
    print(f"  {c('92','[✓]')} {len(tokens)} base tokens extracted.")

    label = (info.get('first_name') or 'target').lower().replace(' ', '_')
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if gen_u:
        print(f"\n  {c('93','[*] Generating username list...')}")
        unames = generate_usernames(info, tokens)
        path, n = save_wordlist(unames, f"{label}_usernames_{stamp}.txt")
        print_stats("Username list", n, path)

    if gen_p:
        print(f"\n  {c('93','[*] Generating password list (may take a few seconds)...')}")
        pwds = generate_passwords(info, tokens)
        path, n = save_wordlist(pwds, f"{label}_passwords_{stamp}.txt")
        print_stats("Password list", n, path)

    print(f"\n{div}")
    print(f"  {c('92','Done!')} Wordlist(s) saved in your current directory.")
    print(f"  {c('93','[!] Use responsibly and only on authorized targets.')}\n")


if __name__ == '__main__':
    main()
