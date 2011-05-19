truncate bible_tidbits_tidbit_cross_refs cascade;
truncate bible_tidbits_tidbit_tags cascade;
truncate bible_tidbits_crossref cascade;
truncate bible_tidbits_tag cascade;
truncate bible_tidbits_tidbit cascade;
SELECT setval('public.bible_tidbits_tidbit_tags_id_seq', 1, false);
SELECT setval('public.bible_tidbits_crossref_id_seq', 1, false);
SELECT setval('public.bible_tidbits_tag_id_seq', 1, false);
SELECT setval('public.bible_tidbits_tidbit_cross_refs_id_seq', 1, false);
SELECT setval('public.bible_tidbits_tidbit_id_seq', 1, false);

