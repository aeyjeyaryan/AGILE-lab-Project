# train_model.py
import tensorflow as tf
import numpy as np
import json
import pickle
import os
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

def train_poetry_model(poetry_data, model_dir='poetry_model'):
    max_sequence_len = 20
    max_vocab_size = 1000
    embedding_dim = 100
    
    tokenizer = Tokenizer(num_words=max_vocab_size, oov_token="<OOV>")
    
    poems = [poem['content'] for poem in poetry_data]
    
    tokenizer.fit_on_texts(poems)
    total_words = len(tokenizer.word_index) + 1
    
    input_sequences = []
    for poem in poems:
        token_list = tokenizer.texts_to_sequences([poem])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    
    # Padding the sequences
    input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')
    
    # Creating the predictors from the data and the targets
    predictors, target = input_sequences[:,:-1], input_sequences[:,-1]
    target = tf.keras.utils.to_categorical(target, num_classes=total_words)
    
    
    model = Sequential([
        Embedding(total_words, embedding_dim, input_length=max_sequence_len-1),
        LSTM(150, return_sequences=True),
        Dropout(0.2),
        LSTM(100),
        Dense(100, activation='relu'),
        Dropout(0.2),
        Dense(total_words, activation='softmax')
    ])
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    print("Training model...") #debug
    model.fit(predictors, target, epochs=100, batch_size=32, verbose=1)
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model.save(os.path.join(model_dir, 'model.h5'))
    with open(os.path.join(model_dir, 'tokenizer.pickle'), 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    config = {
        'max_sequence_len': max_sequence_len,
        'max_vocab_size': max_vocab_size
    }
    with open(os.path.join(model_dir, 'config.json'), 'w') as f:
        json.dump(config, f)
    
    print(f"Model and configuration saved in {model_dir}")

if __name__ == "__main__":
    # Data generated by GPT, Give credits to me if you use this data :)
    poetry_data = [
    {
      "title": "The Dancing Wind",
      "author": "Anonymous",
      "genre": "Nature",
      "form": "Free Verse",
      "content": "Through autumn leaves\nA whispered dance begins\nGold and crimson partners\nSwaying in the breeze\nNature's ballet\nUndirected, yet precise",
      "mood": "contemplative",
      "themes": ["nature", "movement", "season"],
      "meter": "none",
      "rhyme_scheme": "none",
      "year": "contemporary"
    },
    {
      "title": "Midnight Dreams",
      "author": "Anonymous",
      "genre": "Lyric",
      "form": "Sonnet",
      "content": "When darkness falls upon the sleeping earth,\nAnd stars emerge to dance across the sky,\nThe world transforms, gives evening dreams their birth,\nAs nighttime's whispers echo nature's sigh.\n\nBeneath the moon's soft glow, shadows take flight,\nTheir forms mysterious in the gentle haze,\nWhile creatures hidden from the day's harsh light\nEmerge to wander through the midnight maze.\n\nOh how these hours speak of magic old,\nOf secrets kept within the heart of time,\nOf stories that the ancient stars have told,\nOf mysteries wrapped in reason and in rhyme.\n\nSo let me drift within this peaceful space,\nWhere dreams and reality embrace.",
      "mood": "dreamy",
      "themes": ["night", "dreams", "nature"],
      "meter": "iambic pentameter",
      "rhyme_scheme": "abab cdcd efef gg",
      "year": "contemporary"
    },
    {
      "title": "Urban Symphony",
      "author": "Anonymous",
      "genre": "Modern",
      "form": "Free Verse",
      "content": "Steel and glass reach skyward\nReflecting clouds that race past\nLike thoughts in the minds below\n\nSubway rumbles underfoot\nA city's heartbeat\nPulsing through concrete veins\n\nThousand voices blend\nInto white noise symphony\nThe music of progress",
      "mood": "energetic",
      "themes": ["urban life", "modernity", "society"],
      "meter": "none",
      "rhyme_scheme": "none",
      "year": "contemporary"
    },
    {
      "title": "Ocean's Memory",
      "author": "Anonymous",
      "genre": "Nature",
      "form": "Haiku",
      "content": "Waves crash on the shore\nSalt spray catches morning light\nTime flows like the tide",
      "mood": "serene",
      "themes": ["nature", "time", "ocean"],
      "meter": "5-7-5 syllables",
      "rhyme_scheme": "none",
      "year": "contemporary"
    },
    {
      "title": "Love's First Light",
      "author": "Anonymous",
      "genre": "Romance",
      "form": "Villanelle",
      "content": "The morning light brings thoughts of you,\nLike dawn's first rays through morning dew,\nPainting skies in endless blue.\n\nEach breath feels somehow fresh and new,\nAs hope springs forth in morning's hue,\nThe morning light brings thoughts of you.\n\nLike flowers reaching toward the blue,\nMy heart grows stronger, pure and true,\nPainting skies in endless blue.\n\nThe world seems filled with morning's dew,\nAs love transforms the old to new,\nThe morning light brings thoughts of you.\n\nEach moment holds a precious view,\nOf what our hearts know to be true,\nPainting skies in endless blue.\n\nSo let this love forever grew,\nAs pure as morning's gentle dew,\nThe morning light brings thoughts of you,\nPainting skies in endless blue.",
      "mood": "romantic",
      "themes": ["love", "nature", "hope"],
      "meter": "varied",
      "rhyme_scheme": "aba aba aba aba aba abaa",
      "year": "contemporary"
    },
    {
      "title": "Time's Echo",
      "author": "Anonymous",
      "genre": "Philosophical",
      "form": "Blank Verse",
      "content": "The ancient clock ticks softly in the hall,\nEach moment passing like a grain of sand\nThrough time's vast hourglass. We cannot hold\nThe present in our hands; it slips away\nBefore we recognize its precious worth.\nYet memory keeps its echo in our minds,\nA ghost of what was once reality,\nReminding us that every second lived\nBecomes a part of who we choose to be.",
      "mood": "reflective",
      "themes": ["time", "memory", "existence"],
      "meter": "iambic pentameter",
      "rhyme_scheme": "none",
      "year": "contemporary"
    },
    {
      "title": "Whispers of the Forest",
      "author": "Anonymous",
      "genre": "Nature",
      "form": "Quatrain",
      "content": "Deep in the woods where shadows play,\nThe ancient trees in silence stay.\nWhispered secrets on the breeze,\nCarried far across the seas.",
      "mood": "mysterious",
      "themes": ["nature", "mystery", "tranquility"],
      "meter": "tetrameter",
      "rhyme_scheme": "aabb",
      "year": "contemporary"
    },
    {
      "title": "Eternal Flame",
      "author": "Anonymous",
      "genre": "Philosophical",
      "form": "Ode",
      "content": "Burning bright through time and space,\nA flame that no wind can erase.\nHope eternal, burning true,\nLighting paths for me and you.\nThrough the dark and stormy night,\nGuiding souls with endless light.",
      "mood": "inspirational",
      "themes": ["hope", "eternity", "guidance"],
      "meter": "varied",
      "rhyme_scheme": "aabbcc",
      "year": "contemporary"
    },
    {
      "title": "The Forgotten City",
      "author": "Anonymous",
      "genre": "Modern",
      "form": "Limerick",
      "content": "There once was a city of gold,\nWhose stories were ancient and old.\nIt stood by the sea,\nWith secrets to free,\nBut now its ruins grow cold.",
      "mood": "nostalgic",
      "themes": ["history", "mystery", "decay"],
      "meter": "anapestic",
      "rhyme_scheme": "aabba",
      "year": "contemporary"
    },
    {
      "title": "Celestial Waltz",
      "author": "Anonymous",
      "genre": "Fantasy",
      "form": "Ballad",
      "content": "Underneath the silver moon,\nStars align in cosmic tune.\nDancers made of stardust bright,\nGliding through the endless night.\n\nPlanets spin in perfect grace,\nOrbiting through time and space.\nGalaxies in harmony,\nEternal cosmic symphony.",
      "mood": "ethereal",
      "themes": ["cosmos", "dance", "eternity"],
      "meter": "iambic tetrameter",
      "rhyme_scheme": "abcb abcb",
      "year": "contemporary"
    },
    {
        "title": "Whispers of Dawn",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Quatrain",
        "content": "Softly breaks the morning light,\nCasting shadows in its flight.\nBirds sing songs to greet the day,\nChasing weary night away.",
        "mood": "hopeful",
        "themes": ["nature", "morning", "renewal"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
    {
        "title": "Echoes of the Ancients",
        "author": "Anonymous",
        "genre": "Historical",
        "form": "Ode",
        "content": "Hear the drums of ages past,\nBeating strong and holding fast.\nStories told in stone and air,\nLegends whispered everywhere.",
        "mood": "reverent",
        "themes": ["history", "legacy", "tradition"],
        "meter": "varied",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
    },
    {
        "title": "Fragments of Time",
        "author": "Anonymous",
        "genre": "Philosophical",
        "form": "Blank Verse",
        "content": "Time is but a shattered glass,\nEach shard reflecting moments passed.\nWe gather pieces, hold them near,\nYet future's edge is never clear.",
        "mood": "introspective",
        "themes": ["time", "memory", "reflection"],
        "meter": "none",
        "rhyme_scheme": "none",
        "year": "contemporary"
    },
    {
        "title": "The Traveler's Song",
        "author": "Anonymous",
        "genre": "Adventure",
        "form": "Ballad",
        "content": "Across the hills and valleys wide,\nI journey forth with stars as guide.\nThrough rivers deep and forests tall,\nI heed the distant wild's call.\n\nThe road ahead, unknown, untamed,\nYet every step is brightly framed.\nA path that twists, a fate unseen,\nThe world beyond remains serene.",
        "mood": "adventurous",
        "themes": ["journey", "exploration", "freedom"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "abcb abcb",
        "year": "contemporary"
      },
      {
        "title": "Winter's Embrace",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Haiku",
        "content": "Snow falls gently down,\nBlanketing the earth in white,\nSilence all around.",
        "mood": "peaceful",
        "themes": ["winter", "nature", "stillness"],
        "meter": "5-7-5 syllables",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "The Midnight Bell",
        "author": "Anonymous",
        "genre": "Mystery",
        "form": "Quatrain",
        "content": "The midnight bell rings through the air,\nA sound that chills, a sound so rare.\nIt calls to those who walk alone,\nThrough streets of shadows, paths unknown.",
        "mood": "eerie",
        "themes": ["mystery", "night", "solitude"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
      {
        "title": "Wings of Freedom",
        "author": "Anonymous",
        "genre": "Inspirational",
        "form": "Ode",
        "content": "Oh wings that lift to skies so wide,\nCarry dreams on winds that glide.\nBeyond the clouds, beyond the sea,\nWhere hearts and souls are truly free.",
        "mood": "uplifting",
        "themes": ["freedom", "dreams", "hope"],
        "meter": "varied",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
      {
        "title": "Desert Mirage",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Sonnet",
        "content": "Upon the sands where whispers fade to dust,\nA mirage dances in the heat's cruel sway.\nThe shifting dunes hold secrets deep in trust,\nWhile sunburned skies chase fleeting clouds away.\n\nAn endless stretch of gold that never ends,\nWhere shadows play and ancient winds remain.\nEach grain of sand a story that transcends,\nA tapestry of loss and silent pain.\n\nYet beauty lives within the barren land,\nIn colors bold that bloom against the odds.\nA testament to life's enduring hand,\nResilient, strong, beneath the desert gods.\n\nSo wander on, through sun and shifting haze,\nFor beauty hides in every harshest place.",
        "mood": "majestic",
        "themes": ["nature", "resilience", "beauty"],
        "meter": "iambic pentameter",
        "rhyme_scheme": "abab cdcd efef gg",
        "year": "contemporary"
    },
    {
        "title": "The Whispering Forest",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Free Verse",
        "content": "Among the ancient trees they stand,\nWhispers carried on the wind.\nLeaves rustle tales of yore,\nOf times and spirits gone before.",
        "mood": "mystical",
        "themes": ["nature", "history", "mystery"],
        "meter": "none",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "Digital Heartbeat",
        "author": "Anonymous",
        "genre": "Modern",
        "form": "Free Verse",
        "content": "Code flows like rivers unseen,\nZeros and ones create dreams.\nA heartbeat in circuits found,\nLife in electric sound.",
        "mood": "futuristic",
        "themes": ["technology", "life", "innovation"],
        "meter": "none",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "Beneath the Waves",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Quatrain",
        "content": "Beneath the waves, a world unknown,\nWhere creatures swim, their beauty shown.\nCorals bloom in colors bright,\nA hidden world of pure delight.",
        "mood": "wonder",
        "themes": ["ocean", "life", "exploration"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
      {
        "title": "The Eternal Flame",
        "author": "Anonymous",
        "genre": "Inspirational",
        "form": "Sonnet",
        "content": "In darkest night, a flame does gently burn,\nIts light a beacon through the endless dark.\nWithin our hearts, its warmth we always yearn,\nA spark of hope, a never-fading mark.\n\nThough winds may howl and storms may rage outside,\nThe flame endures, defying all despair.\nIt keeps us whole, it is our inner guide,\nA constant source of comfort, love, and care.\n\nSo hold it close, this ember bright and pure,\nFor through the night, it shines, steadfast and true.\nNo storm nor time can make it less endure,\nIts radiant glow will carry us all through.\n\nThus let it be our anchor and our light,\nThe flame that turns our darkest night to bright.",
        "mood": "hopeful",
        "themes": ["hope", "resilience", "light"],
        "meter": "iambic pentameter",
        "rhyme_scheme": "abab cdcd efef gg",
        "year": "contemporary"
      },
      {
        "title": "Silken Threads",
        "author": "Anonymous",
        "genre": "Philosophical",
        "form": "Villanelle",
        "content": "Life weaves its threads both dark and light,\nA tapestry of joy and woe.\nEach moment gleams in day's or night.\n\nThough patterns shift, remain in sight,\nThe silken threads still ebb and flow.\nLife weaves its threads both dark and light.\n\nWe stitch with hope, hearts burning bright,\nAnd let the broken pieces go.\nEach moment gleams in day's or night.\n\nIn times of doubt, through fading light,\nThe woven paths will surely show.\nLife weaves its threads both dark and light,\nEach moment gleams in day's or night.",
        "mood": "reflective",
        "themes": ["life", "choices", "time"],
        "meter": "varied",
        "rhyme_scheme": "aba aba aba aba aba abaa",
        "year": "contemporary"
      },
      {
        "title": "Lighthouse of Hope",
        "author": "Anonymous",
        "genre": "Inspirational",
        "form": "Ballad",
        "content": "Upon the cliffs so high and steep,\nA light shines through the darkened deep.\nGuiding ships through stormy seas,\nWith whispered hope upon the breeze.\n\nThough waves may crash and winds may wail,\nThe beacon stands through every gale.\nA steadfast glow to light the way,\nAnd lead the lost to break of day.",
        "mood": "encouraging",
        "themes": ["guidance", "hope", "perseverance"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
      {
        "title": "Starlit Dreams",
        "author": "Anonymous",
        "genre": "Fantasy",
        "form": "Sonnet",
        "content": "Beneath the stars, a world of dreams unfolds,\nWhere wishes drift upon the midnight air.\nA secret realm that destiny upholds,\nWith magic hidden everywhere.\n\nThe moonlight casts its silver glow so wide,\nAnd whispers tales of lands unseen, untamed.\nWithin this space where fantasy resides,\nOur hearts find freedom, unrestrained, unnamed.\n\nSo close your eyes and let the night reveal,\nThe wonders waiting in that endless sky.\nWith every star, a new world you will feel,\nA boundless journey where your spirit flies.\n\nEmbrace the dark, where all your dreams ignite,\nAnd let your soul take flight in starlit night.",
        "mood": "dreamy",
        "themes": ["dreams", "magic", "freedom"],
        "meter": "iambic pentameter",
        "rhyme_scheme": "abab cdcd efef gg",
        "year": "contemporary"
      },
      {
        "title": "Autumn's Farewell",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Haiku",
        "content": "Leaves fall, winds do sigh,\nGolden hues kiss earth goodbye,\nWinter draws near now.",
        "mood": "melancholic",
        "themes": ["seasons", "change", "farewell"],
        "meter": "5-7-5 syllables",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "The Iron City",
        "author": "Anonymous",
        "genre": "Modern",
        "form": "Free Verse",
        "content": "Smoke rises in spirals above the gray,\nMachines hum a song of progress.\nBeneath the towers of steel and glass,\nPeople move like clockwork,\nTicking through their days,\nChasing dreams in electric haze.",
        "mood": "industrial",
        "themes": ["urban life", "progress", "society"],
        "meter": "none",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "Echoes in the Valley",
        "author": "Anonymous",
        "genre": "Mystery",
        "form": "Quatrain",
        "content": "In the valley deep and still,\nWhispers ride on evening's chill.\nSecrets hidden in the mist,\nBy the moonlight softly kissed.",
        "mood": "mysterious",
        "themes": ["nature", "secrets", "night"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
      {
        "title": "Whispers of the Rain",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Free Verse",
        "content": "Raindrops tap on window panes,\nA soothing rhythm, soft refrain.\nThe earth drinks deeply, quenched at last,\nAs memories wash through the past.\n\nPuddles form on cobblestone streets,\nReflecting skies where gray clouds meet.\nEach droplet tells a story true,\nOf life renewed, of skies once blue.",
        "mood": "soothing",
        "themes": ["rain", "renewal", "memory"],
        "meter": "none",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "The Forgotten Garden",
        "author": "Anonymous",
        "genre": "Mystery",
        "form": "Quatrain",
        "content": "A gate of rust, a path of stone,\nLeads to a garden overgrown.\nWhere flowers once in colors bright,\nNow slumber softly out of sight.",
        "mood": "nostalgic",
        "themes": ["nature", "mystery", "time"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
      {
        "title": "The Silent Library",
        "author": "Anonymous",
        "genre": "Philosophical",
        "form": "Villanelle",
        "content": "In silent halls where stories sleep,\nThe echoes of the past remain.\nWithin each page, our souls they keep.\n\nA thousand lives, a secret deep,\nEach tale a joy, or heartfelt pain.\nIn silent halls where stories sleep.\n\nThe wisdom gained, we always reap,\nAs time moves on, yet words remain.\nWithin each page, our souls they keep.\n\nThrough whispered words, emotions leap,\nAnd knowledge flows like gentle rain.\nIn silent halls where stories sleep,\nWithin each page, our souls they keep.",
        "mood": "reflective",
        "themes": ["knowledge", "memory", "time"],
        "meter": "varied",
        "rhyme_scheme": "aba aba aba aba abaa",
        "year": "contemporary"
      },
      {
        "title": "Twilight's Embrace",
        "author": "Anonymous",
        "genre": "Romance",
        "form": "Sonnet",
        "content": "As day retreats and twilight takes its place,\nThe sky is painted hues of dusk and flame.\nIn that brief moment, hearts begin to race,\nAnd lovers whisper softly each sweet name.\n\nThe stars appear, a million points of light,\nA cosmic dance to serenade the eve.\nTheir glow reflects within the lovers' sight,\nA promise made that neither will deceive.\n\nSo in the twilight's gentle, warm embrace,\nLet hearts entwine beneath the starlit dome.\nFor in this space, love finds its rightful place,\nAnd in each other, both will find their home.\n\nAs night descends and covers earth in peace,\nTheir bond, like stars, will never cease.",
        "mood": "romantic",
        "themes": ["love", "night", "eternity"],
        "meter": "iambic pentameter",
        "rhyme_scheme": "abab cdcd efef gg",
        "year": "contemporary"
      },
      {
        "title": "Embers of the Past",
        "author": "Anonymous",
        "genre": "Historical",
        "form": "Blank Verse",
        "content": "The fire burns low, its embers softly glow,\nWhispers of days gone by linger in the air.\nA tapestry of memories, woven slow,\nBy hands that shaped the world with tender care.\n\nEach ember holds a tale of love and loss,\nOf battles fought, and dreams that once took flight.\nThe past remains, a shadow we must cross,\nTo find our way toward morning's guiding light.\n\nSo let the embers warm us through the night,\nA gentle reminder of our shared fight.",
        "mood": "nostalgic",
        "themes": ["history", "memory", "resilience"],
        "meter": "iambic pentameter",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "Whispers of the Forest",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Free Verse",
        "content": "The trees speak in hushed tones,\nLeaves rustling like ancient scrolls.\nSunlight filters through the canopy,\nWriting stories on the forest floor.\n\nA deer steps softly, unaware\nOf the secrets woven in the moss.\nEach branch and root holds memories\nOf seasons that have come and gone.",
        "mood": "peaceful",
        "themes": ["nature", "mystery", "time"],
        "meter": "none",
        "rhyme_scheme": "none",
        "year": "contemporary"
      },
      {
        "title": "Wanderer's Lament",
        "author": "Anonymous",
        "genre": "Philosophical",
        "form": "Sonnet",
        "content": "I walk a path unknown, beneath the sky,\nWith stars as guides and wind to lead the way.\nEach step a question, echoing a sigh,\nIn search of meaning at the break of day.\n\nThe road is long, with shadows trailing near,\nYet hope persists, a flame that will not die.\nThough doubts may whisper softly in my ear,\nI lift my gaze and seek the endless sky.\n\nFor life is but a journey we must take,\nThrough trials, joys, and all we leave behind.\nThe dawn will break, a new horizon wake,\nAnd truth reveal itself to those who find.\n\nSo let me walk this road until the end,\nWhere time and space and spirit all transcend.",
        "mood": "reflective",
        "themes": ["journey", "hope", "self-discovery"],
        "meter": "iambic pentameter",
        "rhyme_scheme": "abab cdcd efef gg",
        "year": "contemporary"
      },
      {
        "title": "Midnight Rain",
        "author": "Anonymous",
        "genre": "Lyric",
        "form": "Quatrain",
        "content": "The midnight rain begins to fall,\nA gentle tap upon the pane.\nIt sings of dreams that softly call,\nAnd washes sorrow with its rain.",
        "mood": "melancholic",
        "themes": ["rain", "dreams", "healing"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "abab",
        "year": "contemporary"
      },
      {
        "title": "Forgotten Shores",
        "author": "Anonymous",
        "genre": "Adventure",
        "form": "Ballad",
        "content": "On shores untouched by mortal feet,\nWhere ocean and the heavens meet,\nLies treasure hidden from the eye,\nBeneath the stars that light the sky.\n\nThe winds of fate do call me near,\nTo seek the truths that I hold dear.\nThrough storms and tides, I'll find my way,\nTo greet the dawn of a brighter day.",
        "mood": "adventurous",
        "themes": ["exploration", "destiny", "hope"],
        "meter": "iambic tetrameter",
        "rhyme_scheme": "aabb",
        "year": "contemporary"
      },
      {
        "title": "Echoes of the Mountain",
        "author": "Anonymous",
        "genre": "Nature",
        "form": "Haiku",
        "content": "Mountains stand so still,\nEchoes carry through the winds,\nTimeless tales they tell.",
        "mood": "majestic",
        "themes": ["nature", "time", "history"],
        "meter": "5-7-5 syllables",
        "rhyme_scheme": "none",
        "year": "contemporary"
      }

  ]
  
    
    train_poetry_model(poetry_data)