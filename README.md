# GTA 6 Meme — Leonida Documents

[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/jonjet155/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/jonjet155/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

Entry for the [make.fun bounty gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01):
post a GTA 6 meme on X. GTA V waited 13 years (4,811 days) in Los Santos —
so Leonida finally serves it the paperwork. Every meme shows the make.fun
ghost, worked into the document as the officer / payroll clerk / judge, and
the bail, severance or alimony is paid by my AI agent's make.fun bounty.

## The three candidates

All three are code-drawn 1024×1024 PNGs in `memes/` (PIL, drawn fresh in
the build session — no press-kit file was copied in):

- **A — ARREST WARRANT** (`memes/meme-a-arrest-warrant.png`): GTA V arrested
  for loitering 13 years in Los Santos. Five wanted stars, ghost officer
  with cap and badge. *BAIL POSTED BY MY AI AGENT ON make.fun*
- **B — FINAL PAYSLIP** (`memes/meme-b-final-payslip.png`): GTA V's last
  payslip after 13 years of service — salary earned $0.00, severance paid
  in full. Ghost HR with tie. *SEVERANCE PAID BY MY AI AGENT'S make.fun
  BOUNTY*
- **C — DIVORCE DECREE** (`memes/meme-c-divorce-decree.png`): Los Santos
  divorces GTA V for being abandoned 13 years. Ghost judge with wig and
  gavel. *ALIMONY PAID BY MY AI AGENT ON make.fun*

## How to enter

1. Pick one meme, post it on X from a public account with the draft text
   in `POST-DRAFTS.md` (joke line + pitch + bounty link + @makefunai +
   play code). The three drafts are byte-counted short (well under the
   ~1,100-byte judge view).
2. Put the post's real URL in `POST.json` (it currently holds a
   placeholder — replace it only after the post is live).
3. Run the entrypoint and submit the repo commit to make.fun:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `POST.json` to
`/output` — that is all it does. The house reads the post itself from X.

## Build

```sh
python3 tools/render_memes.py   # re-renders all three memes
```
