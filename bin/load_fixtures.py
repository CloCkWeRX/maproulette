#!/usr/bin/env python

from maproulette import app, config
from maproulette.models import db, Challenge, Task, TaskGeometry, Action
import geojson
from shapely.geometry import Point, LineString, GeometryCollection
import uuid
import random

NUM_TASKS = 1000

# the gettysburg address
words = """Four score and seven years ago our fathers
brought forth on this continent, a new nation, conceived
in Liberty, and dedicated to the proposition that all men
are created equal. Now we are engaged in a great civil war,
testing whether that nation, or any nation so conceived and
so dedicated, can long endure. We are met on a great
battle-field of that war. We have come to dedicate a
portion of that field, as a final resting place for those
who here gave their lives that that nation might live.
It is altogether fitting and proper that we should do this.
But, in a larger sense, we can not dedicate -- we can not
consecrate -- we can not hallow -- this ground. The brave men,
living and dead, who struggled here, have consecrated it,
far above our poor power to add or detract. The world will
little note, nor long remember what we say here, but it can
never forget what they did here. It is for us the living,
rather, to be dedicated here to the unfinished work which
they who fought here have thus far so nobly advanced. It
is rather for us to be here dedicated to the great task
remaining before us -- that from these honored dead we take
increased devotion to that cause for which they gave the last
full measure of devotion -- that we here highly resolve that
these dead shall not have died in vain -- that this nation,
under God, shall have a new birth of freedom -- and that
government of the people, by the people, for the people, shall
not perish from the earth."""

# the first part of the I have a dream speech
words2 = """Five score years ago, a great American, in whose
symbolic shadow we stand signed the Emancipation Proclamation.
This momentous decree came as a great beacon light of hope
to millions of Negro slaves who had been seared in the flames
of withering injustice. It came as a joyous daybreak to end the
long night of captivity."""

point = Point(0.0, 0.0)

app.config.from_object(config.DevelopmentConfig)

# delete old tasks and challenges
db.session.query(TaskGeometry).delete()
db.session.query(Action).delete()
db.session.query(Task).delete()
db.session.query(Challenge).delete()
db.session.commit()

# add a new challenge
challenge = Challenge('test')
challenge.title = 'Test Challenge'
challenge.difficulty = 1
challenge.active = True
challenge.blurb = 'This is a test challenge'
challenge.description = 'This is a test challenge'
challenge.help = words
challenge.instruction = words2
db.session.add(challenge)

# add some tasks
cnt = 0
# generate NUM_TASKS random tasks
for i in range(NUM_TASKS):
    # generate a unique identifier
    identifier = str(uuid.uuid4())
    # instantiate the task and register it with challenge 'test'
    # Initialize a task with its challenge slug and persistent ID
    task = Task('test', identifier)
    # create two random points not too far apart
    p1 = Point(
        random.randrange(-120, -40) + random.random(),
        random.randrange(20, 50) + random.random())
    p2 = Point(
        p1.x + (random.random() * random.choice((1, -1))),
        p1.y + (random.random() * random.choice((1, -1))))
    # create a linestring connecting the two points
    # no constructor for linestring from points?
    l1 = LineString([(p1.x, p1.y), (p2.x, p2.y)])
    # add the first point and the linestring to the task's geometries
    task.geometries.append(TaskGeometry(p1))
    task.geometries.append(TaskGeometry(l1))
    # and add the first point as the task's location
    task.location = p1
    # set the run number to 1, this is the initial run
    task.run = 1
    # generate random string for the instruction
    task.instruction = ' '.join([random.choice(words.split())
                                for _ in range(15)])
    # add the task to the session
    db.session.add(task)

# commit the generated tasks and the challenge to the database.
db.session.commit()
