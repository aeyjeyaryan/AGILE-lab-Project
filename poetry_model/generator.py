# import tensorflow as tf
# import numpy as np
# import json
# import pickle
# import os
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.models import load_model

# def generate_poem(seed_text, model_dir='poetry_model'):
#     try:
#         # Load configuration
#         with open(os.path.join(model_dir, 'config.json'), 'r') as f:
#             config = json.load(f)
        
#         # Load tokenizer
#         with open(os.path.join(model_dir, 'tokenizer.pickle'), 'rb') as handle:
#             tokenizer = pickle.load(handle)
        
#         # Load model
#         model = load_model(os.path.join(model_dir, 'model.h5'))
        
#         # Generate poem
#         next_words = 50  # You can adjust this
#         for _ in range(next_words):
#             token_list = tokenizer.texts_to_sequences([seed_text])[0]
#             token_list = pad_sequences([token_list], 
#                                      maxlen=config['max_sequence_len']-1, 
#                                      padding='pre')
#             predicted = model.predict(token_list, verbose=0)
#             predicted = np.argmax(predicted, axis=-1)
            
#             output_word = ""
#             for word, index in tokenizer.word_index.items():
#                 if index == predicted:
#                     output_word = word
#                     break
            
#             seed_text += " " + output_word
        
#         return seed_text
    
#     except Exception as e:
#         return f"Error generating poem: {str(e)}"

# if __name__ == "__main__":
#     while True:
#         # Get seed text from user
#         seed_text = input("\nEnter a few words to start the poem (or 'quit' to exit): ")
        
#         if seed_text.lower() == 'quit':
#             break
        
#         # Generate and display poem
#         print("\nGenerating poem...\n")
#         generated_poem = generate_poem(seed_text)
#         print("Generated Poem:")
#         print("--------------")
#         print(generated_poem)
#         print("--------------")

import streamlit as st
import tensorflow as tf
import numpy as np
import json
import pickle
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import time
import base64

def load_custom_css():
    """Add custom CSS for better styling"""
    # Apparently we can write css in streamlit as well, wow!!
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #1a1a1a, #2d2d2d);
            color: #ffffff;
        }
        .poem-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeIn 1s ease-in;
        }
        .title-text {
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        .subtitle-text {
            font-size: 24px;
            color: #bebebe;
            text-align: center;
            margin-bottom: 40px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .generated-text {
            font-family: 'Georgia', serif;
            font-size: 20px;
            line-height: 1.6;
            color: #ffffff;
            white-space: pre-line;
        }
        .stTextInput > div > div {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
        }
        .stButton > button {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 30px;
            font-size: 18px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

def add_bg_image():
    st.markdown("""
        <style>
        .stApp {
            background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%239C92AC' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
        }
        </style>
    """, unsafe_allow_html=True)

def generate_poem(seed_text, model_dir='poetry_model'):
    
    try:
        with st.spinner('🌟 Crafting your poem...'):
            with open(os.path.join(model_dir, '/Users/aryanjha/Desktop/AGILE lab/poetry_model/config.json'), 'r') as f:
                config = json.load(f)
            
            with open(os.path.join(model_dir, '/Users/aryanjha/Desktop/AGILE lab/poetry_model/tokenizer.pickle'), 'rb') as handle:
                tokenizer = pickle.load(handle)
            
            
            model = load_model(os.path.join(model_dir, '/Users/aryanjha/Desktop/AGILE lab/poetry_model/model.h5'))
            
            # The poem is generated here!!
            next_words = 50
            for _ in range(next_words):
                token_list = tokenizer.texts_to_sequences([seed_text])[0]
                token_list = pad_sequences([token_list], 
                                         maxlen=config['max_sequence_len']-1, 
                                         padding='pre')
                predicted = model.predict(token_list, verbose=0)
                predicted = np.argmax(predicted, axis=-1)
                
                output_word = ""
                for word, index in tokenizer.word_index.items():
                    if index == predicted:
                        output_word = word
                        break
                
                seed_text += " " + output_word
            
            time.sleep(1)  # Add dramatic pause
            return seed_text
    
    except Exception as e:
        return f"Error generating poem: {str(e)}"

def main():
    st.set_page_config(
        page_title="AI Poetry Generator",
        page_icon="✨",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    load_custom_css()
    add_bg_image()
    
    
    # basic things
    st.markdown('<p class="title-text">✨ AI Poetry Generator ✨</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Generate poetries with our simple tensorflow Model!</p>', 
                unsafe_allow_html=True)
    
    # take seed text from user....
    col1, col2 = st.columns([3, 1])
    with col1:
        seed_text = st.text_input("Enter your inspiration:", 
                                 placeholder="Type a few words to begin...",
                                 key="seed_input")
    with col2:
        generate_button = st.button("Generate ✨")
    
    if generate_button and seed_text:
        generated_poem = generate_poem(seed_text)
        
        # to display the poems beautifully
        st.markdown('<div class="poem-container">', unsafe_allow_html=True)
        st.markdown(f'<p class="generated-text">{generated_poem}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #bebebe; padding: 20px;'>
        Made with ❤️ by Team Aryan 
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()