# Greek UTF-8 character mappings
class alphabet:
    lc_alpha = u'\u03b1'
    lc_beta = u'\u03b2'
    lc_gamma = u'\u03b3'
    lc_delta = u'\u03b4'
    lc_epsilon = u'\u03b5'
    lc_zeta = u'\u03b6'
    lc_eta = u'\u03b7'
    lc_theta = u'\u03b8'
    lc_iota = u'\u03b9'
    lc_kappa = u'\u03ba'
    lc_lamda = u'\u03bb'
    lc_mu = u'\u03bc'
    lc_nu = u'\u03bd'
    lc_xi = u'\u03be'
    lc_omicron = u'\u03bf'
    lc_pi = u'\u03c0'
    lc_rho = u'\u03c1'
    lc_sigma_f = u'\u03c2'
    lc_sigma = u'\u03c3'
    lc_tau = u'\u03c4'
    lc_upsilon = u'\u03c5'
    lc_phi = u'\u03c6'
    lc_chi = u'\u03c7'
    lc_psi = u'\u03c8'
    lc_omega = u'\u03c9'

    lc_letters = [
        lc_alpha,
        lc_beta,
        lc_gamma,
        lc_delta,
        lc_epsilon,
        lc_zeta,
        lc_eta,
        lc_theta,
        lc_iota,
        lc_kappa,
        lc_lamda,
        lc_mu,
        lc_nu,
        lc_xi,
        lc_omicron,
        lc_pi,
        lc_rho,
        lc_sigma,
        #lc_sigma_f,
        lc_tau,
        lc_upsilon,
        lc_phi,
        lc_chi,
        lc_psi,
        lc_omega
    ]

# definite articles dependent on gender, number, case
articles = {}
articles['msn'] = u'\u1f41'
articles['msg'] = u'\u03c4\u03bf\u1fe6'
articles['msd'] = u'\u03c4\u1ff7'
articles['msa'] = u'\u03c4\u03cc\u03bd'
articles['mpn'] = u'\u03bf\u1f31'
articles['mpg'] = u'\u03c4\u1ff6\u03bd'
articles['mpd'] = u'\u03c4\u03bf\u1fd6\u03c2'
articles['mpa'] = u'\u03c4\u03bf\u03cd\u03c2'
articles['fsn'] = u'\u1f21'
articles['fsg'] = u'\u03c4\u1fc6\u03c2'
articles['fsd'] = u'\u03c4\u1fc7'
articles['fsa'] = u'\u03c4\u03ae\u03bd'
articles['fpn'] = u'\u03b1\u1f31'
articles['fpg'] = articles['mpg']
articles['fpd'] = u'\u03c4\u03b1\u1fd6\u03c2'
articles['fpa'] = u'\u03c4\u03ac\u03c2'
articles['nsn'] = u'\u03c4\u03cc'
articles['nsg'] = articles['msg']
articles['nsd'] = articles['msd']
articles['nsa'] = articles['nsn']
articles['npn'] = u'\u03c4\u03ac'
articles['npg'] = articles['mpg']
articles['npd'] = articles['mpd']
articles['npa'] = articles['npn']

# single char equiv -> logos multi-char equiv
accented_characters_map = {
    u'\u03b0': u'\u03c5\u0308\u0301',
    u'\u03aa': u'\u0399\u0308',
    u'\u0386': u'\u0391\u0301',
    u'\u0389': u'\u0397\u0301',
    u'\u0388': u'\u0395\u0301',
    u'\u03ab': u'\u03a5\u0308',
    u'\u038a': u'\u0399\u0301',
    u'\u03ad': u'\u03b5\u0301',
    u'\u038c': u'\u039f\u0301',
    u'\u038f': u'\u03a9\u0301',
    u'\u038e': u'\u03a5\u0301',
    u'\u03cd': u'\u03c5\u0301',
    u'\u0390': u'\u03b9\u0308\u0301',
    u'\u03af': u'\u03b9\u0301',
    u'\u03ca': u'\u03b9\u0308',
    u'\u03ac': u'\u03b1\u0301',
    u'\u03cc': u'\u03bf\u0301',
    u'\u03ae': u'\u03b7\u0301',
    u'\u03cb': u'\u03c5\u0308',
    u'\u03ce': u'\u03c9\u0301',

    # extended greek characters
    u'\u1f00': u'\u03b1\u0313',
    u'\u1f01': u'\u03b1\u0314',
    u'\u1f02': u'\u03b1\u0313\u0300',
    u'\u1f03': u'\u03b1\u0314\u0300',
    u'\u1f04': u'\u03b1\u0313\u0301',
    u'\u1f05': u'\u03b1\u0314\u0301',
    u'\u1f06': u'\u03b1\u0313\u0342',
    u'\u1f07': u'\u03b1\u0314\u0342',
    u'\u1f08': u'\u0391\u0313',
    u'\u1f09': u'\u0391\u0314',
    u'\u1f0a': u'\u0391\u0313\u0300',
    u'\u1f0b': u'\u0391\u0314\u0300',
    u'\u1f0c': u'\u0391\u0313\u0301',
    u'\u1f0d': u'\u0391\u0314\u0301',
    u'\u1f0e': u'\u0391\u0313\u0342',
    u'\u1f0f': u'\u0391\u0314\u0342',
    u'\u1f10': u'\u03b5\u0313',
    u'\u1f11': u'\u03b5\u0314',
    u'\u1f12': u'\u03b5\u0313\u0300',
    u'\u1f13': u'\u03b5\u0314\u0300',
    u'\u1f14': u'\u03b5\u0313\u0301',
    u'\u1f15': u'\u03b5\u0314\u0301',
    u'\u1f18': u'\u0395\u0313',
    u'\u1f19': u'\u0395\u0314',
    u'\u1f1a': u'\u0395\u0313\u0300',
    u'\u1f1b': u'\u0395\u0314\u0300',
    u'\u1f1c': u'\u0395\u0313\u0301',
    u'\u1f1d': u'\u0395\u0314\u0301',
    u'\u1f20': u'\u03b7\u0313',
    u'\u1f21': u'\u03b7\u0314',
    u'\u1f22': u'\u03b7\u0313\u0300',
    u'\u1f23': u'\u03b7\u0314\u0300',
    u'\u1f24': u'\u03b7\u0313\u0301',
    u'\u1f25': u'\u03b7\u0314\u0301',
    u'\u1f26': u'\u03b7\u0313\u0342',
    u'\u1f27': u'\u03b7\u0314\u0342',
    u'\u1f28': u'\u0397\u0313',
    u'\u1f29': u'\u0397\u0314',
    u'\u1f2a': u'\u0397\u0313\u0300',
    u'\u1f2b': u'\u0397\u0314\u0300',
    u'\u1f2c': u'\u0397\u0313\u0301',
    u'\u1f2d': u'\u0397\u0314\u0301',
    u'\u1f2e': u'\u0397\u0313\u0342',
    u'\u1f2f': u'\u0397\u0314\u0342',
    u'\u1f30': u'\u03b9\u0313',
    u'\u1f31': u'\u03b9\u0314',
    u'\u1f32': u'\u03b9\u0313\u0300',
    u'\u1f33': u'\u03b9\u0314\u0300',
    u'\u1f34': u'\u03b9\u0313\u0301',
    u'\u1f35': u'\u03b9\u0314\u0301',
    u'\u1f36': u'\u03b9\u0313\u0342',
    u'\u1f37': u'\u03b9\u0314\u0342',
    u'\u1f38': u'\u0399\u0313',
    u'\u1f39': u'\u0399\u0314',
    u'\u1f3a': u'\u0399\u0313\u0300',
    u'\u1f3b': u'\u0399\u0314\u0300',
    u'\u1f3c': u'\u0399\u0313\u0301',
    u'\u1f3d': u'\u0399\u0314\u0301',
    u'\u1f3e': u'\u0399\u0313\u0342',
    u'\u1f3f': u'\u0399\u0314\u0342',
    u'\u1f40': u'\u03bf\u0313',
    u'\u1f41': u'\u03bf\u0314',
    u'\u1f42': u'\u03bf\u0313\u0300',
    u'\u1f43': u'\u03bf\u0314\u0300',
    u'\u1f44': u'\u03bf\u0313\u0301',
    u'\u1f45': u'\u03bf\u0314\u0301',
    u'\u1f48': u'\u039f\u0313',
    u'\u1f49': u'\u039f\u0314',
    u'\u1f4a': u'\u039f\u0313\u0300',
    u'\u1f4b': u'\u039f\u0314\u0300',
    u'\u1f4c': u'\u039f\u0313\u0301',
    u'\u1f4d': u'\u039f\u0314\u0301',
    u'\u1f50': u'\u03c5\u0313',
    u'\u1f51': u'\u03c5\u0314',
    u'\u1f52': u'\u03c5\u0313\u0300',
    u'\u1f53': u'\u03c5\u0314\u0300',
    u'\u1f54': u'\u03c5\u0313\u0301',
    u'\u1f55': u'\u03c5\u0314\u0301',
    u'\u1f56': u'\u03c5\u0313\u0342',
    u'\u1f57': u'\u03c5\u0314\u0342',
    u'\u1f59': u'\u03a5\u0314',
    u'\u1f5b': u'\u03a5\u0314\u0300',
    u'\u1f5d': u'\u03a5\u0314\u0301',
    u'\u1f5f': u'\u03a5\u0314\u0342',
    u'\u1f60': u'\u03c9\u0313',
    u'\u1f61': u'\u03c9\u0314',
    u'\u1f62': u'\u03c9\u0313\u0300',
    u'\u1f63': u'\u03c9\u0314\u0300',
    u'\u1f64': u'\u03c9\u0313\u0301',
    u'\u1f65': u'\u03c9\u0314\u0301',
    u'\u1f66': u'\u03c9\u0313\u0342',
    u'\u1f67': u'\u03c9\u0314\u0342',
    u'\u1f68': u'\u03a9\u0313',
    u'\u1f69': u'\u03a9\u0314',
    u'\u1f6a': u'\u03a9\u0313\u0300',
    u'\u1f6b': u'\u03a9\u0314\u0300',
    u'\u1f6c': u'\u03a9\u0313\u0301',
    u'\u1f6d': u'\u03a9\u0314\u0301',
    u'\u1f6e': u'\u03a9\u0313\u0342',
    u'\u1f6f': u'\u03a9\u0314\u0342',
    u'\u1f70': u'\u03b1\u0300',
    u'\u1f71': u'\u03b1\u0301',
    u'\u1f72': u'\u03b5\u0300',
    u'\u1f73': u'\u03b5\u0301',
    u'\u1f74': u'\u03b7\u0300',
    u'\u1f75': u'\u03b7\u0301',
    u'\u1f76': u'\u03b9\u0300',
    u'\u1f77': u'\u03b9\u0301',
    u'\u1f78': u'\u03bf\u0300',
    u'\u1f79': u'\u03bf\u0301',
    u'\u1f7a': u'\u03c5\u0300',
    u'\u1f7b': u'\u03c5\u0301',
    u'\u1f7c': u'\u03c9\u0300',
    u'\u1f7d': u'\u03c9\u0301',
    u'\u1fb6': u'\u03b1\u0342',
    u'\u1fba': u'\u0391\u0300',
    u'\u1fbb': u'\u0391\u0301',
    u'\u1fc6': u'\u03b7\u0342',
    u'\u1fc8': u'\u0395\u0300',
    u'\u1fc9': u'\u0395\u0301',
    u'\u1fca': u'\u0397\u0300',
    u'\u1fcb': u'\u0397\u0301',
    u'\u1fd2': u'\u03b9\u0308\u0300',
    u'\u1fd3': u'\u03b9\u0308\u0301',
    u'\u1fd6': u'\u03b9\u0342',
    u'\u1fda': u'\u0399\u0300',
    u'\u1fdb': u'\u0399\u0301',
    u'\u1fe2': u'\u03c5\u0308\u0300',
    u'\u1fe3': u'\u03c5\u0308\u0301',
    u'\u1fe4': u'\u03c1\u0313',
    u'\u1fe5': u'\u03c1\u0314',
    u'\u1fe6': u'\u03c5\u0342',
    u'\u1fe7': u'\u03c5\u0308\u0342',
    u'\u1fea': u'\u03a5\u0300',
    u'\u1feb': u'\u03a5\u0301',
    u'\u1fec': u'\u03a1\u0300',
    u'\u1ff6': u'\u03c9\u0342',
    u'\u1ff8': u'\u039f\u0300',
    u'\u1ff9': u'\u039f\u0301',
    u'\u1ffa': u'\u03a9\u0300',
    u'\u1ffb': u'\u03a9\u0301',
}

def replace_accented_characters(word):
    """Utility method for replacing accented characters with the
        logos keyboard equivalent"""
    result = word
    for letter in word:
        replacement = accented_characters_map.get(letter, False)
        if replacement != False:
            result = result.replace(letter, replacement)
    return result

def find_difference():
    words_by_letter = []
    from siteapps_v1.ntgreekvocab.models import SimpleCard
    for letter in alphabet.lc_letters:
        words_by_letter.append((letter, SimpleCard.objects.filter(greek_word__istartswith=letter).order_by('greek_word').values('id','greek_word','definition','lesson_number','part_of_speech')))

    # debugging to see if some words excluded in the letter filter
    qs = words_by_letter[0][1]
    for t in words_by_letter:
        qs = qs | t[1]
    diff = list(set(SimpleCard.objects.all().values_list('id', flat=True)) - set(qs.values_list('id', flat=True)))
    return diff

def correct_difference():
    ids = find_difference()
    from siteapps_v1.ntgreekvocab.models import SimpleCard
    words = SimpleCard.objects.filter(id__in=ids)
    for w in words:
        print w.id
        w.greek_word = replace_accented_characters(w.greek_word)
        w.save(force_update=True)

"""
#-----------------------------
# Unused code below
#-----------------------------

ALPHA = 0
BETA = 1
GAMMA = 2
DELTA = 3
EPSILON = 4
ZETA = 5
ETA = 6
THETA = 7
IOTA = 8
KAPPA = 9
LAMDA = 10
MU = 11
NU = 12
XI = 13
OMICRON = 14
PI = 15
RHO = 16
SIGMA = 17
TAU = 18
UPSILON = 19
PHI = 20
CHI = 21
PSI = 22
OMEGA = 23

uc_letters = [
    u'\u0391',
    u'\u0392',
    u'\u0393',
    u'\u0394',
    u'\u0395',
    u'\u0396',
    u'\u0397',
    u'\u0398',
    u'\u0399',
    u'\u039a',
    u'\u039b',
    u'\u039c',
    u'\u039d',
    u'\u039e',
    u'\u039f',
    u'\u03a0',
    u'\u03a1',
    u'\u03a3',
    u'\u03a4',
    u'\u03a5',
    u'\u03a6',
    u'\u03a7',
    u'\u03a8',
    u'\u03a9'
]

"""