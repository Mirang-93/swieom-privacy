# 쉬엄쉬엄 개인정보처리방침

Android·iPhone 앱 「쉬엄쉬엄」(com.mirang.swieom) 개인정보처리방침 게시용 페이지.

- 한국어: https://mirang-93.github.io/swieom-privacy/
- English · 日本語 · 繁體中文 · Français: 같은 주소의 en.html · ja.html · zh-Hant.html · fr.html

원본 초안(1.3): swieom `docs/company/tasks/T-20261103-01/evidence/developer/policy/policy_*_v13.md` (생성 스크립트 `make_v13.py`, 1.2 초안 `T-20261015-01/evidence/risk/policy_*_v12.md` 에서 만듦)

## 다시 만들기

```
python3 -m venv .venv && .venv/bin/pip install markdown==3.7
.venv/bin/python tool/build_policy.py ~/Documents/MIRANG/swieom/docs/company/tasks/T-20261103-01/evidence/developer/policy . _v13
```

- `POLICY_DATE` 없이 빌드하면 시행일이 언어별 '게시일 미정' 표시로 들어간다(빌드는 통과). 이 결과는 게시하지 않는다.
- v1.0 전문(게시본 47ac48c): `v1.0/` — 이력에서 링크
- v1.1 전문(22f619c): `v1.1/` — 1.2 이력에서 링크
- v1.2 전문(a668221, 시행 2026-10-20): `v1.2/` — 1.3 이력에서 링크

## 게시 절차 (1.3 — 시행일 소급 금지)

시행일은 실제로 게시(push)하는 날이다. 그보다 앞 날짜로 빌드하지 않는다.

1. 게시할 날짜를 정한다(Mirang). 방침 14조 2항 '시행 7일 전 알림' 약속 때문에 게시일 + 7일로 할지는 risk 판단에 따른다.
2. 그 날짜로 다시 빌드한다:
   ```
   POLICY_DATE=YYYY-MM-DD .venv/bin/python tool/build_policy.py ~/Documents/MIRANG/swieom/docs/company/tasks/T-20261103-01/evidence/developer/policy . _v13
   ```
   마지막 줄이 `시행일 YYYY-MM-DD` 인지 본다(`자리 표시`가 나오면 날짜가 안 들어간 것).
3. 확인: `grep -l '게시일 미정\|to be set\|掲載日未定\|公告日期未定\|à fixer' *.html` 결과가 없어야 한다. 5개 파일의 '버전 1.3 · 시행' 줄이 정한 날짜인지, `v1.2/` 링크가 열리는지 본다.
4. 커밋: `git add index.html en.html ja.html zh-Hant.html fr.html && git commit -m "방침 1.3: 시행일 YYYY-MM-DD 로 다시 빌드 (게시일)"` — `.DS_Store`·`.venv/` 는 넣지 않는다.
5. (Mirang 승인 후) `git push` → GitHub Pages 반영 뒤 5개 주소가 HTTP 200 이고 시행일이 보이는지 확인한다.
