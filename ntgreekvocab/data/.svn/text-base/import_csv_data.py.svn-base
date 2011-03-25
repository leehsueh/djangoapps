"""
CREATE script from excel/CSV data
setup:
- from google docs, save as Text file (.tsv)
OR
- from excel, save greek_vocab.xls as Unicode text (tab delimited)
- open the unicode txt in notepad++
- set the Format to "Encode in UTF-8 without BOM"
- save the txt
"""

"""Constants"""
POS_NOUN_SHORT = 'n'
POS_PRONOUN_SHORT = 'pn'
POS_VERB_SHORT = 'v'
POS_ADJ_SHORT = 'adj'
POS_PREP_SHORT = 'prep'
POS_ADV_SHORT = 'adv'
POS_CONJ_SHORT = 'conj'
POS_PRTCPL_SHORT = 'prtcpl'
POS_CONSTRUCT_SHORT = 'construct'
POS_PHRASE_SHORT = 'phrase'
POS_PRTCL_SHORT = 'prtcl'
POS_CMP_SHORT = 'cmp'

col_word = 'greek_word'
col_pos = 'part_of_speech'
col_def = 'definition'
col_parse = 'parsing_info'
col_notes = 'notes'
col_ln = 'lesson_number'
col_hints = 'hints'

def create_script(input_file, output_file):
    DELIMITER = '\t'
    tbl = 'ntgreekvocab_simplecard'
    pos_map = {
        'noun': POS_NOUN_SHORT,
        'pronoun': POS_PRONOUN_SHORT,
        'verb': POS_VERB_SHORT,
        'conjunction': POS_CONJ_SHORT,
        'preposition': POS_PREP_SHORT,
        'adverb': POS_ADV_SHORT,
        'adjective': POS_ADJ_SHORT,
        'participle': POS_PRTCPL_SHORT,
        'construct': POS_CONSTRUCT_SHORT,
        'phrase': POS_PHRASE_SHORT,
        'particle': POS_PRTCL_SHORT,
        'comparative': POS_CMP_SHORT,
        }
    
    fi = open(input_file, 'r')
    data = []
    for line in fi:
        if not line.strip() or line[0] == '#':
            continue
        row = line.split(DELIMITER)
        if row[0].strip() == 'Word':
            continue
        if len(row) == 6:
            data.append({
                col_word: row[0].replace('"',''),
                col_pos: pos_map[row[1]].replace('"',''),
                col_def: row[2].replace('"','').replace("'","''"),
                col_ln: row[3],
                col_parse: row[4].replace('"',''),
                col_notes: row[5].replace('"','').strip()
            })
        elif len(row) == 7: # sheets for ln14ff have hints column
            data.append({
                col_word: row[0].replace('"',''),
                col_pos: pos_map[row[1]].replace('"',''),
                col_def: row[2].replace('"','').replace("'","''"),
                col_ln: row[3],
                col_parse: row[4].replace('"',''),
                col_notes: row[5].replace('"','').strip(),
                col_hints: row[6].replace('"','').strip()
            })
        else:
            print 'Skipped row: ', row
    fi.close()

    # create script file
    fo = open(output_file,'w')
    for row in data:
        sql = 'INSERT INTO ' + tbl + '\n\t('
        attrs = row.keys()
        for attr in attrs[:-1]:
            sql += attr + ','
        sql += attrs[-1] + ')\n\tVALUES ('
        for attr in attrs[:-1]:
            sql += "'" + row[attr] + "'" + ','
        sql += "'" + row[attrs[-1]] + "'" + ');\n'  # last attribute is parsing_info
        fo.write(sql)
    fo.close()


#create_script('greek_vocab_utf8.txt', 'create_script_101108.sql')
import sys
import datetime
if len(sys.argv) != 2:
    print "Usage: python import_csv_data.py [filename]"
else:
    input_filename = sys.argv[1]
    try:
        test_open = open(input_filename, 'r')
        test_open.close()
        output_filename = 'create_script_' + str(datetime.date.today()) + '.sql'
        create_script(input_filename, output_filename)
        print output_filename + ' created.'
    except IOError:
        print input_filename + ' does not exist or is not a file.'