"""risk 방침 초안(md) → 게시용 HTML. 빈칸을 채우고, 남은 [자리 표시]가 있으면 실패한다.
사용: [POLICY_DATE=YYYY-MM-DD] build_policy.py <초안 폴더> <출력 폴더> [파일 이름 접미사, 예: _v13]
POLICY_DATE = 이번 판의 시행일(실제 게시일, 소급 금지 — 오늘보다 앞 날짜면 실패).
없으면 언어별 '게시일 미정' 표시로 <출력 폴더>/_draft/ 에만 빌드하고 게시 파일(index.html 등)은 건드리지 않는다
(_draft/ 는 .gitignore, Jekyll 도 _ 폴더를 게시하지 않는다)."""
import datetime, os, re, sys, pathlib, markdown

SRC, OUT = map(pathlib.Path, sys.argv[1:3])
SUFFIX = sys.argv[3] if len(sys.argv) > 3 else ''
NAME, MAIL = 'Kim Junho (Mirang)', 'wnshroqkf@naver.com'
KO_NAME = '김준호(Mirang)'
ADDR_EN = '3F, 41 Gwongwang-ro 56beon-gil, Gwonseon-gu, Suwon-si, Gyeonggi-do 16556, Republic of Korea'
BASE = 'https://mirang-93.github.io/swieom-privacy/'

DATE = os.environ.get('POLICY_DATE', '').strip()
EN_M = 'January February March April May June July August September October November December'.split()
FR_M = 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'.split()
if DATE:
    d = datetime.date.fromisoformat(DATE)  # 형식이 틀리면 여기서 실패
    if d < datetime.date.today():  # 시행일 소급 금지 (swieom-privacy 2d581a5, risk R-3)
        sys.exit(f'실패: POLICY_DATE={DATE} 가 오늘({datetime.date.today()})보다 앞입니다. 시행일은 게시하는 날 이후로.')
    EFFECTIVE = {'ko': f'{d.year}년 {d.month}월 {d.day}일', 'en': f'{d.day} {EN_M[d.month - 1]} {d.year}',
                 'ja': f'{d.year}年{d.month}月{d.day}日', 'zh-Hant': f'{d.year} 年 {d.month} 月 {d.day} 日',
                 'fr': f"{'1er' if d.day == 1 else d.day} {FR_M[d.month - 1]} {d.year}"}
else:  # 자리 표시: 대괄호를 쓰지 않아 빌드는 통과하고, 읽으면 미정인 것이 바로 보인다. 게시 파일 대신 _draft/ 에만 쓴다 (risk R-1)
    OUT = OUT / '_draft'
    EFFECTIVE = {'ko': '게시일 미정', 'en': 'date of posting (to be set)', 'ja': '掲載日未定',
                 'zh-Hant': '公告日期未定', 'fr': 'date de publication à fixer'}
# 언어 코드 → (출력 파일, html lang, 링크 이름, 제목)
LANGS = {
    'ko': ('index.html', 'ko', '한국어', '쉬엄쉬엄 개인정보처리방침'),
    'en': ('en.html', 'en', 'English', 'Take Your Time — Privacy Policy'),
    'ja': ('ja.html', 'ja', '日本語', 'ゆるりあそび プライバシーポリシー'),
    'zh-Hant': ('zh-Hant.html', 'zh-Hant', '繁體中文', '慢慢玩 隱私權政策'),
    'fr': ('fr.html', 'fr', 'Français', 'Sans se presser — Politique de confidentialité'),
}

def other_langs(code):
    return ' · '.join(f'[{LANGS[c][2]}]({LANGS[c][0]})' for c in LANGS if c != code)

FILL = {
    'ko': [
        ('[운영자 이름]', KO_NAME), ('[개인정보 문의 이메일]', MAIL), ('[성명]', '김준호'),
        ('- 전화: [전화번호 — 선택]\n', ''),
        ('[ ]개월', '3개월'),
        ('| [메일 서비스 회사 이름] |', '| 네이버 주식회사 |'),
        ('[2단계 인증 등 실제 조치]로', '2단계 인증으로'),  # 조사까지 바꿈 ('인증로' 방지)
        ('[수사기관 이름·연락처 — 게시 직전 재확인]', '대검찰청: 국번 없이 1301 (www.spo.go.kr)'),
        ('[시행일]', EFFECTIVE['ko']), ('[1.1 시행일]', '2026년 10월 20일'),
    ],
    'en': [
        ('[operator name]', NAME), ('[privacy email]', MAIL), ('[ ] months', '3 months'),
        ('[email service provider]', 'NAVER Corporation (Republic of Korea)'),
        ('[actual measures, e.g. two-step verification]', 'two-step verification'),
        ('(Google, [email provider])', '(Google)'),
        ('[Transfer safeguard — to be confirmed before publishing.]',
         'The European Commission has recognised the Republic of Korea as ensuring an adequate level of '
         'protection (adequacy decision of 17 December 2021); Google relies on the transfer safeguards '
         'described in its own privacy policy.'),
        (' [EU representative: name and address — or delete this sentence if not required.]', ''),
        ('[effective date]', EFFECTIVE['en']), ('[1.1 effective date]', '20 October 2026'),
    ],
    'ja': [
        ('[運営者名]', NAME), ('[個人情報お問い合わせメール]', MAIL),
        ('（[運営者住所 — 回答用]）', ''), ('- 代表者：[法人の場合のみ代表者名]\n', ''),
        ('[ ] か月', '3 か月'),
        ('[メールサービス事業者名]（所在国：[国名]）', 'NAVER Corporation（所在国：大韓民国）'),
        ('[二段階認証など実際の措置] で', '二段階認証で'),
        ('[施行日]', EFFECTIVE['ja']), ('[1.1 施行日]', '2026年10月20日'),
    ],
    'zh-Hant': [
        ('[營運者名稱]，[地址]，電子郵件 [個資聯絡信箱]', f'{NAME}，地址 {ADDR_EN}，電子郵件 {MAIL}'),
        ('[營運者名稱]', NAME), ('[個資聯絡信箱]', MAIL), ('[ ] 個月', '3 個月'),
        ('韓國（營運者），[郵件服務所在國家]（電子郵件服務）', '韓國（營運者與電子郵件服務）'),
        ('[郵件服務業者名稱]', 'NAVER Corporation'),
        ('以 [兩步驟驗證等實際措施] 保護', '以兩步驟驗證保護'),
        ('[施行日]', EFFECTIVE['zh-Hant']), ('[1.1 施行日]', '2026 年 10 月 20 日'),
    ],
    'fr': [
        ('[nom de l\'éditeur], [adresse], [e-mail de contact vie privée].',
         f'{NAME}, {ADDR_EN}, {MAIL}.'),
        ('[Représentant dans l\'UE (article 27 du RGPD) : nom et adresse — ou supprimer cette phrase si l\'exemption de l\'article 27(2) est confirmée.]\n', ''),
        ('[nom de l\'éditeur]', NAME), ('[e-mail de contact vie privée]', MAIL), ('[ ] mois', '3 mois'),
        ('[prestataire e-mail] ([pays])', 'NAVER Corporation (République de Corée)'),
        ('(Google, [prestataire e-mail])', '(Google)'),
        ('[décision d\'adéquation de la Commission pour la République de Corée / garanties appropriées du prestataire — à confirmer avant publication]',
         'décision d\'adéquation de la Commission européenne pour la République de Corée (17 décembre 2021) ; '
         'pour Google, les garanties décrites dans ses propres règles de confidentialité'),
        ('[mesures réelles, ex. validation en deux étapes]', 'la validation en deux étapes'),
        ('[date d\'entrée en vigueur]', EFFECTIVE['fr']), ('[date 1.1]', '20 octobre 2026'),
    ],
}

CSS = """:root{color-scheme:light dark;--bg:#faf7f2;--paper:#fff;--ink:#1f1b16;--muted:#6b6259;--line:#e5ddd2;--primary:#b23a48}
@media (prefers-color-scheme:dark){:root{--bg:#171513;--paper:#211e1b;--ink:#eee8e1;--muted:#a89f95;--line:#3a352f;--primary:#e0707d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);line-height:1.7;
font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR","Hiragino Sans","PingFang TC","Segoe UI",sans-serif}
main{max-width:880px;margin:0 auto;padding:32px 16px 64px}article{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:28px 20px}
@media (min-width:640px){article{padding:40px}}h1{color:var(--primary);font-size:28px;line-height:1.3;margin:0 0 12px}
h2{font-size:20px;margin:32px 0 10px}a{color:var(--primary);overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:15px;margin:8px 0}th,td{border:1px solid var(--line);padding:8px;vertical-align:top;text-align:left}
th{background:var(--bg)}"""

def build(code):
    file, lang, _, title = LANGS[code]
    md = (SRC / f'policy_{code}{SUFFIX}.md').read_text()
    md = re.sub(r'\A<!--.*?-->\s*', '', md, flags=re.S)           # 작성자 주석
    md = md[:md.index('\n---\n\n## 게시 전 확인')]                 # 내부 확인 절
    # 네이버 메일은 국내 서버 → 국외 이전 표의 메일 행 삭제 (초안: '국외 서버를 쓰는 경우만')
    md = re.sub(r'^\| \[메일 서비스 회사 이름 \(연락처\)\].*\n', '', md, flags=re.M)
    for old, new in FILL[code]:
        assert old in md, (code, old)
        md = md.replace(old, new)
    md = re.sub(r'^(다른 언어|Other languages|他の言語|其他語言|Autres langues)(\s*[:：]\s*).*$',
                lambda m: m[1] + m[2] + other_langs(code), md, count=1, flags=re.M)
    # Python-Markdown 은 목록 앞에 빈 줄이 있어야 목록으로 본다
    item = re.compile(r'^(\s*[-*] |\s*\d+\. )')
    lines = md.split('\n')
    md = '\n'.join(l if not (item.match(l) and i and lines[i-1].strip() and not item.match(lines[i-1]))
                    else '\n' + l for i, l in enumerate(lines))
    # 버전 치환('Version 1.3'→'1.2' 등)이 남아 있으면 이력 줄이 사라진다 → 실패
    assert re.search(r'1\.3\D{1,6}(시행|施行|effective|en vigueur)', md), (code, 'v1.3 이력 줄 없음')
    left = [m for m in re.findall(r'\[[^\]]*\](?!\()', md)]
    assert not left, (code, left)
    body = markdown.markdown(md, extensions=['tables'])
    body = body.replace('<table>', '<div class="tbl"><table>').replace('</table>', '</table></div>')
    body = re.sub(r'(?<![">])(https?://[^\s<)]+)', r'<a href="\1">\1</a>', body)  # 맨 URL 링크화
    (OUT / file).write_text(f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="canonical" href="{BASE}{'' if file == 'index.html' else file}">
<style>{CSS}</style>
</head>
<body><main><article>
{body}
</article></main></body>
</html>
""")

OUT.mkdir(parents=True, exist_ok=True)
for c in LANGS:
    build(c)
print('ok', sorted(p.name for p in OUT.glob('*.html')))
print('시행일', DATE or f'자리 표시(게시일 미정) — {OUT} 에만 썼다(게시 파일은 그대로). 게시 때 POLICY_DATE=YYYY-MM-DD 로 다시 빌드')
