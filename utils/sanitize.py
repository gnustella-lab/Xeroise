import re

# Matches emoji across the Unicode ranges plus variation selectors and ZWJ,
# plus the zero-width space (\u200b) that disable_mentions injects into mentions.
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # symbols & pictographs, emoji
    "\U00002600-\U000027BF"  # misc symbols and dingbats
    "\U0001F000-\U0001F02F"  # mahjong / cards
    "\U0001F1E6-\U0001F1FF"  # regional indicators (flags)
    "\U00002190-\U000021FF"  # arrows that are often used as emoji
    "\U00002B00-\U00002BFF"  # misc symbols and arrows
    "\uFE0F"  # variation selector-16 (emoji presentation)
    "\u200D"  # zero-width joiner (used in multi-codepoint emoji)
    "\u20E3"  # combining enclosing keycap (e.g. #️⃣)
    "]+",
    flags=re.UNICODE,
)


def strip_emojis(text):
    """Remove all emoji and zero-width characters from text, returning clean text."""
    if not text:
        return text
    cleaned = _EMOJI_PATTERN.sub("", text)
    # Collapse any leftover runs of whitespace created by removals.
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip()
