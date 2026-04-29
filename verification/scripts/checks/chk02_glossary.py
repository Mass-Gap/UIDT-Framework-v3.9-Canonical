import os
import re
import mpmath as mp

mp.mp.dps = 80

def run_check(repo_root):
    status = "PASS"
    messages = []

    formalism_path = os.path.join(repo_root, "FORMALISM.md")
    glossary_path = os.path.join(repo_root, "GLOSSARY.md")

    if not os.path.exists(formalism_path):
        return status, messages
    if not os.path.exists(glossary_path):
        return status, messages

    try:
        with open(formalism_path, 'r', encoding='utf-8') as f:
            formalism_text = f.read()

        with open(glossary_path, 'r', encoding='utf-8') as f:
            glossary_text = f.read()

        terms_in_formalism = []
        for match in re.findall(r'\*\*(.+?)\*\*|\$(.+?)\$', formalism_text):
            term = match[0] if match[0] else match[1]
            term = term.strip()
            # Ignore long math expressions and very short symbols
            # Avoid Category X:, Limitation LX:
            if 3 < len(term) < 50 and not '\\' in term and not 'Category' in term and not 'Limitation' in term and not 'Strict Caveat' in term and not 'Verification' in term and not 'N=99' in term:
                terms_in_formalism.append(term)

        glossary_lower = glossary_text.lower()
        # Find all defined terms in glossary (lines starting with ### or **)
        glossary_terms = []
        for match in re.findall(r'^###\s+(.+?)$|^\*\*(.+?)\*\*', glossary_text, re.MULTILINE):
            term = match[0] if match[0] else match[1]
            if term and len(term.strip()) > 3 and not 'Category' in term and not 'Scientific Legacy' in term:
                glossary_terms.append(term.strip())

        for term in set(terms_in_formalism):
            # Simplistic check
            if term.lower() not in glossary_lower:
                if term.istitle() or ' ' in term:
                    messages.append(f"FAIL: Term '{term}' from FORMALISM.md not in GLOSSARY.md")
                    status = "FAIL"

        formalism_lower = formalism_text.lower()
        for term in glossary_terms:
            if term.lower() not in formalism_lower:
                messages.append(f"WARN: Term '{term}' in GLOSSARY.md not found in FORMALISM.md (Zombie)")
                if status == "PASS":
                    status = "WARN"

    except Exception as e:
        messages.append(f"FAIL: Error processing files - {str(e)}")
        status = "FAIL"

    return status, messages
