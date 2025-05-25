def extract_section_code(section):
    if isinstance(section, str) and len(section) >= 4:
        return section[-4:]
    return ''