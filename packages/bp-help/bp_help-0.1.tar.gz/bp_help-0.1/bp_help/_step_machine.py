
import time
import random
import os
import sys
import pickle
import datetime
import cloudpickle as cp
from urllib.request import urlopen
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

# from .doom_text import doom
from .expressions import get_expression

exec(open(os.path.dirname(__file__) + '/steps.py').read())


def get_input(prompt, allow_empty=False):
    prompt_input = input(prompt).strip()
    while not (allow_empty or prompt_input.isdigit() or prompt_input.lower() == 'quit'):
        print("You need to give a number, or 'quit' to quit.")
        prompt_input = input(prompt).strip()
    if prompt_input.lower() == 'quit':
        raise KeyboardInterrupt
    return prompt_input 


def order_steps():


    global foo, bar, baz, n, label, tag, count, order, mat, counts, records

    integers = [1, 2, 5, 7] # values should overlap with indexes and keys
    random.shuffle(integers)
    foo, bar, baz = integers 
    label, tag, count = 'Ib', 'abcdefg', '42' # values should overlap with keys
    order, mat = [1, 2, 3], [[11, 22], [33, 444]]
    counts, records = {1:11, 2:22}, {'Ib':{'x': 1, 'y': 2}, 'Bo':{'x': 1, 'y': 2}}

    numbers = ['foo', 'bar', 'baz']
    strings = ['label', 'tag', 'count']
    lists = ['order', 'mat']
    dicts = ['counts', 'records']


    global x, y, z, s, t, d, e, f, l, m

    global a, b, aa, bb, aaa, bbb, aaaa, bbbb
    a, b = 1, 2 # values should overlap with indexes and keys
    aa, bb = 'a', 'x' # values should overlap with keys
    aaa, bbb = [1, 2, 3], [[11, 22], [33, 444]]
    aaaa, bbbb = {1:11, 2:22}, {'a':{'x': 1, 'y': 2}, 'b':{'x': 1, 'y': 2}}

    course_start_week = 35

#    course_week_nr = datetime.date.today().isocalendar()[1] - course_start_week + 1
    course_week_nr = 1

    goal_score = sum(x * y for (x, y) in zip(reversed([1/x for x in range(1, course_week_nr+1)]), list(range(1, course_week_nr+1))))

    # for course_week_nr in range(1, 8):
    #     goal_score = sum(x * y for (x, y) in zip(reversed([1/x for x in range(1, course_week_nr+1)]), list(range(1, course_week_nr+1))))
    #     print(goal_score)
    # sys.exit()

    from collections import OrderedDict

    course_week_nr = 8

    leaf_prob = 0.7
    topic_probs = dict(
        types=OrderedDict(dicts=int(course_week_nr >= 5) * 1, 
                lists=int(course_week_nr >= 4) * 1, 
                strings=int(course_week_nr >= 3) * 1, 
                number=int(course_week_nr >= 1) * 1, 
                number_literals=int(course_week_nr >= 1) * 1),
        operations=OrderedDict(parentheses=int(course_week_nr >= 1) * 2, 
                        len=int(course_week_nr >= 3) * 5, 
                        sorted=int(course_week_nr >= 3) * 1, 
                        not_op=int(course_week_nr >= 2) * 1, 
                        logic_op=int(course_week_nr >= 2) * 1, 
                        arithmetic_op=int(course_week_nr >= 1) * 50)
    )
    tot = sum(topic_probs['types'].values())
    for key in topic_probs['types']:
        topic_probs['types'][key] /= tot
    tot = 0
    for key in topic_probs['types']:
        tot += topic_probs['types'][key]
        topic_probs['types'][key] = tot

    tot = sum(topic_probs['operations'].values())
    for key in topic_probs['operations']:
        topic_probs['operations'][key] /= tot
    tot = 0
    for key in topic_probs['operations']:
        print(tot)
        tot += topic_probs['operations'][key]
        print(tot)
        topic_probs['operations'][key] = tot

    # print(topic_probs['types'].values())    
    # print(topic_probs['operations'].values())    
    # assert 0



    try:

        pickle_file_name = os.path.dirname(__file__) + '/progress.pkl'
        if os.path.exists(pickle_file_name):
            with open(pickle_file_name, 'rb') as pickle_file:
                progress = pickle.load(pickle_file)
        else:
            progress = {'scores': [], 'current_score': 0}

        # update scores
        now = time.time()
        progress['scores'] = [(s * 0.999999**(now - t), now) for s, t in progress['scores']]
        # TODO: make sure score degrades at the right pace

        term_width = os.get_terminal_size().columns

        # print('\n' * 100)
        # title = doom['STEPS OF DOOM']
        # print_width = max(map(len, title.split('\n')))
        # # for line in steps_of_doom.split('\n'):
        # for line in title.split('\n'):
        #     time.sleep(0.1)
        #     pad = 0
        #     if print_width < term_width:
        #         pad = int((term_width - print_width) / 2)
        #     print(' '*pad, line)
        # time.sleep(1)
        # print('\n' * 100)
        # doom_print('Score:', int(progress['current_score']  * 1000000))
        # time.sleep(1)
        # doom_print('Your goal:', int(progress['current_score']  * 1000000))
        # time.sleep(1)
        # user_input = get_input('Press enter to begin ', allow_empty=True)
        # print('\n' * 100)

        while True:

            steps_list = []
            while len(steps_list) < 2 or any(len(x) > 80 for x in steps_list):
                expr = get_expression(1, leaf_prob=leaf_prob, topic_probs=topic_probs)
                steps_list = _steps(expr)

            corret_order = steps_list[:]
            while all(x == y for x, y in zip(steps_list, corret_order)):
                random.shuffle(steps_list)

            attempts_allowed = len(steps_list) * 3

            begin = time.time()
            score = 0 
            for attempt in range(attempts_allowed):
                print('\n' * 100)
                print('The steps are not in the right order!\n')
                for i, s in enumerate(steps_list):
                    print(f'{i+1:<10}', s)
                print('\n' * 4)
                nr = get_input('Pick a line you want to move: ')
                idx = int(nr) - 1
                line = steps_list.pop(idx)

                print('\n' * 100)
                print(f'Ok, this is the order of lines with that line removed:\n')
                for i, s in enumerate(steps_list):
                    print(f'{i+1:<10}', s)
                print(f'{i+1+1:<10}')
                print()
                print('Now, what should be the new position of:\n')
                print(f'{"?".ljust(10)}{line}\n')
                nr = get_input(f'Line nr: ')
                idx = int(nr) - 1
                
                steps_list.insert(idx, line)

                # your running avg score across the past 20 probems must be at least of 1.2 
                # to proceed to next level
                # your score is reduced by roughly 10% every day, so you need to keep practising

                if all(x == y for x, y in zip(steps_list, corret_order)):

                    spent = time.time() - begin
                    print('\n' * 100)
                    for i, s in enumerate(steps_list):
                        print(f'{i+1:<10}', s)
                    # score = int(len(steps_list)/(attempt+1)/spent * 100000)
                    score = course_week_nr * len(steps_list)/(attempt+1)

                    doom_print('Correct! +', int(score * 1000000))

                    # TODO: Make sure no progress is lost on KeyboardInterrupt: catch keyboard interrupt like in slurm-jupyter

                    break

            if attempt == attempts_allowed:
                print(doom['Skipping this one...'])
                # TODO: allow user to skip same was as quit
                # TODO: punish for skipping or using all attempts
            else:
                progress['scores'].append((score, time.time()))
                progress['current_score'] = sum(s for (s, t) in progress['scores'][-20:])/20 #* 0.9**(time.time() - progress['time'])/(60 * 60 * 24)

                with open(pickle_file_name, 'wb') as pickle_file:
                    pickle.dump(progress, pickle_file)

                doom_print('Score:', int(progress['current_score']  * 1000000))

                points_missing = goal_score - progress['current_score']  * 1000000
                if points_missing > 0  and points_missing < 100000000:
                    print('Almost there...')
                    print('Earn', 'XX' 'to reach goal')

                # # encouragement:
                # print(random.choices(doom['praise'], k=1)[0])



            user_input = get_input('Press enter when you are ready for the next one or "quit" to quit: ', allow_empty=True)
            if user_input.strip() == 'quit':
                break
    except KeyboardInterrupt:
        print('\n' * 100)
        doom_print('Score:', int(progress['current_score']  * 1000000))
        print(random.choices(doom['praise'], k=1)[0])
        doom_print('Bye for now...')
        sys.exit()
            


# TODO

# How to save progress accross sessions (maybe just write a pickle file in the library dir)
# How to make new levels available week by week (release by date or password given at lectures)
# How to compute proficiency at each level
# How to compute how score at each level expires (invert arrow when close)
