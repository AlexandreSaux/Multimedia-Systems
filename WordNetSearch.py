﻿# API KEY - AIzaSyCsz2kG8FnqX_ehWEQimvreksyBRWL1eNg

from googleapiclient.discovery import build
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter

nltk.download('omw-1.4')

ps = PorterStemmer()
lm = WordNetLemmatizer()

SEARCH_TYPE = "customsearch"
VERSION = "v1"
API_KEY = "AIzaSyCsz2kG8FnqX_ehWEQimvreksyBRWL1eNg"

SEARCH_ENGINE_ID = 'b360fd3ec1b70b6b8'

service = build(SEARCH_TYPE, VERSION, developerKey=API_KEY)

##################################
# Data retrieval and processing
##################################
def get_results(query, num_results):
    position = 1        # Current search result (default to 1).

    titles = []         # To hold data.
    snippets = []
    links = []
    all_items = []

    for num in range(1, num_results):     # Retrieves search results in batches of 10, based on NUM_RESULTS. 
        position += 10

        search_results = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, start=position).execute()

        # Key Types: ['kind', 'url', 'queries', 'context', 'searchInformation', 'items']

        query_info = search_results['queries']
        items = search_results['items']

        all_items += items

        #print(items)
        #print()

        for item in items:                          # Get specific metadata from search result.
            titles.append(item['title'])
            snippets.append(item['snippet'])
            links.append(item['link'])

    return { 'items': all_items, 'titles': titles, 'snippets': snippets, 'links': links }
    
#print(titles)
#print(snippets)
#print(links)


def process_results(data):

    raw_tokens = []
    # Constant set of previously retrieved tokens to test with if needed.
    #raw_tokens = ['Supreme', 'Court', 'Strikes', 'Down', 'Curtis', "Flowers'", 'Death', 'Row', 'Conviction', '...', '5', 'Moments', 'of', "Chopin's", 'Life', 'As', 'If', 'They', 'Were', 'Flowers', '—', 'Google', 'Arts', '...', 'Spring', 'Flowers', 'HD', 'Wallpapers', 'New', 'Tab', 'Theme', 'Bengals', 'Acquire', 'CB', 'Trey', 'Flowers', 'On', 'Waivers', 'Detroit', 'Lions', 'sign', 'Trey', 'Flowers', 'to', 'five-year', 'deal', 'Roses,', 'Convolvulus,', 'Poppies,', 'and', 'Other', 'Flowers', 'in', 'an', 'Urn', 'on', 'a', '...', 'The', 'Latest', 'on', 'Curtis', 'Flowers', '|', 'APM', 'Reports', 'The', 'Tomb', 'of', 'the', 'Unknown', 'Soldier:', 'Public', 'allowed', 'to', 'lay', 'flowers', 'at', '...', 'Stop', 'and', 'Smell', 'the', 'Flowers', 'Taylor', 'Swift', 'sends', 'flowers', 'to', 'Don', 'McLean', 'after', 'song', 'breaks', 'record', '...', 'Tyler', 'Flowers', 'Joins', 'The', 'Atlanta', 'Braves', 'Once', 'Again', 'Why', 'are', 'my', 'hops', 'producing', 'male', 'flowers?', '-', 'MSU', 'Extension', 'There', 'Is', 'A', 'Massive', 'Flower', 'Shortage', 'Right', 'Now', '|', 'Washingtonian', '(DC)', 'The', 'Supreme', 'Court', 'cases', 'that', 'could', 'free', 'Curtis', 'Flowers', '|', 'In', 'the', 'Dark', '...', 'Supernatural', 'with', 'Ashley', 'Flowers', 'on', 'Apple', 'Podcasts', 'Opinion', 'analysis:', 'Justices', 'reverse', 'death', 'sentence', 'for', 'Mississippi', '...', 'Supreme', 'Court', 'agrees', 'to', 'hear', 'Curtis', 'Flowers', 'appeal', '|', 'In', 'the', 'Dark', '...', 'Obituary', 'for', 'Cleon', 'Aurelius', 'Flowers,', 'Philadelphia,', 'PA', 'Flowers', 'v.', 'Mississippi:', 'An', 'annotated', 'transcript', 'of', 'oral', 'arguments', 'at', '...', 'Starlings', 'Say', 'It', 'With', 'Flowers', '|', 'BirdNote', 'Very', 'Presidential', 'with', 'Ashley', 'Flowers', 'on', 'Apple', 'Podcasts', 'Power', 'plants:', 'making', 'electricity', 'from', 'flowers', 'and', 'fruits', 'Success', 'with', 'Sweet', 'Peas', '-', 'Floret', 'Flowers', 'Lions', 'trade', 'rumors:', 'Is', 'there', 'a', 'robust', 'market', 'for', 'Trey', 'Flowers?', 'Marguerite', 'Flowers', 'Birds', 'and', 'Flowers', 'of', 'Spring', 'and', 'Summer', '-', 'Kano', 'Eino', '—', 'Google', '...', 'Tyler', 'Flowers', 'To', 'Retire', '-', 'MLB', 'Trade', 'Rumors', 'Cat', 'Knocking', 'over', 'a', 'Vase', 'of', 'Flowers', '-', 'Abraham', 'Mignon', '—', 'Google', '...', 'Flowers', 'in', 'a', 'Wooden', 'Vessel', '-', 'Jan', 'Brueghel', 'the', 'Elder', '—', 'Google', '...', 'Bumblebees', 'use', 'logic', 'to', 'find', 'the', 'best', 'flowers', '--', 'ScienceDaily', 'Why', 'marigolds', 'are', 'the', 'iconic', 'flower', 'of', 'the', 'Day', 'of', 'the', 'Dead', ':', 'NPR', 'Flowers:', 'How', 'Do', 'They', 'Move?', '|', 'Time', 'Oldest', 'Use', 'of', 'Grave', 'Flowers', 'Unearthed', '|', 'Live', 'Science', 'Bouquet', 'of', 'Flowers', 'in', 'a', 'Glass', 'Vase', '-', 'Ambrosius', 'Bosschaert', 'the', '...', 'Newsletter', '-', 'Floret', 'Flowers', 'Vase', 'of', 'Flowers', '-', 'Jan', 'Davidsz', 'de', 'Heem', '—', 'Google', 'Arts', '&', 'Culture', 'International', 'Infamy', 'with', 'Ashley', 'Flowers', 'on', 'Apple', 'Podcasts', 'Curtis', 'Flowers:', 'Charges', 'dropped', 'by', 'Mississippi', 'Attorney', 'General', 'Flowwow', '–', 'Reliable', 'delivery', '-', 'Apps', 'on', 'Google', 'Play', 'Ecuadorian', 'Cactus', 'Absorbs', 'Ultrasound,', 'Enticing', 'Bats', 'to', 'Flowers', '...', 'Crystal', 'Flowers', 'Spring', 'Activity', '-', 'Little', 'Bins', 'for', 'Little', 'Hands', 'International', 'Infamy', 'with', 'Ashley', 'Flowers', 'on', 'Apple', 'Podcasts', 'Curtis', 'Flowers:', 'Charges', 'dropped', 'by', 'Mississippi', 'Attorney', 'General', 'Ecuadorian', 'Cactus', 'Absorbs', 'Ultrasound,', 'Enticing', 'Bats', 'to', 'Flowers', '...', 'What', 'to', 'Know', 'About', 'the', 'Flowers', 'at', 'the', '2020', 'Summer', 'Olympics', '|', 'Time', "UK's", 'McQueens', 'Flowers', 'opens', 'in', 'NYC', 'Still-Life', 'with', 'Flowers', '-', 'Ambrosius', 'Bosschaert', 'the', 'Elder', '—', 'Google', '...', 'Springtime', 'in', 'the', 'city:', 'Thousands', 'of', 'flowers', 'now', 'in', 'bloom', 'on', "NYC's", '...', 'New', 'deal', 'to', 'sell', 'Koffee', 'Kup', 'to', 'Flowers', 'Foods', 'Best', 'Flowers', 'to', 'Plant', 'in', 'Fall', '-', '12+', 'Fall', 'Flowers', 'to', 'Plant', '99', 'million-year-old', 'flowers', 'found', 'perfectly', 'preserved', 'in', 'amber', 'Detroit', 'Lions', 'training', 'camp', 'spotlight:', 'Outside', 'linebacker', 'Trey', 'Flowers.', 'Buy', 'the', 'flowers', '–', 'Modern', 'Mrs', 'Darcy', 'Spotlight:', 'The', 'Supreme', 'Court', 'on', 'Curtis', 'Flowers—Right', 'for', 'the', '...', 'The', 'origin', 'of', 'flowers:', 'DNA', 'of', 'storied', 'plant', 'provides', 'insight', 'into', 'the', '...', 'These', 'Flowers', 'Come', 'Straight', 'From', 'the', 'Farm', 'to', 'Your', 'Door', '...', 'Cut', 'flowers', 'last', 'longer', 'with', 'silver', 'nanotechnology', '--', 'ScienceDaily', 'Dolphins', 'paid', 'Ereck', 'Flowers', '$6', 'million', 'of', 'his', '2021', 'pay', 'before', '...', 'Court', 'Ladies', 'Adorning', 'Their', 'Hair', 'with', 'Flowers', '-', 'Zhou', 'Fang', '...', 'The', 'daily', 'dance', 'of', 'flowers', 'tracking', 'the', 'sun', 'is', 'more', 'fascinating', 'than', '...', 'Curtis', 'Flowers', 'suing', 'DA', 'who', 'prosecuted', 'him', '-', 'Mississippi', 'Today', 'How', 'a', 'Love', 'of', 'Flowers', 'Helped', 'Charles', 'Darwin', 'Validate', 'Natural', '...', 'Delivering', 'smiles', 'and', 'sparking', 'innovation', 'at', '1-800-FLOWERS.COM', '...', 'Why', 'Fruits', 'Ripen', 'And', 'Flowers', 'Die:', 'Scientists', 'Discover', 'How', 'Key', '...', 'Untitled', '(Vase', 'of', 'Flowers)', '-', 'Georgia', "O'Keeffe", '—', 'Google', 'Arts', '&', 'Culture', 'Financials', 'of', "Dolphins'", 'trade', 'of', 'Ereck', 'Flowers', 'tell', 'quite', 'the', 'story', 'Flowers', 'never', 'last.', 'A', 'Tampa', 'Bay', 'group', 'gives', 'them', 'a', 'final', 'gasp.', 'Vodka,', 'Aspirin', 'or', '7Up:', 'What', 'Keeps', 'Flowers', 'Fresh?', '|', 'Live', 'Science', 'Bloom:', '28,000', 'Potted', 'Flowers', 'Installed', 'at', 'the', 'Massachusetts', 'Mental', '...', "It's", 'bloom', 'time', 'in', "Chile's", "'flowering", "desert',", 'despite', 'drought', '|', 'Reuters', 'Makeup', 'Artist,', 'Model', 'and', 'Muse', 'Raisa', 'Flowers', 'Is', 'Bringing', 'Her', 'Own', '...', 'These', 'Are', 'the', 'Trending', 'Flowers', 'for', '2022,', 'According', 'to', '6', 'Experts', '...', 'Lions', 'activate', 'defensive', 'end', 'Trey', 'Flowers', 'from', 'PUP', 'list,', 'putting', 'him', '...', 'Buzz', 'pollination:', 'studying', 'bee', 'vibrations', 'on', 'flowers', '-', 'Vallejo‐Marín', '...', 'Bees', 'Prefer', 'Shortest', 'Distance', 'Between', 'Two', 'Flowers', '--', 'ScienceDaily', 'Aspidistrafly,', "'The", 'Voice', 'of', "Flowers'", ':', '#NowPlaying', ':', 'NPR', 'Beautiful', 'Blooms', 'Look', 'Like', 'Real-Life', 'Flowers', 'Takashi', 'Murakami', 'Teases', "'Murakami.Flower'", 'NFTs', '|', 'HYPEBEAST', 'Ancient', 'Roots:', 'Flowers', 'May', 'Have', 'Existed', 'When', 'First', 'Dinosaur', 'Was', '...', 'Flowers', 'for', 'Society', 'Is', 'Uniting', 'Sneakers', 'and', 'NFT', '|', 'HYPEBEAST', '9', 'Places', 'to', 'Buy', "Mother's", 'Day', 'Flowers', 'Online', 'in', '2021:', 'the', 'Bouqs', 'Co', '...', "Missouri's", 'ephemeral', "'ice", "flowers'", 'emerge', 'this', 'time', 'of', 'year.', 'Spot', '...', 'How', 'to', 'Arrange', 'Flowers', 'Like', 'a', 'Pro', '-', 'Whole', 'Foods', 'Market', '|', 'Whole', '...', 'Purple', 'flowers(Non-Aero)', 'Sending', "Mother's", 'Day', 'flowers?', 'Take', 'caution', 'Apple', 'Arcade', 'exclusive', 'Wylde', 'Flowers', 'is', 'a', 'cozy', 'life', 'and', 'farming', 'sim', '...', 'Lohmann:', 'Program', 'started', 'by', 'VCU', 'medical', 'student', 'repurposes', '...', 'Announcing', 'the', 'Flea', 'Market', 'Flowers', 'Stitch', 'Along', '-', 'The', 'Jolly', 'Jabber', '...', 'The', 'Best', 'Beauty', 'Instagrams', 'of', 'the', 'Week:', 'Raisa', 'Flowers,', 'Lady', 'Gaga', '...', 'Crystal', 'Flowers', 'Spring', 'Activity', '-', 'Little', 'Bins', 'for', 'Little', 'Hands', 'Jun', '21,', '2019', '...', 'Curtis', 'Flowers', 'was', 'tried', 'six', 'times', 'for', 'the', 'same', 'crime,', 'and', 'the', 'court', 'said', 'it', 'made', 'its', 'decision', 'because', 'of', 'bias', 'in', 'jury', 'selection.', 'Discover', 'flowers', 'that', 'accompanied', 'Chopin', 'in', 'the', 'key', 'moments', 'of', 'his', 'life.', 'By', 'The', 'Fryderyk', 'Chopin', 'Institute.', 'Paweł', 'Siechowicz', '(Chopin', 'Institute).', 'Jan', '31,', '2021', '...', 'Install', 'this', 'theme', 'and', 'enjoy', 'HD', 'wallpapers', 'of', 'Spring', 'Flowers', 'every', 'time', 'you', 'open', 'a', 'new', 'tab.', 'Oct', '14,', '2021', '...', 'The', 'Bengals', 'acquired', 'CB', 'Tre', 'Flowers', 'on', 'waivers', 'from', 'the', 'Seattle', 'Seahawks.', 'Flowers', '(6-3,', '203),', 'a', 'fourth-year', 'player', 'out', 'of', 'Oklahoma', 'State', '...', 'Mar', '11,', '2019', '...', 'The', 'Lions', 'have', 'landed', 'yet', 'another', 'former', 'Patriots', 'player.', 'Detroit', 'is', 'expected', 'to', 'sign', 'defensive', 'end', 'Trey', 'Flowers', 'to', 'a', 'five-year', 'deal,', '...', 'The', 'exuberant', 'profusion', 'of', 'flowers', 'in', 'this', 'still', 'life', 'by', 'Rachel', 'Ruysch', 'celebrates', 'color,', 'texture,', 'and', 'form.', 'Her', 'minute', 'attention', 'to', 'detail', 'captured', 'even', 'th.', 'On', 'Sept.', '4,', '2020,', 'the', 'Mississippi', 'Attorney', 'General', 'dropped', 'all', 'charges', 'against', 'Curtis', 'Flowers.', 'With', 'that,', 'the', 'criminal', 'case', 'of', 'the', 'State', 'of', 'Mississippi', 'v.', 'Nov', '9,', '2021', '...', 'People', 'place', 'flowers', 'during', 'a', 'centennial', 'commemoration', 'event', 'at', 'the', 'Tomb', 'of', 'the', 'Unknown', 'Soldier,', 'in', 'Arlington', 'National', 'Cemetery', 'in', 'Arlington,', '...', 'Longwood', 'Gardens.', 'Garden', 'in', 'the', 'Chester', 'County,', 'Pennsylvania.', 'Vast', 'collection', 'of', 'vibrant', 'flower', 'gardens,', 'plus', 'a', 'greenhouse', 'and', 'fountain', 'shows', '...', 'Dec', '6,', '2021', '...', 'The', 'songstress', 'sent', 'flowers', 'to', 'Don', 'McLean,', 'whose', 'song', '"American', 'Pie"', 'first', 'set', 'the', 'record', 'when', 'it', 'hit', 'No.', '1', 'in', '1972,', 'with', 'a', 'runtime', 'of', 'around', '8', '...', 'Apr', '18,', '2021', '...', 'Tyler', 'Flower', 'has', 'joined', 'the', 'Atlanta', 'Braves', '...', 'In', '2019', 'Flowers', 'tied', 'for', 'first', 'in', 'all', 'of', 'baseball', 'with', 'Austin', 'Hedges', 'in', 'Runs', 'Extra', 'Strikes.', 'Sep', '26,', '2017', '...', 'Male', 'plants', 'produce', 'pollen', 'that', 'can', 'be', 'carried', 'by', 'the', 'wind', 'to', 'female', 'cones;', 'the', 'resulting', 'fertilized', 'female', 'flowers', 'produce', 'seed.', "''", 'Figure', '1.', 'a', '...', 'Sep', '10,', '2021', '...', 'White', 'roses,', 'speciality', 'blooms,', 'and', 'blue', 'flowers', 'have', 'reportedly', 'been', 'impacted', 'the', 'most,', 'but', 'all', 'types', 'of', 'flowers', 'are', 'expensive', 'now,', 'with', 'costs', '...', 'Mar', '14,', '2019', '...', 'The', 'outcome', 'of', 'Flowers', 'v.', 'Mississippi', 'may', 'hinge', 'on', 'how', 'justices', 'interpret', 'a', 'few', 'key', 'precedents', 'designed', 'to', 'bring', 'more', 'fairness', 'and', 'equality', '...', 'Join', 'Parcast', 'and', 'Crime', "Junkie's", 'Ashley', 'Flowers', 'as', 'they', 'dive', 'deep', 'into', 'the', 'strange', 'and', 'surreal', 'to', 'explain', 'some', 'of', 'the', "world's", 'most', 'bizarre', 'true', 'crime', 'occurrences', '...', 'Jun', '21,', '2019', '...', 'Flowers', 'was', 'convicted', 'and', 'sentenced', 'to', 'death.', 'Today', 'the', 'Supreme', 'Court', 'threw', 'out', "Flowers'", 'conviction,', 'with', 'seven', 'justices', 'agreeing', 'that', 'the', 'jury', '...', 'Nov', '2,', '2018', '...', 'In', 'looking', 'at', 'the', 'controversial', 'Mississippi', 'death', 'penalty', 'case,', 'the', 'justices', 'will', 'examine', 'if', 'District', 'Attorney', 'Doug', 'Evans', 'had', 'a', 'history', 'of', '...', 'Jul', '30,', '2021', '...', 'Flowers', 'was', 'born', 'to', 'Dr.', 'Cleon', 'Aurelius', 'Flowers,', 'Sr.', 'and', 'Martha', 'Raspberry', 'Flowers', 'on', 'Saturday,', 'March', '4,', '1944,', 'at', 'Meharry,', 'Hubbard', 'Hospital', 'in', '...', 'Mar', '26,', '2019', '...', 'The', 'full', 'transcript', 'of', 'oral', 'arguments', 'in', 'the', 'Curtis', 'Flowers', 'case,', 'with', 'analysis,', 'context', 'and', 'fact-checks', 'from', 'our', 'team', 'of', 'reporters.', 'Oct', '2,', '2021', '...', 'European', 'Starlings', 'regularly', 'adorn', 'their', 'twig', 'nests', 'with', 'marigolds,', 'elderberry', 'flowers,', 'yarrow', 'leaves,', 'and', 'even', 'willow', 'bark', '—', 'all', 'of', 'which', '...', 'Every', 'Tuesday', 'through', 'the', '2020', 'election,', 'host', 'Ashley', 'Flowers', 'shines', 'a', 'light', 'on', 'the', 'darker', 'side', 'of', 'the', 'American', 'presidency…', 'From', 'torrid', 'love', 'affairs', 'and', '...', 'Aug', '9,', '2021', '...', 'I', 'build', 'solar', 'cells', 'using', 'natural', 'dyes', 'that', 'I', 'find', 'in', 'fruit', 'and', 'flowers.', 'Plant', 'pigments', 'called', 'anthocyanins', 'absorb', 'light', 'and', 'turn', 'it', 'into', '...', 'Dec', '28,', '2019', '...', 'One', 'of', 'my', 'jobs', 'was', 'to', 'keep', 'fresh', 'flowers', 'by', 'my', "Grammy's", 'bedside', 'table.', 'She', 'had', 'a', 'number', 'of', 'beautiful', 'bloomers', 'growing', 'in', 'her', 'garden,', 'but', 'the', '...', 'Oct', '28,', '2021', '...', 'Trey', 'Flowers', 'is', 'widely', 'seen', 'as', 'a', 'player', 'the', 'Lions', 'can', 'and', 'should', 'trade,', 'but', 'is', 'there', 'really', 'a', 'robust', 'market', 'for', 'him', 'as', 'the', 'deadline', 'gets', '...', 'Oct', '13,', '2018', '...', 'Marguerite', 'Flowers', 'Theme', 'For', 'Chrome', '-', 'This', 'Theme', 'Is', 'Free', 'To', 'Download', '&', 'Comes', 'With', 'Free', 'Lifetime', 'Updates...', '•CHROME', 'THEMES', '->-…', 'Birds', 'and', 'Flowers', 'of', 'Spring', 'and', 'Summer.', 'Kanō', 'EinōEdo', 'period', '(latter', 'half', 'of', '17th', 'century).', 'Zoom', 'in.', 'View', 'in', 'Augmented', 'Reality', '...', 'May', '14,', '2021', '...', 'Twelve-year', 'Major', 'League', 'veteran', 'Tyler', 'Flowers', 'is', 'retiring', 'from', 'baseball.', 'Read', 'more', 'about', 'his', 'decision', 'and', 'his', 'career', 'at', 'MLB', 'Trade', 'Rumors.', 'A', 'perfectly', 'identical', 'version', 'of', 'this', 'picture', 'can', 'be', 'seen', 'in', 'the', 'Rijksmuseum', 'in', 'Amsterdam.', 'The', 'question', 'over', 'whether', 'this', 'is', 'the', 'original', 'or', 'a', 'copy,', 'replic.', 'when', 'winter', 'approaches,', 'covering', 'everything', 'in', 'ice,', 'I', 'take', 'pleasure', 'in', 'the', 'view', '–', 'and', 'in', 'my', 'imagination', 'even', 'in', 'the', 'scent', '–', 'of', 'flowers,', 'if', 'not', 'real', 'on...', 'Apr', '4,', '2013', '...', 'Most', 'worker', 'bees', 'visit', 'thousands', 'of', 'flowers', 'every', 'day', 'in', 'their', 'search', 'for', 'nectar', 'to', 'feed', 'their', "queen's", 'brood.', 'Copying', 'flower', 'colour', 'choices', 'may', '...', 'Oct', '30,', '2021', '...', 'Still,', 'Jimenez', 'expects', 'that', 'will', 'include', 'thousands', 'of', 'the', 'vibrant', 'orange', 'flowers,', 'whose', 'pungent', 'scent', 'comes', 'from', 'their', 'leaves', 'and', 'stem.', 'Aug', '4,', '2016', '...', 'OK,', "that's", 'true', 'of', 'all', 'plants,', 'which', 'is', 'why', 'they', 'orient', 'their', 'flowers', 'and', 'leaves', 'to', 'follow', 'the', 'sun', 'as', 'it', 'moves', 'across', 'the', 'sky.', 'Jul', '1,', '2013', '...', 'The', 'oldest', 'example', 'of', 'flowers', 'used', 'in', 'burial', 'rituals', 'has', 'been', 'unearthed', 'in', 'Raqefet', 'Cave', 'in', 'Israel.', 'Ambrosius', 'Bosschaert,', 'a', 'pioneer', 'in', 'the', 'history', 'of', 'Dutch', 'still-life', 'painting,', 'infused', 'his', 'flower', 'bouquets', 'with', 'a', 'sense', 'of', 'joy.', 'He', 'had', 'an', 'unerring', 'compositio.', 'When', 'you', 'join', 'our', 'newsletter,', "you'll", 'receive', 'helpful', 'flower-growing', 'tips,', 'special', 'offers,', 'advance', 'notice', 'about', 'upcoming', 'workshops,', 'exciting', 'announcements,', 'and', '...', 'The', 'still', 'life', 'was', 'developed', 'as', 'a', 'separate', 'category', 'of', 'painting', 'in', 'the', 'seventeenth', 'century.', 'Dutch', 'artists', 'worked', 'in', 'a', 'variety', 'of', 'still–life', 'traditions', 'that.', '15', 'countries.', '15', 'true', 'crimes.', 'Ashley', 'Flowers', 'takes', 'you', 'on', 'a', 'wicked', 'world', 'tour,', 'exploring', 'notoriously', 'high-profile', 'cases', 'and', 'the', 'cultural', 'details', 'that', 'make', '...', 'Sep', '4,', '2020', '...', "Mississippi's", 'Attorney', 'General', 'Office', 'is', 'dropping', 'its', 'case', 'against', 'Curtis', 'Flowers,', 'a', 'Black', 'man', 'who', 'was', 'tried', 'six', 'times', 'for', 'the', 'same', 'crime.', 'Flowwow', 'is', 'a', 'marketplace', 'for', 'sellers', 'and', 'buyers.', 'With', 'Flowwow', 'you', 'can', 'purchase', 'flowers,', 'gifts,', 'vintage,', 'plants,', 'accessories,', 'safely', 'and', 'fast.', 'Convenient', 'Jan', '17,', '2020', '...', 'It', 'has', 'small', 'flowers', 'on', 'its', 'side', 'that', 'open', 'at', 'night,', 'attracting', 'bats', 'as', 'they', 'fly', 'from', 'flower', 'to', 'flower', 'in', 'search', 'of', 'nectar.', 'One', 'of', 'its', 'main', '...', 'Make', 'these', 'fun', 'borax', 'crystal', 'flowers', 'for', 'spring', 'science.', 'Our', 'crystals', 'flowers', 'are', 'also', 'great', 'for', 'Mothers', 'Day', 'activities.', '15', 'countries.', '15', 'true', 'crimes.', 'Ashley', 'Flowers', 'takes', 'you', 'on', 'a', 'wicked', 'world', 'tour,', 'exploring', 'notoriously', 'high-profile', 'cases', 'and', 'the', 'cultural', 'details', 'that', 'make', '...', 'Sep', '4,', '2020', '...', "Mississippi's", 'Attorney', 'General', 'Office', 'is', 'dropping', 'its', 'case', 'against', 'Curtis', 'Flowers,', 'a', 'Black', 'man', 'who', 'was', 'tried', 'six', 'times', 'for', 'the', 'same', 'crime.', 'Jan', '17,', '2020', '...', 'It', 'has', 'small', 'flowers', 'on', 'its', 'side', 'that', 'open', 'at', 'night,', 'attracting', 'bats', 'as', 'they', 'fly', 'from', 'flower', 'to', 'flower', 'in', 'search', 'of', 'nectar.', 'One', 'of', 'its', 'main', '...', 'Feb', '7,', '2020', '...', 'David', 'Wise', 'from', 'the', 'USA', 'celebrates', 'winning', 'the', 'gold', 'medal', 'on', 'the', 'podium', 'during', 'the', 'flower', 'ceremony.', 'Getty', 'Images—Angelika', 'Warmuth.', 'At', 'the', '2018', '...', 'Nov', '11,', '2021', '...', 'McQueens', 'Flowers', '—', 'the', 'British', 'florist', 'known', 'for', 'decking', 'the', 'halls', 'of', 'haute', 'hotels', 'and', 'posh', 'parties', 'like', 'New', 'York', 'Fashion', 'Week,', '...', 'Bosschaert', 'seldom', 'varied', 'his', 'compositions,', 'no', 'doubt', 'relying', 'upon', 'the', 'customer´s', 'great', 'demand', 'for', 'flower', 'pieces.', 'Three', 'main', 'motifs', 'are', 'common:', 'flower', 'in', 'a', 'v.', 'May', '4,', '2021', '...', 'A', 'vibrant', 'burst', 'of', 'rich', 'hues', 'in', 'the', 'form', 'of', 'more', 'than', '7000', 'flowers', 'is', 'now', 'on', 'display', 'on', "NYC's", 'famed', 'Fifth', 'Avenue.', 'Jun', '7,', '2021', '...', 'Koffee', 'Kup', 'and', 'its', 'assets,', 'including', 'the', 'Brattleboro-based', 'Vermont', 'Bread', 'Company', 'and', 'Superior', 'Bakery', 'in', 'Connecticut,', 'will', 'now', 'be', 'sold', 'to', 'Flowers', '...', 'Aug', '21,', '2021', '...', 'Planting', 'some', 'fall-blooming', 'flowers', 'for', 'a', 'fresh', 'look', 'is', 'a', 'perfect', 'remedy', 'to', 'perk', 'up', 'your', 'tired', 'yard,', 'and', 'fall', 'is', 'also', 'the', 'time', 'to', 'plant', '...', 'Feb', '1,', '2022', '...', 'Flowers', 'discovered', 'perfectly', 'preserved', 'in', 'globs', 'of', 'amber', 'bloomed', 'at', 'the', 'feet', 'of', 'dinosaurs,', 'suggesting', 'that', 'flowers', 'that', 'grow', 'in', 'South', 'Africa', '...', 'Aug', '4,', '2021', '...', 'TREY', 'FLOWERS.', 'Position:', 'Outside', 'linebacker.', 'Ht/Wt:', '6-2/265.', 'College:', 'Arkansas.', 'Experience:', 'Seventh', 'season', '...', 'Feb', '27,', '2020', '...', '“Last', 'time', 'I', 'bought', 'flowers,', 'I', 'bought', 'two', 'bouquets.', 'Then', 'I', 'gave', 'the', 'second', 'bouquet', 'to', 'the', 'cashier', 'and', 'asked', 'her', 'to', 'gift', 'it', 'to', 'the', 'woman', 'behind', '...', 'Jun', '27,', '2019', '...', 'The', 'Flowers', 'case', 'in', 'fact', 'urges', 'the', 'opposite', 'conclusion.', 'At', "Flowers's", 'first', 'trial,', 'Evans', 'struck', 'all', 'five', 'qualified', 'Black', 'prospective', 'jurors,', '...', 'Dec', '19,', '2013', '...', 'The', 'genome', 'sequence', 'sheds', 'new', 'light', 'on', 'a', 'major', 'event', 'in', 'the', 'history', 'of', 'life', 'on', 'Earth:', 'the', 'origin', 'of', 'flowering', 'plants,', 'including', 'all', 'major', '...', 'Feb', '13,', '2017', '...', 'By', 'cutting', 'out', 'the', 'middleman,', 'this', 'startup', 'is', 'aiming', 'for', 'better', 'bouquets', 'and', 'a', 'greener', 'flower', 'industry.', 'Aug', '20,', '2014', '...', 'Once', 'cut', 'and', 'dunked', 'in', 'a', 'vase', 'of', 'water,', 'flowers', 'are', 'susceptible', 'to', 'bacterial', 'growth', 'that', 'shortens', 'the', 'length', 'of', 'time', 'one', 'has', 'to', 'enjoy', 'the', '...', 'Apr', '27,', '2021', '...', 'Flowers', 'was', 'set', 'to', 'get', 'paid', '$9', 'million', 'in', '2021', 'on', 'his', 'old', 'contract', 'with', 'the', 'Dolphins,', 'but', 'just', 'before', 'the', 'trade,', 'he', 'and', 'the', 'Dolphins', 'agreed', 'to', 'a', '...', 'There', 'has', 'not', 'been', 'an', 'agreed', 'opinion', 'on', 'the', 'time', 'when', 'this', 'painting', 'was', 'created.', 'But', 'what', 'is', 'certain', 'is', 'that', 'this', 'work', 'deserves', 'the', 'recognition', 'as', 'a', 'classi.', 'Sep', '9,', '2021', '...', 'We', 'can', 'see', 'it', 'most', 'clearly', 'as', 'spring', 'arrives', 'and', 'various', 'species', 'burst', 'into', 'flower', '—', 'you', 'might', 'even', 'get', 'the', 'feeling', 'that', 'some', 'flowers', 'are', '...', 'Sep', '3,', '2021', '...', 'Curtis', 'Flowers,', 'who', 'spent', '23', 'years', 'in', 'prison', 'on', 'murder', 'charges', 'later', 'dropped,', 'Is', 'suing', 'the', 'Mississippi', 'district', 'attorney', 'who', 'prosecuted', 'him.', 'Feb', '12,', '2019', '...', "Darwin's", 'experiments', 'with', 'flowers', 'would', 'also', 'lay', 'the', 'foundations', 'for', 'the', 'nascent', 'field', 'of', 'plant', 'reproductive', 'biology.', 'Following', 'the', 'publication', '...', 'May', '4,', '2021', '...', 'See', 'how', 'gift', 'retailer', '1-800-FLOWERS.COM,', 'Inc.,', 'migrated', 'its', 'customer', 'touchpoints', 'to', 'cloud,', 'including', 'GKE', 'and', 'BigQuery,', 'to', 'build', 'a', '...', 'Feb', '11,', '2009', '...', 'Best', 'known', 'for', 'its', 'effects', 'on', 'fruit', 'ripening', 'and', 'flower', 'fading,', 'the', 'gaseous', 'plant', 'hormone', 'ethylene', 'shortens', 'the', 'shelf', 'life', 'of', 'many', 'fruits', '...', 'Watercolor', 'study', 'of', 'red', 'flowers', 'on', 'thorny,', 'leaf', 'covered', 'branches', 'in', 'glass', 'vase.', 'The', 'vase', 'of', 'flowers', 'is', 'positioned', 'slightly', 'left', 'of', 'the', 'center', 'at', 'the', 'bottom.', 'Apr', '28,', '2021', '...', 'To', 'make', 'his', 'trade', 'to', 'Washington', 'from', 'Miami', 'official,', 'OL', 'Ereck', 'Flowers', 'restructured', 'his', 'contract', 'whereby', 'the', 'Dolphins', 'will', 'pay', '$6', 'million', 'in', 'a', '...', 'Sep', '24,', '2021', '...', 'Random', 'Acts', 'of', 'Flowers', 'collects', 'blooms', 'from', 'funerals,', 'weddings', 'and', 'grocery', 'stores', 'to', 'bring', 'a', 'lift', 'to', 'people', 'in', 'need.', 'Aug', '14,', '2013', '...', 'To', 'prolong', 'the', 'life', 'of', 'fresh-cut', 'flowers,', 'florists', 'recommend', 'commercial', 'flower', 'preservatives.', 'Homemade', 'vase', 'solutions', '—', 'using', 'pennies,', '...', 'Mar', '12,', '2012', '...', 'Nearly', '28,000', 'potted', 'flowers', 'would', 'fill', 'almost', 'every', 'square', 'foot', 'of', 'the', 'MMHC', 'including', 'corridors,', 'stairwells,', 'offices,', 'and', 'even', 'a', 'swimming', '...', 'Oct', '22,', '2021', '...', 'The', 'sand', 'dunes', 'of', "Chile's", 'Atacama', 'are', 'once', 'again', 'bathed', 'in', 'vibrant', 'colors', 'following', 'the', 'sprouting', 'of', 'flowers', 'in', 'recent', 'weeks', 'in', 'the', "world's", '...', 'Sep', '3,', '2019', '...', 'Raisa', 'Flowers', 'in', 'ASOS', 'and', 'Pat', 'McGrath', 'Labs', 'makeup.', 'Photo:', 'Jeremy', 'Grier/Fashionista.', 'Here', 'at', 'Fashionista,', "we're", 'passionate', 'about', 'covering', 'all', '...', 'Jan', '31,', '2022', '...', "We've", 'consulted', 'a', 'handful', 'of', 'flower', 'experts', 'to', 'find', 'out', 'which', 'florals', 'will', 'be', 'trending', 'for', '2022,', 'from', 'technicolored', 'flowers', 'to', 'boho-inspired', '...', 'Aug', '10,', '2019', '...', 'Trey', 'Flowers', 'has', 'been', 'activated', 'by', 'the', 'Lions,', 'and', 'will', 'take', 'the', 'field', 'in', 'Week', '1', 'against', 'the', 'Cardinals.', 'Dec', '26,', '2018', '...', 'Summary', 'Approximately', '6%', 'of', 'flowering', 'plant', 'species', 'possess', 'flowers', 'with', 'anthers', 'that', 'open', 'through', 'small', 'pores', 'or', 'slits.', 'Mar', '26,', '2009', '...', 'Honeybees', 'and', 'bumble', 'bees', 'are', 'predictable', 'in', 'the', 'way', 'they', 'move', 'among', 'flowers,', 'typically', 'moving', 'directly', 'from', 'one', 'to', 'another', 'in', 'the', 'same', 'row', '...', 'Dec', '7,', '2021', '...', '25).', 'In', 'its', 'gauzy-yet-glossy', 'arrangement', 'of', 'flute,', 'strings,', 'clarinet,', 'saxophone', 'and', 'piano,', '"The', 'Voice', 'of', 'Flowers"', 'feels', 'less', 'like', 'the', 'wispy', '...', '1', 'day', 'ago', '...', 'Argentinian', 'artist', 'Maria', 'Marta', 'Morelli', 'creates', 'realistic', 'flower', 'paintings', 'of', 'hand-picked', 'pink', 'and', 'red', 'blooms.', 'Jan', '19,', '2022', '...', 'Takashi', 'Murakami', 'Teases', 'New', '"Murakami.Flowers"', 'NFT', 'Project:', 'A', 'Tamagotchi-like', 'mobile', 'game', 'is', 'expected', 'to', 'release', 'by', 'the', 'end', 'of', 'this', 'year.', 'Oct', '1,', '2013', '...', 'Newfound', 'fossils', 'suggest', 'flowering', 'plants', 'arose', 'on', 'Earth', 'some', '100', 'million', 'years', 'before', 'previously', 'thought,', 'suggesting', 'the', 'blooms', 'dotted', 'the', '...', 'Oct', '27,', '2021', '...', 'Flowers', 'for', 'Society', 'Is', 'Bridging', 'the', 'World', 'of', 'Sneakers', 'and', 'NFTs:', 'Aiming', 'to', 'become', '“a', 'safe', 'space', 'for', 'collectors', 'and', 'sneakerheads”.', 'May', '4,', '2021', '...', 'Looking', 'to', 'send', 'Mom', 'a', 'beautiful,', 'fresh', 'bouquet?', 'Here', 'are', '9', 'reliable', 'online', 'flower', 'delivery', 'services', 'we', 'use', 'ourselves.', 'Nov', '10,', '2019', '...', 'LOUIS', '—', 'It', 'was', 'just', 'before', '7', 'a.m.', 'Friday', 'and', 'the', 'conditions', 'were', 'perfect', 'for', 'spotting', 'the', 'elusive', 'frost', 'flower.', 'Despite', 'the', 'name,', 'frost', 'flowers', '...', 'A', 'colorful', 'floral', 'arrangement', 'adds', 'the', 'perfect', 'finishing', 'touch', 'to', 'your', 'dinner', 'table,', 'dessert', 'bar', 'or', 'cocktail', 'station.', 'If', "you're", 'new', 'to', 'the', 'art', 'of', 'flower', '...', 'Dec', '1,', '2011', '...', 'Purple', 'flowers', 'Theme', '(Non-Aero).', 'Hope', 'to', 'bring', 'you', 'a', 'good', 'mood.', 'Apr', '24,', '2017', '...', 'But', 'for', 'those', 'living', 'with', 'dementia,', 'those', 'floral', 'arrangements', 'have', 'the', 'potential', 'to', 'be', 'dangerous.', 'Many', 'of', 'the', 'plants', 'and', 'flowers', 'you', 'welcome', '...', '3', 'days', 'ago', '...', 'In', 'Wylde', 'Flowers,', "you'll", 'be', 'stepping', 'into', 'the', 'shoes', 'of', 'a', 'young', 'lady', 'named', 'Tara,', 'who', 'has', 'just', 'moved', 'to', 'a', 'rural', 'island', 'to', 'help', 'out', 'her', 'grandma', 'and', '...', 'Apr', '18,', '2021', '...', 'She', 'learned', 'the', 'basics', 'of', 'caring', 'for', 'flowers', 'and', 'making', 'arrangements', 'during', 'her', 'time', 'at', 'the', 'Philadelphia', 'flower', 'shop,', 'skills', 'that', 'gave', 'her', 'a', '...', 'Mar', '30,', '2021', '...', 'Our', 'Flea', 'Market', 'Flowers', 'sample', 'was', 'stitched', 'by', 'our', 'Stitchy', 'Staffer', 'Cheryl!', 'She', 'stitched', 'this', 'on', 'Barley', '25', 'Count', 'Lugana,', 'and', 'she', 'stitched', 'over', '...', 'Jan', '9,', '2022', '...', 'Makeup', 'artist', 'Raisa', 'Flowers', 'kicked', 'off', 'this', 'year', 'by', 'creating', 'a', 'chic', 'triple-layered', 'eyeliner', 'and', 'glossy', 'nude', 'pout', 'look', 'using', 'Make', 'Up', 'For', '...', 'Make', 'these', 'fun', 'borax', 'crystal', 'flowers', 'for', 'spring', 'science.', 'Our', 'crystals', 'flowers', 'are', 'also', 'great', 'for', 'Mothers', 'Day', 'activities.']

    for title in data['titles']:                           # Tokenize the title and snippets.
        raw_tokens += title.split()

    for snippet in data['snippets']:
        raw_tokens += snippet.split()

    lower_tokens = [word.lower() for word in raw_tokens]

    stemmed_tokens = [] 

    for token in lower_tokens:
        stemmed_tokens.append( lm.lemmatize(token) )

    def filter_words(word):
        if len(word) < 3 or word in list(stopwords.words('english')) or not word.isalpha():         # Filter out stop-listed words and non-alpha tokens.
            return False
        else:
            return True

    stop_listed_tokens = list(filter(filter_words, stemmed_tokens))

    return stop_listed_tokens


def generate_freqs(tokens, num):
    return Counter(tokens).most_common(num)


def print_results(query, data, max):
    print("============================")           # Display information to the user.
    print("Search Results")
    print("============================")

    for x in range(1, max + 1):
        print("-----(" + str(x) + ")-----")
        print("Title: " + data['titles'][x - 1])
        print("Snippet: " + data['snippets'][x - 1])
        print("Link: " + data['links'][x - 1])
        print()

    print("***showing " + str(max) + " of " + str( len(data['titles']) ) + " results for \"" + str(query) + "\"***")
    print()

def print_histogram(term_freqs, num_freqs, max_symbs):        # Prints histogram for top "num_top" most frequent terms, with a width of "max_symbs" characters.
    max_freq = term_freqs[0][1]
    print("============================")
    print("Top " + str(num_freqs) + " Most Frequent Terms")
    print("============================")
    
    print(type(term_freqs[0]))

    for term in term_freqs:
        index = term_freqs.index(term)

        print("#" + str(index + 1) + " ", end="")

        for x in range(1, int( (term_freqs[index][1] / max_freq) * max_symbs) ):
            print("*", end="")

        print(" " + term_freqs[index][0] + " (" + str(term_freqs[index][1]) + ")")

################################################################
# Query expansion using WordNet and search result reordering
################################################################

# Constants
NUM_RESULTS = 20            # Number of results to retrieve (must be multiple of 10).
NUM_FREQS = 20              # Number of most frequent terms to calculate to.
MAX_SYMBS = 60              # Width of the printed rudimentary histogram in characters.
MAX_PRINT = 10              # Max search results to display at a time.

def reorder(results, term):
    #print(len(results['items']))

    def lemma_counter(title, snippet):
        count = 0

        lemmatized = []

        for x in title.lower().split():
            lemmatized.append( lm.lemmatize(x) )

        for x in snippet.lower().split():
            lemmatized.append( lm.lemmatize(x) )

        return lemmatized.count(term)

    #for x in results['items']:
    #    print(lemma_counter(x['title'], x['snippet']))

    results['items'].sort(key=lambda x: lemma_counter(x['title'], x['snippet']), reverse=True)

    #print()
    #for x in results['items']:
    #    print(lemma_counter(x['title'], x['snippet']))

    #print(results['items'][0]['title'])

    titles = []         # To hold data.
    snippets = []
    links = []

    for item in results['items']:                          # Get specific metadata from search result.
        titles.append(item['title'])
        snippets.append(item['snippet'])
        links.append(item['link'])

    return { 'items': results['items'], 'titles': titles, 'snippets': snippets, 'links': links }

def main():
    user_input = ""

    refinement_state = False        # True if user is performing query refinement or search result reordering.
    sorting_state = False
    
    print("*Type 'QUIT' to exit the program.*\n")

    while (not user_input == "QUIT"):
        if not refinement_state and not sorting_state:
            user_input = input("Enter a query: ")
        
        query = user_input

        if (user_input == "QUIT"):
            return

        if not sorting_state:
            data = get_results(user_input, int( (NUM_RESULTS / 10) + 1) )         # Ten results per count retrieved, divide by 10 to get actual amount.
            print("data:" + str(len(data['items'])))
            tokens = process_results(data)
            freqs = generate_freqs(tokens, NUM_FREQS)

        print_results(user_input, data, MAX_PRINT)


        print_histogram(freqs, NUM_FREQS, MAX_SYMBS)
        
        if not sorting_state:
            user_input = int( input("Make a selection: \n\
                                [1] Search Result Reordering \n\
                                [2] Query Refinement\n\
                                [3] Return\n\n") )
        else:
            user_input = 1

        if user_input == 1:
            sorting_state = True
            user_input = int( input("Enter a target term to sort results by: ") )

            print( str(user_input) )
            
            if (user_input > NUM_FREQS or user_input <= 0):
                print("Invalid selection made. Aborting.\n")
                sorting_state = False
                continue


            #print("LEN:" + str(len(data['items'])))
            data = reorder(data, freqs[user_input - 1][0])
            user_input = str(query)


        elif user_input == 2:
            user_input = int( input("Enter a term number to expand: ") )

            if (user_input > NUM_FREQS or user_input <= 0):
                print("Invalid selection made. Aborting.\n")
                continue

            term = freqs[user_input - 1][0]
            senses = wn.synsets(term)

            if (len(senses) > 0):

                index = 0

                print("============================")
                print("Alternative Senses For Term \"" + term + "\"")
                print("============================")

                for sense in senses:
                    print("#" + str(index + 1) + " " + sense.name() + ": " + sense.definition())
                    index += 1

                print()
                user_input = int(input("Select a sense of the term: "))

                if (user_input > len(senses) or user_input <= 0):
                    print("Invalid selection made. Aborting.\n")
                    continue
                else:
                    user_input = str(query) + " " + senses[user_input - 1].name().split(".")[0]
                    refinement_state = True
                
            else:
                print("No alternative senses found for term \"" + term + "\"\n")
                user_input = str(query) + " " + term
                refinement_state = True

        else:
            print("Returning to query formulation.")
            refinement_state = False
            sorting_state = False

main()


    


