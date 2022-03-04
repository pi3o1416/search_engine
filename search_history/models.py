
from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
import nltk
import json
import re
# Create your models here.


class SearchHistory(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='user_searched',
        on_delete=models.CASCADE,
    )

    search_text = models.CharField(
        verbose_name=_('User search text'),
        max_length=200,
        blank=False,
    )

    search_time = models.DateTimeField(
        verbose_name=_('Search Time'),
    )

    search_result = models.JSONField(
        verbose_name=_('Search Result Appeared for that perticular search'),
    )

    def __str__(self):
        return self.search_text

    def get_absolute_url(self):
        pass


class KeywordOccurences(models.Model):
    date = models.DateField(
        verbose_name=_('Date')
    )

    keywords = models.JSONField()

    def __str__(self):
        return self.date.__str__()


@receiver(post_save, sender=SearchHistory)
def update_keyword_occurences(sender, instance, **kwargs):
    """
    Update keywordOccurence from search_texts
    """
    tagged_nouns = tag_sentence_words(instance.search_text)
    print('tagged_nouns:', tagged_nouns)
    date = instance.search_time.date()
    try:
        occurence_obj = KeywordOccurences.objects.get(date=date)
        previews_keywords = json.loads(occurence_obj.keywords)
        keywords_dict = defaultdict(int, previews_keywords)

    except ObjectDoesNotExist:
        occurence_obj = KeywordOccurences()
        keywords_dict = defaultdict(int)

    for noun in tagged_nouns:
        keywords_dict[noun] += 1

    keywords_json = json.dumps(keywords_dict)
    print(date, keywords_json)
    occurence_obj.date = date
    occurence_obj.keywords = keywords_json
    occurence_obj.save()


def tag_sentence_words(text):
    """
    Find tag for sentece words
    """
    # remove noisy data
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub('\[[^]]*\]', '', text)

    # remove special charecter
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)

    #Remove Stop Words
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in set(stopwords.words('english'))]

    #Stemming Text
    pstammer = PorterStemmer()
    stemed_words = [pstammer.stem(word) for word in words]

    #determine tag
    tagged_words = nltk.pos_tag(stemed_words)

    final_words = [word for word, tag in tagged_words if tag[0] == 'N']
    return final_words


