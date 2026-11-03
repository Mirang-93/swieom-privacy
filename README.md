# 쉬엄쉬엄 개인정보처리방침

Android·iPhone 앱 「쉬엄쉬엄」(com.mirang.swieom) 개인정보처리방침 게시용 페이지.

- 한국어: https://mirang-93.github.io/swieom-privacy/
- English · 日本語 · 繁體中文 · Français: 같은 주소의 en.html · ja.html · zh-Hant.html · fr.html

원본 초안(1.3): swieom `docs/company/tasks/T-20261103-02/evidence/developer/policy/policy_*_v13.md` — 1.2 초안 `T-20261015-01/evidence/risk/policy_*_v12.md` 에서 `make_v13.py` 로 만든 뒤(T-20261103-01) `edit_v13_t02.py` 로 시행 이유 문장·사용법 안내 확인 여부를 더함(T-20261103-02). 처음 판은 `T-20261103-01/evidence/developer/policy/` 에 그대로 있다

## 다시 만들기

```
python3 -m venv .venv && .venv/bin/pip install markdown==3.7
.venv/bin/python tool/build_policy.py ~/Documents/MIRANG/swieom/docs/company/tasks/T-20261103-02/evidence/developer/policy . _v13
```

- `POLICY_DATE` 없이 빌드하면 시행일이 언어별 '게시일 미정' 표시로 들어간 초안을 **`_draft/` 에만** 쓴다(빌드는 통과). 게시 파일(`index.html`·`en.html`·`ja.html`·`zh-Hant.html`·`fr.html`)은 건드리지 않으므로 지금 게시본(1.2, a668221) 그대로다. `_draft/` 는 `.gitignore` 에 있어 커밋·게시되지 않는다.
- `POLICY_DATE=YYYY-MM-DD` 로 빌드하면 게시 파일 5개가 그 시행일의 1.3 으로 바뀐다.
- `POLICY_DATE` 가 오늘보다 앞 날짜면 빌드가 실패한다(종료 코드 1, 시행일 소급 금지). 오늘·미래 날짜만 통과한다.
- v1.0 전문(게시본 47ac48c): `v1.0/` — 이력에서 링크
- v1.1 전문(22f619c): `v1.1/` — 1.2 이력에서 링크
- v1.2 전문(a668221, 시행 2026-10-20): `v1.2/` — 1.3 이력에서 링크

## 게시 절차 (1.3 — 시행일 소급 금지)

시행일은 실제로 게시(push)하는 날이다. 그보다 앞 날짜로 빌드하지 않는다.

1. 게시할 날짜를 정한다(Mirang). 1.2 시행 기간에 배포한 빌드가 없어(Mirang 확인 2026-11-03) 1.3 은 게시일 시행이며, 제14조 5항에 그 이유 문장이 있다(risk R-2 (a)). 게시 전에 어떤 트랙·TestFlight 로든 빌드를 배포했다면 이유 문장을 지우고 시행일 = 게시일 + 7일로 한다.
2. 그 날짜로 다시 빌드한다:
   ```
   POLICY_DATE=YYYY-MM-DD .venv/bin/python tool/build_policy.py ~/Documents/MIRANG/swieom/docs/company/tasks/T-20261103-02/evidence/developer/policy . _v13
   ```
   마지막 줄이 `시행일 YYYY-MM-DD` 인지 본다(`자리 표시`가 나오면 날짜가 안 들어가 `_draft/` 에만 쓴 것 — 게시 파일은 1.2 그대로). 날짜가 오늘보다 앞이면 `실패:` 로 멈춘다.
3. 확인: `grep -l '게시일 미정\|to be set\|掲載日未定\|公告日期未定\|à fixer' *.html` 결과가 없어야 한다. 5개 파일의 '버전 1.3 · 시행' 줄이 정한 날짜인지, `v1.2/` 링크가 열리는지 본다.
4. 커밋: `git add index.html en.html ja.html zh-Hant.html fr.html && git commit -m "방침 1.3: 시행일 YYYY-MM-DD 로 다시 빌드 (게시일)"` — `.DS_Store`·`.venv/` 는 넣지 않는다.
5. (Mirang 승인 후) `git push` → GitHub Pages 반영 뒤 5개 주소가 HTTP 200 이고 시행일이 보이는지 확인한다.
