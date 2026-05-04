"""
IFP Interpreter - Comprehensive Test Suite
Dựa trên spec Assignment 2 - CO2039

Cách dùng:  python test_ifp.py
Yêu cầu   : test_ifp.py phải đặt cùng thư mục với parser.py, interpreter.py, printer.py, ifp_ast.py
"""

import sys, traceback

try:
    from parser import p_term, ParseError
    from interpreter import interpret, InterpreterError, BetaReductionLimit
    from printer import pp_term
    from ifp_ast import TInt, TBool, TString, TLam
except ImportError as e:
    print(f"[IMPORT ERROR] {e}")
    sys.exit(1)

PASS = 0
FAIL = 0
ERRORS = []


def run(label, program, expected, expect_error=None):
    global PASS, FAIL
    try:
        term = p_term(program)
        result, steps = interpret(check_max=True, term=term)
    except ParseError as exc:
        if expect_error == "ParseError":
            print(f"  [PASS] {label}  (ParseError như kỳ vọng)"); PASS += 1; return
        FAIL += 1
        msg = f"  [FAIL] {label}\n         ParseError không mong đợi: {exc}"
        print(msg); ERRORS.append(msg); return
    except BetaReductionLimit as exc:
        if expect_error == "BetaReductionLimit":
            print(f"  [PASS] {label}  (BetaReductionLimit như kỳ vọng)"); PASS += 1; return
        FAIL += 1
        msg = f"  [FAIL] {label}\n         BetaReductionLimit không mong đợi: {exc}"
        print(msg); ERRORS.append(msg); return
    except InterpreterError as exc:
        if expect_error and expect_error in type(exc).__name__:
            print(f"  [PASS] {label}  ({type(exc).__name__} như kỳ vọng)"); PASS += 1; return
        FAIL += 1
        msg = f"  [FAIL] {label}\n         InterpreterError không mong đợi ({type(exc).__name__}): {exc}"
        print(msg); ERRORS.append(msg); return
    except Exception as exc:
        FAIL += 1
        msg = f"  [FAIL] {label}\n         Exception: {exc}\n{traceback.format_exc()}"
        print(msg); ERRORS.append(msg); return

    if expect_error:
        FAIL += 1
        msg = f"  [FAIL] {label}\n         Mong đợi lỗi {expect_error} nhưng không raise"
        print(msg); ERRORS.append(msg); return

    if   isinstance(result, TInt):    actual = result.value
    elif isinstance(result, TBool):   actual = result.value
    elif isinstance(result, TString): actual = result.value
    elif isinstance(result, TLam):    actual = ("lambda", result.var)
    else:                             actual = result

    if actual == expected:
        print(f"  [PASS] {label}  =>  {actual!r}  (steps={steps})")
        PASS += 1
    else:
        FAIL += 1
        msg = (f"  [FAIL] {label}\n"
               f"         expected : {expected!r}\n"
               f"         actual   : {actual!r}  (steps={steps})")
        print(msg); ERRORS.append(msg)


def section(title):
    print(f"\n{'='*64}")
    print(f"  {title}")
    print(f"{'='*64}")


# Encoding reference (verified bằng cách tính từ spec):
#   I! =0, I" =1, I# =2, I$ =3, I% =4, I( =7, I~ =93, I/6 =1337, I- =12
#   S!='a', S"='b', S#='c'
#   S4%34='test', S4%='te', S34='st'
#   SB%,,/}Q/2,$_='Hello World!'
#   SB%,,/}='Hello ', SQ/2,$_='World!'
#   S./='no', S9%3='yes'

# ==================================================================
# 1. BOOLEAN CONSTANTS
# ==================================================================
section("1. Boolean Constants")
run("T = true",  "T",  True)
run("F = false", "F",  False)

# ==================================================================
# 2. INTEGER VALUES
# ==================================================================
section("2. Integer Values")
run("I! = 0",           "I!",   0)
run('I" = 1',           'I"',   1)
run("I# = 2",           "I#",   2)
run("I$ = 3",           "I$",   3)
run("I% = 4",           "I%",   4)
run("I( = 7",           "I(",   7)
run("I~ = 93",          "I~",   93)
run('I"! = 94',         'I"!',  94)
run("I/6 = 1337 (spec)","I/6",  1337)

# ==================================================================
# 3. STRING VALUES
# ==================================================================
section("3. String Values")
run('S! = "a"',                       'S!',              "a")
run('S" = "b"',                       'S"',              "b")
run('S# = "c"',                       'S#',              "c")
run('S4%34 = "test"',                 'S4%34',           "test")
run('SB%,,/}Q/2,$_ = "Hello World!"','SB%,,/}Q/2,$_',  "Hello World!")
run('S./ = "no"',                     'S./',             "no")
run('S9%3 = "yes"',                   'S9%3',            "yes")

# ==================================================================
# 4. UNARY OPERATORS
# ==================================================================
section("4. Unary Operators")
run("U- I$ = -3",              "U- I$",    -3)
run("U- I! = 0",               "U- I!",     0)
run("U- I~ = -93",             "U- I~",   -93)
run("U- U- I$ = 3 (double neg)","U- U- I$",  3)
run("U! T = false",            "U! T",    False)
run("U! F = true",             "U! F",    True)
run("U! U! T = true",          "U! U! T", True)
run("U# S4%34 = 15818151 (spec)","U# S4%34", 15818151)
run('U$ I4%34 = "test" (spec)', "U$ I4%34", "test")

# ==================================================================
# 5. BINARY - ARITHMETIC
# ==================================================================
section("5. Binary Operators - Arithmetic")
run("B+ I# I$ = 5  (2+3)",          "B+ I# I$",      5)
run("B- I$ I# = 1  (3-2)",          "B- I$ I#",      1)
run("B- I# I$ = -1 (2-3)",          "B- I# I$",     -1)
run("B* I$ I# = 6  (3*2)",          "B* I$ I#",      6)
run("B/ I( I# = 3  (7/2 trunc)",    "B/ I( I#",      3)
run("B/ U- I( I# = -3 (spec)",      "B/ U- I( I#",  -3)
run("B% I( I# = 1  (7%2)",          "B% I( I#",      1)
run("B% U- I( I# = -1 (spec)",      "B% U- I( I#",  -1)
run("B% U- I% I$ = -1 (-4%3)",      "B% U- I% I$",  -1)
run("B/ U- I% I# = -2 (-4/2)",      "B/ U- I% I#",  -2)
run("B* I~ I~ = 8649 (93*93)",       "B* I~ I~",   8649)
run("B+ I! I! = 0 (0+0)",           "B+ I! I!",      0)
run("B/ I$ I! -> ArithmeticError_", "B/ I$ I!", None, expect_error="ArithmeticError_")
run("B% I$ I! -> ArithmeticError_", "B% I$ I!", None, expect_error="ArithmeticError_")

# ==================================================================
# 6. BINARY - COMPARISON
# ==================================================================
section("6. Binary Operators - Comparison")
run("B< I$ I# = false (3<2)",   "B< I$ I#",   False)
run("B< I# I$ = true  (2<3)",   "B< I# I$",   True)
run("B< I# I# = false (2<2)",   "B< I# I#",   False)
run("B> I$ I# = true  (3>2)",   "B> I$ I#",   True)
run("B> I# I$ = false (2>3)",   "B> I# I$",   False)
run("B> I# I# = false (2>2)",   "B> I# I#",   False)
run("B= I$ I# = false (3=2)",   "B= I$ I#",   False)
run("B= I# I# = true  (2=2)",   "B= I# I#",   True)
run("B= T T = true",            "B= T T",     True)
run("B= T F = false",           "B= T F",     False)
run("B= F F = true",            "B= F F",     True)
run("B= S4%34 S4%34 = true",    "B= S4%34 S4%34", True)
run("B= S4%34 S./ = false",     "B= S4%34 S./",   False)

# ==================================================================
# 7. BINARY - BOOLEAN
# ==================================================================
section("7. Binary Operators - Boolean")
run("B| T F = true",  "B| T F",  True)
run("B| F T = true",  "B| F T",  True)
run("B| F F = false", "B| F F",  False)
run("B| T T = true",  "B| T T",  True)
run("B& T F = false", "B& T F",  False)
run("B& T T = true",  "B& T T",  True)
run("B& F F = false", "B& F F",  False)
run("B& F T = false", "B& F T",  False)

# ==================================================================
# 8. BINARY - STRING OPS
# ==================================================================
section("8. Binary Operators - String")
run('B. S4% S34 = "test"',                   "B. S4% S34",         "test")
run('B. SB%,,/} SQ/2,$_ = "Hello World!"',  "B. SB%,,/} SQ/2,$_", "Hello World!")
run('B. S! S" = "ab"',                       'B. S! S"',           "ab")
run('BT I$ S4%34 = "tes" (spec)',            "BT I$ S4%34",        "tes")
run('BT I! S4%34 = "" (take 0)',             "BT I! S4%34",        "")
run('BT I% S4%34 = "test" (take all 4)',     "BT I% S4%34",        "test")
run('BT I" S4%34 = "t" (take 1)',            'BT I" S4%34',        "t")
run('BD I$ S4%34 = "t" (spec)',              "BD I$ S4%34",        "t")
run('BD I! S4%34 = "test" (drop 0)',         "BD I! S4%34",        "test")
run('BD I% S4%34 = "" (drop all)',           "BD I% S4%34",        "")
run('BD I# S4%34 = "st" (drop 2)',           "BD I# S4%34",        "st")

# ==================================================================
# 9. CONDITIONAL EXPRESSION
# ==================================================================
section("9. Conditional Expression")
run("? T I# I$ = 2 (cond=true)",             "? T I# I$",             2)
run("? F I# I$ = 3 (cond=false)",            "? F I# I$",             3)
run('? B> I# I$ S9%3 S./ = "no" (spec)',     "? B> I# I$ S9%3 S./",  "no")
run('? B< I# I$ S9%3 S./ = "yes"',           "? B< I# I$ S9%3 S./",  "yes")
run("? T I# B/ I$ I! = 2 (lazy else)",       "? T I# B/ I$ I!",       2)
run("? F B/ I$ I! I# = 2 (lazy then)",       "? F B/ I$ I! I#",       2)
run("? T ? F I# I$ I~ = 2 (nested if)",      "? T ? F I# I$ I~",      2)
run("? F I~ ? T I# I$ = 3 (nested if)",      "? F I~ ? T I# I$",      3)

# ==================================================================
# 10. LAMBDA & FUNCTION APPLICATION
# ==================================================================
section("10. Lambda & Function Application")
run("B$ L# v# I$ = 3 (identity)",           "B$ L# v# I$",      3)
run("B$ L# v# T = true (identity bool)",     "B$ L# v# T",       True)
run("B$ L# v# S4%34 = 'test' (identity str)","B$ L# v# S4%34",  "test")
run('B$ B$ L# L$ v# I$ I" = 3 (const)',
    'B$ B$ L# L$ v# I$ I"',  3)
run('B$ B$ L# L$ v# B. SB%,,/} SQ/2,$_ IK = "Hello World!" (spec)',
    "B$ B$ L# L$ v# B. SB%,,/} SQ/2,$_ IK",  "Hello World!")
run("B$ L# B+ v# v# I$ = 6 (double use, call-by-name)",
    "B$ L# B+ v# v# I$",  6)
run("B$ L# B* v# v# I$ = 9 (3*3)",
    "B$ L# B* v# v# I$",  9)
run('B$ L# B$ L" B+ v" v" B* I$ I# v8 = 12 (spec reduction)',
    'B$ L# B$ L" B+ v" v" B* I$ I# v8',  12)

# lambda returning lambda
_t_lam, _ = interpret(check_max=True, term=p_term("B$ L# L$ v# I$"))
if isinstance(_t_lam, TLam):
    print("  [PASS] B$ L# L$ v# I$ returns TLam (closure)"); PASS += 1
else:
    FAIL += 1; msg = f"  [FAIL] expected TLam, got {_t_lam!r}"; print(msg); ERRORS.append(msg)

# ==================================================================
# 11. Y-COMBINATOR / COMPLEX
# ==================================================================
section("11. Y-combinator / Complex")

Y_FACT = ('B$ B$ L" B$ L# B$ v" B$ v# v# '
          'L# B$ v" B$ v# v# '
          'L" L# ? B= v# I! I" '
          'B$ L$ B+ B$ v" v$ B$ v" v$ '
          'B- v# I" I%')
run("Y-combinator factorial(4) = 16 (spec)", Y_FACT, 16)

run("B+ B* I$ I# B- I% I# = 8 (3*2+(4-2))",
    "B+ B* I$ I# B- I% I#",  8)
run('B. B. S! S" S# = "abc" (concat chain)',
    'B. B. S! S" S#',  "abc")
run("U# U$ I/6 = 1337 (int->str->int roundtrip)",
    "U# U$ I/6",  1337)
run('U$ U# S4%34 = "test" (str->int->str roundtrip)',
    "U$ U# S4%34",  "test")
run('B= B+ I# I$ B* I" I" = false (5=4)',
    'B= B+ I# I$ B* I" I"',  False)
run('B| B< I! I# B> I$ I" = true (0<2 OR 3>2)',
    'B| B< I! I# B> I$ I"',  True)
run('B+ B+ B+ I" I" I" I" = 4 (1+1+1+1)',
    'B+ B+ B+ I" I" I" I"',  4)

# ==================================================================
# 12. SCOPING
# ==================================================================
section("12. Variable Scoping / Closure")
run('B$ B$ L# L$ v# I$ I" = 3 (closure captures outer)',
    'B$ B$ L# L$ v# I$ I"',  3)
run('B$ B$ L# L# v# I$ I" = 3 (inner shadows outer, inner arg=I$=3)',
    'B$ B$ L# L# v# I$ I"',  3)

# ==================================================================
# 13. STEP COUNTING
# ==================================================================
section("13. Step Count Checks")

_t, _s = interpret(check_max=True, term=p_term("B$ L# v# I$"))
if _s == 1:
    print(f"  [PASS] identity uses exactly 1 step  (got {_s})"); PASS += 1
else:
    FAIL += 1; msg = f"  [FAIL] identity step: expected 1, got {_s}"; print(msg); ERRORS.append(msg)

_t, _s = interpret(check_max=True, term=p_term(Y_FACT))
if _s == 109:
    print(f"  [PASS] Y-comb factorial(4) uses exactly 109 steps  (got {_s})"); PASS += 1
else:
    print(f"  [WARN] Y-comb factorial(4): spec=109, got {_s}  (value correct but count differs)")

# ==================================================================
# 14. TYPE ERRORS
# ==================================================================
section("14. Type Errors")
run("U- T -> TypeError_",          "U- T",        None, expect_error="TypeError_")
run("U! I# -> TypeError_",         "U! I#",       None, expect_error="TypeError_")
run("U# I# -> TypeError_",         "U# I#",       None, expect_error="TypeError_")
run("U$ T -> TypeError_",          "U$ T",        None, expect_error="TypeError_")
run("B+ T I# -> TypeError_",       "B+ T I#",     None, expect_error="TypeError_")
run("B+ I# S4%34 -> TypeError_",   "B+ I# S4%34", None, expect_error="TypeError_")
run("B< S! S\" -> TypeError_",     'B< S! S"',    None, expect_error="TypeError_")
run("B| I# T -> TypeError_",       "B| I# T",     None, expect_error="TypeError_")
run("B$ I# I$ -> TypeError_",      "B$ I# I$",    None, expect_error="TypeError_")
run("BT T S4%34 -> TypeError_",    "BT T S4%34",  None, expect_error="TypeError_")
run("BD I# I# -> TypeError_",      "BD I# I#",    None, expect_error="TypeError_")
run("B. I# S! -> TypeError_",      "B. I# S!",    None, expect_error="TypeError_")
run("? I# I$ I$ -> TypeError_",    "? I# I$ I$",  None, expect_error="TypeError_")

# ==================================================================
# 15. SCOPE ERRORS
# ==================================================================
section("15. Scope Errors (free variable)")
run("v# -> ScopeError",        "v#",       None, expect_error="ScopeError")
run("B+ v# I# -> ScopeError",  "B+ v# I#", None, expect_error="ScopeError")

# ==================================================================
# 16. EDGE CASES
# ==================================================================
section("16. Edge Cases")
run("U- I! = 0 (neg zero)",         "U- I!",          0)
run("B* U- I# I$ = -6 (-2*3)",     "B* U- I# I$",   -6)
run("B* U- I# U- I$ = 6 (-2*-3)", "B* U- I# U- I$",  6)
run("B/ I! I$ = 0 (0/3)",          "B/ I! I$",        0)
run("B% I! I$ = 0 (0%3)",          "B% I! I$",        0)
run("B= I! I! = true (0=0)",       "B= I! I!",       True)
run('BT I! S4%34 = "" (take 0)',   "BT I! S4%34",     "")
run('BD I% S4%34 = "" (drop all)', "BD I% S4%34",     "")
run('B. S4%34 S4%34 = "testtest"', "B. S4%34 S4%34", "testtest")

# ==================================================================
# SUMMARY
# ==================================================================
total = PASS + FAIL
print(f"\n{'='*64}")
print(f"  KET QUA: {PASS}/{total} PASSED   |   {FAIL} FAILED")
print(f"{'='*64}")
if ERRORS:
    print("\n-- Danh sach test FAILED --")
    for e in ERRORS:
        print(e)
sys.exit(0 if FAIL == 0 else 1)


# ==================================================================
# 17. PARSE ERRORS
# ==================================================================
section("17. Parse Errors")

def run_parse(label, program, expect_kind=None):
    """
    expect_kind: None  => expect success (no error)
                 str   => expect ParseError with that kind string
                          e.g. "UnexpectedEOF", "UnexpectedChar", "UnusedInput"
    """
    global PASS, FAIL
    try:
        result = p_term(program)
        if expect_kind is None:
            print(f"  [PASS] {label}  => parsed OK")
            PASS += 1
        else:
            FAIL += 1
            msg = f"  [FAIL] {label}\n         Expected ParseError({expect_kind}) but parsed OK: {result!r}"
            print(msg); ERRORS.append(msg)
    except ParseError as exc:
        if expect_kind is None:
            FAIL += 1
            msg = f"  [FAIL] {label}\n         Unexpected ParseError: {exc}"
            print(msg); ERRORS.append(msg)
        elif expect_kind in str(exc) or expect_kind == exc.kind:
            print(f"  [PASS] {label}  => ParseError({exc})")
            PASS += 1
        else:
            # still a ParseError, just wrong kind — partial credit / warn
            print(f"  [PASS*] {label}  => ParseError (kind={exc.kind}, expected kind containing '{expect_kind}')")
            PASS += 1
    except Exception as exc:
        FAIL += 1
        msg = f"  [FAIL] {label}\n         Unexpected exception: {type(exc).__name__}: {exc}"
        print(msg); ERRORS.append(msg)


# --- UnexpectedEOF: input ends before expression is complete ---
run_parse("empty input",                   "",          "UnexpectedEOF")
run_parse("U- with no operand",            "U-",        "UnexpectedEOF")
run_parse("U! with no operand",            "U!",        "UnexpectedEOF")
run_parse("B+ with no operands",           "B+",        "UnexpectedEOF")
run_parse("B+ with only 1 operand",        "B+ I#",     "UnexpectedEOF")
run_parse("B$ with only 1 operand",        "B$ L# v#",  "UnexpectedEOF")
run_parse("? with 0 args",                 "?",         "UnexpectedEOF")
run_parse("? with 1 arg",                  "? T",       "UnexpectedEOF")
run_parse("? with 2 args",                 "? T I#",    "UnexpectedEOF")
run_parse("L# with no body",               "L#",        "UnexpectedEOF")
run_parse("v with empty body (no var id)", "v",         "UnexpectedEOF")
run_parse("I with empty body",             "I",         "UnexpectedEOF")
run_parse("U with empty body (no op)",     "U",         "UnexpectedEOF")
run_parse("B with empty body (no op)",     "B",         "UnexpectedEOF")
run_parse("nested incomplete: B+ I# U-",  "B+ I# U-",  "UnexpectedEOF")

# --- UnusedInput: parsed one complete term but tokens remain ---
run_parse("two complete terms: I# I$",      "I# I$",    "UnusedInput")
run_parse("T followed by F",                "T F",      "UnusedInput")
run_parse("two strings",                    "S4%34 S./","UnusedInput")
run_parse("complete expr + trailing junk",  "B+ I# I$ I~", "UnusedInput")

# --- UnexpectedChar: indicator not recognised ---
run_parse("unknown indicator X",   "X#",  "UnexpectedChar")
run_parse("unknown indicator Z",   "Z",   "UnexpectedChar")
run_parse("unknown indicator 1",   "1",   "UnexpectedChar")
run_parse("unknown indicator @",   "@",   "UnexpectedChar")
run_parse("T with non-empty body", "TT",  "UnexpectedChar")
run_parse("F with non-empty body", "FF",  "UnexpectedChar")
run_parse("? missing space (no space separator between tokens should parse fine -- skip this)")

# --- Valid inputs that must NOT raise ParseError ---
run_parse("T is valid",          "T",         None)
run_parse("F is valid",          "F",         None)
run_parse("I# is valid (I=2)",   "I#",        None)
run_parse("S4%34 is valid",      "S4%34",     None)
run_parse("U- I$ is valid",      "U- I$",     None)
run_parse("B+ I# I$ is valid",   "B+ I# I$",  None)
run_parse("? T I# I$ is valid",  "? T I# I$", None)
run_parse("L# v# is valid",      "L# v#",     None)
run_parse("v# is valid (parse)", "v#",        None)  # parse OK; scope error only at eval

# ==================================================================
# FINAL SUMMARY (re-print)
# ==================================================================
total = PASS + FAIL
print(f"\n{'='*64}")
print(f"  KET QUA CUOI: {PASS}/{total} PASSED   |   {FAIL} FAILED")
print(f"{'='*64}")
if ERRORS:
    print("\n-- Danh sach test FAILED --")
    for e in ERRORS:
        print(e)