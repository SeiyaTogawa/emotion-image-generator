import streamlit as st
import os
import base64
from openai import AzureOpenAI
import requests
from PIL import Image
import json


endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"  # Replace with your Azure OpenAI endpoint
api_key = "YOUR_AZURE_OPENAI_API_KEY"  # Replace with your Azure OpenAI API key

client = AzureOpenAI(
azure_endpoint = endpoint,
api_key=api_key,
api_version="2024-02-01"
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def encode_images_in_folder(folder_path):
    encoded_images = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')): 
            file_path = os.path.join(folder_path, filename)
            encoded_images[filename] = encode_image(file_path)
    return encoded_images

def response_gpt4o_with_images(model, client, systyem_promnpt, json_list):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": systyem_promnpt},
            {"role": "user", "content": json_list}
        ],
        temperature=1.0,
    )
    return response.choices[0].message.content

def responce_gpt4o_with_text(model, client, system_prompt, emotions):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": emotions},
            ]}
        ],
        temperature=1.0,
    )
    return response.choices[0].message.content

def call_dalle(client, prompt_by_gpt):
    result = client.images.generate(
        model="dalle3", 
        prompt=prompt_by_gpt,
        n=1
    )
    json_response = json.loads(result.model_dump_json())
    image_dir = os.path.join(os.curdir, 'images')
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    image_path = os.path.join(image_dir, 'generated_image.png')

    image_url = json_response["data"][0]["url"]  
    generated_image = requests.get(image_url).content
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)


    return image_path

model = "gpt-4o-2" 
system_prompt_for_get_emotions = "You are an AI assistant that helps people find information.You are an AI assistant that extracts emotions from uploaded images as ten adjectives. You should extract emotions from all of images uploaded not for each images. Your answer is only adjectives: Don't include any other information"
system_prompt_for_generate_image = "You should create prompt for DALL-E 3 to generate an image. The prompt should related to adjectives below and express only one object in city, and should be in Japanese. You should'nt include adjectives given."
# image = r'static\background_original.png'
image = r'static/background_original.png'

css = f'''
<style>
    .stApp {{
        background-image: url({f"data:image/png;base64,{encode_image(image)}"});
        background-size: cover;
        background-position: center;
        background-color:rgba(255,255,255,0.4);

    }}
    .stApp > header {{
        background-color: transparent;
    }}
    .block-container {{
        background-color: #FFFFFF;
        padding: 60px; 
        border-radius: 40px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        min-height: 300vh;
        min-width: 70vh;
    }}
</style>
'''
st.markdown(css, unsafe_allow_html=True)
if st.button("リセット"):
    st.session_state['step'] = 0
st.header("エモーション画像ジェネレータ", divider='rainbow')

if 'step' not in st.session_state:
    st.session_state['step'] = 0  
if 'image_path_list' not in st.session_state:
    st.session_state['image_path_list'] = []
if 'get_emotions' not in st.session_state:
    st.session_state['get_emotions'] = None
if 'get_prompt_for_Dalle' not in st.session_state:
    st.session_state['get_prompt_for_Dalle'] = None
if 'generate_image' not in st.session_state:
    st.session_state['generate_image'] = None


st.subheader('好きな画像をアップロードしてね(最大20枚まで)', divider='grey')

if st.session_state['step'] >= 0:
    image_path_list = []
    uploaded_files = st.file_uploader("画像ファイルを選んでください", accept_multiple_files=True)

    if uploaded_files:
        if st.button("あなたの心の声を分析"):
            json_list = [{"type": "text", "text": "extract emotions in Japanese"}]
            for upload_file in uploaded_files:
                    json_list.append( {"type": "image_url", "image_url": {"url": f'data:image/png;base64,{base64.b64encode(upload_file.getvalue()).decode("utf-8")}'}})
            st.session_state['json_list'] = json_list
            st.session_state['step'] = 2
    
if st.session_state['step'] >= 2:
    if st.session_state['get_emotions'] is None:
        with st.spinner('あなたの心の声を分析中です'):
            get_emotions = response_gpt4o_with_images(model, client, system_prompt_for_get_emotions, st.session_state['json_list'])
            st.session_state['get_emotions'] = get_emotions
            st.markdown("### あなたの心の声はこちら！！" )
            st.code(st.session_state['get_emotions'])
            st.session_state['step'] = 3
    else:
        st.markdown("### あなたの心の声はこちら！！" )
        st.code(st.session_state['get_emotions'])
        st.session_state['step'] = 3
        
if st.session_state['step'] >= 3:
    get_prompt_for_Dalle = responce_gpt4o_with_text(model, client, system_prompt_for_generate_image, st.session_state['get_emotions'])
    st.session_state['get_prompt_for_Dalle'] = get_prompt_for_Dalle
    st.session_state['step'] = 4

if st.session_state['step'] >= 4:
    if st.button("あなたの心の声を表す画像を生成"):
        with st.spinner('あなたの心の声を表す画像を生成しています'):
            generate_image = call_dalle(client, st.session_state['get_prompt_for_Dalle'])
            st.session_state['step'] = 5
    
if st.session_state['step'] >= 5:
    st.markdown("### あなたの心の声を表した画像はこちら！！" )
    file_path = generate_image
    img = Image.open(file_path)
    st.image(img)
    st.code(get_prompt_for_Dalle)
    st.balloons()
    st.session_state['step'] = 0
    if st.button("もう一度試す"):
        pass