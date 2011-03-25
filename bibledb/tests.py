from django.test import TestCase

class ViewSanityTest(TestCase):
    fixtures = ['verse_data.json']
    def test_bible_views(self):
        """
        Tests that bible views return 200
        """
        response = self.client.get('/bible/')
        self.assertEquals(200, response.status_code)
        response = self.client.get('/bible/', {'book':'Genesis', 'chapter':1, 'startverse':2, 'endverse':3})
        self.assertRedirects(response,'/bible/genesis/1/2-3/',msg_prefix='Browse bible redirect')
        
        response = self.client.get('/bible/2-timothy/')
        self.assertEquals(200, response.status_code,'display chapters for a book')
        
        response = self.client.get('/bible/1-timothy/2/')
        self.assertEquals(200, response.status_code, 'display verses for a chapter')
        
        response = self.client.get('/bible/1-kings/23/')
        self.assertEquals(404, response.status_code, 'invalid chapter reference expects 404')

class AjaxTest(TestCase):
    fixtures = ['verse_data.json']
    
    def test_ajax_passage(self):
        """
        Tests that passages are returned if
        parameters are correct and valid
        """
        # error strings
        invalid_verses = 'Invalid verse(s)'
        ev_gt_sv = 'End verse must be greater than start verse.'
        invalid_chapter_frag = 'Invalid chapter'
        
        # valid request
        response = self.client.get('/ajax/passage/Genesis/1/2-7/')
        self.assertContains(response,'Genesis 1:2-7',msg_prefix='Valid request: ')

        # valid request with one verse
        response = self.client.get('/ajax/passage/1%20Corinthians/13/1/')
        self.assertContains(response,'1 Corinthians 13:1',msg_prefix='Valid request, 1 verse: ')
        
        # valid request with spaces in the bookname
        response = self.client.get('/ajax/passage/Song%20of%20Solomon/8/3-12/')
        self.assertContains(response,'Song of Solomon 8:3-12',msg_prefix='Valid request, bookname with spaces: ')
        
        # invalid request with ev > sv
        response = self.client.get('/ajax/passage/Proverbs/22/4-1/')
        self.assertContains(response,ev_gt_sv,msg_prefix='Invalid request, ev > sv: ')
        
        # invalid request with invalid verses
        response = self.client.get('/ajax/passage/Matthew/28/4-100/')
        self.assertContains(response,invalid_verses,msg_prefix='Invalid request, invalid verses: ')
        
        # invalid request with invalid chapter
        response = self.client.get('/ajax/passage/Obadiah/2/1-2/')
        self.assertContains(response,invalid_chapter_frag,msg_prefix='Invalid request, invalid chapter: ')