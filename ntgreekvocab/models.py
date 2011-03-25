from django.db import models
from siteapps_v1.ntgreekvocab import greek

"""Constants"""
POS_NOUN_SHORT = 'n'
POS_NOUN_LONG = 'noun'
POS_PRONOUN_SHORT = 'pn'
POS_PRONOUN_LONG = 'pronoun'
POS_VERB_SHORT = 'v'
POS_VERB_LONG = 'verb'
POS_ADJ_SHORT = 'adj'
POS_ADJ_LONG = 'adjective'
POS_PREP_SHORT = 'prep'
POS_PREP_LONG = 'preposition'
POS_ADV_SHORT = 'adv'
POS_ADV_LONG = 'adverb'
POS_CONJ_SHORT = 'conj'
POS_CONJ_LONG = 'conjunction'
POS_PRTCPL_SHORT = 'prtcpl'
POS_PRTCPL_LONG = 'participle'
POS_CONSTRUCT_SHORT = 'construct'
POS_CONSTRUCT_LONG = 'construct'
POS_PHRASE_SHORT = 'phrase'
POS_PHRASE_LONG = 'phrase'
POS_PRTCL_SHORT = 'prtcl'
POS_PRTCL_LONG = 'particle'
POS_CMP_SHORT = 'cmp'
POS_CMP_LONG = 'comparative'

PARTS_OF_SPEECH_MAP = {
    POS_NOUN_SHORT: POS_NOUN_LONG,
    POS_PRONOUN_SHORT: POS_PRONOUN_LONG,
    POS_VERB_SHORT: POS_VERB_LONG,
    POS_ADJ_SHORT:POS_ADJ_LONG,
    POS_PREP_SHORT: POS_PREP_LONG,
    POS_ADV_SHORT:POS_ADV_LONG,
    POS_CONJ_SHORT: POS_CONJ_LONG,
    POS_PRTCPL_SHORT: POS_PRTCPL_LONG,
    POS_CONSTRUCT_SHORT: POS_CONSTRUCT_LONG,
    POS_PHRASE_SHORT: POS_PHRASE_LONG,
    POS_PRTCL_SHORT: POS_PRTCL_LONG,
    POS_CMP_SHORT: POS_CMP_LONG
}

PARTS_OF_SPEECH_CHOICES = (
    (POS_NOUN_SHORT, PARTS_OF_SPEECH_MAP[POS_NOUN_SHORT]),
    (POS_PRONOUN_SHORT, PARTS_OF_SPEECH_MAP[POS_PRONOUN_SHORT]),
    (POS_VERB_SHORT, PARTS_OF_SPEECH_MAP[POS_VERB_SHORT]),
    (POS_ADJ_SHORT, PARTS_OF_SPEECH_MAP[POS_ADJ_SHORT]),
    (POS_PREP_SHORT, PARTS_OF_SPEECH_MAP[POS_PREP_SHORT]),
    (POS_ADV_SHORT, PARTS_OF_SPEECH_MAP[POS_ADV_SHORT]),
    (POS_CONJ_SHORT, PARTS_OF_SPEECH_MAP[POS_CONJ_SHORT]),
    (POS_PRTCPL_SHORT, PARTS_OF_SPEECH_MAP[POS_PRTCPL_SHORT]),
    (POS_CONSTRUCT_SHORT, PARTS_OF_SPEECH_MAP[POS_CONSTRUCT_SHORT]),
    (POS_PHRASE_SHORT, PARTS_OF_SPEECH_MAP[POS_PHRASE_SHORT]),
    (POS_PRTCL_SHORT, PARTS_OF_SPEECH_MAP[POS_PRTCL_SHORT]),
    (POS_CMP_SHORT, PARTS_OF_SPEECH_MAP[POS_CMP_SHORT]),
    )
LESSON_NUMBER_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    ('16','16'),
    ('17','17'),
    ('18A','18A'),
    ('18B','18B'),
    ('19','19'),
    ('20','20'),
    ('21','21'),
    ('22','22'),
    ('23','23'),
    ('24','24'),
    ('25','25'),
    ('26','26'),
    ('27','27'),
    ('28','28'),
    ('29','29'),
    ('30','30'),
    ('31','31'),
    ('32','32'),
    ('33','33'),
    ('34','34'),
)

# Create your models here.
class SimpleCard(models.Model):
    greek_word = models.CharField(max_length=128, unique=True)
    part_of_speech = models.CharField(max_length=64, choices=PARTS_OF_SPEECH_CHOICES)
    definition = models.TextField(blank=True, null=True)
    hints = models.TextField(blank=True, null=True)
    parsing_info = models.CharField(max_length=256, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    lesson_number = models.CharField(max_length=4, blank=True, choices=LESSON_NUMBER_CHOICES, null=True)
    related_cards = models.ManyToManyField('self', blank=True, related_name="related_cards")

    PARSING_TERMS = [
        # tenses
        'present','imperfect','aorist','1st aorist', '2nd aorist', 'perfect', 'future',
        # voices
        'active', 'passive', 'middle', 'middle/passive',
        # moods
        'indicative', 'subjunctive', 'imperative', 'infinitive', 'vocative',
        # persons
        '1st person', '2nd person', '3rd person',
        # numbers
        'singular', 'plural',
        # genders
        'masculine', 'feminine', 'neuter', 'masculine/feminine', 'masculine/neuter',
        # cases
        'nominative', 'genitive', 'dative', 'accusative', 'nominative/accusative','nominative/genitive',
    ]

    class Meta:
        ordering = ['greek_word']

    def __unicode__(self):
        return u'%s, %s' % (self.greek_word, PARTS_OF_SPEECH_MAP[self.part_of_speech])

    def get_part_of_speech(self):
        return PARTS_OF_SPEECH_MAP[self.part_of_speech]

    def get_def_article(self):
        if self.part_of_speech == POS_NOUN_SHORT:
            # gender
            if self.parsing_info.find('masculine') > -1:
                gen = 'm'
            elif self.parsing_info.find('feminine') > -1:
                gen = 'f'
            elif self.parsing_info.find('neuter') > -1:
                gen = 'n'
            else:
                gen = ''

            # number
            if self.parsing_info.find('singular') > -1:
                num = 's'
            elif self.parsing_info.find('plural') > -1:
                num = 'p'
            else:
                num = ''

            # case
            if self.parsing_info.find('nominative') > -1:
                case = 'n'
            elif self.parsing_info.find('genitive') > -1:
                case = 'g'
            elif self.parsing_info.find('dative') > -1:
                case = 'd'
            elif self.parsing_info.find('accusative') > -1:
                case = 'a'
            else:
                case = ''

            try:
                return greek.articles[gen + num + case]
            except KeyError:
                pass
        return ''