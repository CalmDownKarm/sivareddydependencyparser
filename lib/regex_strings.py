SGML_TAG = r"""
    (?:                         # make enclosing parantheses non-grouping
    <!-- .*? -->                # XML/SGML comment
    |                           # -- OR --
    <[!?/]?(?!\d)\w[-\.:\w]*    # Start of tag/directive
    (?:                         # Attributes
        [^>'"]*                 # - attribute name (+whitespace +equal sign)
        (?:'[^']*'|"[^"]*")     # - attribute value
    )*
    \s*                         # Spaces at the end
    /?                          # Forward slash at the end of singleton tags
    \s*                         # More spaces at the end
    >                           # +End of tag/directive
    )"""
SGML_END_TAG = r"</(?!\d)\w[-\.:\w]*>"
IP_ADDRESS = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
DNS_HOST = r"""
    (?:
        [-a-z0-9]+\.                # Host name
        (?:[-a-z0-9]+\.)*           # Intermediate domains
                                    # And top level domain below
        (?:
        com|edu|gov|int|mil|net|org|            # Common historical TLDs
        biz|info|name|pro|aero|coop|museum|     # Added TLDs
        arts|firm|info|nom|rec|shop|web|        # ICANN tests...
        asia|cat|jobs|mail|mobi|post|tel|
        travel|xxx|
        glue|indy|geek|null|oss|parody|bbs|     # OpenNIC
        localdomain|                            # Default 127.0.0.0

        # And here the country TLDs
        ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|
        ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|
        ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|
        de|dj|dk|dm|do|dz|
        ec|ee|eg|eh|er|es|et|
        fi|fj|fk|fm|fo|fr|
        ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|
        hk|hm|hn|hr|ht|hu|
        id|ie|il|im|in|io|iq|ir|is|it|
        je|jm|jo|jp|
        ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|
        la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|
        ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|
        na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|
        om|
        pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|
        qa|
        re|ro|ru|rw|
        sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|sv|sy|sz|
        tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|
        ua|ug|uk|um|us|uy|uz|
        va|vc|ve|vg|vi|vn|vu|
        wf|ws|
        ye|yt|yu|
        za|zm|zw
        )

        |

        localhost
    )"""
URL = r"""
    (?:

    # Scheme part
    (?:ftp|https?|gopher|mailto|news|nntp|telnet|wais|file|prospero)://

    # User authentication (optional)
    (?:[-a-z0-9_;?&=](?::[-a-z0-9_;?&=]*)?@)?

    # "www" without the scheme part
    |(?:www|web)\.

    )

    # DNS host / IP
    (?:
        """ + DNS_HOST + """
        |
        """ + IP_ADDRESS + """
    )

    # Port specification (optional)
    (?::[0-9]+)?

    # Scheme specific extension (optional)
    (?:/[-\w;/?:@=&\$_.+!*'(~#%,]*)?
"""
EMAIL = r"[-a-z0-9._']+@" + DNS_HOST
ACRONYM = r"""
    (?<!\w)     # should not be preceded by a letter
    # sequence of single letter followed by . (e.g. U.S.)
    (?:
        (?![\d_])\w         # alphabetic character
        \.
    )+
    # optionaly followed by a single letter (e.g. U.S.A)
    (?:
        (?![\d_])\w         # alphabetic character
        (?!\w)              # we don't want any more letters to follow
                            # we only want to match U.S. in U.S.Army (not U.S.A)
    )?
"""
CONTROL_CHAR = r"[\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008" \
    r"\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013" \
    r"\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C" \
    r"\u001D\u001E\u001F]"
MULTICHAR_PUNCTUATION = r"(?:[?!]+|``|'')"
OPEN_CLOSE_PUNCTUATION = r"""
    [
        \u00AB \u2018 \u201C \u2039 \u00BB \u2019 \u201D \u203A \u0028 \u005B
        \u007B \u0F3A \u0F3C \u169B \u2045 \u207D \u208D \u2329 \u23B4 \u2768
        \u276A \u276C \u276E \u2770 \u2772 \u2774 \u27E6 \u27E8 \u27EA \u2983
        \u2985 \u2987 \u2989 \u298B \u298D \u298F \u2991 \u2993 \u2995 \u2997
        \u29D8 \u29DA \u29FC \u3008 \u300A \u300C \u300E \u3010 \u3014 \u3016
        \u3018 \u301A \u301D \uFD3E \uFE35 \uFE37 \uFE39 \uFE3B \uFE3D \uFE3F
        \uFE41 \uFE43 \uFE47 \uFE59 \uFE5B \uFE5D \uFF08 \uFF3B \uFF5B \uFF5F
        \uFF62 \u0029 \u005D \u007D \u0F3B \u0F3D \u169C \u2046 \u207E \u208E
        \u232A \u23B5 \u2769 \u276B \u276D \u276F \u2771 \u2773 \u2775 \u27E7
        \u27E9 \u27EB \u2984 \u2986 \u2988 \u298A \u298C \u298E \u2990 \u2992
        \u2994 \u2996 \u2998 \u29D9 \u29DB \u29FD \u3009 \u300B \u300D \u300F
        \u3011 \u3015 \u3017 \u3019 \u301B \u301E \u301F \uFD3F \uFE36 \uFE38
        \uFE3A \uFE3C \uFE3E \uFE40 \uFE42 \uFE44 \uFE48 \uFE5A \uFE5C \uFE5E
        \uFF09 \uFF3D \uFF5D \uFF60 \uFF63
    ]
"""
PHONE_NUMBER = r"\+?[0-9]+(?:[-\u2012 ][0-9]+)*"
NUMBER_INTEGER_PART = r"""
    (?:
        0
        |
        [1-9][0-9]{0,2}(?:[ ,.][0-9]{3})+  # with thousand separators
        |
        [1-9][0-9]*
	|
	[\d]+
    )"""
NUMBER_DECIMAL_PART = r"""
    (?:
        [.,]
        [0-9]+
        (?:[eE][-\u2212+]?[0-9]+)?
	|
	[.,]
	[\d]+
	(?:[eE][-\u2212+]?[\d]+)?
    )"""
NUMBER = r"""
    (?:(?:\A|(?<=\s))[-\u2212+])?
    (?:
        %(integer)s %(decimal)s?
        |
        %(decimal)s
    )""" % {'integer': NUMBER_INTEGER_PART, 'decimal': NUMBER_DECIMAL_PART}
WHITESPACE = r"\s+"
SPACE = r"[\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006" \
    r"\u2007\u2008\u2009\u200A\u202F\u205F\u3000]"
ANY_SEQUENCE = r"(.)\1*"
HTMLENTITY = r"&(?:#x?[0-9]+|\w+);"
GLUE_TAG = u'<g/>'

clictics = {
    # Defaults: None
    # re.UNICODE | re.VERBOSE | re.IGNORECASE -> English flags
    'English': r"""
            (?:
                (?<=\w)     # only consider clictics preceded by a letter
                (?:
                    ['`\u2018\u2019\u2032](?:s|re|ve|d|m|em|ll)
                    |
                    n['`\u2018\u2019\u2032]t
                )
                |
                # cannot
                (?<=can)
                not
            )
            (?!\w)          # clictics should not be followed by a letter
            """,
    # re.UNICODE | re.VERBOSE) French Flags
    'French': r"""
            (?:
                # left clictics
                (?<!\w)     # should not be preceded by a letter
                (?:
                    [dcjlmnstDCJLNMST] | [Qq]u | [Jj]usqu | [Ll]orsqu
                )
                ['\u2019]   # apostrophe
                |
                # right clictics
                (?<=\w)     # should be preceded by a letter
                [-\u2010]   # hypen
                (?:
                    # FIXME!
                    [-\u2010]t[-\u2010]elles? | [-\u2010]t[-\u2010]ils? |
                    [-\u2010]t[-\u2010]on | [-\u2010]ce | [-\u2010]elles? |
                    [-\u2010]ils? | [-\u2010]je | [-\u2010]la | [-\u2010]les? |
                    [-\u2010]leur | [-\u2010]lui | [-\u2010]m\u00eames? |
                    [-\u2010]m['\u2019] | [-\u2010]moi | [-\u2010]nous |
                    [-\u2010]on | [-\u2010]toi | [-\u2010]tu |
                    [-\u2010]t['\u2019] | [-\u2010]vous | [-\u2010]en |
                    [-\u2010]y | [-\u2010]ci | [-\u2010]l\u00e0
                )
                (?!w)      # should not be followed by a letter
            )
            """,
    # Flags are same as French
    'Italian': r"""
            (?:
                # left clictics
                (?<!\w)     # should not be preceded by a letter
                (?:
                    [dD][ae]ll | [nN]ell | [Aa]ll | [lLDd] | [Ss]ull | [Qq]uest |
                    [Uu]n | [Ss]enz | [Tt]utt
                )
                ['\u2019]   # apostrophe
                (?=\w)      # should be followed by a letter
            )
            """,
    # UNICODE, VERBOSE, IGNORECASE
    'Czech': r"""
            (?:
                (?<=\w)     # only consider clictics preceded by a letter
                -li
            )
            (?!\w)          # clictics should not be followed by a letter
            """

}

word = {
    # use re.UNICODE flag
    'Hindi': r"([-\u2010\u0900-\u0963\u0966-\u097f\w])+",
    'default': r"(?:(?![\d])[-\u2010\w])+"
}

abbreviations = {
    #  re.IGNORECASE | re.UNICODE | re.VERBOSE
    'default': r"""
    (?<!\w)     # should not be preceded by a letter
    (?:
        co\.|inc\.|ltd\.|dr\.|prof\.|jr\.
    )
    """,
    # English Flags -> re.UNICODE | re.VERBOSE
    'English': r"""
(?<!\w)     # should not be preceded by a letter
(?:
    Adm\.|Ala\.|Ariz\.|Ark\.|Aug\.|Ave\.|Bancorp\.|Bhd\.|Brig\.|
    Bros\.|CO\.|CORP\.|COS\.|Ca\.|Calif\.|Canada[-\u2010]U\.S\.|
    Canadian[-\u2010]U\.S\.|Capt\.|Cia\.|Cie\.|Co\.|Col\.|Colo\.|
    Conn\.|Corp\.|Cos\.|D[-\u2010]Mass\.|Dec\.|Del\.|Dept\.|Dr\.|
    Drs\.|Etc\.|Feb\.|Fla\.|Ft\.|Ga\.|Gen\.|Gov\.|Hon\.|INC\.|
    Ill\.|Inc\.|Ind\.|Jan\.|Japan[-\u2010]U\.S\.|Jr\.|Kan\.|
    Korean[-\u2010]U\.S\.|Ky\.|La\.|Lt\.|Ltd\.|Maj\.|Mass\.|Md\.|
    Messrs\.|Mfg\.|Mich\.|Minn\.|Miss\.|Mo\.|Mr\.|Mrs\.|Ms\.|Neb\.
    |Nev\.|No\.|Nos\.|Nov\.|Oct\.|Okla\.|Ont\.|Ore\.|Pa\.|Ph\.|
    Prof\.|Prop\.|Pty\.|Rep\.|Reps\.|Rev\.|S\.p\.A\.|Sen\.|Sens\.|
    Sept\.|Sgt\.|Sino[-\u2010]U\.S\.|Sr\.|St\.|Ste\.|Tenn\.|Tex\.|
    U\.S\.[-\u2010]U\.K\.|U\.S\.[-\u2010]U\.S\.S\.R\.|Va\.|Vt\.|W\.Va\.|
    Wash\.|Wis\.|Wyo\.|a\.k\.a\.|a\.m\.|anti[-\u2010]U\.S\.|cap\.|
    etc\.|ft\.|i\.e\.|non[-\u2010]U\.S\.|office/dept\.|p\.m\.|
    president[-\u2010]U\.S\.|s\.r\.l\.|v\.|v\.B\.|v\.w\.|vs\.
)
""",
    # French Flags ->re.UNICODE | re.VERBOSE
    'French': r"""
(?<!\w)     # should not be preceded by a letter
(?:
    rendez[-\u2010]vous|d['\u2019]abord|d['\u2019]accord|d['\u2019]ailleurs|
    d['\u2019]apr\u00e8s|d['\u2019]autant|d['\u2019]\u0153uvre|
    d['\u2019]oeuvre|c['\u2019]est[-\u2010]\u00e0[-\u2010]dire|
    moi[-\u2010]m\u00eame|toi[-\u2010]m\u00eame|lui[-\u2010]m\u00eame|
    elle[-\u2010]m\u00eame|nous[-\u2010]m\u00eames|vous[-\u2010]m\u00eames|
    eux[-\u2010]m\u00eames|elles[-\u2010]m\u00eames|par[-\u2010]ci|
    par[-\u2010]l\u00e0|Rendez[-\u2010]vous|D['\u2019]abord|D['\u2019]accord|
    D['\u2019]ailleurs|D['\u2019]apr\u00e8s|D['\u2019]autant|
    D['\u2019]\u0153uvre|D['\u2019]oeuvre|
    C['\u2019]est[-\u2010]\u00e0[-\u2010]dire|Moi[-\u2010]m\u00eame|
    Toi[-\u2010]m\u00eame|Lui[-\u2010]m\u00eame|Elle[-\u2010]m\u00eame|
    Nous[-\u2010]m\u00eames|Vous[-\u2010]m\u00eames|Eux[-\u2010]m\u00eames|
    Elles[-\u2010]m\u00eames|Par[-\u2010]ci|Par[-\u2010]l\u00e0
)
(?!w)      # should not be followed by a letter
""",
    # Italian Flags are same as French
    'Italian': r"""
            (?<!\w)     # should not be preceded by a letter
            (?:
                L\. | Lit\. | art\. | lett\. | n\. | no\. | pagg\. | prot\. | tel\.
            )
            """,
    # German flags are same as french
    'German': r"""
(?:
    # these can be preceded by a letter
    (?:
        [-\u2010]hdg\.|[-\u2010]tlg\.
    )
    |
    # these should not be preceded by a letter
    (?<!\w)
    (?:
        # from http://en.wiktionary.org/wiki/Category:German_abbreviations
        AB[-\u2010]Whg\.|Abl\.|Bio\.|Bj\.|Blk\.|Eigent\.[-\u2010]Whg\.|
        Eigent\.[-\u2010]Whgn\.|Eigt\.[-\u2010]Whg\.|Eigt\.[-\u2010]Whgn\.|Fr\.|
        Gal\.|Gart\.ant\.|Grd\.|Grdst\.|Hdt\.|Jg\.|Kl\.[-\u2010]Whg\.|
        Kl\.[-\u2010]Whgn\.|Mais\.[-\u2010]Whg\.|Mais\.[-\u2010]Whgn\.|Mio\.|
        Mrd\.|NB[-\u2010]Whg\.|Nb\.[-\u2010]Whg\.|Nb\.[-\u2010]Whgn\.|Nfl\.|
        Pak\.|Prov\.|Sout\.|Tsd\.|Whg\.|Whgn\.|Zi\.|Ziegelbauw\.|
        Ztr\.[-\u2010]Hzg\.|Ztrhzg\.|Zw\.[-\u2010]Whg\.|Zw\.[-\u2010]Whgn\.|
        abzgl\.|bezugsf\.|bzgl\.|bzw\.|d\.[ ]h\.|engl\.|freist\.|frz\.|
        i\.[ ]d\.[ ]R\.|m\u00f6bl\.|ren\.|ren\.bed\.|rest\.|san\.|usw\.|
        z\.[ ]B\.|zz\.|zzgl\.|zzt\.
    )
)
""",
    # Dutch flags are the same as french
    'Dutch': r"""
(?:
    # these can be preceded by a letter
    (?:
        ['\u2019]t | ['\u2019]s | ['\u2019]n
    )
    |
    # these should not be preceded by a letter
    (?<!\w)
    (?:
        2bis\.|3bis\.|7bis\.|AR\.|Actualit\.|Afd\.|Antw\.|Arbh\.|Art\.|
        B\.St\.|B\.s\.|Besl\.W\.|Bull\.|Bull\.Bel\.|Cass\.|Cf\.|
        Com\.I\.B\.|D\.t/V\.I\.|Dhr\.|Doc\.|Dr\.|Fisc\.|Fr\.|Gec\.|II\.
        |III\.|J\.[-\u2010]L\.M\.|NR\.|NRS\.|Nat\.|No\.|Nr\.|Onderafd\.|
        PAR\.|Par\.|RECHTSFAK\.|RKW\.|TELEF\.|Volksvert\.|Vr\.|a\.|
        adv\.[-\u2010]gen\.|afd\.|aj\.|al\.|arb\.|art\.|artt\.|b\.|
        b\.v\.|b\.w\.|bijv\.|blz\.|bv\.|c\.q\.|cf\.|cfr\.|concl\.|d\.
        |d\.d\.|d\.i\.|d\.w\.z\.|dd\.|doc\.|e\.|e\.d\.|e\.v\.|enz\.|
        f\.|fr\.|g\.w\.|gepubl\.|i\.p\.v\.|i\.v\.m\.|j\.t\.t\.|jl\.|
        k\.b\.|kol\.|m\.b\.t\.|m\.i\.|max\.|n\.a\.v\.|nl\.|nr\.|nrs\.|
        o\.a\.|o\.b\.s\.i\.|o\.m\.|opm\.|p\.|par\.|pct\.|pp\.|ref\.|
        resp\.|respekt\.|t\.a\.v\.|t\.o\.v\.|vb\.|w\.
    )
)
""",
    'Spanish': r"""
            (?<!\w)     # should not be preceded by a letter
            (?:
                Ref\. | Vol\. | etc\. | App\. | Rec\.
            )
            """,
    'Czech': r"""
(?:
    # these should not be preceded by a letter
    (?<!\w)
    (?:
#Generated from http://cs.wiktionary.org/wiki/Kategorie:%C4%8Cesk%C3%A9_zkratky by Makefile.Czech.abbr
např\.|mudr\.|abl\.|absol\.|adj\.|adv\.|ak\.|ak\. sl\.|alch\.|amer\.|anat\.|angl\.|anglosas\.|archit\.|arg\.|astr\.|astrol\.|att\.|bás\.|belg\.|bibl\.|biol\.|boh\.|bulh\.|círk\.|csl\.|č\.|čes\.|dět\.|dial\.|dór\.|dopr\.|dosl\.|ekon\.|el\.|epic\.|eufem\.|f\.|fam\.|fem\.|fil\.|form\.|fr\.|fut\.|fyz\.|gen\.|geogr\.|geol\.|geom\.|germ\.|hebr\.|herald\.|hist\.|hl\.|hud\.|hut\.|chcsl\.|chem\.|ie\.|imp\.|impf\.|ind\.|indoevr\.|inf\.|instr\.|interj\.|iron\.|it\.|katalán\.|kniž\.|komp\.|konj\.|konkr\.|kř\.|kuch\.|lat\.|lit\.|liturg\.|lok\.|m\.|mat\.|mod\.|ms\.|n\.|náb\.|námoř\.|neklas\.|něm\.|nesklon\.|nom\.|ob\.|obch\.|obyč\.|ojed\.|opt\.|pejor\.|pers\.|pf\.|pl\.|plpf\.|prep\.|předl\.|přivl\.|r\.|rcsl\.|refl\.|reg\.|rkp\.|ř\.|řec\.|s\.|samohl\.|sg\.|sl\.|souhl\.|spec\.|srov\.|stfr\.|střv\.|stsl\.|subj\.|subst\.|superl\.|sv\.|sz\.|táz\.|tech\.|telev\.|teol\.|trans\.|typogr\.|var\.|verb\.|vl\. jm\.|voj\.|vok\.|vůb\.|vulg\.|výtv\.|vztaž\.|zahr\.|zájm\.|zast\.|zejm\.|zeměd\.|zkr\.|zř\.|mj\.|dl\.|atp\.|mgr\.|horn\.|mvdr\.|judr\.|rsdr\.|bc\.|phdr\.|thdr\.|ing\.|aj\.|apod\.|pharmdr\.|pomn\.|ev\.|nprap\.|odp\.|dop\.|pol\.|st\.|stol\.|p\. n\. l\.|před n\. l\.|n\. l\.|př\. kr\.|po kr\.|př\. n\. l\.|odd\.|rndr\.|tzv\.|atd\.|tzn\.|resp\.|tj\.|p\.|br\.|č\. j\.|čj\.|č\. p\.|čp\.|a\. s\.|s\. r\. o\.|spol\. s r\. o\.|p\. o\.|s\. p\.|v\. o\. s\.|k\. s\.|o\. p\. s\.|o\. s\.|v\. r\.|v z\.|ml\.|vč\.|kr\.|mld\.|popř\.|ap\.|event\.|švýc\.|p\. t\.|zvl\.|hor\.|dol\.|plk\.|pplk\.|mjr\.|genmjr\.|genpor\.|kpt\.|npor\.|por\.|ppor\.|prap\.|pprap\.|rtm\.|rtn\.|des\.|svob\.|adm\.|brit\.|býv\.|čín\.|fin\.|chil\.|jap\.|nám\.|niz\.|špan\.|tur\.|bl\.|mga\.|zn\.|říj\.|etnonym\.|b\. k\.|škpt\.|nrtm\.|nstržm\.|stržm\.|genplk\.|šprap\.|št\. prap\.|brig\. gen\.|arm\. gen\.|doc\.|prof\.|csc\.|bca\.|dis\.
    )
)
""",
    'Hindi': r"""
(?<!\w)     # should not be preceded by a letter
(?:
    Adm\.|Ala\.|Ariz\.|Ark\.|Aug\.|Ave\.|Bancorp\.|Bhd\.|Brig\.|
    Bros\.|CO\.|CORP\.|COS\.|Ca\.|Calif\.|Canada[-\u2010]U\.S\.|
    Canadian[-\u2010]U\.S\.|Capt\.|Cia\.|Cie\.|Co\.|Col\.|Colo\.|
    Conn\.|Corp\.|Cos\.|D[-\u2010]Mass\.|Dec\.|Del\.|Dept\.|Dr\.|
    Drs\.|Etc\.|Feb\.|Fla\.|Ft\.|Ga\.|Gen\.|Gov\.|Hon\.|INC\.|
    Ill\.|Inc\.|Ind\.|Jan\.|Japan[-\u2010]U\.S\.|Jr\.|Kan\.|
    Korean[-\u2010]U\.S\.|Ky\.|La\.|Lt\.|Ltd\.|Maj\.|Mass\.|Md\.|
    Messrs\.|Mfg\.|Mich\.|Minn\.|Miss\.|Mo\.|Mr\.|Mrs\.|Ms\.|Neb\.
    |Nev\.|No\.|Nos\.|Nov\.|Oct\.|Okla\.|Ont\.|Ore\.|Pa\.|Ph\.|
    Prof\.|Prop\.|Pty\.|Rep\.|Reps\.|Rev\.|S\.p\.A\.|Sen\.|Sens\.|
    Sept\.|Sgt\.|Sino[-\u2010]U\.S\.|Sr\.|St\.|Ste\.|Tenn\.|Tex\.|
    U\.S\.[-\u2010]U\.K\.|U\.S\.[-\u2010]U\.S\.S\.R\.|Va\.|Vt\.|W\.Va\.|
    Wash\.|Wis\.|Wyo\.|a\.k\.a\.|a\.m\.|anti[-\u2010]U\.S\.|cap\.|
    etc\.|ft\.|i\.e\.|non[-\u2010]U\.S\.|office/dept\.|p\.m\.|
    president[-\u2010]U\.S\.|s\.r\.l\.|v\.|v\.B\.|v\.w\.|vs\.|डाॅ\.|श्री\.|सुश्री\.|श्रीमती\.|कि.मी.
)
"""

}

