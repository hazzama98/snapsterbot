import random
import string

def generate_random_user_agent(device_type='android', browser_type='chrome'):
    chrome_versions = list(range(110, 130))
    firefox_versions = list(range(90, 105))
    safari_versions = ['13.0', '14.0', '15.0', '16.0', '17.0']
    edge_versions = list(range(90, 110))

    if browser_type == 'chrome':
        major_version = random.choice(chrome_versions)
        minor_version = random.randint(0, 9)
        build_version = random.randint(1000, 9999)
        patch_version = random.randint(0, 99)
        browser_version = f"{major_version}.{minor_version}.{build_version}.{patch_version}"
    elif browser_type == 'firefox':
        browser_version = random.choice(firefox_versions)
    elif browser_type == 'safari':
        browser_version = random.choice(safari_versions)
    elif browser_type == 'edge':
        browser_version = random.choice(edge_versions)

    if device_type == 'android':
        android_versions = ['10.0', '11.0', '12.0', '13.0', '14.0']
        android_device = random.choice([
            'SM-G960F', 'Pixel 5', 'SM-A505F', 'Pixel 4a', 'Pixel 6 Pro', 'SM-N975F',
            'SM-G973F', 'Pixel 3', 'SM-G980F', 'Pixel 5a', 'SM-G998B', 'Pixel 4',
            'SM-G991B', 'SM-G996B', 'SM-F711B', 'SM-F916B', 'SM-G781B', 'SM-N986B',
            'SM-N981B', 'Pixel 2', 'Pixel 2 XL', 'Pixel 3 XL', 'Pixel 4 XL',
            'Pixel 5 XL', 'Pixel 6', 'Pixel 6 XL', 'Pixel 6a', 'Pixel 7', 'Pixel 7 Pro',
            'OnePlus 8', 'OnePlus 8 Pro', 'OnePlus 9', 'OnePlus 9 Pro', 'OnePlus Nord', 'OnePlus Nord 2',
            'OnePlus Nord CE', 'OnePlus 10', 'OnePlus 10 Pro', 'OnePlus 10T', 'OnePlus 10T Pro',
            'Xiaomi Mi 9', 'Xiaomi Mi 10', 'Xiaomi Mi 11', 'Xiaomi Redmi Note 8', 'Xiaomi Redmi Note 9',
            'Huawei P30', 'Huawei P40', 'Huawei Mate 30', 'Huawei Mate 40', 'Sony Xperia 1',
            'Sony Xperia 5', 'LG G8', 'LG V50', 'LG V60', 'Nokia 8.3', 'Nokia 9 PureView',
            'OPPO Find X3', 'OPPO Reno 6', 'Vivo X60', 'Vivo V21', 'Realme GT', 'Realme 8 Pro',
            'Motorola Edge 20', 'Motorola G Power', 'ASUS Zenfone 8', 'ASUS ROG Phone 5'
        ])
        android_version = random.choice(android_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Android {android_version}; Mobile; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (Linux; Android {android_version}; {android_device}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36 EdgA/{browser_version}")

    elif device_type == 'ios':
        ios_versions = ['13.0', '14.0', '15.0', '16.0', '17.0']
        ios_devices = ['iPhone', 'iPad']
        ios_version = random.choice(ios_versions)
        ios_device = random.choice(ios_devices)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 ({ios_device}; CPU {ios_device} OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 ({ios_device}; CPU {ios_device} OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{browser_version} Mobile/15E148 Safari/605.1.15")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 ({ios_device}; CPU {ios_device} OS {ios_version.replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{browser_version} Mobile/15E148 Safari/604.1")

    elif device_type == 'windows':
        windows_versions = ['10.0', '11.0']
        windows_version = random.choice(windows_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'edge':
            return (f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36 Edg/{browser_version}")

    elif device_type == 'macos':
        macos_versions = ['10.15', '11.0', '12.0', '13.0']
        macos_version = random.choice(macos_versions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version.replace('.', '_')}) AppleWebKit/537.36 "
                    f"(KHTML, like Gecko) Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version.replace('.', '_')}; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")
        elif browser_type == 'safari':
            return (f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version.replace('.', '_')}) AppleWebKit/605.1.15 "
                    f"(KHTML, like Gecko) Version/{browser_version} Safari/605.1.15")

    elif device_type == 'linux':
        linux_distributions = ['Ubuntu', 'Fedora', 'Debian', 'CentOS', 'Arch']
        linux_distribution = random.choice(linux_distributions)
        if browser_type == 'chrome':
            return (f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    f"Chrome/{browser_version} Safari/537.36")
        elif browser_type == 'firefox':
            return (f"Mozilla/5.0 (X11; {linux_distribution}; Linux x86_64; rv:{browser_version}.0) "
                    f"Gecko/{browser_version}.0 Firefox/{browser_version}.0")

    return None

def generate_random_device_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def generate_random_app_version():
    major = random.randint(1, 5)
    minor = random.randint(0, 9)
    patch = random.randint(0, 99)
    return f"{major}.{minor}.{patch}"

def generate_random_build_number():
    return ''.join(random.choices(string.digits, k=8))

def generate_random_locale():
    locales = ['en_US', 'en_GB', 'fr_FR', 'de_DE', 'es_ES', 'it_IT', 'ja_JP', 'ko_KR', 'pt_BR', 'ru_RU']
    return random.choice(locales)

def generate_random_timezone():
    timezones = ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney', 'Pacific/Auckland']
    return random.choice(timezones)

def generate_device_info():
    return {
        'user_agent': generate_random_user_agent(),
        'device_id': generate_random_device_id(),
        'app_version': generate_random_app_version(),
        'build_number': generate_random_build_number(),
        'locale': generate_random_locale(),
        'timezone': generate_random_timezone()
    }