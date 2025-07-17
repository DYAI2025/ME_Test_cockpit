import html
from pathlib import Path
import streamlit as st

from src.config_loader import load_schema
from src.marker_loader import load_markers, Marker
from src.engine import MarkerEngine, MarkerMatch
from src.gpt_baseline import gpt4_analysis


def highlight_text(text: str, matches: list[MarkerMatch], markers: list[Marker]) -> str:
    marker_dict = {m.id: m for m in markers}
    sorted_matches = sorted(matches, key=lambda m: m.start)
    result = []
    last = 0
    for m in sorted_matches:
        result.append(html.escape(text[last:m.start]))
        marker = marker_dict.get(m.marker_id)
        desc = marker.description if marker else ''
        highlighted = html.escape(text[m.start:m.end])
        span = f"<span style='background-color: #ffff99;' title='{html.escape(desc)}'>{highlighted}</span>"
        result.append(span)
        last = m.end
    result.append(html.escape(text[last:]))
    return ''.join(result)


def main():
    st.title('Marker Analysis Cockpit')

    with st.sidebar:
        st.header('Configuration')
        schema_file = st.file_uploader('Schema-Datei hochladen', type=['yaml', 'yml', 'json'])
        if schema_file:
            schema_path = Path(schema_file.name)
            with open(schema_path, 'wb') as f:
                f.write(schema_file.read())
            schema_label = schema_file.name
        else:
            schema_path = Path('default_schema.yaml')
            schema_label = 'default_schema.yaml'

        st.markdown(f"**Aktives Schema:** `{schema_label}`")

        marker_files = st.file_uploader('Marker-Dateien hochladen', type=['yaml', 'yml', 'json'], accept_multiple_files=True)
        folder_input = st.text_input('Alternativ: Ordnername für Marker-Dateien')
        openai_key = st.text_input('OpenAI API Key', type='password')
        if openai_key:
            st.session_state['OPENAI_API_KEY'] = openai_key

        text_input = st.text_area('Text für Analyse', max_chars=50000)
        analyse_button = st.button('Analysieren')

    marker_paths = []
    if marker_files:
        for mf in marker_files:
            path = Path(mf.name)
            with open(path, 'wb') as f:
                f.write(mf.read())
            marker_paths.append(path)
    if folder_input:
        folder = Path(folder_input)
        if folder.exists() and folder.is_dir():
            marker_paths.extend(list(folder.glob('*.yaml')) + list(folder.glob('*.yml')) + list(folder.glob('*.json')))

    if not marker_paths:
        marker_paths = list(Path('sample_markers').glob('*.yaml'))

    if analyse_button and text_input:
        schema = load_schema(schema_path)
        markers = load_markers(marker_paths)
        engine = MarkerEngine(schema, markers)
        atomic_matches = engine.atomic_scan(text_input)
        semantic_matches = engine.evaluate_semantic(atomic_matches)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Analyse durch Marker-System')
            html_text = highlight_text(text_input, atomic_matches, markers)
            st.markdown(html_text, unsafe_allow_html=True)
            with st.expander('Gefundene Marker'):
                st.json({
                    'atomic': [m.__dict__ for m in atomic_matches],
                    'semantic': [m.__dict__ for m in semantic_matches],
                })
        with col2:
            st.subheader('Semantische Analyse durch GPT-4')
            gpt_result = gpt4_analysis(text_input)
            st.write(gpt_result)

    if 'OPENAI_API_KEY' in st.session_state:
        import os
        os.environ['OPENAI_API_KEY'] = st.session_state['OPENAI_API_KEY']


if __name__ == '__main__':
    main()
