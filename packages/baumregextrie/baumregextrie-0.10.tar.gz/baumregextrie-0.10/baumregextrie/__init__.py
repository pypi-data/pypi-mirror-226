import regex as re
from mymulti_key_dict import MultiKeyDict
from functools import cache


class Trie:
    r"""
    A Trie data structure for efficient pattern matching using regular expressions.

    This class implements a Trie structure optimized for generating regular expressions
    based on a set of words. It allows you to efficiently construct a regular expression
    pattern that matches any of the provided words.

    Attributes:
        data (MultiKeyDict): A multi-key dictionary representing the Trie structure.
        compiled_regex (str): Compiled regular expression pattern.
        _oldhash (int): Hash value of the last compiled regular expression.
        _isbytes (bool): Indicates whether the Trie supports bytes or strings.

    Methods:
        _addbytes(self, word): Add a word to the Trie for byte-based matching.
        _add(self, word: str): Add a word to the Trie for string-based matching.
        _quote(self, char): Return a quoted version of a character for regex escaping.
        _pattern(self, pdata): Generate the regular expression pattern for the Trie.
        _get_pattern(self): Get the current compiled regular expression pattern.
        compile(self, add_before="", add_after="", boundary_right=False, boundary_left=False,
                capture=False, match_whole_line=False, flags=re.IGNORECASE):
            Compile the Trie into a regular expression pattern.
        regex_from_words(self, words: list): Construct the Trie from a list of words.

    Note:
        - The Trie can be used to efficiently generate a regular expression pattern
          that matches any of the provided words.
        - The `compile` method generates the compiled regular expression pattern based on
          Trie data and various optional settings.
        - The `regex_from_words` method constructs the Trie from a list of words.

    Example:

        verbliste1 = 'backen befehlen beginnen beißen bergen bersten beten betten bewegen biegen bieten binden bitten blasen erblassen bleiben braten brechen brennen bringen denken drängen dringen dreschen dürfen empfangen empfehlen erlöschen erschrecken essen fahren fallen fällen fangen fechten finden flechten fliegen fliehen fließen fressen frieren gären gebären geben gedeihen gehen gelangen gelingen gelten genesen genießen geschehen gewinnen gieren gießen gleichen gleiten glimmen graben greifen haben halten hängen hauen heben heißen helfen kennen klingen kneifen kommen können kriechen kriegen laden lassen laufen leiden leihen leiten legen lesen liegen lügen mahlen malen meiden melken messen misslingen mögen missen müssen nehmen nennen pfeifen preisen quellen raten reiben reißen reisen reiten rennen riechen ringen rinnen rufen saufen schaffen scheiden scheinen scheißen schelten schieben schießen schlafen schlagen schleichen schleifen schließen schlingen schlingern schmeißen schmelzen schneiden schreiben schreien schreiten schweigen schwimmen schwinden schwingen schwören sehen sein senden senken singen sinnen sitzen sollen spalten speien spinnen sprechen sprießen springen stechen stecken stehen stehlen steigen sterben stinken stoßen streichen streiten tragen treffen treten triefen trinken trügen tun verderben vergessen verlieren verlöschen wachsen waschen weben weichen weisen wenden werben werden werfen wiegen winden winken wissen wollen wringen zeigen zeihen ziehen zwingen'

        import requests

        binc = requests.get(
            "https://github.com/GITenberg/Der-Tod-in-Venedig_12108/raw/master/12108-8.txt"
        ).content
        unic = binc.decode("utf-8", "ignore")
        t1 = (
            Trie()
            .regex_from_words(verbliste1.split())
            .compile(
                add_before="",
                add_after="",
                boundary_right=False,
                boundary_left=False,
                capture=False,
                match_whole_line=False,
                flags=re.IGNORECASE,
            )
        )
        print(t1.compiled_regex)
        t2 = Trie().regex_from_words(verbliste1.encode().split()).compile()
        print(t2.compiled_regex)
        print(t1.compiled_regex.findall(unic))
        print(t2.compiled_regex.findall(binc))
        t3 = (
            Trie()
            .regex_from_words(verbliste1.split())
            .compile(
                add_before="auf",
                add_after="",
                boundary_right=True,
                boundary_left=False,
                capture=False,
                match_whole_line=False,
                flags=re.IGNORECASE,
            )
        )

        t4 = (
            Trie()
            .regex_from_words([x[:-2] for x in verbliste1.encode().split()])
            .compile(
                add_before=b"auf",
                add_after=rb"(?:[te]*)\b",
                boundary_right=False,
                boundary_left=False,
                capture=False,
                match_whole_line=False,
                flags=re.IGNORECASE,
            )
        )

        print(t3.compiled_regex.findall(unic))
        print(t4.compiled_regex.findall(binc))

        # output
        regex.Regex('(?:b(?:acken|e(?:fehlen|ginnen|ißen|r(?:gen|sten)|t(?:en|ten)|wegen)|i(?:e(?:gen|ten)|nden|tten)|l(?:asen|eiben)|r(?:aten|e(?:chen|nnen)|ingen))|d(?:enken|r(?:eschen|ingen|ängen)|ürfen)|e(?:mpf(?:angen|ehlen)|r(?:blassen|löschen|schrecken)|ssen)|f(?:a(?:hren|llen|ngen)|echten|inden|l(?:echten|ie(?:gen|hen|ßen))|r(?:essen|ieren)|ällen)|g(?:e(?:b(?:en|ären)|deihen|hen|l(?:angen|ingen|ten)|n(?:esen|ießen)|schehen|winnen)|ie(?:ren|ßen)|l(?:ei(?:chen|ten)|immen)|r(?:aben|eifen)|ären)|h(?:a(?:ben|lten|uen)|e(?:ben|ißen|lfen)|ängen)|k(?:ennen|lingen|neifen|ommen|rie(?:chen|gen)|önnen)|l(?:a(?:den|ssen|ufen)|e(?:gen|i(?:den|hen|ten)|sen)|iegen|ügen)|m(?:a(?:hlen|len)|e(?:iden|lken|ssen)|iss(?:en|lingen)|ögen|üssen)|ne(?:hmen|nnen)|p(?:feifen|reisen)|quellen|r(?:aten|e(?:i(?:ben|sen|ten|ßen)|nnen)|i(?:echen|n(?:gen|nen))|ufen)|s(?:aufen|ch(?:affen|e(?:i(?:den|nen|ßen)|lten)|ie(?:ben|ßen)|l(?:a(?:fen|gen)|ei(?:chen|fen)|i(?:eßen|nge(?:rn|n)))|me(?:ißen|lzen)|neiden|rei(?:ben|en|ten)|w(?:eigen|i(?:mmen|n(?:den|gen))|ören))|e(?:hen|in|n(?:den|ken))|i(?:n(?:gen|nen)|tzen)|ollen|p(?:alten|eien|innen|r(?:echen|i(?:eßen|ngen)))|t(?:e(?:c(?:hen|ken)|h(?:en|len)|igen|rben)|inken|oßen|rei(?:chen|ten)))|t(?:r(?:agen|e(?:ffen|ten)|i(?:efen|nken)|ügen)|un)|ver(?:derben|gessen|l(?:ieren|öschen))|w(?:a(?:chsen|schen)|e(?:ben|i(?:chen|sen)|nden|r(?:ben|den|fen))|i(?:egen|n(?:den|ken)|ssen)|ollen|ringen)|z(?:ei(?:gen|hen)|iehen|wingen))', flags=regex.I | regex.V0)
        regex.Regex(b'(?:b(?:acken|e(?:fehlen|ginnen|i\xc3\x9fen|r(?:gen|sten)|t(?:en|ten)|wegen)|i(?:e(?:gen|ten)|nden|tten)|l(?:asen|eiben)|r(?:aten|e(?:chen|nnen)|ingen))|d(?:enken|r(?:eschen|ingen|\xc3\xa4ngen)|\xc3\xbcrfen)|e(?:mpf(?:angen|ehlen)|r(?:blassen|l\xc3\xb6schen|schrecken)|ssen)|f(?:a(?:hren|llen|ngen)|echten|inden|l(?:echten|ie(?:gen|hen|\xc3\x9fen))|r(?:essen|ieren)|\xc3\xa4llen)|g(?:e(?:b(?:en|\xc3\xa4ren)|deihen|hen|l(?:angen|ingen|ten)|n(?:esen|ie\xc3\x9fen)|schehen|winnen)|ie(?:ren|\xc3\x9fen)|l(?:ei(?:chen|ten)|immen)|r(?:aben|eifen)|\xc3\xa4ren)|h(?:a(?:ben|lten|uen)|e(?:ben|i\xc3\x9fen|lfen)|\xc3\xa4ngen)|k(?:ennen|lingen|neifen|ommen|rie(?:chen|gen)|\xc3\xb6nnen)|l(?:a(?:den|ssen|ufen)|e(?:gen|i(?:den|hen|ten)|sen)|iegen|\xc3\xbcgen)|m(?:a(?:hlen|len)|e(?:iden|lken|ssen)|iss(?:en|lingen)|\xc3(?:\xb6gen|\xbcssen))|ne(?:hmen|nnen)|p(?:feifen|reisen)|quellen|r(?:aten|e(?:i(?:ben|sen|ten|\xc3\x9fen)|nnen)|i(?:echen|n(?:gen|nen))|ufen)|s(?:aufen|ch(?:affen|e(?:i(?:den|nen|\xc3\x9fen)|lten)|ie(?:ben|\xc3\x9fen)|l(?:a(?:fen|gen)|ei(?:chen|fen)|i(?:e\xc3\x9fen|nge(?:rn|n)))|me(?:i\xc3\x9fen|lzen)|neiden|rei(?:ben|en|ten)|w(?:eigen|i(?:mmen|n(?:den|gen))|\xc3\xb6ren))|e(?:hen|in|n(?:den|ken))|i(?:n(?:gen|nen)|tzen)|ollen|p(?:alten|eien|innen|r(?:echen|i(?:e\xc3\x9fen|ngen)))|t(?:e(?:c(?:hen|ken)|h(?:en|len)|igen|rben)|inken|o\xc3\x9fen|rei(?:chen|ten)))|t(?:r(?:agen|e(?:ffen|ten)|i(?:efen|nken)|\xc3\xbcgen)|un)|ver(?:derben|gessen|l(?:ieren|\xc3\xb6schen))|w(?:a(?:chsen|schen)|e(?:ben|i(?:chen|sen)|nden|r(?:ben|den|fen))|i(?:egen|n(?:den|ken)|ssen)|ollen|ringen)|z(?:ei(?:gen|hen)|iehen|wingen))', flags=regex.A | regex.I | regex.V0)
        ['sein', 'sein', 'sein', 'tun', 'schwingen', 'sein', 'tun', 'nehmen', 'sein', 'helfen', 'fallen', 'essen', 'sein', 'bringen', 'sein', 'sehen', 'stehen', 'schweigen', 'scheiden', 'treffen', 'gehen', 'lesen', 'sein', 'scheinen', 'verlieren', 'lassen', 'sein', 'essen', 'sein', 'tun', 'treten', 'sehen', 'wachsen', 'fallen', 'essen', 'sein', 'sehen', 'kommen', 'sehen', 'essen', 'sein', 'wachsen', 'sein', 'sein', 'sein', 'tun', 'hauen', 'gehen', 'sein', 'sein', 'lassen', 'sein', 'reiben', 'zwingen', 'haben', 'vergessen', 'sein', 'haben', 'sein', 'tun', 'sein', 'stehen', 'treten', 'Leiden', 'sein', 'hauen', 'Werden', 'gehen', 'weben', 'sehen', 'sein', 'sein', 'Reisen', 'werden', 'sein', 'tun', 'sein', 'gewinnen', 'lassen', 'sein', 'sein', 'werden', 'laufen', 'sein', 'Sein', 'geben', 'weisen', 'sein', 'sein', 'wissen', 'sein', 'kommen', 'tun', 'sehen', 'Vergessen', 'leiden', 'sein', 'wachsen', 'wissen', 'raten', 'brechen', 'sein', 'lassen', 'wollen', 'brechen', 'kommen', 'sein', 'tragen', 'sein', 'sein', 'lassen', 'sein', 'Essen', 'sein', 'stehen', 'tun', 'sein', 'Reisen', 'steigen', 'halten', 'essen', 'sein', 'sein', 'leiden', 'tun', 'Sein', 'fahren', 'tun', 'kommen', 'sein', 'wissen', 'stehen', 'sein', 'sein', 'sein', 'sein', 'sein', 'sein', 'sein', 'schaffen', 'reiten', 'gewinnen', 'tun', 'sein', 'Sehen', 'sein', 'sein', 'rufen', 'wachsen', 'kennen', 'sein', 'sein', 'geben', 'sein', 'halten', 'sein', 'leiten', 'werden', 'halten', 'nennen', 'sein', 'sein', 'tragen', 'gehen', 'sein', 'wenden', 'schieben', 'sein', 'wissen', 'tun', 'sein', 'sein', 'halten', 'sein', 'tun', 'sein', 'stehen', 'wissen', 'reiten', 'lassen', 'Leiden', 'kommen', 'sein', 'sein', 'sein', 'gehen', 'sein', 'tun', 'tun', 'stehen', 'schwingen', 'werfen', 'tun', 'halten', 'tun', 'tun', 'gewinnen', 'sein', 'sein', 'raten', 'sein', 'lassen', 'tun', 'leiden', 'mahlen', 'geben', 'raten', 'sein', 'sein', 'halten', 'wissen', 'Wissen', 'sehen', 'Leiden', 'weichen', 'sein', 'gehen', 'stehen', 'zeihen', 'fangen', 'sein', 'sein', 'Wissen', 'senden', 'laufen', 'nehmen', 'raten', 'Leiden', 'tun', 'sein', 'tun', 'stehen', 'halten', 'wissen', 'sein', 'sein', 'saufen', 'halten', 'essen', 'Sein', 'Sein', 'spalten', 'leiden', 'sein', 'sehen', 'sein', 'Leiden', 'bringen', 'sein', 'tun', 'legen', 'sein', 'gewinnen', 'sein', 'haben', 'sein', 'sein', 'weichen', 'reisen', 'wollen', 'sein', 'sein', 'schreiten', 'treten', 'Reisen', 'laufen', 'essen', 'sein', 'Reisen', 'sein', 'fahren', 'werden', 'fallen', 'tun', 'tun', 'heben', 'nehmen', 'sein', 'fallen', 'sein', 'sein', 'sein', 'ringen', 'sein', 'gleichen', 'sein', 'sein', 'schlafen', 'greifen', 'tun', 'sein', 'Schwimmen', 'Erschrecken', 'sehen', 'sein', 'schlagen', 'sein', 'Befehlen', 'waschen', 'tun', 'sein', 'Reisen', 'tun', 'sehen', 'kommen', 'reiten', 'messen', 'essen', 'sehen', 'geschehen', 'empfangen', 'sein', 'sein', 'fahren', 'halten', 'sein', 'malen', 'werden', 'tun', 'kommen', 'kommen', 'sehen', 'reisen', 'sein', 'Sein', 'halten', 'halten', 'fallen', 'sein', 'sein', 'treten', 'hauen', 'treten', 'lassen', 'beginnen', 'stehen', 'sein', 'bringen', 'nehmen', 'sein', 'haben', 'sein', 'steigen', 'sein', 'kommen', 'Sein', 'sein', 'reisen', 'weichen', 'sein', 'halten', 'steigen', 'kommen', 'sein', 'lassen', 'nehmen', 'Reisen', 'sein', 'gleiten', 'nehmen', 'schlagen', 'sein', 'sein', 'sein', 'sein', 'stehen', 'essen', 'Sein', 'sein', 'scheinen', 'schaffen', 'sein', 'sein', 'fahren', 'lassen', 'geben', 'werden', 'tun', 'Reisen', 'sein', 'lassen', 'gehen', 'sein', 'sein', 'fallen', 'sein', 'sein', 'rufen', 'sehen', 'werden', 'geben', 'fahren', 'wollen', 'sehen', 'fahren', 'haben', 'gleichen', 'halten', 'wiegen', 'fahren', 'sein', 'sein', 'haben', 'fahren', 'sein', 'bringen', 'empfangen', 'sein', 'nehmen', 'essen', 'sein', 'tun', 'sein', 'tun', 'Schweigen', 'werden', 'sein', 'sein', 'Reisen', 'bieten', 'denken', 'geben', 'wissen', 'sein', 'sein', 'fahren', 'sein', 'tun', 'leiden', 'sein', 'tun', 'Essen', 'tun', 'sein', 'nehmen', 'tun', 'wachsen', 'kommen', 'Sein', 'fallen', 'hauen', 'haben', 'halten', 'tun', 'wachsen', 'gelten', 'scheinen', 'wenden', 'sein', 'sein', 'legen', 'essen', 'sein', 'malen', 'sein', 'sein', 'tun', 'sein', 'leiden', 'sein', 'tragen', 'schaffen', 'kennen', 'bringen', 'kommen', 'rinnen', 'heben', 'tun', 'messen', 'sein', 'halten', 'sein', 'sein', 'tun', 'sehen', 'fallen', 'tun', 'tun', 'sein', 'sein', 'weisen', 'gehen', 'sein', 'wissen', 'weisen', 'sitzen', 'halten', 'treten', 'sein', 'sein', 'finden', 'Fliehen', 'lassen', 'sein', 'sein', 'Bleiben', 'halten', 'sein', 'schlafen', 'essen', 'sein', 'Sein', 'Gehen', 'tun', 'sein', 'sein', 'hauen', 'sein', 'springen', 'leiden', 'weisen', 'sitzen', 'rufen', 'bleiben', 'sein', 'verlieren', 'sein', 'gleiten', 'schwimmen', 'brechen', 'bergen', 'sein', 'kommen', 'essen', 'kommen', 'sein', 'kommen', 'bewegen', 'stehen', 'tun', 'sein', 'Sein', 'sein', 'sein', 'werfen', 'tun', 'wenden', 'sehen', 'Leiden', 'sein', 'scheinen', 'sein', 'nehmen', 'sein', 'sein', 'sein', 'wissen', 'rufen', 'sein', 'messen', 'sein', 'Sein', 'tun', 'lassen', 'reiben', 'Bleiben', 'tun', 'sein', 'Graben', 'legen', 'rufen', 'winken', 'sein', 'sein', 'sein', 'rufen', 'sein', 'rufen', 'Reisen', 'dringen', 'tun', 'raten', 'messen', 'kommen', 'sein', 'sein', 'sein', 'sein', 'sein', 'weichen', 'sein', 'schlagen', 'sehen', 'triefen', 'kommen', 'sein', 'bleiben', 'sein', 'sein', 'legen', 'essen', 'sein', 'sein', 'fahren', 'rinnen', 'sein', 'sein', 'sein', 'sein', 'treffen', 'sein', 'fallen', 'sein', 'sein', 'weben', 'sein', 'schlagen', 'werden', 'geben', 'tun', 'sein', 'riechen', 'sein', 'sein', 'sein', 'sein', 'halten', 'sein', 'bringen', 'tun', 'vergessen', 'finden', 'reisen', 'schlagen', 'nehmen', 'gelten', 'leiten', 'gelangen', 'sein', 'sehen', 'reisen', 'sein', 'lesen', 'sein', 'kommen', 'stehen', 'sein', 'halten', 'kommen', 'lassen', 'fahren', 'wollen', 'finden', 'Reisen', 'bringen', 'tun', 'sein', 'reisen', 'schaffen', 'treten', 'fahren', 'sein', 'nehmen', 'geben', 'sein', 'kommen', 'lassen', 'haben', 'sein', 'Sein', 'gehen', 'brechen', 'scheiden', 'sein', 'schlagen', 'sein', 'kommen', 'tragen', 'geben', 'Leiden', 'lassen', 'nehmen', 'sein', 'fliehen', 'sein', 'sein', 'Tun', 'sehen', 'sehen', 'lassen', 'wachsen', 'sehen', 'halten', 'tragen', 'kennen', 'essen', 'steigen', 'verlieren', 'sein', 'schaffen', 'geben', 'geben', 'treten', 'tun', 'sein', 'halten', 'sein', 'reisen', 'treffen', 'nehmen', 'werden', 'werden', 'gewinnen', 'Reisen', 'sein', 'schlagen', 'tun', 'sehen', 'sein', 'sein', 'laufen', 'sein', 'geben', 'stehen', 'lassen', 'sein', 'malen', 'sein', 'geben', 'tun', 'kommen', 'sein', 'sein', 'sein', 'sein', 'sein', 'tun', 'sein', 'denken', 'gleichen', 'sein', 'sein', 'sein', 'sehen', 'sein', 'Sein', 'sein', 'sein', 'heben', 'reiten', 'kommen', 'lassen', 'nehmen', 'sein', 'sein', 'tun', 'dringen', 'liegen', 'halten', 'sein', 'sehen', 'scheinen', 'sein', 'Sein', 'tun', 'bringen', 'sein', 'zeigen', 'sein', 'sein', 'reiten', 'legen', 'sein', 'sein', 'Wollen', 'sein', 'schmelzen', 'sein', 'Bergen', 'sein', 'Ringen', 'steigen', 'rinnen', 'geben', 'legen', 'brechen', 'halten', 'tun', 'sein', 'sehen', 'kommen', 'treten', 'Erschrecken', 'sein', 'Kommen', 'sein', 'sein', 'reiben', 'Graben', 'Schwimmen', 'rufen', 'sein', 'laufen', 'zeigen', 'fangen', 'laufen', 'sein', 'sein', 'haben', 'sein', 'rufen', 'sein', 'Sein', 'sein', 'Sein', 'raten', 'sein', 'sein', 'sein', 'scheinen', 'kommen', 'reiben', 'Leiden', 'Sein', 'greifen', 'kommen', 'tun', 'kommen', 'Sein', 'sein', 'sein', 'sein', 'tun', 'heben', 'zeigen', 'finden', 'Liegen', 'halten', 'werben', 'Erschrecken', 'sein', 'denken', 'kommen', 'sehen', 'scheinen', 'empfangen', 'tragen', 'scheinen', 'gehen', 'brennen', 'schlagen', 'werden', 'schreiben', 'schaffen', 'brennen', 'kennen', 'nehmen', 'lassen', 'laufen', 'sein', 'sein', 'lassen', 'sein', 'Schreiben', 'nehmen', 'sein', 'lassen', 'sein', 'tragen', 'tun', 'sein', 'sein', 'sein', 'lesen', 'schwingen', 'sein', 'sein', 'Quellen', 'heben', 'tun', 'sein', 'sein', 'wissen', 'lassen', 'legen', 'wissen', 'sein', 'sein', 'sein', 'legen', 'sein', 'sprechen', 'gehen', 'sein', 'werden', 'sein', 'hauen', 'tun', 'wollen', 'sein', 'tun', 'scheiden', 'wissen', 'sein', 'haben', 'sein', 'sein', 'haben', 'sein', 'sein', 'Sein', 'fahren', 'sein', 'gehen', 'Sein', 'dringen', 'Erschrecken', 'sein', 'sein', 'sein', 'gehen', 'werden', 'Scheinen', 'sein', 'sein', 'sein', 'sein', 'rennen', 'springen', 'sein', 'hauen', 'sehen', 'sterben', 'treffen', 'erblassen', 'sein', 'kennen', 'halten', 'tun', 'dringen', 'sein', 'sein', 'Sein', 'legen', 'sein', 'treten', 'gehen', 'sein', 'sein', 'tun', 'wenden', 'sein', 'Sein', 'sein', 'preisen', 'geben', 'sein', 'malen', 'sein', 'sprechen', 'sein', 'sein', 'empfangen', 'fliehen', 'laufen', 'stehen', 'sein', 'treffen', 'steigen', 'sein', 'sein', 'bleiben', 'haben', 'legen', 'schlagen', 'sehen', 'sein', 'sitzen', 'sein', 'dringen', 'sein', 'sein', 'liegen', 'Laden', 'meiden', 'sein', 'stehen', 'tun', 'schweigen', 'schweigen', 'sein', 'raten', 'Leiden', 'brechen', 'kommen', 'sein', 'finden', 'sein', 'essen', 'legen', 'reisen', 'wissen', 'treten', 'schlagen', 'sein', 'Sinnen', 'lassen', 'gewinnen', 'lassen', 'stehen', 'bleiben', 'lassen', 'weichen', 'kommen', 'sein', 'sein', 'treten', 'Sein', 'halten', 'sprechen', 'legen', 'wissen', 'werden', 'sein', 'bringen', 'riechen', 'liegen', 'sein', 'sein', 'sein', 'ziehen', 'wiegen', 'sein', 'gleichen', 'sein', 'weben', 'sein', 'geben', 'gehen', 'lassen', 'kommen', 'sein', 'rennen', 'werden', 'halten', 'sein', 'tun', 'sein', 'fahren', 'denken', 'tun', 'tun', 'sein', 'tun', 'lassen', 'reiben', 'nennen', 'scheinen', 'sein', 'sehen', 'sein', 'tragen', 'geschehen', 'Bitten', 'sein', 'sein', 'sein', 'Leiden', 'essen', 'fahren', 'tun', 'laufen', 'treten', 'denken', 'haben', 'Wissen', 'gehen', 'Schweigen', 'treten', 'senden', 'nehmen', 'werden', 'halten', 'tun', 'fallen', 'lassen', 'sein', 'sein', 'gieren', 'sein', 'gehen', 'Sein', 'Leiden', 'nehmen', 'Sein', 'sein', 'schaffen', 'tun', 'tragen', 'nehmen', 'sein', 'sein', 'essen', 'sein', 'halten', 'kommen', 'sein', 'sein', 'halten', 'nehmen', 'sein', 'weisen', 'sein', 'wissen', 'essen', 'tun', 'essen', 'sein', 'bringen', 'Sein', 'sein', 'tun', 'sein', 'sein', 'wollen', 'halten', 'Sein', 'sein', 'sein', 'sein', 'sein', 'lassen', 'weichen', 'sein', 'fallen', 'Sein', 'essen', 'sein', 'sein', 'sein', 'sein', 'sein', 'gehen', 'ziehen', 'sein', 'sein', 'sein', 'sein', 'legen', 'gleichen', 'stehen', 'fallen', 'gehen', 'klingen', 'sein', 'wiegen', 'sein', 'lassen', 'Sein', 'haben', 'tun', 'sein', 'sein', 'sein', 'geben', 'stecken', 'lassen', 'sein', 'sein', 'fangen', 'sein', 'halten', 'sein', 'bergen', 'legen', 'werden', 'sein', 'essen', 'sein', 'Sein', 'sein', 'Sein', 'sein', 'sein', 'sein', 'geben', 'legen', 'sein', 'liegen', 'tun', 'werden', 'sein', 'schlagen', 'tun', 'sein', 'stehen', 'sein', 'tun', 'tragen', 'sein', 'halten', 'sein', 'sein', 'weichen', 'wollen', 'gelten', 'sein', 'halten', 'sein', 'Sterben', 'fallen', 'tun', 'fahren', 'fallen', 'reiben', 'tun', 'finden', 'tun', 'schweigen', 'halten', 'sein', 'treten', 'gehen', 'wachsen', 'fallen', 'scheiden', 'reisen', 'lassen', 'wissen', 'schlagen', 'sprechen', 'Reisen', 'legen', 'wenden', 'fliehen', 'wollen', 'geben', 'gehen', 'scheinen', 'sein', 'sein', 'schweigen', 'schweigen', 'sein', 'sein', 'sein', 'sein', 'weben', 'schreiten', 'tun', 'sein', 'sein', 'werfen', 'sein', 'sein', 'kommen', 'sein', 'dringen', 'nennen', 'sein', 'schreien', 'schleifen', 'weichen', 'sein', 'sein', 'sein', 'Sein', 'laufen', 'sein', 'sein', 'sein', 'sein', 'fallen', 'halten', 'essen', 'halten', 'weichen', 'sein', 'fangen', 'bleiben', 'sein', 'Sterben', 'fallen', 'sein', 'sein', 'sein', 'sein', 'sein', 'sein', 'legen', 'sein', 'messen', 'sein', 'geben', 'tun', 'sein', 'sein', 'heben', 'tragen', 'sein', 'schwinden', 'kriechen', 'Sein', 'sein', 'kommen', 'reiben', 'gleichen', 'verlieren', 'gehen', 'sein', 'sein', 'Sein', 'sein', 'sein', 'sein', 'sein', 'tun', 'malen', 'geben', 'lassen', 'Sein', 'sein', 'sein', 'laden', 'Gehen', 'lassen', 'sein', 'Wissen', 'wachsen', 'essen', 'essen', 'essen', 'halten', 'sein', 'bergen', 'treten', 'sein', 'sein', 'gewinnen', 'wissen', 'gehen', 'sein', 'Leiden', 'bleiben', 'sein', 'gehen', 'bleiben', 'tun', 'bieten', 'nehmen', 'tun', 'gewinnen', 'wenden', 'senden', 'wissen', 'stehen', 'zeihen', 'tun', 'werfen', 'fangen', 'fangen', 'sein', 'schwingen', 'leiden', 'tun', 'wissen', 'steigen', 'sein', 'liegen', 'essen', 'sein', 'fallen', 'wissen', 'lassen', 'liegen', 'essen', 'halten', 'sein', 'Sein', 'sein', 'tun', 'sein', 'rufen', 'tun', 'nehmen', 'legen', 'sein', 'essen', 'halten', 'Sein', 'tun', 'springen', 'sein', 'bitten', 'sein', 'tun', 'haben', 'sein', 'sein', 'dringen', 'schreiten', 'stehen', 'sein', 'hauen', 'essen', 'sein', 'Sein', 'Schreiten', 'sein', 'sein', 'sein', 'sein', 'tun', 'tun']
        [b'sein', b'sein', b'sein', b'tun', b'schwingen', b'sein', b'tun', b'nehmen', b'sein', b'helfen', b'fallen', b'essen', b'sein', b'bringen', b'sein', b'sehen', b'stehen', b'schweigen', b'scheiden', b'treffen', b'gehen', b'lesen', b'sein', b'scheinen', b'verlieren', b'lassen', b'sein', b'essen', b'sein', b'tun', b'treten', b'sehen', b'wachsen', b'fallen', b'essen', b'sein', b'sehen', b'kommen', b'sehen', b'essen', b'sein', b'wachsen', b'sein', b'sein', b'sein', b'tun', b'hauen', b'gehen', b'sein', b'sein', b'lassen', b'sein', b'reiben', b'zwingen', b'haben', b'vergessen', b'sein', b'haben', b'sein', b'tun', b'sein', b'stehen', b'treten', b'Leiden', b'sein', b'hauen', b'Werden', b'gehen', b'weben', b'sehen', b'sein', b'sein', b'Reisen', b'werden', b'sein', b'tun', b'sein', b'gewinnen', b'lassen', b'sein', b'sein', b'werden', b'laufen', b'sein', b'Sein', b'geben', b'weisen', b'sein', b'sein', b'wissen', b'sein', b'kommen', b'tun', b'sehen', b'Vergessen', b'leiden', b'sein', b'wachsen', b'wissen', b'raten', b'brechen', b'sein', b'lassen', b'wollen', b'brechen', b'kommen', b'sein', b'tragen', b'sein', b'sein', b'lassen', b'sein', b'Essen', b'sein', b'stehen', b'tun', b'sein', b'Reisen', b'steigen', b'halten', b'essen', b'sein', b'sein', b'leiden', b'tun', b'Sein', b'fahren', b'tun', b'kommen', b'sein', b'wissen', b'stehen', b'sein', b'sein', b'sein', b'sein', b'sein', b'sein', b'sein', b'schaffen', b'reiten', b'gewinnen', b'tun', b'sein', b'Sehen', b'sein', b'sein', b'rufen', b'wachsen', b'kennen', b'sein', b'sein', b'geben', b'sein', b'halten', b'sein', b'leiten', b'werden', b'halten', b'nennen', b'sein', b'sein', b'tragen', b'gehen', b'sein', b'wenden', b'schieben', b'sein', b'wissen', b'tun', b'sein', b'sein', b'halten', b'sein', b'tun', b'sein', b'stehen', b'wissen', b'reiten', b'lassen', b'Leiden', b'kommen', b'sein', b'sein', b'sein', b'gehen', b'sein', b'tun', b'tun', b'stehen', b'schwingen', b'werfen', b'tun', b'halten', b'tun', b'tun', b'gewinnen', b'sein', b'sein', b'raten', b'sein', b'lassen', b'tun', b'leiden', b'mahlen', b'geben', b'raten', b'sein', b'sein', b'halten', b'wissen', b'Wissen', b'sehen', b'Leiden', b'weichen', b'sein', b'gehen', b'stehen', b'zeihen', b'fangen', b'sein', b'sein', b'Wissen', b'senden', b'laufen', b'nehmen', b'raten', b'Leiden', b'tun', b'sein', b'tun', b'stehen', b'halten', b'wissen', b'sein', b'sein', b'saufen', b'halten', b'essen', b'Sein', b'Sein', b'spalten', b'leiden', b'sein', b'sehen', b'sein', b'Leiden', b'bringen', b'sein', b'tun', b'legen', b'sein', b'gewinnen', b'sein', b'haben', b'sein', b'sein', b'weichen', b'reisen', b'wollen', b'sein', b'sein', b'schreiten', b'treten', b'Reisen', b'laufen', b'essen', b'sein', b'Reisen', b'sein', b'fahren', b'werden', b'fallen', b'tun', b'tun', b'heben', b'nehmen', b'sein', b'fallen', b'sein', b'sein', b'sein', b'ringen', b'sein', b'gleichen', b'sein', b'sein', b'schlafen', b'greifen', b'tun', b'sein', b'Schwimmen', b'Erschrecken', b'sehen', b'sein', b'schlagen', b'sein', b'Befehlen', b'waschen', b'tun', b'sein', b'Reisen', b'tun', b'sehen', b'kommen', b'reiten', b'messen', b'essen', b'sehen', b'geschehen', b'empfangen', b'sein', b'sein', b'fahren', b'halten', b'sein', b'malen', b'werden', b'tun', b'kommen', b'kommen', b'sehen', b'reisen', b'sein', b'Sein', b'halten', b'halten', b'fallen', b'sein', b'sein', b'treten', b'hauen', b'treten', b'lassen', b'beginnen', b'stehen', b'sein', b'bringen', b'nehmen', b'sein', b'haben', b'sein', b'steigen', b'sein', b'kommen', b'Sein', b'sein', b'reisen', b'weichen', b'sein', b'halten', b'steigen', b'kommen', b'sein', b'lassen', b'nehmen', b'Reisen', b'sein', b'gleiten', b'nehmen', b'schlagen', b'sein', b'sein', b'sein', b'sein', b'stehen', b'essen', b'Sein', b'sein', b'scheinen', b'schaffen', b'sein', b'sein', b'fahren', b'lassen', b'geben', b'werden', b'tun', b'Reisen', b'sein', b'lassen', b'gehen', b'sein', b'sein', b'fallen', b'sein', b'sein', b'rufen', b'sehen', b'werden', b'geben', b'fahren', b'wollen', b'sehen', b'fahren', b'haben', b'gleichen', b'halten', b'wiegen', b'fahren', b'sein', b'sein', b'haben', b'fahren', b'sein', b'bringen', b'empfangen', b'sein', b'nehmen', b'essen', b'sein', b'tun', b'sein', b'tun', b'Schweigen', b'werden', b'sein', b'sein', b'Reisen', b'bieten', b'denken', b'geben', b'wissen', b'sein', b'sein', b'fahren', b'sein', b'tun', b'leiden', b'sein', b'tun', b'Essen', b'tun', b'sein', b'nehmen', b'tun', b'wachsen', b'kommen', b'Sein', b'fallen', b'hauen', b'haben', b'halten', b'tun', b'wachsen', b'gelten', b'scheinen', b'wenden', b'sein', b'sein', b'legen', b'essen', b'sein', b'malen', b'sein', b'sein', b'tun', b'sein', b'leiden', b'sein', b'tragen', b'schaffen', b'kennen', b'bringen', b'kommen', b'rinnen', b'heben', b'tun', b'messen', b'sein', b'halten', b'sein', b'sein', b'tun', b'sehen', b'fallen', b'tun', b'tun', b'sein', b'sein', b'weisen', b'gehen', b'sein', b'wissen', b'weisen', b'sitzen', b'halten', b'treten', b'sein', b'sein', b'finden', b'Fliehen', b'lassen', b'sein', b'sein', b'Bleiben', b'halten', b'sein', b'schlafen', b'essen', b'sein', b'Sein', b'Gehen', b'tun', b'sein', b'sein', b'hauen', b'sein', b'springen', b'leiden', b'weisen', b'sitzen', b'rufen', b'bleiben', b'sein', b'verlieren', b'sein', b'gleiten', b'schwimmen', b'brechen', b'bergen', b'sein', b'kommen', b'essen', b'kommen', b'sein', b'kommen', b'bewegen', b'stehen', b'tun', b'sein', b'Sein', b'sein', b'sein', b'werfen', b'tun', b'wenden', b'sehen', b'Leiden', b'sein', b'scheinen', b'sein', b'nehmen', b'sein', b'sein', b'sein', b'wissen', b'rufen', b'sein', b'messen', b'sein', b'Sein', b'tun', b'lassen', b'reiben', b'Bleiben', b'tun', b'sein', b'Graben', b'legen', b'rufen', b'winken', b'sein', b'sein', b'sein', b'rufen', b'sein', b'rufen', b'Reisen', b'dringen', b'tun', b'raten', b'messen', b'kommen', b'sein', b'sein', b'sein', b'sein', b'sein', b'weichen', b'sein', b'schlagen', b'sehen', b'triefen', b'kommen', b'sein', b'bleiben', b'sein', b'sein', b'legen', b'essen', b'sein', b'sein', b'fahren', b'rinnen', b'sein', b'sein', b'sein', b'sein', b'treffen', b'sein', b'fallen', b'sein', b'sein', b'weben', b'sein', b'schlagen', b'werden', b'geben', b'tun', b'sein', b'riechen', b'sein', b'sein', b'sein', b'sein', b'halten', b'sein', b'bringen', b'tun', b'vergessen', b'finden', b'reisen', b'schlagen', b'nehmen', b'gelten', b'leiten', b'gelangen', b'sein', b'sehen', b'reisen', b'sein', b'lesen', b'sein', b'kommen', b'stehen', b'sein', b'halten', b'kommen', b'lassen', b'fahren', b'wollen', b'finden', b'Reisen', b'bringen', b'tun', b'sein', b'reisen', b'schaffen', b'treten', b'fahren', b'sein', b'nehmen', b'geben', b'sein', b'kommen', b'lassen', b'haben', b'sein', b'Sein', b'gehen', b'brechen', b'scheiden', b'sein', b'schlagen', b'sein', b'kommen', b'tragen', b'geben', b'Leiden', b'lassen', b'nehmen', b'sein', b'fliehen', b'sein', b'sein', b'Tun', b'sehen', b'sehen', b'lassen', b'wachsen', b'sehen', b'halten', b'tragen', b'kennen', b'essen', b'steigen', b'verlieren', b'sein', b'schaffen', b'geben', b'geben', b'treten', b'tun', b'sein', b'halten', b'sein', b'reisen', b'treffen', b'nehmen', b'werden', b'werden', b'gewinnen', b'Reisen', b'sein', b'schlagen', b'tun', b'sehen', b'sein', b'sein', b'laufen', b'sein', b'geben', b'stehen', b'lassen', b'sein', b'malen', b'sein', b'geben', b'tun', b'kommen', b'sein', b'sein', b'sein', b'sein', b'sein', b'tun', b'sein', b'denken', b'gleichen', b'sein', b'sein', b'sein', b'sehen', b'sein', b'Sein', b'sein', b'sein', b'heben', b'reiten', b'kommen', b'lassen', b'nehmen', b'sein', b'sein', b'tun', b'dringen', b'liegen', b'halten', b'sein', b'sehen', b'scheinen', b'sein', b'Sein', b'tun', b'bringen', b'sein', b'zeigen', b'sein', b'sein', b'reiten', b'legen', b'sein', b'sein', b'Wollen', b'sein', b'schmelzen', b'sein', b'Bergen', b'sein', b'Ringen', b'steigen', b'rinnen', b'geben', b'legen', b'brechen', b'halten', b'tun', b'sein', b'sehen', b'kommen', b'treten', b'Erschrecken', b'sein', b'Kommen', b'sein', b'sein', b'reiben', b'Graben', b'Schwimmen', b'rufen', b'sein', b'laufen', b'zeigen', b'fangen', b'laufen', b'sein', b'sein', b'haben', b'sein', b'rufen', b'sein', b'Sein', b'sein', b'Sein', b'raten', b'sein', b'sein', b'sein', b'scheinen', b'kommen', b'reiben', b'Leiden', b'Sein', b'greifen', b'kommen', b'tun', b'kommen', b'Sein', b'sein', b'sein', b'sein', b'tun', b'heben', b'zeigen', b'finden', b'Liegen', b'halten', b'werben', b'Erschrecken', b'sein', b'denken', b'kommen', b'sehen', b'scheinen', b'empfangen', b'tragen', b'scheinen', b'gehen', b'brennen', b'schlagen', b'werden', b'schreiben', b'schaffen', b'brennen', b'kennen', b'nehmen', b'lassen', b'laufen', b'sein', b'sein', b'lassen', b'sein', b'Schreiben', b'nehmen', b'sein', b'lassen', b'sein', b'tragen', b'tun', b'sein', b'sein', b'sein', b'lesen', b'schwingen', b'sein', b'sein', b'Quellen', b'heben', b'tun', b'sein', b'sein', b'wissen', b'lassen', b'legen', b'wissen', b'sein', b'sein', b'sein', b'legen', b'sein', b'sprechen', b'gehen', b'sein', b'werden', b'sein', b'hauen', b'tun', b'wollen', b'sein', b'tun', b'scheiden', b'wissen', b'sein', b'haben', b'sein', b'sein', b'haben', b'sein', b'sein', b'Sein', b'fahren', b'sein', b'gehen', b'Sein', b'dringen', b'Erschrecken', b'sein', b'sein', b'sein', b'gehen', b'werden', b'Scheinen', b'sein', b'sein', b'sein', b'sein', b'rennen', b'springen', b'sein', b'hauen', b'sehen', b'sterben', b'treffen', b'erblassen', b'sein', b'kennen', b'halten', b'tun', b'dringen', b'sein', b'sein', b'Sein', b'legen', b'sein', b'treten', b'gehen', b'sein', b'sein', b'tun', b'wenden', b'sein', b'Sein', b'sein', b'preisen', b'geben', b'sein', b'malen', b'sein', b'sprechen', b'sein', b'sein', b'empfangen', b'fliehen', b'laufen', b'stehen', b'sein', b'treffen', b'steigen', b'sein', b'sein', b'bleiben', b'haben', b'legen', b'schlagen', b'sehen', b'sein', b'sitzen', b'sein', b'dringen', b'sein', b'sein', b'liegen', b'Laden', b'meiden', b'sein', b'stehen', b'tun', b'schweigen', b'schweigen', b'sein', b'raten', b'Leiden', b'brechen', b'kommen', b'sein', b'finden', b'sein', b'essen', b'legen', b'reisen', b'wissen', b'treten', b'schlagen', b'sein', b'Sinnen', b'lassen', b'gewinnen', b'lassen', b'stehen', b'bleiben', b'lassen', b'weichen', b'kommen', b'sein', b'sein', b'treten', b'Sein', b'halten', b'sprechen', b'legen', b'wissen', b'werden', b'sein', b'bringen', b'riechen', b'liegen', b'sein', b'sein', b'sein', b'ziehen', b'wiegen', b'sein', b'gleichen', b'sein', b'weben', b'sein', b'geben', b'gehen', b'lassen', b'kommen', b'sein', b'rennen', b'werden', b'halten', b'sein', b'tun', b'sein', b'fahren', b'denken', b'tun', b'tun', b'sein', b'tun', b'lassen', b'reiben', b'nennen', b'scheinen', b'sein', b'sehen', b'sein', b'tragen', b'geschehen', b'Bitten', b'sein', b'sein', b'sein', b'Leiden', b'essen', b'fahren', b'tun', b'laufen', b'treten', b'denken', b'haben', b'Wissen', b'gehen', b'Schweigen', b'treten', b'senden', b'nehmen', b'werden', b'halten', b'tun', b'fallen', b'lassen', b'sein', b'sein', b'gieren', b'sein', b'gehen', b'Sein', b'Leiden', b'nehmen', b'Sein', b'sein', b'schaffen', b'tun', b'tragen', b'nehmen', b'sein', b'sein', b'essen', b'sein', b'halten', b'kommen', b'sein', b'sein', b'halten', b'nehmen', b'sein', b'weisen', b'sein', b'wissen', b'essen', b'tun', b'essen', b'sein', b'bringen', b'Sein', b'sein', b'tun', b'sein', b'sein', b'wollen', b'halten', b'Sein', b'sein', b'sein', b'sein', b'sein', b'lassen', b'weichen', b'sein', b'fallen', b'Sein', b'essen', b'sein', b'sein', b'sein', b'sein', b'sein', b'gehen', b'ziehen', b'sein', b'sein', b'sein', b'sein', b'legen', b'gleichen', b'stehen', b'fallen', b'gehen', b'klingen', b'sein', b'wiegen', b'sein', b'lassen', b'Sein', b'haben', b'tun', b'sein', b'sein', b'sein', b'geben', b'stecken', b'lassen', b'sein', b'sein', b'fangen', b'sein', b'halten', b'sein', b'bergen', b'legen', b'werden', b'sein', b'essen', b'sein', b'Sein', b'sein', b'Sein', b'sein', b'sein', b'sein', b'geben', b'legen', b'sein', b'liegen', b'tun', b'werden', b'sein', b'schlagen', b'tun', b'sein', b'stehen', b'sein', b'tun', b'tragen', b'sein', b'halten', b'sein', b'sein', b'weichen', b'wollen', b'gelten', b'sein', b'halten', b'sein', b'Sterben', b'fallen', b'tun', b'fahren', b'fallen', b'reiben', b'tun', b'finden', b'tun', b'schweigen', b'halten', b'sein', b'treten', b'gehen', b'wachsen', b'fallen', b'scheiden', b'reisen', b'lassen', b'wissen', b'schlagen', b'sprechen', b'Reisen', b'legen', b'wenden', b'fliehen', b'wollen', b'geben', b'gehen', b'scheinen', b'sein', b'sein', b'schweigen', b'schweigen', b'sein', b'sein', b'sein', b'sein', b'weben', b'schreiten', b'tun', b'sein', b'sein', b'werfen', b'sein', b'sein', b'kommen', b'sein', b'dringen', b'nennen', b'sein', b'schreien', b'schleifen', b'weichen', b'sein', b'sein', b'sein', b'Sein', b'laufen', b'sein', b'sein', b'sein', b'sein', b'fallen', b'halten', b'essen', b'halten', b'weichen', b'sein', b'fangen', b'bleiben', b'sein', b'Sterben', b'fallen', b'sein', b'sein', b'sein', b'sein', b'sein', b'sein', b'legen', b'sein', b'messen', b'sein', b'geben', b'tun', b'sein', b'sein', b'heben', b'tragen', b'sein', b'schwinden', b'kriechen', b'Sein', b'sein', b'kommen', b'reiben', b'gleichen', b'verlieren', b'gehen', b'sein', b'sein', b'Sein', b'sein', b'sein', b'sein', b'sein', b'tun', b'malen', b'geben', b'lassen', b'Sein', b'sein', b'sein', b'laden', b'Gehen', b'lassen', b'sein', b'Wissen', b'wachsen', b'essen', b'essen', b'essen', b'halten', b'sein', b'bergen', b'treten', b'sein', b'sein', b'gewinnen', b'wissen', b'gehen', b'sein', b'Leiden', b'bleiben', b'sein', b'gehen', b'bleiben', b'tun', b'bieten', b'nehmen', b'tun', b'gewinnen', b'wenden', b'senden', b'wissen', b'stehen', b'zeihen', b'tun', b'werfen', b'fangen', b'fangen', b'sein', b'schwingen', b'leiden', b'tun', b'wissen', b'steigen', b'sein', b'liegen', b'essen', b'sein', b'fallen', b'wissen', b'lassen', b'liegen', b'essen', b'halten', b'sein', b'Sein', b'sein', b'tun', b'sein', b'rufen', b'tun', b'nehmen', b'legen', b'sein', b'essen', b'halten', b'Sein', b'tun', b'springen', b'sein', b'bitten', b'sein', b'tun', b'haben', b'sein', b'sein', b'dringen', b'schreiten', b'stehen', b'sein', b'hauen', b'essen', b'sein', b'Sein', b'Schreiten', b'sein', b'sein', b'sein', b'sein', b'tun', b'tun']
        ['Aufschlagen', 'aufsteigen', 'aufheben', 'aufgehen', 'Auftreten', 'Auftreten', 'aufnehmen', 'aufspringen']
        [b'Auftrag', b'aufgeh', b'aufgelangt', b'aufte', b'aufgeh']
    """

    def __init__(self):
        self.data = MultiKeyDict({})
        self.compiled_regex = ""
        self._oldhash = 0
        self._isbytes = False

    def _addbytes(self, word):
        ref = self.data
        for char in range(len(word)):
            ref[word[char : char + 1]] = (
                word[char : char + 1] in ref and ref[word[char : char + 1]] or {}
            )
            ref = ref[word[char : char + 1]]
        ref[b""] = 1

    def _add(self, word: str):
        if self._isbytes:
            self._addbytes(word)
        else:
            word2 = list(word)
            word2.append("")
            self.data[word2] = 1

    @cache
    def _quote(self, char):
        return re.escape(char)

    def _pattern(self, pdata):
        data = pdata
        if not self._isbytes:
            if "" in data and len(data) == 1:
                return None
        else:
            if b"" in data and len(data) == 1:
                return None
        alt = []
        cc = []
        q = 0
        for char in sorted(data):
            if isinstance(data[char], dict):
                qu = self._quote(char)
                try:
                    recurse = self._pattern(data[char])
                    alt.append(qu + recurse)
                except Exception:
                    cc.append(qu)
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                if not self._isbytes:
                    alt.append("[" + "".join(cc) + "]")
                else:
                    alt.append(b"[" + b"".join(cc) + b"]")

        if len(alt) == 1:
            result = alt[0]
        else:
            if not self._isbytes:
                result = "(?:" + "|".join(alt) + ")"
            else:
                result = b"(?:" + b"|".join(alt) + b")"

        if q:
            if cconly:
                if not self._isbytes:
                    result += "?"
                else:
                    result += b"?"
            else:
                if not self._isbytes:
                    result = f"(?:{result})?"
                else:
                    result = b"(?:" + result + b")?"
        return result

    def _get_pattern(self):
        return self._pattern(self.data)

    def compile(
        self,
        add_before="",
        add_after="",
        boundary_right: bool = False,
        boundary_left: bool = False,
        capture: bool = False,
        match_whole_line: bool = False,
        flags: int = re.IGNORECASE,
    ):
        r"""
        Compile the Trie into a regular expression pattern.

        This method generates a compiled regular expression pattern based on the current
        state of the Trie and various optional settings. The generated pattern can be used
        for pattern matching operations using the `regex` module.

        Args:
            add_before (str or bytes, optional): Prefix to add before the pattern.
            add_after (str or bytes, optional): Suffix to add after the pattern.
            boundary_right (bool, optional): If True, add a word boundary to the right of the pattern.
            boundary_left (bool, optional): If True, add a word boundary to the left of the pattern.
            capture (bool, optional): If True, capture the pattern in a group.
            match_whole_line (bool, optional): If True, match the entire line.
            flags (int, optional): Additional regex flags to apply (default is re.IGNORECASE).

        Returns:
            Trie: The Trie instance with the compiled regular expression pattern.

        Example:
            trie = Trie()
            words = ['apple', 'banana', 'cherry']
            trie.regex_from_words(words).compile(add_before="\\b", add_after="\\b",
                                                 boundary_right=True, boundary_left=True,
                                                 capture=True, match_whole_line=True)
        """
        if not self._isbytes:
            anfang = ""
            ende = ""

            if match_whole_line is True:
                anfang += r"^\s*"
            if boundary_right is True:
                ende += r"\b"
            if capture is True:
                anfang += "("
            if boundary_left is True:
                anfang += r"\b"
            if capture is True:
                ende += ")"

            if match_whole_line is True:
                ende += r"\s*$"
        else:
            anfang = b""
            ende = b""

            if match_whole_line is True:
                anfang += rb"^\s*"
            if boundary_right is True:
                ende += rb"\b"
            if capture is True:
                anfang += b"("
            if boundary_left is True:
                anfang += rb"\b"
            if capture is True:
                ende += b")"

            if match_whole_line is True:
                ende += rb"\s*$"
            if not isinstance(add_before, bytes):
                add_before = add_before.encode("utf-8")

            if not isinstance(add_after, bytes):
                add_after = add_after.encode("utf-8")
        if (
            newhash := hash(
                f"""{add_before}{anfang}{self.data.to_dict()}{ende}{add_after}{flags}"""
            )
        ) == self._oldhash:
            return self

        else:
            self.compiled_regex = re.compile(
                add_before + anfang + self._get_pattern() + ende + add_after, flags
            )
            self._oldhash = newhash
        return self

    def regex_from_words(
        self,
        words: list,
    ):
        r"""
        Construct the Trie from a list of words and enable byte-based matching if needed.

        This method populates the Trie data structure with the provided list of words.
        If the words contain bytes (e.g., b'word'), the Trie will be configured to
        support byte-based matching. Otherwise, the Trie will work with string-based
        matching.

        Args:
            words (list): A list of words to add to the Trie.

        Returns:
            Trie: The Trie instance with the added words.

        Example:
            trie = Trie()
            words = ['apple', 'banana', 'cherry']
            trie.regex_from_words(words)
        """
        if not isinstance(words[0], str):
            self._isbytes = True
            if isinstance(self.compiled_regex, str):
                self.compiled_regex = b""

        for word in words:
            self._add(word)
        return self
