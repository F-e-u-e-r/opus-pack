import re
import shlex
import sys

cmd = sys.argv[1]

# Strip heredoc bodies: a line containing "<<[-~]?QUOTE?WORD" opens a heredoc;
# its body runs until a line that is exactly the (possibly dash-stripped)
# delimiter.
def strip_heredocs(text):
    lines = text.split("\n")
    out = []
    delim = None
    dash = False
    opener_re = re.compile(r"<<(-?)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")
    for line in lines:
        if delim is not None:
            check = line.strip() if dash else line
            if check == delim:
                delim = None
            continue
        m = opener_re.search(line)
        if m:
            dash = m.group(1) == "-"
            delim = m.group(3)
            out.append(line[: m.start()])
            continue
        out.append(line)
    return "\n".join(out)

text = strip_heredocs(cmd)

# Newlines are statement separators just like ; & | outside quotes, but shlex
# treats \n as plain whitespace and never emits it as a token even when it's
# listed in punctuation_chars — so it can't be caught after the fact. Recode
# every newline to "; " before tokenizing instead. This is safe: shlex's quote
# tracking depends only on unescaped quote characters, not on what ordinary
# character sits in a given position, so a newline that was inside a quoted
# string becomes a literal ";" inside that same string (harmless — we only
# care whether a commit occurred and its target dir, not exact message text);
# a newline that was a real statement separator becomes the ";" boundary token
# we need.
text = text.replace("\n", " ; ")

lex = shlex.shlex(text, posix=True, punctuation_chars="();<>|&")
lex.whitespace_split = True
try:
    tokens = list(lex)
except ValueError:
    # Unbalanced quote etc. — can't safely parse.
    print("UNPARSEABLE")
    sys.exit(0)

BOUNDARY = {";", "&", "&&", "|", "||", "(", ")", "\n"}
VALUE_OPTS = {"-C", "--git-dir", "--work-tree", "-c"}
COMMAND_WRAPPERS = {"command", "builtin"}
ENV_VALUE_OPTS = {"-u", "--unset", "-S", "--split-string"}
ENV_FLAG_OPTS = {"-i", "--ignore-environment", "-0", "--null"}
ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")

commit_dirs = []
last_cd = ""


def skip_env(words, i):
    if i >= len(words) or words[i] != "env":
        return i
    i += 1
    while i < len(words):
        w = words[i]
        if w == "--":
            return i + 1
        if w in ENV_FLAG_OPTS:
            i += 1
            continue
        if w in ENV_VALUE_OPTS:
            i += 2
            continue
        if w.startswith("-u") and len(w) > 2:
            i += 1
            continue
        if ASSIGNMENT_RE.match(w):
            i += 1
            continue
        return i
    return i


def skip_wrappers(words, i):
    while i < len(words):
        before = i
        i = skip_env(words, i)
        if i >= len(words):
            return i
        if words[i] in COMMAND_WRAPPERS:
            i += 1
            while i < len(words) and words[i].startswith("-"):
                i += 1
            continue
        if i == before:
            return i
    return i


def flush_statement(words):
    global last_cd
    if not words:
        return
    i = 0
    while i < len(words) and ASSIGNMENT_RE.match(words[i]):
        i += 1
    i = skip_wrappers(words, i)
    if i >= len(words):
        return
    if words[i] == "cd":
        if i + 1 < len(words):
            last_cd = words[i + 1]
        return
    if words[i] != "git":
        return
    i += 1
    stmt_dir = ""
    subcmd = ""
    while i < len(words):
        w = words[i]
        if w in VALUE_OPTS:
            if w == "-C" and i + 1 < len(words):
                stmt_dir = words[i + 1]
            i += 2
            continue
        if w.startswith("-"):
            i += 1
            continue
        subcmd = w
        break
    if subcmd == "commit":
        commit_dirs.append(stmt_dir if stmt_dir else last_cd)


buf = []
for tok in tokens:
    if tok in BOUNDARY:
        flush_statement(buf)
        buf = []
    else:
        buf.append(tok)
flush_statement(buf)

if commit_dirs:
    print("COMMIT")
    for target in commit_dirs:
        print("DIR:" + target)
else:
    print("NOCOMMIT")
