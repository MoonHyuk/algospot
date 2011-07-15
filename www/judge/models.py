# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Problem(models.Model):
    DRAFT, PENDING_REVIEW, HIDDEN, PUBLISHED = range(4)
    STATE_CHOICES = ((DRAFT, "DRAFT"),
            (PENDING_REVIEW, "PENDING REVIEW"),
            (HIDDEN, "HIDDEN"),
            (PUBLISHED, "PUBLISHED"))

    slug = models.SlugField(blank=True,max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    state = models.SmallIntegerField(default=DRAFT, choices=STATE_CHOICES)
    user = models.ForeignKey(User)
    source = models.TextField(max_length=100, blank=True)
    name = models.TextField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    input = models.TextField(blank=True)
    output = models.TextField(blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    note = models.TextField(blank=True)
    judge_module = models.TextField(blank=True,max_length=100)
    time_limit = models.PositiveIntegerField(default=10000)
    memory_limit = models.PositiveIntegerField(default=65536)
    submissions_count = models.IntegerField(default=0)
    accepted_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("judge-problem-read", kwargs={"slug": self.slug})

class Submission(models.Model):
    (RECEIVED, COMPILING, RUNNING, JUDGING, COMPILE_ERROR,
    OK, ACCEPTED, WRONG_ANSWER, RUNTIME_ERROR, TIME_LIMIT_EXCEEDED,
    CANT_BE_JUDGED, REJUDGE_REQUESTED) = range(12)
    STATES_KOR = dict([
        (RECEIVED, u"수신"),
        (COMPILING, u"컴파일중"),
        (RUNNING, u"실행중"),
        (JUDGING, u"채점중"),
        (COMPILE_ERROR, u"컴파일 실패"),
        (OK, u"수행완료"),
        (ACCEPTED, u"정답"),
        (WRONG_ANSWER, u"오답"),
        (RUNTIME_ERROR, u"런타임 오류"),
        (TIME_LIMIT_EXCEEDED, u"시간초과"),
        (CANT_BE_JUDGED, u"채점실패"),
        (REJUDGE_REQUESTED, u"재채점")])
    STATES_ENG = dict([
        (RECEIVED, "RECEIVED"),
        (COMPILING, "COMPILING"),
        (RUNNING, "RUNNING"),
        (JUDGING, "JUDGING"),
        (COMPILE_ERROR, "COMPILE_ERROR"),
        (OK, "OK"),
        (ACCEPTED, "ACCEPTED"),
        (WRONG_ANSWER, "WRONG_ANSWER"),
        (RUNTIME_ERROR, "RUNTIME_ERROR"),
        (TIME_LIMIT_EXCEEDED, "TIME_LIMIT_EXCEEDED"),
        (CANT_BE_JUDGED, "CANT_BE_JUDGED"),
        (REJUDGE_REQUESTED, "REJUDGE_REQUESTED")])


    PROGRAM_HAS_RUN = [OK, ACCEPTED, WRONG_ANSWER]
    HAS_MESSAGES = [COMPILE_ERROR, RUNTIME_ERROR]

    submitted_on = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey(User)
    language = models.TextField(max_length=100)
    state = models.SmallIntegerField(default=RECEIVED,
            choices=STATES_ENG.items())
    length = models.IntegerField()
    source = models.TextField()
    message = models.TextField(blank=True, default="")
    time = models.IntegerField(null=True)
    memory = models.IntegerField(null=True)

    def has_run(self):
        return self.state in self.PROGRAM_HAS_RUN

    def has_messages(self):
        return self.state in self.HAS_MESSAGES

    def name_kor(self):
        return self.STATES_KOR[self.state]

    def name_eng(self):
        return self.STATES_ENG[self.state]

