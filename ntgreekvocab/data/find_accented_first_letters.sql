SELECT * FROM ntgreekvocab_simplecard
WHERE
    greek_word like 'Ά%' OR
    greek_word like 'Έ%' OR
    greek_word like 'Ή%' OR
    greek_word like 'Ί%' OR
    greek_word like 'Ό%' OR
    greek_word like 'Ύ%' OR
    greek_word like 'Ώ%' OR
    greek_word like 'ΐ%' OR
    greek_word like 'Ϊ%' OR
    greek_word like 'Ϋ%' OR
    greek_word like 'ά%' OR
    greek_word like 'έ%' OR
    greek_word like 'ή%' OR
    greek_word like 'ί%' OR
    greek_word like 'ΰ%' OR
    greek_word like 'ϊ%' OR
    greek_word like 'ϋ%' OR
    greek_word like 'ό%' OR
    greek_word like 'ύ%' OR
    greek_word like 'ώ%';

SELECT * FROM ntgreekvocab_simplecard
WHERE
    greek_word like '%ά%' OR
    greek_word like '%έ%' OR
    greek_word like '%ή%' OR
    greek_word like '%ί%' OR
    greek_word like '%ΰ%' OR
    greek_word like '%ϊ%' OR
    greek_word like '%ϋ%' OR
    greek_word like '%ό%' OR
    greek_word like '%ύ%' OR
    greek_word like '%ώ%';
