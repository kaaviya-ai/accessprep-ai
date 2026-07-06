import streamlit as st


def responsive_image(image, caption: str | None = None, width: int | None = None) -> None:
    if width:
        st.image(image, caption=caption, width=width)
        return
    try:
        st.image(image, caption=caption, use_container_width=True)
    except TypeError:
        st.image(image, caption=caption, use_column_width=True)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root { color-scheme: dark; }
        .block-container { max-width: 1180px; padding-top: 1.4rem; }
        h1, h2, h3 { letter-spacing: 0; }
        h1 { font-size: clamp(2.1rem, 4vw, 4.2rem); font-weight: 800; }
        h2 { font-size: 2rem; }
        p, li, label, div { font-size: 1.06rem; }
        .hero {
          border: 1px solid rgba(138,180,248,.28);
          background: linear-gradient(135deg, rgba(26,115,232,.22), rgba(52,168,83,.13));
          padding: 2rem;
          border-radius: 8px;
          margin-bottom: 1.2rem;
        }
        .metric-card {
          border: 1px solid rgba(255,255,255,.11);
          background: rgba(255,255,255,.045);
          border-radius: 8px;
          padding: 1rem;
          min-height: 132px;
        }
        .material-button button {
          min-height: 3rem;
          font-size: 1.08rem;
          border-radius: 8px;
        }
        .stTextArea textarea, .stTextInput input {
          font-size: 1.08rem;
          line-height: 1.55;
        }
        .access-note {
          border-left: 4px solid #34a853;
          padding: .8rem 1rem;
          background: rgba(52,168,83,.1);
          border-radius: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def logo_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div style="font-size:3rem;font-weight:900;">AccessPrep AI</div>
          <div style="font-size:1.35rem;color:#cbd5e1;margin-top:.35rem;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if title != "AccessPrep AI":
        st.title(title)


def info_card(title: str, body: str, icon: str = "◼") -> None:
    st.markdown(
        f"""
        <div class="metric-card" role="group" aria-label="{title}">
          <div style="font-size:1.6rem;">{icon}</div>
          <h3 style="margin:.35rem 0 .35rem 0;">{title}</h3>
          <p style="margin:0;color:#d9e2f1;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
