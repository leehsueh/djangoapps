# script to parse the plain text kjv Bible ('bible13.txt')
# bible13.txt downloaded from Project Gutenburg
import string
import re

def strip_header(file, starttext):
    temp = file.readline()
    while temp.find(starttext) == -1:
        temp = file.readline()
    return file

def read_kjv(filename):
    """Parse KJV bible into a dictionary
    books[(book#, 'bookname')]['chp#']['verse#'] = verse text
    """
    books = dict()
    curr_book = ''
    curr_chapter = 0
    curr_verse = 0
    empty = []
    verse_text = empty
    endtext = 'python_end'
    
    fi = open(filename)
    fi = strip_header(fi, 'python_start')
    for line in fi:
        if line.find(endtext) != -1:
            fi.close()
            
            # store the text of last verse
            if verse_text != empty:
                #print curr_book, str(curr_chapter) + ':' + str(curr_verse), ' '.join(verse_text)
                books[curr_book][curr_chapter][curr_verse] = ' '.join(verse_text)
                verse_text = empty
            break
        
        line = line.strip()
        words = line.split()
        if line == '\n' or not len(words): 
            #print 'line break'
            continue
        
        new_book = words[0] == 'Book'
        new_verse = re.match(r'[0-9]{2}:[0-9]{3}:[0-9]{3}', words[0])
        
        # new book or new verse
        if new_book or new_verse:
            # store the text of previous verse
            if verse_text != empty:
                #print curr_book, str(curr_chapter) + ':' + str(curr_verse), ' '.join(verse_text)
                books[curr_book][curr_chapter][curr_verse] = ' '.join(verse_text)
                verse_text = empty
            
            if new_book:
                print "\nReading Book", words[1], ":", ' '.join(words[2:])
                curr_book = (int(words[1]), ' '.join(words[2:]))
                curr_chapter = 0
                books[curr_book] = dict()
            else:
                # parse reference
                ref = words[0].split(':')
                chapter = string.atoi(ref[1])
                curr_verse = string.atoi(ref[2])
                
                # update current chapter if changes
                if chapter != curr_chapter:
                    curr_chapter = chapter
                    books[curr_book][curr_chapter] = dict()
                    # print "\nnew chapter key for", curr_book, "\n"
                
                # start building new verse
                verse_text = words[1:]
        
        # continue aggregating text of current verse
        else:
            verse_text += words
    
    return books
    
# print some stats
def print_stats(bible_dict):
    # chapters and verses per book
    num_chapters = 0
    num_verses = 0
    books = bible_dict.keys()
    books.sort()
    for book in books:
        num_chapters += len(bible_dict[book])
        book_verses = 0
        for chapter in bible_dict[book]:
            book_verses += len(bible_dict[book][chapter])
        num_verses += book_verses
        print book[1], '\t\t', str(len(bible_dict[book])), 'chapters\t', str(book_verses), 'verses'
    print 'Total of 66 books,', str(num_chapters), 'chapters', str(num_verses), 'verses'
 
# generate sql from bible dictionary generated from read_kjv
def generate_sql(bible_dict, db_table, dbtype, filename):
    #insert into bibledb_verse (book, chapter_ref, verse_ref, verse_text) values ('Genesis', 1, 1, 'In the beginning, God created the heaven and the earth')
    if not dbtype == 'mysql' and not dbtype == 'postgresql': return
    
    sql_file = open(filename, 'w')
    books = bible_dict.keys()
    books.sort()
    for book in books:
        for chapter in bible_dict[book]:
            for verse, text in bible_dict[book][chapter].items():
                if dbtype == 'mysql':
                    sql_file.write("INSERT INTO " + db_table \
                    + "\n\t(book, chapter_ref, verse_ref, verse_text)\n\tvalues ('" \
                    + book[1] + "'," + str(chapter) + "," + str(verse) + ", \"" + text + "\"\n);\n")
                else: #postgresql
                    text = text.replace("'","''")
                    sql_file.write("INSERT INTO " + db_table \
                    + " (id, book, chapter_ref, verse_ref) values (nextval('" + db_table + "_id_seq'::regclass), '" \
                    + book[1] + "'," + str(chapter) + "," + str(verse) + ");\n")
    
    sql_file.close()
    
filename = 'bible13'
bible = read_kjv(filename + '.txt')
dbtype = 'postgresql'
generate_sql(bible, 'bible_tidbits_verse', 'postgresql', 'verse_data' + '_' + dbtype + '.sql')