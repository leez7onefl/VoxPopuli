import streamlit as st
import os
import pandas as pd

# Set up Streamlit page
st.set_page_config(
    page_title="VoxPopuli",
    page_icon="🌱",
    layout="wide",
)

# CSS pour le style
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .navbar {
        background-color: #FFFFFF;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #F0F2F6;
        color: #31333F;
        font-weight: bold;
        font-size: 18px;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    .navbar a {
        text-decoration: none;
        color: #31333F;
        margin: 0 15px;
    }
    .navbar a:hover {
        color: #FF4B4B;
    }
    .header {
        font-size: 28px;
        font-weight: bold;
        color: #FF4B4B;
        margin-bottom: 20px;
    }
    .card {
        background-color: #F9F9F9;
        padding: 20px;
        border-radius: 10px;
        margin: 50px 0;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
    }
    .card-title {
        font-size: 20px;
        font-weight: bold;
        color: #333;
    }
    .card-text {
        font-size: 16px;
        color: #666;
    }
    .comment {
        background-color: #f0f2f5;
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .comment-section {
        max-height: 150px;
        overflow-y: auto;
        padding-right: 10px;
    }
    .comment-box {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .comment-box input[type='text'] {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .comment-box button {
        background-color: #FF4B4B;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 12px;
        cursor: pointer;
    }
    .comment-box button:hover {
        background-color: #e43e3e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"
if "comments" not in st.session_state:
    st.session_state["comments"] = [[] for _ in range(3)]
if "new_comments" not in st.session_state:
    st.session_state["new_comments"] = ["" for _ in range(3)]
if "proposals" not in st.session_state:
    st.session_state["proposals"] = []
if "announcements" not in st.session_state:
    st.session_state["announcements"] = [
        {
            "title": "Projet environnemental Rue de la Paix",
            "date": "10 février",
            "desc": "Une initiative pour réduire les déchets et promouvoir la biodiversité urbaine.",
            "image": "images/environment.jpg",
        },
        {
            "title": "Aménagement cyclable Avenue des Fleurs",
            "date": "15 février",
            "desc": "Proposition de nouvelles pistes cyclables pour une mobilité durable.",
            "image": "images/cycling.jpg",
        },
        {
            "title": "Réhabilitation de l'École Jean Moulin",
            "date": "20 février",
            "desc": "Travaux pour moderniser l'école et améliorer son efficacité énergétique.",
            "image": "images/school.jpg",
        },
    ]
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Admin Authentication with a Secret Code
def authenticate_admin(secret_code):
    if secret_code == "SECRET123":
        st.session_state["is_admin"] = True
        st.success("Access granted! You are now logged in as an admin.")
    else:
        st.error("Invalid secret code. Please try again.")

# Admin Authentication Section
if not st.session_state["is_admin"]:
    st.sidebar.subheader("Admin Login")
    admin_code = st.sidebar.text_input("Enter Admin Secret Code", type="password")
    if st.sidebar.button("Authenticate"):
        authenticate_admin(admin_code)

# Function to add a new announcement
def add_announcement(title, description, image_path):
    new_announcement = {
        "title": title,
        "date": "Ajoutée aujourd'hui",
        "desc": description,
        "image": image_path,
    }
    st.session_state["announcements"].append(new_announcement)
    st.session_state["comments"].append([])
    st.session_state["new_comments"].append("")

# Function to add an announcement to proposals
def add_to_proposals(index):
    announcement = st.session_state["announcements"][index]
    comments = st.session_state["comments"][index]
    st.session_state["proposals"].append({
        "announcement": announcement,
        "comments": comments.copy()
    })

# Gestion des pages
if st.session_state["current_page"] == "dashboard":
    st.button("⬅️ Retour aux analyses", on_click=lambda: st.session_state.update({"current_page": "home"}))
    st.markdown("<div class='header'>📈 Analyse du thème</div>", unsafe_allow_html=True)
    st.write("Voici les analyses détaillées pour le thème sélectionné.")

    # Exemple de tableau de bord
    st.subheader("Statistiques clés")
    st.bar_chart({"Mois": ["Janvier", "Février", "Mars"], "Réponses": [100, 150, 120]})
    st.subheader("Détails des réponses")
    st.dataframe(
        pd.DataFrame({
            "Catégorie": ["Très satisfait", "Satisfait", "Neutre", "Insatisfait", "Très insatisfait"],
            "Nombre": [40, 60, 30, 20, 10],
        })
    )
else:
    # Layout management
    if st.session_state["is_admin"]:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📢 Annonces", "📊 Sondages", "📊 Analyses", "💬 Chat", "📌 Propositions"])
    else:
        tab1, tab2, tab4, tab5 = st.tabs(["📢 Annonces", "📊 Sondages","💬 Chat", "📌 Propositions"])

    # Tab 1: Annonces
    with tab1:
        st.markdown("<div class='header'>📢 Annonces</div>", unsafe_allow_html=True)

        # Add new announcement
        with st.expander("Ajouter une nouvelle idée"):
            new_title = st.text_input("Titre de l'idée", key="new_title")
            new_desc = st.text_area("Description de l'idée", key="new_desc")
            new_image = st.file_uploader("Uploader une image", type=["png", "jpg", "jpeg"], key="new_image")
            if st.button("Soumettre", key="submit_new_idea"):
                if new_title and new_desc:
                    image_folder = "images"
                    if not os.path.exists(image_folder):
                        os.makedirs(image_folder)
                    image_path = "images/default.jpg"
                    if new_image:
                        image_path = os.path.join(image_folder, new_image.name)
                        with open(image_path, "wb") as f:
                            f.write(new_image.read())
                    add_announcement(new_title, new_desc, image_path)
                    st.success("Votre idée a été ajoutée avec succès !")
                else:
                    st.error("Veuillez remplir tous les champs.")

        # Display announcements
        for i, announcement in enumerate(st.session_state["announcements"]):
            if os.path.exists(announcement["image"]):
                col1, col2, col3 = st.columns([1, 4, 1])
                with col1:
                    st.image(announcement["image"], use_container_width=True)
                with col2:
                    st.markdown(
                        f"""
                        <div class="card-title">{announcement['title']}</div>
                        <div class="card-text">
                            <strong>{announcement['date']}</strong> - {announcement['desc']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col3:
                    # Restrict "Ajouter à Propositions" button to admin
                    if st.session_state["is_admin"]:
                        if st.button("Ajouter à Propositions", key=f"proposal_{i}"):
                            add_to_proposals(i)
                            st.success("Annonce ajoutée aux propositions !")

                # Comments section
                st.markdown("**Commentaires**")
                with st.container():
                    st.markdown(
                        f"<div class='comment-section'>" +
                        "".join([f"<div class='comment'>{comment}</div>" for comment in st.session_state['comments'][i]]) +
                        "</div>",
                        unsafe_allow_html=True,
                    )

                # Input and send button for comments
                comment_col1, comment_col2 = st.columns([8, 1])
                with comment_col1:
                    st.session_state["new_comments"][i] = st.text_input(
                        "Ajouter un commentaire", 
                        value=st.session_state["new_comments"][i], 
                        key=f"comment_input_{i}", 
                        label_visibility="collapsed"
                    )
                with comment_col2:
                    if st.button("➤", key=f"send_comment_{i}"):
                        if st.session_state["new_comments"][i].strip():
                            st.session_state["comments"][i].append(st.session_state["new_comments"][i].strip())
                            st.session_state["new_comments"][i] = ""

            else:
                st.error(f"Image non trouvée : {announcement['image']}")

    # Onglet 2 : Sondages
        with tab2:
            st.markdown("<div class='header'>📊 Sondages</div>", unsafe_allow_html=True)
            themes = ["Pollution environnementale", "Social", "Économie", "Transport", "Culture"]
            theme_selection = st.selectbox("Choisissez un thème :", themes)
            st.multiselect("Quels sont les sous-thèmes qui vous concernent le plus ?", [
                "Qualité de l'air",
                "Gestion des déchets",
                "Chauffage urbain",
                "Énergies renouvelables",
            ])
            st.text_area("Commentaires libres :", placeholder="Partagez vos idées...")
            if st.button("Soumettre"):
                st.success("Merci pour votre contribution !")
        
        # Onglet 3 : Analyses
        if st.session_state["is_admin"]:
            with tab3:
                st.markdown("<div class='header'>📈 Analyses</div>", unsafe_allow_html=True)

                analysis_themes = ["Pollution environnementale", "Social", "Économie", "Transport", "Culture"]
                st.markdown("### Cliquez sur un thème pour voir les analyses :")
                for theme in analysis_themes:
                    if st.button(f"📊 {theme}", key=theme):
                        st.session_state["current_page"] = "dashboard"

        # Onglet 4 : Chat
        with tab4:
            st.markdown("<div class='header'>💬 Chat</div>", unsafe_allow_html=True)
            chat_themes = ["Tous les thèmes", "Pollution environnementale", "Social", "Économie", "Transport", "Culture"]
            selected_chat_theme = st.selectbox("Choisissez un thème pour discuter :", chat_themes)

            st.text_area("Chatbot :", value="Bonjour ! Comment puis-je vous aider ?", height=200, key="chatbot_output", disabled=True)
            user_input = st.text_input("Vous :", placeholder="Tapez votre message ici...")

            if st.button("Envoyer"):
                if user_input:
                    # Ajoutez ici la logique pour traiter les messages avec un chatbot
                    chatbot_response = f"Vous avez choisi le thème '{selected_chat_theme}'. Voici une réponse automatique : {user_input}"
                    st.session_state.chatbot_output = chatbot_response
                else:
                    st.warning("Veuillez entrer un message avant d'envoyer.")

    # Tab 5: Propositions
    with tab5:
        st.markdown("<div class='header'>📌 Propositions</div>", unsafe_allow_html=True)
        for idx, proposal in enumerate(st.session_state["proposals"]):
            announcement = proposal["announcement"]
            comments = proposal["comments"]
            if os.path.exists(announcement["image"]):
                col1, col2, col3 = st.columns([1, 4, 1])
                with col1:
                    st.image(announcement["image"], use_container_width=True)
                with col2:
                    st.markdown(
                        f"""
                        <div class="card-title">{announcement['title']}</div>
                        <div class="card-text">
                            <strong>{announcement['date']}</strong> - {announcement['desc']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col3:
                    like_col, dislike_col = st.columns([1, 1])
                    with like_col:
                        if st.button(f"👍 {proposal.get('likes', 0)}", key=f"like_proposal_{idx}"):
                            proposal["likes"] = proposal.get("likes", 0) + 1
                    with dislike_col:
                        if st.button(f"👎 {proposal.get('dislikes', 0)}", key=f"dislike_proposal_{idx}"):
                            proposal["dislikes"] = proposal.get("dislikes", 0) + 1

                # Comments section
                st.markdown("**Commentaires**")
                with st.container():
                    st.markdown(
                        f"<div class='comment-section'>" +
                        "".join([f"<div class='comment'>{comment}</div>" for comment in comments]) +
                        "</div>",
                        unsafe_allow_html=True,
                    )

                # Input and send button for comments
                comment_col1, comment_col2 = st.columns([8, 1])
                with comment_col1:
                    st.session_state["new_proposal_comment"] = st.text_input(
                        f"Ajouter un commentaire pour la proposition {idx}", 
                        key=f"proposal_comment_input_{idx}", 
                        label_visibility="collapsed"
                    )
                with comment_col2:
                    if st.button("➤", key=f"send_proposal_comment_{idx}"):
                        new_comment = st.session_state["new_proposal_comment"]
                        if new_comment.strip():
                            comments.append(new_comment.strip())
                            st.session_state["new_proposal_comment"] = ""

            else:
                st.error(f"Image non trouvée : {announcement['image']}")
