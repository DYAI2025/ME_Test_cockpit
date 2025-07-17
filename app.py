import json
from pathlib import Path
import streamlit as st

from src.config_loader import load_schema
from src.marker_loader import load_markers
from src.engine import MarkerEngine
from src.gpt_baseline import gpt4_analysis


def main():
    st.title('Marker Analysis Cockpit')

    with st.sidebar:
        st.header('Configuration')
        schema_file = st.file_uploader('Upload Schema File', type=['yaml', 'yml', 'json'])
        if schema_file:
            schema_path = Path(schema_file.name)
            with open(schema_path, 'wb') as f:
                f.write(schema_file.read())
        else:
            schema_path = Path('default_schema.yaml')

        text_input = st.text_area('Text Input', max_chars=50000)
        openai_key = st.text_input('OpenAI API Key', type='password')
        if openai_key:
            st.session_state['OPENAI_API_KEY'] = openai_key

        marker_files = st.file_uploader('Upload Marker Files', type=['yaml', 'yml', 'json'], accept_multiple_files=True)
        marker_paths = []
        if marker_files:
            for mf in marker_files:
                path = Path(mf.name)
                with open(path, 'wb') as f:
                    f.write(mf.read())
                marker_paths.append(path)
        else:
            marker_paths = list(Path('sample_markers').glob('*.yaml'))

        if st.button('Analyse') and text_input:
            schema = load_schema(schema_path)
            markers = load_markers(marker_paths)
            engine = MarkerEngine(schema, markers)
            result = engine.run(text_input)
            st.subheader(f"Analyse gemäß Schema: {schema.get('schema_name')}")
            st.json(result)
            gpt_result = gpt4_analysis(text_input)
            st.subheader('Semantische Analyse durch GPT-4')
            st.write(gpt_result)

    if 'OPENAI_API_KEY' in st.session_state:
        import os
        os.environ['OPENAI_API_KEY'] = st.session_state['OPENAI_API_KEY']


if __name__ == '__main__':
    main()
