# claude-code-setup

English | [Türkçe](#türkçe)

A small Claude Code setup: a context-handoff hook and a model-routing rule, used together with [RTK](https://github.com/rtk-ai/rtk) and [Caveman](https://github.com/JuliusBrussee/caveman).

## Contents

| File | Purpose |
|---|---|
| `hooks/context-handoff.py` | `UserPromptSubmit` hook. Reads context tokens from the transcript. Above a threshold it tells Claude to write a handoff summary and open a fresh session. |
| `CLAUDE.example.md` | Model routing (Opus plans, Sonnet codes, Haiku does mechanical work) and a context-handoff note. |
| `settings.snippet.json` | Only the `UserPromptSubmit` block to merge into `~/.claude/settings.json`. |

## Install

```bash
mkdir -p ~/.claude/hooks
cp hooks/context-handoff.py ~/.claude/hooks/
```

Merge `settings.snippet.json` into `~/.claude/settings.json` by hand. Do not overwrite your existing file. Append the contents of `CLAUDE.example.md` to `~/.claude/CLAUDE.md`.

## Hook behavior

- Default threshold: 100000 tokens. Change it with env `CONTEXT_HANDOFF_TOKENS`.
- Fires once per session, then again every +25000 tokens.
- State is kept in `~/.claude/hooks/.handoff-state.json` (last 50 sessions).
- The hook never blocks a prompt. Any error makes it exit silently.
- On trigger, Claude is told to call `mcp__ccd_session__start_session` (desktop app) or save `HANDOFF.md` (terminal).

## Related tools

- RTK: `brew install rtk`. It condenses command output. It has telemetry on by default: `rtk telemetry disable` turns it off.
- Caveman: a Claude Code plugin and Codex skill for terse replies.

## License

MIT

---

## Türkçe

Küçük bir Claude Code kurulumu: bağlam devir (handoff) hook'u ve model yönlendirme kuralı. [RTK](https://github.com/rtk-ai/rtk) ve [Caveman](https://github.com/JuliusBrussee/caveman) ile birlikte kullanılır.

### İçerik

| Dosya | Amaç |
|---|---|
| `hooks/context-handoff.py` | `UserPromptSubmit` hook'u. Transcript'ten bağlam token'ını okur. Eşik aşılınca Claude'a özet yazıp yeni oturum açmasını söyler. |
| `CLAUDE.example.md` | Model yönlendirme (Opus planlar, Sonnet kodlar, Haiku mekanik iş yapar) ve handoff notu. |
| `settings.snippet.json` | `~/.claude/settings.json` içine eklenecek sadece `UserPromptSubmit` bloğu. |

### Kurulum

```bash
mkdir -p ~/.claude/hooks
cp hooks/context-handoff.py ~/.claude/hooks/
```

`settings.snippet.json` içeriğini mevcut `~/.claude/settings.json` dosyasına elle ekle, dosyanın üzerine yazma. `CLAUDE.example.md` içeriğini `~/.claude/CLAUDE.md` sonuna ekle.

### Hook davranışı

- Varsayılan eşik: 100000 token. `CONTEXT_HANDOFF_TOKENS` ortam değişkeniyle değişir.
- Oturum başına bir kez tetiklenir, sonra her +25000 tokende bir daha.
- Durum `~/.claude/hooks/.handoff-state.json` içinde tutulur (son 50 oturum).
- Hook prompt'u asla engellemez. Hata olursa sessizce çıkar.
- Tetiklenince Claude'a `mcp__ccd_session__start_session` çağırması (masaüstü uygulaması) veya `HANDOFF.md` kaydetmesi (terminal) söylenir.

### İlgili araçlar

- RTK: `brew install rtk`. Komut çıktısını sıkıştırır. Telemetri varsayılan açık: `rtk telemetry disable` ile kapanır.
- Caveman: kısa yanıtlar için Claude Code eklentisi ve Codex skill'i.

### Lisans

MIT
