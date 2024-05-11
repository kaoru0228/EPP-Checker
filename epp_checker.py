import streamlit as st
import pandas as pd

import csv
import base64


st.set_page_config(
    page_title="EPP Checker",
    page_icon="🐧",
    layout="centered",
    initial_sidebar_state='auto',
    menu_items={
        'About': "This is an application that identifies individuals who may be the biological fathers of children who may have EPP."
    }
)


# ページリンク
st.sidebar.title('ページリンク')
st.sidebar.page_link("epp_checker.py", label="Home", icon="🐧", disabled=True)
st.sidebar.page_link("pages/identifying_father.py",
                     label="Identifying the father", icon="♂️")
st.sidebar.page_link("pages/identifying_mother.py",
                     label="Identifying the mother", icon="♀️")


# CSSのスタイルを定義
css = """
<style>
.title {
    color: white;
    font-size: 54px;
    font-weight: bold;
}
.custom-field {
    background-color: rgba(240, 242, 246, 0.8);  /* 背景色に透明度を設定 */
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ccc;
}
.indented-text {
    padding-left: 15px;  /* 左に15pxのパディングを追加 */
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


# st.title('EPP Checker')
st.markdown('<p class="title">EPP Checker</p>', unsafe_allow_html=True)


# 説明テキスト
st.markdown("""
<div class="custom-field">
    <h3>アプリの概要</h3>
    <div>
        <p>　本アプリは、EPP（つがい外父性）が起こった疑いのある親子について、実の父親を遺伝情報から特定するツールです。</p>
        <p>　EPPが発覚した場合、同じコロニーに生息する全てのオス個体が父親の候補となります。これらの個体の遺伝子を照合しなければ実の父親を特定できませんが、多量の遺伝情報を手作業で解析するのは現実的ではありません。本アプリでは、EPPが発覚したつがいにおける母親・子の個体の遺伝情報と、コロニー内の全てのオス個体の遺伝情報を自動で解析し、生物学上の父親を特定することができます。</p>
        <p>　本アプリには、２つのメニューがあり、サイドバーから選択できます。<br></p>
        <br>
    </div>
    <h3>使用方法</h3>
    <div>
        <u><b>1. 父親候補の特定（Identifying the Father）</b></u>
        <p>　このメニューでは、上記の通り、EPPの疑いがある母親と子の遺伝情報に対し、コロニー内すべてのオス個体の遺伝情報を照合し、解析することで遺伝的な父親を特定します。</p>
        <ol class="indented-text">
            <b><li>入力データの準備</li></b>
            <p>　‘Download’ボタンより、テンプレートデータを取得できます。これは、’child’, ‘mother’, ‘father’という３つのシートからなるエクセルファイルです。テンプレートに従い、入力データを作成してください。’child’, ‘mother’シートにはEPPの疑いがある個体を、‘father’シートには実の父親である可能性があるオス個体の情報を記述してください。</p>
            <b>注意点</b>
            <ul class="indented-text">
                <li>子と母親は１対１で対応しているため、対応順に各シートに遺伝情報を記述してください。また、これにより’child’と’mother’の個体数は同じにならなければなりません。（例えば、’child’シートの３番目の個体と’mother’シートの３番目の個体は、親子関係でなければなりません。）</li>
                <li>‘father’シートの個体数は、確認したいオスの個体数によって可変です。</li>
                <li>個体の名前は重複がなければ自由に決められます。</li>
                <li>マーカー名については特に指定がありません。ただし、各シートで同じ順になるようにしてください。</li>
            </ul>
            <br>
            <b><li>パラメータの設定</li></b>
            <p>　サイドバーから各パラメータを設定してください。まず、使用するマーカーの数を設定してください。（テンプレートファイルでは14種のマーカーの情報があるため、デフォルトは14となっています。）次に、許容度を設定してください。この値により、何種類以上のマーカーが遺伝的に一致すれば親子と判定されるかが決まります。厳しい判定を行いたい場合、マーカー数と同じ値にすることをお勧めします。</p>
            <b><li>データのアップロード</li></b>
            <p>　作成したエクセルファイル形式のデータを、’Browse files’ボタンよりアップロードしてください。アップロードしたデータのプレビューが表示されます。</p>
            <b><li>データの解析（親子鑑定の実施）</li></b>
            <p>　データが正常にアップロードされた状態で‘Analyze’ボタンをクリックすると、解析が始まります。</p>
            <b><li>結果の確認</li></b>
            <p>　各子の個体に対して、遺伝的に父親である可能性があるオス個体が表示されます。もし表示されない場合は、パラメータである許容度を少し低くして再度解析を行うことをお勧めします。また、’Download results’ボタンより結果をエクセルファイル形式でダウンロードできます。一致したマーカーの種類など、より詳細な解析結果を確認する際に利用してください。</p>
        </ol>
        <br>
    </div>
    <div>
        <u><b>2. 母親候補の特定（Identifying the Mother）</b></u>
        <p>　このメニューでは、とある子の個体に対し、遺伝的な母親を特定します。子育てはEPPの有無に関係なく両親のつがいが行います。これにより母親は特定できていることが多いですが、母親が不明であるときにこのメニューで確認することができます。また、この解析により母親が遺伝的に正しいかを確認できるため、併せて子の取り違いが発生していないかを確認することができます。</p>
        <ol class="indented-text">
            <b><li>入力データの準備</li></b>
            <p>　‘Download’ボタンより、テンプレートデータを取得できます。これは、’child’, ‘mother’, という２つのシートからなるエクセルファイルです。テンプレートに従い、入力データを作成してください。’child’シートにはEPPの疑いがある個体を、‘mother’シートには実の母親である可能性があるメス個体の情報を記述してください。</p>
            <b>注意点</b>
            <ul class="indented-text">
                <li>‘mother’シートの個体数は、確認したいオスの個体数によって可変です。</li>
                <li>個体の名前は重複がなければ自由に決められます。</li>
                <li>マーカー名については特に指定がありません。ただし、各シートで同じ順になるようにしてください。</li>
            </ul>
            <br>
            <b><li>パラメータの設定</li></b>
            <p>　サイドバーから各パラメータを設定してください。まず、使用するマーカーの数を設定してください。（テンプレートファイルでは14種のマーカーの情報があるため、デフォルトは14となっています。）次に、許容度を設定してください。この値により、何種類以上のマーカーが遺伝的に一致すれば親子と判定されるかが決まります。厳しい判定を行いたい場合、マーカー数と同じ値にすることをお勧めします。</p>
            <b><li>データのアップロード</li></b>
            <p>　作成したエクセルファイル形式のデータを、’Browse files’ボタンよりアップロードしてください。アップロードしたデータのプレビューが表示されます。</p>
            <b><li>データの解析（親子鑑定の実施）</li></b>
            <p>　データが正常にアップロードされた状態で‘Analyze’ボタンをクリックすると、解析が始まります。</p>
            <b><li>結果の確認</li></b>
            <p>　各子の個体に対して、遺伝的に母親である可能性があるメス個体が表示されます。もし表示されない場合は、パラメータである許容度を少し低くして再度解析を行うことをお勧めします。また、’Download results’ボタンより結果をエクセルファイル形式でダウンロードできます。一致したマーカーの種類など、より詳細な解析結果を確認する際に利用してください。</p>
            <p>　さらに、’Download new data’ボタンより、解析結果から作成したデータをダウンロードできます。これは、父親候補の特定における入力データの形式に合わせたエクセルファイル形式のデータとなっています。このデータに’father’シートを追加することで、すぐに父親候補の特定を行うことができます。</p>
        </ol>
        <br>
    </div>
    <b>※ サイドバーからメニューを選択できます。</b>
</br>
""", unsafe_allow_html=True)


# エフェクト
st.snow()
# st.balloons()


# 画像の挿入
# st.image('Images/penguin_001.jpg')
img_path = 'Images/penguin_001.jpg'
with open(img_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
